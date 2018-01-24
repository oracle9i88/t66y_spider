import os
import asyncio
import random

import aiohttp
from bs4 import BeautifulSoup
from aiosocks.connector import ProxyConnector, ProxyClientRequest

# socks5 addr
socks5 = 'socks5://127.0.0.1:1080'

c_path = os.getcwd()
async def start_urls():

    start_url = 'http://t66y.com/thread0806.php?fid=16'
    async with aiohttp.ClientSession(connector= ProxyConnector(),request_class=ProxyClientRequest) as session:
        async with session.get(start_url, proxy = socks5,) as response:
            if response.status == 200:
                await get_title_url(await response.text(encoding = 'GBK'))

async def get_title_url(response):

    bsobj = BeautifulSoup(response,'lxml')
    for title in bsobj.find_all('font', {"color": {"green"}}):
        new_title = title.get_text()
        print('Downloading%s' % new_title)
        path = str(new_title).replace("?", '_')

        if not mkdir(path):  # Skip existing folders.
            print('Jump Over%s' % path)
            continue

        herf = 'http://t66y.com/' + str(title.parent['href'])
        await find_imgs(herf)

async def find_imgs(page_url):
    '''
    :param page_url:page_url
    :return:
    '''
    async with aiohttp.ClientSession(connector=ProxyConnector(), request_class=ProxyClientRequest) as session:
        async with session.get(page_url, proxy=socks5, ) as response:
            bsobj = BeautifulSoup(await response.text(encoding = 'GBK'), 'lxml')
            for url in bsobj.find_all('input', {'src': True}):
                new_imgae_url = str(url['src'])
                await download(new_imgae_url)

async def download(img_url):
    name = '%d.jpg'%random.randint(1000, 9999)
    async with aiohttp.ClientSession(connector=ProxyConnector(), request_class=ProxyClientRequest) as session:
        async with session.get(img_url, proxy=socks5, ) as response:
            with open(name,'wb') as img_file:
                img_file.write(await response.read())

def mkdir(path):
    '''
    :param path: path_name
    '''
    path = path.strip()
    isExists = os.path.exists(os.path.join(c_path, path))
    if not isExists:
        print(' Create %s folder!' % path)
        os.makedirs(os.path.join(c_path, path))
        os.chdir(os.path.join(c_path, path))  ##切换到目录
        return True
    else:
        print('%s The folder already exists !' % path)
        return False

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [start_urls()]
    loop.run_until_complete(asyncio.wait(tasks))
