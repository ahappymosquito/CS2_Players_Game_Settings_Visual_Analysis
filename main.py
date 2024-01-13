import csv
import time

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://prosettings.net/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'cmplz_saved_categories=["marketing","statistics","preferences","functional"]; cmplz_saved_services={}; google-analytics_v4_IHyH__engagementDuration=0; google-analytics_v4_IHyH__ga4sid=988145713; google-analytics_v4_IHyH__session_counter=1; google-analytics_v4_IHyH__ga4=61929da8-c8c0-444c-8675-30efe80835c7; google-analytics_v4_IHyH___z_ga_audiences=61929da8-c8c0-444c-8675-30efe80835c7; advanced_ads_pro_visitor_referrer=%7B%22expires%22%3A1736679013%2C%22data%22%3A%22https%3A%2F%2Fprosettings.net%2F%22%7D; _ga=GA1.1.129696637.1705143014; cmplz_consented_services=; cmplz_policy_id=37; cmplz_marketing=allow; cmplz_statistics=allow; cmplz_preferences=allow; cmplz_functional=allow; advanced_ads_visitor=%7B%22browser_width%22%3A306%7D; advanced_ads_page_impressions=%7B%22expires%22%3A2020503013%2C%22data%22%3A2%7D; google-analytics_v4_IHyH__engagementStart=1705143162499; google-analytics_v4_IHyH__counter=5; google-analytics_v4_IHyH__let=1705143162499; _ga_Z7WWLGPBME=GS1.1.1705143013.1.0.1705143160.0.0.0',
}


def get_players_url():
    url = "https://prosettings.net/games/cs2/"
    # url_num = "https://prosettings.net/games/cs2/page/2/"

    res = requests.get(url, headers=headers)
    # print(res.text)

    bs = BeautifulSoup(res.text, 'lxml')
    players = bs.find_all(class_="card cta-box player linked")
    # players_url = bs.find_all(class_="js-link-target")

    players_urls = []

    for player in players:
        a_tag = player.find('a', class_='js-link-target')
        if a_tag:
            player_url = a_tag.get('href')
            players_urls.append(player_url)

    for i in range(2, 35):
        url_num = "https://prosettings.net/games/cs2/page/{}/".format(i)

        res = requests.get(url_num, headers=headers)
        # print(res.text)

        bs = BeautifulSoup(res.text, 'lxml')
        players = bs.find_all(class_="card cta-box player linked")

        for player in players:
            a_tag = player.find('a', class_='js-link-target')
            if a_tag:
                player_url = a_tag.get('href')
                players_urls.append(player_url)

        time.sleep(0.2)

    print("共有{}位职业哥记录在案".format(len(players_urls)))
    # print(get_players_url())

    return players_urls


def save_players_data(players_url):
    for url in players_url:

        res = requests.get(url, headers=headers)
        # print(res.text)

        bs = BeautifulSoup(res.text, 'lxml')

        # 个人信息
        info = {}
        bio = bs.find(id="bio")
        name = bio.find('h1').text
        info['nick'] = name

        rows = bio.find('table').find_all('tr')
        for row in rows:
            label = row.find_all('th')
            data = row.find_all('td')
            for la, da in zip(label, data):
                info[la.text.strip()] = da.text.strip()
        # print(info)


        # 鼠标设置
        mouse = {}
        cs2_mouse = bs.find(id="cs2_mouse")
        model = cs2_mouse.find('h4').text
        mouse['model'] = model

        rows = cs2_mouse.find('table').find_all('tr')
        for row in rows:
            label = row.find_all('th')
            data = row.find_all('td')
            for la, da in zip(label, data):
                mouse[la.text.strip()] = da.text.strip()
        # print(mouse)

        # 准星设置
        crosshair = {}
        cs2_crosshair = bs.find(id="cs2_crosshair")

        rows = cs2_crosshair.find('table').find_all('tr')
        for row in rows:
            label = row.find_all('th')
            data = row.find_all('td')
            for la, da in zip(label, data):
                crosshair[la.text.strip()] = da.text.strip()
        # print(crosshair)

        # 持枪视角
        viewmodel = {}
        cs2_viewmodel = bs.find(id="cs2_viewmodel")

        rows = cs2_viewmodel.find('table').find_all('tr')
        for row in rows:
            label = row.find_all('th')
            data = row.find_all('td')
            for la, da in zip(label, data):
                viewmodel[la.text.strip()] = da.text.strip()
        # print(viewmodel)

        # 视频设置
        video = {}
        cs2_video_settings = bs.find(id="cs2_video_settings")

        rows = cs2_video_settings.find('table').find_all('tr')
        for row in rows:
            label = row.find_all('th')
            data = row.find_all('td')
            for la, da in zip(label, data):
                video[la.text.strip()] = da.text.strip()
        # 高级视频设置

        advanced_video = bs.find(id="advanced_video")

        rows = advanced_video.find('table').find_all('tr')
        for row in rows:
            label = row.find_all('th')
            data = row.find_all('td')
            for la, da in zip(label, data):
                video[la.text.strip()] = da.text.strip()
        # print(video)

        # 界面大小
        hud = {}
        cs2_hud = bs.find(id="cs2_hud")

        rows = cs2_hud.find('table').find_all('tr')
        for row in rows:
            label = row.find_all('th')
            data = row.find_all('td')
            for la, da in zip(label, data):
                hud[la.text.strip()] = da.text.strip()
        # print(hud)

        # 雷达大小
        radar = {}
        cs2_radar = bs.find(id="cs2_radar")

        rows = cs2_radar.find('table').find_all('tr')
        for row in rows:
            label = row.find_all('th')
            data = row.find_all('td')
            for la, da in zip(label, data):
                radar[la.text.strip()] = da.text.strip()
        # print(radar)

        # 皮肤
        rows = (bs.find(id="cs2_skins"))
        if rows:
            rows = rows.find_all('h4')

            skins = {'skins' : [skin.text.strip() for skin in rows[1:]]}
            # print(skins)

        # 外设
        device = bs.find(id="gear").find_all(class_="cta-box__tag cta-box__tag--top-right")
        rows = bs.find(id="gear").find_all('h4')
        # gear = [skin.text.strip() for skin in rows]
        gear = {device.text.strip(): name.text.strip() for device, name in zip(device, rows)}
        # print(gear)

        # 显示器设置
        game_set = {}
        game_settings = bs.find(id="game_settings")
        if game_settings:
            rows = game_settings.find('table')
            if rows:
                rows = rows.find_all('tr')
                for row in rows:
                    label = row.find_all('th')
                    data = row.find_all('td')
                    for la, da in zip(label, data):
                        game_set[la.text.strip()] = da.text.strip()

                picture = bs.find(id="picture")

                rows = picture.find('table').find_all('tr')
                for row in rows:
                    label = row.find_all('th')
                    data = row.find_all('td')
                    for la, da in zip(label, data):
                        game_set[la.text.strip()] = da.text.strip()
                # print(game_set)

        ####################################################################
        # info mouse crosshair viewmodel video hud radar skins gear game_set
        csv_file_path = 'data/{}.csv'.format(info['nick'])

        with open(csv_file_path, 'w', newline='',encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            # 写入表头（第一行）
            csv_writer.writerow(['设置', '选项名称', '值'])

            # 遍历并写入数据
            def write_data(setting, parameters):
                for parameter, value in parameters.items():
                    csv_writer.writerow([setting, parameter, value])

            write_data('选手信息', info)
            write_data('鼠标', mouse)
            write_data('准星设置', crosshair)
            write_data('持枪 视角', viewmodel)
            write_data('视频设置', video)
            write_data('界面 大小', hud)
            write_data('雷达', radar)
            write_data('展示皮肤', skins)
            write_data('外设', gear)
            write_data('显示器设置', game_set)

        print(f'数据成功保存在{csv_file_path}')

        time.sleep(0.2)


if __name__ == "__main__":
    test_url = ["https://prosettings.net/players/s1mple/", "https://prosettings.net/players/niko/",'https://prosettings.net/players/scream/#cs2']
    save_players_data(test_url)

    # save_players_data(get_players_url())
