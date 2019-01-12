#coding=utf-8

import requests
from bs4 import BeautifulSoup

from functools import partial

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,de;q=0.7,pt;q=0.6',
    'Connection': 'keep-alive',
}


class GradeFetcher(object):
    def __init__(self, username, password, http_timeout=15, try_to_connect_times=10):
        self._session = requests.Session()
        # initialize customized `get` and `post` methods.
        self._get = partial(self._session.get, headers=HEADERS, timeout=http_timeout)
        self._post = partial(self._session.post, headers=HEADERS, timeout=http_timeout)
        self.username = username
        self.password = password
        self.try_to_connect_times = try_to_connect_times

    def _login(self):
        login_url = 'https://ids.shanghaitech.edu.cn/authserver/login'
        params = {
            "service": 'http://egate.shanghaitech.edu.cn/login?'
                       'service=http://egate.shanghaitech.edu.cn/new/index.html'
        }

        def prepare_login():
            response = self._get(login_url, params=params)
            response.encoding= 'utf-8'
            text = response.text
            soup = BeautifulSoup(text, 'html.parser')
            items = soup.find_all('input', attrs={'type': 'hidden'})
            hidden_data = dict(map(lambda i: (i.get('name'), i.get('value')), items))
            return hidden_data

        hidden_data = prepare_login()
        auth_data = dict(
            username=self.username, password=self.password,
            **hidden_data
        )
        # login
        response = self._post(login_url, params=params, data=auth_data)
        # make sure that the crawler has logged into the site successfully.
        if response.history:
            assert response.history[-1].headers['Location'] == \
                   'http://egate.shanghaitech.edu.cn/new/index.html', 'login failed!'

    def fetch_grade(self):
        manage_url = 'http://grad.shanghaitech.edu.cn/'
        auth_url = 'http://ids.shanghaitech.edu.cn/authserver/login?' \
                   'service=http://grad.shanghaitech.edu.cn/sso/'
        grade_url = 'http://grad.shanghaitech.edu.cn/PostGraduate' \
                    '/WitMis_CourseScoreView.aspx'

        def try_to_connect_manage():
            import os, time

            print('starting try to connect managing website...')
            times = 1
            while True:
                try:
                    print(f'{times} try...')
                    self._get(manage_url)
                except requests.exceptions.ConnectionError:
                    times += 1
                    if times > self.try_to_connect_times:
                        print('connected failed!!!')
                        os._exit(1)
                else:
                    break
            print('connected succeeded!')

        def prepare_grade_list():
            self._login()
            print('logged succeeded!')
            # try to connect managing website
            try_to_connect_manage()
            # multiple redirects
            self._get(auth_url)
            response = self._get(grade_url)
            response.encoding = 'utf-8'
            return response.text

        def convert_text_to_list(tr):
            tds = tr.find_all('td')
            # choose `class_name`, `grade`
            tds = [tds[2], tds[9]]
            return list(map(lambda i: i.text.strip(), tds))

        text = prepare_grade_list()
        soup = BeautifulSoup(text, 'html.parser')
        table = soup.find('table', id='AutoNumber1')
        tbody = table.tbody
        trs = tbody.find_all('tr')
        # title = convert_text_to_list(trs[0])
        classes = list(map(convert_text_to_list, trs[1:-1]))
        return classes


def make_grade_fetcher(cfg):
    return GradeFetcher(cfg.username, cfg.password, cfg.http_timeout)


if __name__ == '__main__':
    import config as cfg
    
    grade_fetcher = make_grade_fetcher(cfg)
    classes = grade_fetcher.fetch_grade()
    print(classes)



