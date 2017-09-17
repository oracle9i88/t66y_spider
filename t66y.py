# coding:utf-8
# author:wang
# date:2017-09-17
# email:wzw15517028333@gmail.com

import requests
from bs4 import BeautifulSoup
import random
import os
import requests


class t66y(object):
    
    def __init__(self):
        self.url = 'http://t66y.com/thread0806.php?fid=16'
        self.sock5 = '127.0.0.1'
        self.socks_port = 1080

    def requestspic(self, url, Referer):
        '''
        This function gets the response of the image page and returns.
        Randomly select a UA.
        :param url: url
        :param Referer: Referer
        :return: response
        '''
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; rv:11.0) like Gecko"
        ]

        headers = {
            'User-Agent': random.choice(self.user_agent_list),
            'Referer': Referer
        }
        content = requests.get(url, headers=headers, verify=False)
        return content

    def request(self, url):
        '''
        Get the response of the page and then return
        :param url : url
        :return: content
        '''
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }
        content = requests.get(url, headers=header, verify=False)
        return content

    def all_url(self):
        """
        Get the link to Dagel's banner.
        self.img(herf): Download the picture

        """
        html = self.request(self.url)
        html.encoding = 'gbk'
        bsObj = BeautifulSoup(html.text, "html.parser")
        for title in bsObj.find_all('font', {"color": {"green"}}):
            new_title = title.get_text()
            print('Downloading%s' % new_title)
            path = str(new_title).replace("?", '_')
            if not self.mkdir(path):  # Skip existing folders.
                print('Jump Over%s' % title)
                continue
            herf = 'http://t66y.com/' + str(title.parent['href'])
            self.img(herf)

    def mkdir(self, path):
        '''
        :param path: path_name
        '''
        path = path.strip()
        isExists = os.path.exists(os.path.join("C://t66y", path))
        if not isExists:
            print(' Create %s folder!' % path)
            os.makedirs(os.path.join("C://t66y", path))
            os.chdir(os.path.join("C://t66y", path))  ##切换到目录
            return True
        else:
            print('%s The folder already exists !' % path)
            return False

    def img(self, page_url):
        """
        :param page_url: page_url
        self.save() download img to C:\t66y
        """
        img_html = self.request(page_url)
        bsObj = BeautifulSoup(img_html.text, "html.parser")
        for url in bsObj.find_all('input', {'src': True}):
            new_imgae_url = str(url['src'])

            self.save(new_imgae_url, page_url)

    def save(self, img_url, page_url):
        '''
        :param img_url: img_url
        :param page_url: Referer
        :return:
        '''
        name = img_url[-9:-4]
        try:
            img = self.requestspic(img_url, page_url)
            with open(name + '.jpg', 'ab') as f:
                f.write(img.content)
        except FileNotFoundError as e:
            print('error: %s \n image_url:%s') % (e, img_url)
            return False


if __name__ == '__main__':
    t66y = t66y()
    t66y.all_url()