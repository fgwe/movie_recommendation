import csv
import re
import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from html_download import HtmlDownload


class Handle():
    # def __init__(self):
    #     self.

    def handle(self, content):
        if content is None:
            return '', '', ''
        soup = BeautifulSoup(content, 'html.parser')
        genres_tmp = soup.find(class_='genres')
        genres = genres_tmp.get_text()
        # print(genres)
        genres = re.sub(r'\s+', '', genres)
        overview_tmp = soup.find(class_='overview')
        overview = overview_tmp.get_text()
        overview = overview.replace('\n', '')
        overview.strip()
        img_tmp = soup.find(class_='backdrop')
        img_url = ''
        if img_tmp and img_tmp.img:
            tmp = img_tmp.img
            try:
                img_url = tmp['src']
            except:
                pass
        img_url = img_url.replace('_filter(blur)', '')
        return genres, overview, img_url


if __name__ == '__main__':
    ti = time.time()
    dl = HtmlDownload()
    test = Handle()
    f = open('ml-latest-small/movie2.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(f)
    # writer.writerow(['movieId', 'title', 'genres', 'overview', 'imgurl'])
    df1 = pd.read_csv('ml-latest-small/links.csv', dtype={'tmdbId': str})
    df2 = pd.read_csv('ml-latest-small/movies.csv')
    df = pd.merge(df1, df2, on='movieId')
    num = 3115
    for i in range(3116,6000):
        num += 1
        text = dl.download(df.loc[i]['tmdbId'])
        genres1, overview1, img_url1 = test.handle(text)
        if genres1 != '':
            writer.writerow([df.loc[i]['movieId'], df.loc[i]['title'], genres1, overview1, img_url1])
            # print(df.loc[i]['movieId'])
            print(num, '、', df.loc[i]['title'], ' ', img_url1,' ',time.time()-ti)
    f.close()
