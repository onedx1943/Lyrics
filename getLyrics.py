# -*- coding: utf-8 -*-
import requests
import json
import os
from time import sleep


def main():
    base_dir = os.path.dirname(__file__)
    music_dir = os.path.join(base_dir, 'music')
    if not os.path.exists(music_dir):
        print('文件夹不存在: %s' % (os.path.abspath(music_dir),))
        return
    print('开始获取歌词')
    output_dir = os.path.join(base_dir, 'lyric')
    faile_list = []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.endswith('.flac') or file.endswith('.mp3'):            
                file_path = os.path.join(root, file)
                music_name = os.path.splitext(os.path.basename(file))[0]
                result = getMusicLyics(music_name, output_dir)
                if not result:
                    faile_list.append(music_name)
                print('下载歌词: %s, %s' % (file_path, result))
    print('获取结束')
    print('歌词保存目录: %s' % (os.path.abspath(output_dir),))
    with open(os.path.join(base_dir, 'faile.txt'), 'w', encoding='utf-8') as file:
        for name in faile_list:
            file.write(name)


def getMusicLyics(name, output_path):
    try:
        headers = {'Referer': 'http://music.163.com/',
                   'Host': 'music.163.com',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', }
        url_search = 'http://music.163.com/api/cloudsearch/pc'
        data_search = {'s':name, 'offset':0, 'limit':1, 'type':1}
        res_song = str(requests.post(url=url_search, headers=headers, data=data_search).content, encoding='utf-8')
        sleep(1)
        res_song = json.loads(res_song)
        song_id = res_song['result']['songs'][0]['id']
        url_lyric = "http://music.163.com/api/song/lyric?id=%s&lv=-1&kv=-1&tv=-1" % (song_id,)
        res_lyric = str(requests.get(url=url_lyric, headers=headers).content, encoding='utf-8')
        sleep(1)
        res_lyric = json.loads(res_lyric)
        save_path = os.path.join(output_path, '%s.lrc' % (name, ))
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(res_lyric['lrc']['lyric'])
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    main()
