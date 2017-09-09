#coding:utf-8
#author:wang
#date:2017-09-09
#email:wzw15517028333@gmail.com


import requests
import re
import time
from bs4 import BeautifulSoup
import re
import shutil


class t66y(object):

    def __init__(self):
        self.header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6,en-US;q=0.4',
            'Referer':'http://t66y.com/mobile.php?ismobile=yes',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
        }

        self.url='http://t66y.com/thread0806.php?fid=16'


    def get_posts_url(self):
        posts_url=[]
        session=requests.session()
        try:
            index_session=session.get(url=self.url,headers=self.header)
        except BaseException as e:
            print('error',e)
        else:
            index_session.encoding='gbk'
            bsObj=BeautifulSoup(index_session.text,"html.parser")
            for post in bsObj.find_all('font', {"color": {"green"}}):
                posts_url.append('http://t66y.com/'+str(post.parent['href']))
        return posts_url

    def get_image(self):
        imagenum=1
        postsnum=1
        session=requests.session()
        for post_url in self.get_posts_url():
            image_html=session.get(post_url,headers=self.header)
            image_html.encoding='gbk'
            print('正在下载第%s组图片'%postsnum)
            postsnum+=1
            bsObj=BeautifulSoup(image_html.text,"html.parser")
            for url in bsObj.find_all('input',{'src':True}):
                new_url=str(url['src'])
                print('正在下载第%s张图片'%imagenum)
                imagenum+=1
                response = requests.get(new_url, stream=True,verify=False)
                with open(new_url[-8:], 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)

if __name__ == '__main__':
    T66y=t66y()
    T66y.get_image()