from threading import Thread

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from selenium import webdriver

proxyMeta = ""

proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
}


ua = UserAgent()

file_name = '../dataProcess/data/rawData/test.csv'
web_dir = 'D:/Code/CodeWareHouse/py/page-requests/'
batch_size = 8
threads_num = 8
sleep_time = 0.5
base_url = 'https://www.amazon.com/dp/'
headers = {
    "User-Agent": ua.random,
    "Connection": "closer",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}

# 随机ip代理获取
PROXY_POOL_URL = 'http://localhost:5555/random'
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            # print(response.text)
            return response.text
    except ConnectionError:
        return None

def thread_loop(t_id, t_max):
    # 读取p_id
    df = pd.read_csv(file_name)['pid']
    p_id_array = df.values
    for index, p_id in enumerate(p_id_array):
        if (index + 1) % t_max == t_id:
            attempts, success = 0, False
            while attempts < 5 and not success:
                try:
                    while True:
                        url = base_url + p_id
                        # proxyMeta = get_proxy()
                        # proxies = {
                        #     "http": 'http://' + proxyMeta,
                        #     "https": 'https://' + proxyMeta,
                        # }
                        result = requests.get(url, proxies=proxies, headers=headers)
                        result = result.text.encode('gbk', 'ignore').decode('gbk')
                        soup = BeautifulSoup(result, 'lxml')
                        movie_title = str(soup.select('title')[0].getText())
                        if (movie_title != 'Robot Check') and (movie_title != 'Sorry! Something went wrong!') and (movie_title != 'Amazon.com'):
                            print('[t_id]: ', t_id, " [p_id]:", p_id)
                            fo = open(web_dir + p_id + ".html", "w")
                            fo.write(result)
                            fo.close()
                            success = True
                            break
                        else:
                            print('[title error]', movie_title, '[t_id]: ', t_id, " [p_id]:", p_id)
                except Exception as e:
                    print('[error]', e)
                    attempts += 1
                    time.sleep(sleep_time)
                    if attempts == 3:
                        break


if __name__ == '__main__':
    for t_id in range(threads_num):
        print('[Thread]:', t_id, ' begins')
        t = Thread(target=thread_loop, args=(t_id,threads_num,))
        t.start()
