import requests as rq
import asyncio
import time
import sys
import csv

from bs4 import BeautifulSoup
from proxybroker import Broker

async def show(proxies, proxy_list):
    while True:
        proxy = await proxies.get()
        if proxy is None:
            # print('done...')
            break
        proxy_list.append(f'{proxy.host}:{proxy.port}')
        # print('Found proxy: %s' % proxy)
        # print(proxy_list)

def get_proxy():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    proxy_list = []
    tasks = asyncio.gather(
        broker.find(types=['HTTPS'], limit=10),
        show(proxies, proxy_list))
    loop = asyncio.get_event()
    loop.run_until_complete(tasks)
    return proxy_list


def clean_proxy():
    proxy_use = []
    proxies = get_proxy()
    for proxy in proxies:
        print(f'Running {proxy}')
        proxies = {
            'https': 'https://' + proxy
            }
        target_url = "https://www.mlbtraderumors.com"

        try:
            res = rq.get(target_url, proxies=proxies, timeout=10)
        except EnvironmentError:
            print('Try Error!')
            continue
        time.sleep(3)
        if not res.ok:
            print('Request fail')
            continue
        else:
            proxy_use.append(proxy)

    return proxy_use


def start():
    code_list = clean_proxy()
    print('------------------------------------------------------')
    print('Proxies can be used:', code_list)
    print('------------------------------------------------------')
    proxy_num = 0
    finish = 0
    target_url = "https://www.mlbtraderumors.com"
    while finish == 0:
        final_proxy = {
            'https': 'https://' + code_list[proxy_num]
            }
        print('The proxy is be using:', final_proxy)

        try:
            res = rq.get(target_url, proxies=final_proxy, timeout=10)
        except rq.exceptions.ConnectionError as e:
            print(e)
            print('------------------------------------------------------')
            r = "No response"
            proxy_num += 1
            if proxy_num >= len(code_list):
                break
            else:
                continue

        if not res.ok:
            print('Request fail')
            proxy_num += 1
            if proxy_num >= len(code_list):
                break
            else:
                continue

        time.sleep(5)
        res.encoding = 'utf-8'
        soup_rumors = BeautifulSoup(res.text, 'html.parser')
        crawler(soup_rumors)
        finish += 1

def crawler(soup_rumors):
    article_num = 0
    final_data = []
    url_quan_list = []
    user_article_num = sys.argv[1:]
    all_content = soup_rumors.select('.content .entry-title a')
    for quan in all_content:
        url_slice = str(quan).split('mlbtraderumors.com')[1].split('"')[0]
        url_quan_list.append(url_slice)
    for url_slice_quan in url_quan_list[1:int(user_article_num[0])+1]:
        content_url = f'https://www.mlbtraderumors.com{url_slice_quan}'
        # print(content_url)

        res2 = rq.get(content_url)
        time.sleep(5)
        article_soup = BeautifulSoup(res2.text, 'html.parser')

        article_title = article_soup.select('.content .entry-header .entry-title')
        title = str(article_title).split('>')[1].strip('</h1')
        # print(title)

        article_content = article_soup.select('.content .entry-content')
        for senetnces in article_content:
            final_text = senetnces.text.strip('\n')
            # print(final_text)

        article_tags = article_soup.select('.entry-meta .entry-categories')
        tags_mix = str(article_tags).split('>')
        tags_list = []
        for tags in tags_mix:
            if '</a' in tags:
                tag = tags.strip('</a')
                tags_list.append(tag)
                final_tags = ';'.join(tags_list)
                # print(final_tags)

        article_date = article_soup.select('.entry-meta .entry-time')
        date = str(article_date).split('datetime="')[1].split('T')[0]
        # print(date)

        final_data.append((
                    title,
                    content_url,
                    final_text,
                    final_tags,
                    'Rumors',
                    date
                ))
        article_num += 1
        print('articles be added：', article_num)

    # print(final_data)

    # with open('MLB_rumors.csv', 'w', newline='', encoding='utf-8-sig') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerow(['title','url','content','tags','category','date'])
    #     for row in final_data:
    #         writer.writerow(row)

def main():
    start()

if __name__ == '__main__':
    main()