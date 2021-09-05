# -*- coding: utf-8 -*-
import requests
import json
import os
import sys
from time import sleep


def main():
    if len(sys.argv) > 1:
        getMusicLyics(sys.argv[1])
        print('结束')
    else:
        print('需要歌曲ID')


def getMusicLyics(song_id):
    try:
        headers = {'Referer': 'http://music.163.com/',
                   'Host': 'music.163.com',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', }
        url_lyric = "http://music.163.com/api/song/lyric?id=%s&lv=-1&kv=-1&tv=-1" % (song_id,)
        res_lyric = str(requests.get(url=url_lyric, headers=headers).content, encoding='utf-8')
        sleep(1)
        res_lyric = json.loads(res_lyric)
        save_path = os.path.join(os.path.dirname(__file__), '%s.lrc' % (song_id, ))
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(res_lyric['lrc']['lyric'])
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    main()
