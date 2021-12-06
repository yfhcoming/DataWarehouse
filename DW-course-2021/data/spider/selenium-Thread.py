from threading import Thread

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

proxyMeta = ""

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

ua = UserAgent()

file_name = '../dataProcess/data/page_check.csv'
web_dir = 'D:/Code/CodeWareHouse/py/webPages_robot/pages/'
pages_404 = 'D:/Code/CodeWareHouse/py/webPages_robot/pages_list_404/pages_404.txt'
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

    option = webdriver.ChromeOptions()
    option.add_argument('lang=en')
    option.headless = True
    s = Service(r"C:/Program Files/Google/Chrome/Application/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=option)

    for index, int_p_id in enumerate(p_id_array):
        if (index + 1) % t_max == t_id:
            p_id = str(int_p_id)
            attempts, success = 0, False
            try:
                while attempts < 5 and not success:
                    url = base_url + p_id

                    driver.get(url)
                    html = driver.page_source

                    # result = requests.get(url, proxies=proxies, headers=headers)
                    html = html.encode('gbk', 'ignore').decode('gbk')

                    soup = BeautifulSoup(html, 'lxml')
                    movie_title = str(soup.select('title')[0].getText())
                    if (movie_title.find('Robot Check') == -1) and (movie_title.find('Sorry! Something went wrong!') == -1)and (
                            movie_title.find('Page Not Found') == -1):
                        print('[t_id]: ', t_id, " [p_id]:", p_id)
                        fo = open(web_dir + p_id + ".html", "w", encoding="utf-8")
                        fo.write(html)
                        fo.close()
                        success = True
                        break
                    else:
                        attempts += 1
                        print('[title error]', movie_title, '[t_id]: ', t_id, " [p_id]:", p_id)
                    if attempts == 4:
                        fo = open(pages_404, "a", encoding="utf-8")
                        fo.write(p_id + '\n')
                        fo.close()
            except Exception as e:
                    print('[error]', e)
                    attempts += 1
                    time.sleep(sleep_time)
                    if attempts == 3:
                        break

    driver.quit()


if __name__ == '__main__':
    for t_id in range(threads_num):
        print('[Thread]:', t_id, ' begins')
        t = Thread(target=thread_loop, args=(t_id, threads_num,))
        t.start()
