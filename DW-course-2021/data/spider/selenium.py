from selenium import webdriver  # 导入selenium中的webdriver包
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent

url = 'https://www.amazon.com/dp/0792845498'
web_dir = 'D:/Code/CodeWareHouse/py/pages/'

PATH = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'

if __name__ == '__main__':

    option = webdriver.ChromeOptions()
    # ua = UserAgent()

    # option.add_argument('user-agent=' + ua.random())
    # option.binary_location = r"C:/Program Files/Google/Chrome/Application/chromedriver.exe"
    option.add_argument('lang=en')
    option.headless = True

    s = Service(r"C:/Program Files/Google/Chrome/Application/chromedriver.exe")
    driver = webdriver.Chrome(service=s,options=option)
    try:
        driver.get(url)
        html = driver.page_source
        # print(threadNmae, r.status_code, url)
        # print('执行')
        # print(html)
        fo = open(web_dir + '123' + ".html", "w", encoding="utf-8")
        fo.write(html)
        fo.close()
        soup = BeautifulSoup(html, 'lxml')
        movie_title = str(soup.select('title')[0].getText())
        print(movie_title)
        print(type(html))
        # text_create(i, html)
        driver.quit()
    except Exception as e:
        print("Error: ", e)
