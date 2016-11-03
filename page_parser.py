from bs4 import BeautifulSoup
import requests
import time
import pymongo
import random
from multiprocessing import Pool
from channel_extract import all_pages_links

client = pymongo.MongoClient('localhost', 27017)
tongcheng = client['tongcheng']
url_list = tongcheng['url_list']
item_info = tongcheng['item_info']

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection': 'keep-alive'
}

# http://cn-proxy.com/
# proxy_list = [
#     'http://117.177.250.151:8081',
#     'http://111.85.219.250:3129',
#     'http://122.70.183.138:8118',
#     ]
# proxy_ip = random.choice(proxy_list) # 随机获取代理ip
# proxies = {'http': proxy_ip}



# spider 1
class link_info(object):
    def __init__(self):
        self.pool = Pool(processes=4)

    def get_links_from(self, channel, pages, who_sell=0):
        #http://cd.58.com/shouji/0/pn3/
        link_view = '{}{}/pn{}/'.format(channel, str(who_sell), str(pages))
        wb_data = requests.get(link_view, headers=headers)
        time.sleep(1)
        links = []
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if soup.find('td', 't'):
            for link in soup.select('td.t a.t'):
                item_link = link.get('href').split('?')[0]
                # get_item_info(item_info)
                url_list.insert_one({'url': item_link})
                print(item_link)
                links.append(item_link)
        else:
            pass
        return links

    def get_item_info(self, url):
        wb_data = requests.get(url, headers=headers)
        # no_longer_exist = '404' in soup.find('script', type="text/javascript").get('src').split('/')
        if wb_data.status_code == 404:
            pass
        else:
            soup = BeautifulSoup(wb_data.text, 'lxml')
            title = soup.title.text
            price = soup.select('span.price_now')[0].text if soup.find('span', 'price_now') else None
            if soup.find_all('span'):
                area = soup.select('div.palce_li > span')[0].text
                print(area)
            elif soup.find_all(''):
                area = soup.select()

            item_info.insert_one({
                 'title': title,
                 'price': price,
                 'area': area
            })
            print(item_info)

    def craw(self, channel, pages, who_sell=0):
        links = self.get_links_from(channel, pages, who_sell=0)
        for link in links:
            self.get_item_info(link)

# if __name__ == '__main__':
#
#     a = link_info()
#     a.get_item_info('http://zhuanzhuan.58.com/detail/747679335197016066z.shtml')

if __name__ == '__main__':
    a = link_info()
    for url in all_pages_links:
        for i in range(1, 101):
            a.craw(url, i)



# urls = get_links_from('http://cd.58.com/shuma/', 2)
# print(urls)
# for link in urls:
#     get_item_info(link)


# def get_all_links_from(channel):
#     for i in range(1, 2):
#         get_links_from(channel, i)


# spider 2


# if __name__ == '__main__':
#     pool = Pool()
#     urls = [
#     "http://zhuanzhuan.58.com/detail/780691227699150852z.shtml",
#     'http://cd.58.com/xiaoyuan/26816545046076x.shtml'
#     'http://cd.58.com/xiaoyuan/27217046880699x.shtml'
#     'http://cd.58.com/xiaoyuan/26987155260108x.shtml']
#     for url in urls:
#
#         get_item_info(url)

# if __name__ == '__main__':
#     pool = Pool()
#     pool.map(get_all_links_from, channel_list.split())
#     # print(type(links))
#     # for link in url:
#     #     get_item_info(link)

# get_item_info(links)
# url = ''
# wb_data = requests.get(url)
# soup = BeautifulSoup(wb_data.text, 'lxml')
# print(soup.prettify())

# get_links_from('http://cd.58.com/shuma/', 2)
#
# get_item_info('http://zhuanzhuan.58.com/detail/777746371933814785z.shtml')

