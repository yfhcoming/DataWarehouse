
import requests
# 引入 requests，实现请求
import pandas as pd
import time

from bs4 import BeautifulSoup
from codecs import open

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Connection": "closer",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}

base_url = 'https://www.amazon.com/dp/'
p_id = 'B005SYZZ7Q'

proxyMeta = ""

proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
}

file_name = '../dataProcess/data/rawData/test.csv'
web_dir = '../dataProcess/data/webPages/'
sleep_time = 0.5

# 随机ip代理获取
PROXY_POOL_URL = 'http://localhost:5555/random'
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


if __name__ == '__main__':

    df = pd.read_csv(file_name)['pid']
    p_id_array = df.values
    for index, p_id in enumerate(p_id_array):
            attempts, success = 0, False
            while attempts < 5 and not success:
                try:
                    while True:
                        url = base_url + p_id
                        proxyMeta = get_proxy()
                        result = requests.get(url, proxies=proxies, headers=headers)
                        result = result.text.encode('gbk', 'ignore').decode('gbk')
                        soup = BeautifulSoup(result, 'lxml')
                        movie_title = str(soup.select('title')[0].getText())
                        if (movie_title != 'Robot Check') and (movie_title != 'Sorry! Something went wrong!') and (movie_title != 'Amazon.com'):
                            print(" [p_id]:", p_id)
                            fo = open(web_dir + p_id + ".html", "w")
                            fo.write(result)
                            fo.close()
                            success = True
                            break
                        else:
                            print('[title error]', movie_title, " [p_id]:", p_id)
                except Exception as e:
                    print('[error]', e)
                    attempts += 1
                    time.sleep(sleep_time)
                    if attempts == 3:
                        break