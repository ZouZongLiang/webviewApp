# encoding utf-8
import json
import requests
import webview
from data import *
from classes import *



class ApiForJS:
    def __init__(self, ):
        self.now_url = None
        self.now_from = None
        self.player_win = None
        self._tid = None
        self._page = 1
        self._vid = None
        self.total_pg = 1
        self.wd = None

        self.video_urls = []
        self.video_title = ''

    # first loading
    def first_loading(self):
        url = api_url['天空资源'] + "?ac=videolist"
        try:
            res = requests.get(url=url, timeout=20, verify=False, allow_redirects=True)
        except Exception as e:
            print(e)
            return '<p style="font-size:28px; margin: 0 auto;">request failed</p>', '共0页'
        res_json = json.loads(res.text)
        self.total_pg = res_json['pagecount']
        self._page = 1
        print(self.total_pg)
        card_info = []
        card_infos = []
        res = ''

        for n in res_json['list']:
            for k in card_keys:
                card_info.append(n[k])
            card_infos.append(template['video_card'] % tuple(card_info[:5]))
            card_info = []

        while len(card_infos) % 5 != 0:
            card_infos.append(template['video_card2'])

        for i in card_infos:
            res += i

        return res, f'共{res_json["pagecount"]}页'

    # 控制全屏
    def full_screen(self, keycode):
        win2 = self.player_win
        if keycode == 27:
            print(win2.fullscreen)
            if win2.fullscreen:
                win2.toggle_fullscreen()
                win2.fullscreen = False
                win2.resize(width=800, height=600)
            else:
                pass
        if keycode == 122:
            if win2.fullscreen:
                win2.toggle_fullscreen()
                win2.fullscreen = False
                win2.resize(width=800, height=600)
            else:
                win2.toggle_fullscreen()
                win2.fullscreen = True

    # 输出web消息
    def p(self, s):
        print('web:', s)

    # 清除本地视频记录
    def clear_his(self):
        pass

    # 视频详情页
    def get_video_id(self, id):
        self.video_urls = []
        print('vedio id:' + id)
        url = api_url['天空资源'] + "?ac=videolist" + f'&ids={id}'
        res = requests.get(url=url, timeout=20, verify=False, allow_redirects=True)
        res_json = json.loads(res.text)
        res_json = res_json['list'][0]
        # print(res_json)
        v_data = []
        v_data.append(res_json['vod_pic'])
        v_data.append(res_json['vod_name'])
        v_data.append(res_json['vod_actor'])
        v_data.append(res_json['vod_blurb'])
        play_from = res_json['vod_play_from'].split('$$$')
        play_url = res_json['vod_play_url'].split('$$$')

        # 筛取有效m3u8资源
        for i in play_url:
            urls = i.split("#")

            if '.' not in urls[0][-6:]:
                play_from.pop(play_url.index(i))
                play_url.pop(play_url.index(i))
        panel_radio = ''
        episode_source = ''

        for num, _platform in enumerate(play_from):
            self.video_urls.append([])
            panel_radio += template['source_panel_radio'] % (
                f'l{num + 1}', 'false' if num != 0 else 'true', f'l{num + 1}', _platform)
            # print(panel_radio)
            urls = play_url[num].split("#")
            episode_episode = ''
            for i in urls:
                if '$' in i:
                    _i = i.split('$')
                else:
                    _i = i.split('http')
                    if _i[0].endswith('$'):
                        _i[0] = _i[0][:-1]
                    _i[1] = 'http' + _i[1]
                if _i[1].find('.m3u8') > 0 or _i[1].find('.mp4') > 0:
                    self.video_urls[num].append([_i[0], _i[1]])
                    episode_episode += template['source_panel_episode_episode'] % (num, urls.index(i), _i[0])
            episode_source += template['source_panel_episode_source'] % (f'l{num + 1}-1', episode_episode)

        v_data.append(panel_radio + episode_source)
        self.video_title = v_data[1]
        return template['detail_panel'] % tuple(v_data)

    # 设置api 未使用
    def set_api(self, _api):
        pass

    # 跳转页面
    def go_pg(self, target):
        print(f'跳转到{target}')

        target = str(target)
        if target == 'f_pg':
            self._page = 1
        if target == 'p_pg':
            self._page -= 1
        if target == 'n_pg':
            self._page += 1
        if target == 'l_pg':
            self._page = self.total_pg
        if target == '' or (not target.endswith('_pg') and target.isdigit()):
            self._page = 1
        if target.isdigit():
            self._page = int(target)

        url = api_url['天空资源'] + "?ac=videolist"
        if self._tid is not None:
            url += f"&t={self._tid}"
        if self.wd is not None:
            url += f"&wd={self.wd}"

        url += f"&pg={self._page}"

        res = requests.get(url=url, timeout=20, verify=False, allow_redirects=True)
        res_json = json.loads(res.text)
        # print(res_json['list'][0])
        card_info = []
        card_infos = []
        res_card_infos = ''

        for n in res_json['list']:
            for k in card_keys:
                card_info.append(n[k])
            card_infos.append(template['video_card'] % tuple(card_info[:5]))
            card_info = []

        while len(card_infos) % 5 != 0:
            card_infos.append(template['video_card2'])

        for i in card_infos:
            res_card_infos += i

        res = {
            'cards': res_card_infos,
            'now_pg': f'第{self._page}页',
        }
        return res

    def get_class_info(self, api_name="天空资源", tid=None, pg=1):
        print(api_name, tid, pg)
        self.wd = None
        self._tid = api_tid['天空资源'][tid[1:]]
        self._page = 1
        url = api_url[api_name] + "?ac=videolist" + f"&t={api_tid['天空资源'][tid[1:]]}" + f"&pg={pg}"
        res = requests.get(url=url, timeout=20, verify=False, allow_redirects=True)
        res_json = json.loads(res.text)

        self.total_pg = res_json['pagecount']
        print(self.total_pg)
        card_info = []
        card_infos = []
        res = ''

        for n in res_json['list']:
            for k in card_keys:
                card_info.append(n[k])
            card_infos.append(template['video_card'] % tuple(card_info[:5]))
            card_info = []

        while len(card_infos) % 5 != 0:
            print(len(card_infos))
            card_infos.append(template['video_card2'])

        for i in card_infos:
            res += i

        return res, f'共{res_json["pagecount"]}页'

    def play(self, _from, _url):
        print(self.video_urls[_from][_url])
        self.now_url = _url
        self.now_from = _from
        if self.player_win is not None:
            if not self.player_win.closed:
                self.player_win.destroy()

        self.player_win = webview.create_window(self.video_title + '-' + self.video_urls[_from][_url][0],
                                                url=r'..\static\html\video_player.html', js_api=api)
        self.player_win.show()
        self.player_win.events.closed += self.player_closed
        self.player_win.closed = False

    def get_episodes(self):
        ret = {
            'now_url': self.video_urls[self.now_from][self.now_url][1],
            'episodes': self.video_urls[self.now_from]
        }
        e_card = ''
        for num, i in enumerate(self.video_urls[self.now_from]):
            e_card += template['episode_div'] % (num, i[0])
        ret['data'] = e_card
        print(ret)
        return ret

    def select_episode(self, e_id):
        self.player_win.set_title(self.video_title + '-' + self.video_urls[self.now_from][e_id][0])

    def search_this(self, wd):
        self._tid = None
        self.wd = wd

        _url = api_url['天空资源'] + "?ac=videolist" + f"&wd={self.wd}"
        res = requests.get(url=_url, timeout=20, verify=False, allow_redirects=True)
        res_json = json.loads(res.text)

        self.total_pg = res_json['pagecount']
        print(self.total_pg)

        card_info = []
        card_infos = []
        res = ''

        for n in res_json['list']:
            for k in card_keys:
                card_info.append(n[k])
            card_infos.append(template['video_card'] % tuple(card_info[:5]))
            card_info = []

        while len(card_infos) % 5 != 0:
            print(len(card_infos))
            card_infos.append(template['video_card2'])

        for i in card_infos:
            res += i

        return res, f'共{res_json["pagecount"]}页'

    def player_closed(self):
        if self.player_win is not None:
            self.player_win.closed = True

    def open_dl_panel(self):
        dl_window = webview.create_window(title="Download", js_api=api, width=1016, height=839, url=r'../static/html/download.html')
        dl_window.show()

    


api = ApiForJS()
main_window = webview.create_window(title='VIDEO ONLINE', url=r'../static/html/index.html', js_api=api,
                               resizable=True, width=1216, height=939)

webview.start(debug=True, http_server=False,)

