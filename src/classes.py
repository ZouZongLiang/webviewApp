import json
import os
import time
import gc
from concurrent.futures import ThreadPoolExecutor, as_completed
from ctypes import c_long, py_object, pythonapi
from threading import Thread
from urllib.parse import urlparse

import m3u8
import requests
import urllib3
from Crypto.Cipher import AES

urllib3.disable_warnings()


class thread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

    def stop(self):
        tid = c_long(self.ident)
        res = pythonapi.PyThreadState_SetAsyncExc(tid, py_object(SystemExit))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

        self._started.clear()

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            self._started.clear()


class hlsDowndloader:
    def init(self, m3u8Url, mediaName):
        self.m3u8Url = m3u8Url
        self.basePath = os.path.dirname(__file__) + '/../temp/'
        self.mediaName = mediaName
        self.tsPath = self.basePath + f'ts/{self.mediaName}/'

        self.m3u8Infos = self.getM3u8Info(self.m3u8Url)

        self.key = self.m3u8Infos['key']

        if self.key[0] == 'AES-128':
            self.decoder = self.decode(*self.key[1:])
        else:
            self.decoder = None

        self.downpercent = 0
        self.downedsuccess = 0
        self.downloaded = 0
        self.err = 0
        self.stopdown = False

        self.m3u8Infos['downloaded'] = self.downloaded
        self.m3u8Infos['err'] = self.err
        self.m3u8Infos['m3u8Name'] = self.mediaName

        self.threadPool = ThreadPoolExecutor(20)
        self.tasks = []

    def reptile(self, url, tryCount=10):
        status = False
        res = None

        while not status:
            tryCount -= 1
            try:
                res = requests.get(url=url, verify=False, timeout=10)
                status = True

            except:
                pass

            finally:
                if tryCount == 0:
                    return False, None

        return True, res

    def decode(self, key, iv=None):
        if iv is None:
            decodder = AES.new(bytes(key, 'utf8'), AES.MODE_CBC)
        else:
            decodder = AES.new(bytes(key, 'utf8'),
                               AES.MODE_CBC, bytes(iv, 'utf8'))

        return decodder.decrypt

    def getM3u8Info(self, url: str):
        x = urlparse(url)
        baseURL = x.scheme + '://' + x.netloc + '/'

        res = self.reptile(url)

        if res[0]:
            m3u8Text = m3u8.loads(res[1].text)
        else:
            return

        while m3u8Text.is_variant:
            for i in res[1].text.split('\n'):
                if i.endswith('.m3u8'):
                    url = baseURL + i
                    break
            print("多级码流 reptile:{}".format(url))
            res = self.reptile(url)

            if res[0]:
                m3u8Text = m3u8.loads(res[1].text)
            else:
                return
        # 获取key
        if m3u8Text.keys is not None and m3u8Text.keys[0] is not None and len(m3u8Text.keys):
            key = [m3u8Text.keys[0].method, None, m3u8Text.keys[0].iv]
            keyRes = self.reptile(baseURL+m3u8Text.keys[0].uri)
            if keyRes[0]:
                key[1] = keyRes[1].text
        else:
            key = [None]*3

        allDuration = 0
        tsInfos = []
        # 获取 ts文件信息
        for index, ts in enumerate(m3u8Text.segments):
            tsInfos.append(
                {'index': index, 'duration': ts.duration, 'url': baseURL+ts.uri, 'download': False})
            allDuration += ts.duration

        # print({'url': url, 'key': key, 'allDuration': float('%.2f'%allDuration),
        #       'num': len(tsInfos), 'tsInfos': tsInfos[0]})
        return {'url': url, 'key': key, 'allDuration': float('%.3f' % allDuration), 'tsInfos': tsInfos}

    def downloadTsFile(self, url, index):
        # 如果停止了，就结束下载
        if self.stopdown or self.m3u8Infos['tsInfos'][index]['download']:
            return

        print(f"开始下载index: {index}")

        res = self.reptile(url)

        if res[0]:
            binary = res[1].content
            self.m3u8Infos['tsInfos'][index]['download'] = True
            self.downloaded += 1
        else:
            self.err += 1

        # 更新百分比
        self.updatePercent()

        # 解密，写入文件
        if self.decoder is not None:
            binary = self.decoder(binary)

        self.write(binary, self.tsPath + f'{index}.ts', 0)

        print(f"end下载index: {index, self.downedsuccess, self.downpercent}")

        del binary
        gc.collect()

    def write(self, data, filePath, mode=0):
        """
            filePath: absolute 路径
            data: any
            mode: 0 bytes 1 utf8
        """
        m = 'wb' if mode == 0 else 'w'
        with open(filePath, m) as f:
            f.write(data)

    def mkdir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def initDir(self):
        self.mkdir(self.tsPath)

    def restart(self, jsonDir):
        self.readJSON(jsonDir)
        # 判断目标目录是否存在，不存在则重新下载
        if not os.path.exists(self.tsPath):
            print('')
            self.init(self.m3u8Infos['url'], self.m3u8Infos['m3u8Name'])
            self.start()
            return

        st = time.time()
        for tsUrl in self.m3u8Infos['tsInfos']:
            self.tasks.append(self.threadPool.submit(
                self.downloadTsFile, tsUrl['url'], tsUrl['index']))

        for fu in as_completed(self.tasks):
            fu.result()

        if not self.stopdown:
            self.combineTsToMp4()
            self.clearTemp()
            self.saveJSON()
            print('操作完成 共用时:%.2f' % (time.time() - st))
        else:
            self.saveJSON()
            print('操作暂停 共用时:%.2f' % (time.time() - st))

    def start(self):
        self.initDir()
        st = time.time()
        for tsUrl in self.m3u8Infos['tsInfos']:
            self.tasks.append(self.threadPool.submit(
                self.downloadTsFile, tsUrl['url'], tsUrl['index']))

        for fu in as_completed(self.tasks):
            fu.result()

        if not self.stopdown:
            self.combineTsToMp4()
            self.clearTemp()
            self.saveJSON()
            print('操作完成 共用时:%.2f' % (time.time() - st))
        else:
            self.saveJSON()
            print('操作暂停 共用时:%.2f' % (time.time() - st))

    def saveJSON(self):
        with open(self.basePath+f'json/{self.mediaName}.json', 'w') as f:
            f.write(json.dumps(self.m3u8Infos))

    def readJSON(self, dir):
        print(f'读取json文件:{dir}')
        with open(dir, 'r') as f:
            jsonDict = json.loads(f.read())
        # 恢复数据
        self.m3u8Url = jsonDict['url']
        self.basePath = os.path.dirname(__file__) + '/../temp/'
        self.mediaName = jsonDict['m3u8Name']
        self.tsPath = self.basePath + f'ts/{self.mediaName}/'

        self.m3u8Infos = jsonDict

        self.key = self.m3u8Infos['key']

        if self.key[0] == 'AES-128':
            self.decoder = self.decode(*self.key[1:])
        else:
            self.decoder = None

        self.downpercent = ''
        self.downedsuccess = ''
        self.downloaded = jsonDict['downloaded']
        self.err = jsonDict['err']
        self.stopdown = False

        self.threadPool = ThreadPoolExecutor(20)
        self.tasks = []

    def updatePercent(self,):
        self.downedsuccess = str(int(
            ((self.downloaded - self.err) / len(self.m3u8Infos['tsInfos']) * 10000))/100)+'%'
        self.downpercent = str(
            int(self.downloaded/len(self.m3u8Infos['tsInfos']) * 10000)/100)+'%'

        self.m3u8Infos['downloaded'] = self.downloaded
        self.m3u8Infos['err'] = self.err

    def combineTsToMp4(self,):
        print('---开始合并ts---')
        binary = b''
        for tsUrl in self.m3u8Infos['tsInfos']:
            if not os.path.exists(self.tsPath):
                print('重复的任务···\nover')
                return
            with open(self.tsPath + f'{tsUrl["index"]}.ts', 'rb') as f:
                binary += f.read()

        self.write(binary, self.basePath + f'{self.mediaName}.mp4')
        del binary
        gc.collect()
        print('---合并ts成功---')

    def clearTemp(self):
        print('清除ts文件')
        os.popen(f'rmdir /s /Q "{self.tsPath}"')

    def stop(self):
        self.stopdown = True


if __name__ == '__main__':
    # def xx():
    #     while (True):
    #         xxx = input()
    #         print(xxx)
    #         x.stop()
    #         return

    # thread(target=xx).start()

    # x = hlsDowndloader()
    # # x.init('https://v8.dious.cc/20230108/dpuVLjFM/index.m3u8', 'xx-1')
    # x.restart(os.path.dirname(__file__) + '/../temp/'+'json/xx-1.json')

    # x.start()

    # res = requests.post(url='https://api.ylibrary.org/api/search/', json={"keyword": "vtk", "page": 1, "sensitive": False})

    pass
    

