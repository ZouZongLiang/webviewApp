template = {
    'video_card':
    '''<div class="card" onclick="go_video_index()" id="%s">
                <div class="card_img"
                    style=" background-image: url(%s);">
                </div>
                <div class="hidden"> </div>
                <div class="card_text"> %s </div>
                <div class="score">%s</div>
                <div class="episode">%s</div>
            </div>
        ''',
    'video_card2':
        '''<div class="card2"></div>''',
    'his_card': '''<div class="his_card">
        <img src="%s" alt="">
        <a class='_title' href="%s">%s</a>
        <span>播放到:</span>
        <i>第%s集</i>
        <a href="%s" class="button">继续播放</a>
    </div>
    ''',
    'episode_div': '<div class="episode_card" onclick="select_episode(%s)">%s</div>',
    # %s => 背景图链接 剧名 演员 简介 资源面板
    'detail_panel': '''<div class="bg"><svg onclick="ask_download()" t="1671846005666" class="d_icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5288" width="32" height="32"><path d="M96 896h832c17.673 0 32 14.327 32 32 0 17.673-14.327 32-32 32H96c-17.673 0-32-14.327-32-32 0-17.673 14.327-32 32-32z m448.906-132.192l276.45-276.45c12.497-12.496 32.758-12.496 45.255 0 12.497 12.497 12.497 32.759 0 45.255L535.597 863.627c-12.497 12.497-32.758 12.497-45.255 0L148.546 524.483c-12.497-12.496-12.497-32.758 0-45.254 12.496-12.497 32.758-12.497 45.254 0l287.106 284.453 0.032-667.427c0-17.673 14.327-32 32-32 17.673 0 32 14.327 32 32l-0.032 667.553z" p-id="5289" fill="#1296db"></path></svg><svg onclick="close_detail()" t="1671845148532" class="x_icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2678" width="32" height="32"><path d="M507.168 473.232L716.48 263.936a16 16 0 0 1 22.624 0l11.312 11.312a16 16 0 0 1 0 22.624L541.12 507.168 750.4 716.48a16 16 0 0 1 0 22.624l-11.312 11.312a16 16 0 0 1-22.624 0L507.168 541.12 297.872 750.4a16 16 0 0 1-22.624 0l-11.312-11.312a16 16 0 0 1 0-22.624l209.296-209.312-209.296-209.296a16 16 0 0 1 0-22.624l11.312-11.312a16 16 0 0 1 22.624 0l209.296 209.296z" fill="#1296db" p-id="2679"></path></svg><img src="%s"><span class="title">%s</span><span class="actor">演员：</span><span class="actors">%s</span><span class="intro">简介：</span><p class="intro_text">%s</p><!--资源table--><div class="episode_panel">%s</div></div>''',
    # 资源面板-单选框 %s => id checked_status id source_name
    'source_panel_radio': '''<input type="radio"id="%s"name="tab"checked="%s"><label for="%s">%s</label> ''',
    # 资源面板-所有集 %s => radio_id+'-1' source_panel_episode_episode*n
    'source_panel_episode_source': '''<div class="tab_content"id="%s">%s</div>''',
    # 资源面板-所有集 %s => radio_id episode_id episode_name
    'source_panel_episode_episode': '''<div class="episode_div"onclick="play(%s,%s)">%s</div>''',

    # 下载列表 进行中的任务 %s => 序号 序号 标题 完整度 下载进度
    "task_tr": '''<tr id="tr-%s"><td class="td-0">%s</td><td class="td-1">%s</td><td class="td-2"><img src="..\\img\\start.svg"></td><td class="td-3"><span class="span-1">%s</span><span class="span-2">%s</span></td><td class="td-4"><img src="..\\img\\ashbin.svg"onclick="delete_tr('')"><img src="..\\img\\file.svg"onclick="explore_tr('')"></td></tr>''',
    # 下载列表 完成的任务 %s => 序号 序号 标题 完整度
    "ok_tr": '''<tr id="ok-%s"><td class="oktd-0">%s</td><td class="td-1">%s</td><td class="td-2"><img src="..\\img\\ok.svg"></td><td class="td-3"><span class="span-1">%s</span><span class="span-2">100%</span></td><td class="td-4"><img src="..\\img\\ashbin.svg"onclick="delete_tr('ok')"><img src="..\\img\\file.svg"onclick="explore_tr('ok')"></td></tr>'''
}

api_url = {
    "天空资源": "https://api.tiankongapi.com/api.php/provide/vod/",
    "鱼乐资源": "https://api.ylzy1.com/api.php/provide/vod/",
    "新浪资源": "http://api.xinlangapi.com/xinlangapi.php/provide/vod/",
    "卧龙资源": "https://collect.wolongzyw.com/api.php/provide/vod/",
    "量子资源": "http://cj.lziapi.com/api.php/provide/vod/",
    "FOX资源": "https://api.foxzyapi.com/api.php/provide/vod/",
    "南国影院": "http://api.nguonphim.tv/api.php/provide/vod/",
    "考拉TV": "https://ikaola.tv/api.php/provide/vod/",
    "光速资源": "https://api.guangsuapi.com/api.php/provide/vod/",
    "红牛资源": "https://www.hongniuzy2.com/api.php/provide/vod/",
    "U酷资源": "https://api.ukuapi.com/api.php/provide/vod/",
    "快播资源": "http://www.kuaibozy.com/api.php/provide/vod/",
    "百度云": "https://api.apibdzy.com/api.php/provide/vod/from/dbm3u8/",
    "樱花资源": "https://m3u8.apiyhzy.com/api.php/provide/vod/",
    "39影视": "https://www.39kan.com/api.php/provide/vod/",
}

api_tid = {
    "天空资源": {
        '默认分类': '',
        "电影": "1",
        "纪录片": "2",
        "连续剧": "3",
        "欧美剧": "4",
        "香港剧": "5",
        "动作片": "6",
        "爱情片": "7",
        "科幻片": "8",
        "恐怖片": "9",
        "剧情片": "10",
        "战争片": "11",
        "喜剧片": "12",
        "动画片": "20",
        "犯罪片": "21",
        "国产剧": "22",
        "韩国剧": "23",
        "动漫": "24",
        "综艺": "25",
        "大陆综艺": "26",
        "港台综艺": "27",
        "日韩综艺": "28",
        "欧美综艺": "29",
        "台湾剧": "30",
        "国产动漫": "31",
        "日本动漫": "32",
        "欧美动漫": "33",
        "海外动漫": "34",
        "泰国剧": "35",
        "日剧": "36",
        "电影解说": "37",
        "奇幻片": "38",
        "灾难片": "39",
        "悬疑片": "40",
        "其他片": "41"
    }
}

api_title = ["天空资源", "鱼乐资源", "新浪资源", "卧龙资源", "量子资源", "FOX资源", "南国影院", "考拉TV",
             "光速资源", "红牛资源", "U酷资源", "快播资源", "百度云", "樱花资源", "39影视", "一拳动漫", "八戒资源"]

card_keys = ['vod_id', 'vod_pic', 'vod_name',
             'vod_score', 'vod_remarks', 'type_id']

