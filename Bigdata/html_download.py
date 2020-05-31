import json
import time

import requests


class HtmlDownload(object):

    def download(self, id):
        url = 'https://www.themoviedb.org/movie/' + str(id)
        try:
            r = requests.get(url, timeout=3)
        except:
            return None
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None


if __name__ == "__main__":
    pass
