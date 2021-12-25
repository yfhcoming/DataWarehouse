import csv
import os
import pickle
from lxml import etree
import time
import calendar
from datetime import datetime
import pandas as pd

pages_check = '/Users/spica/data/pages_check.txt'


class MovieExtract:

    def __init__(self, page_dir_path, uf_path):
        self.labels_path = '.././data/labels.csv',  # 电影标签文件路径
        self.target_path = '.././data/movies.csv',  # movieExtract结果
        self.page_dir_path = page_dir_path  # 网页数据的文件夹路径
        self.uf_path = uf_path  # 并查集的文件路径

        self.uf_dict = {}  # 并查集数据结构
        self.movie_dict = {}
        self.movie_df = pd.DataFrame()  # 电影信息
        self.label_df = pd.read_csv(self.labels_path, header=0)  # 导入 label data frame

        self.init_uf_dict()  # 导入并查集数据
        self.init_movie_df()  # 初始化 movie data frame
        self.movie_df.to_csv(self.target_path, index=False)

    def run(self):
        """
        从webPages文件下遍历网页文件，将id list中的网页进行信息抽取
        """

        for root_path, _, file_names in os.walk(self.page_dir_path):
            for index, file_name in enumerate(file_names):
                p_id = file_name.split('.')[0][-10:]

                if len(p_id) != 10 or p_id in unuse_list:
                    continue
                # if p_id in self.uf_dict.keys():
                # print(p_id)
                # print(self.uf_dict[p_id])
                # print(sorted(self.uf_dict[p_id]))

                self.get_labels(p_id)
                html = etree.parse(os.path.join(root_path, file_name), etree.HTMLParser())
                self.get_title(html)
                isPrimeVideo = True if len(html.xpath('/html/body/div[1]/div[2]/div[1]/div/a')) > 0 else False
                if isPrimeVideo:
                    self.movie_dict['version_count'] = 1
                    # PrimeVideo是版本唯一的，不需要使用并查集
                    try:
                        node_list = \
                            html.xpath('/html/body/div[1]/div[2]/div[4]/div/div/div[2]/div[2]/div/div[3]/div/div')[
                                0].xpath('dl')
                        release_time = html.xpath('.//span[@data-automation-id="release-year-badge"]/text()')[0]
                        self.movie_dict['release_time'] = release_time
                        for node in node_list:
                            key = node.xpath('dt/span/text()')
                            print(key)
                            if 'Starring' in key:
                                self.get_actors(node, 2)
                            if 'Directors' in key:
                                self.get_director(node, 2)
                        self.add_movie()
                    except IndexError as e:
                        print(e)
                        fo = open(pages_check, "a", encoding="utf-8")
                        fo.write(p_id + '\n')
                        fo.close()
                        self.add_movie()

                else:
                    # 第二种页面类型 换解析方法且使用并查集
                    if sorted(self.uf_dict[p_id])[0] == p_id:
                        self.movie_dict['p_id'] = p_id
                        self.movie_dict['version_count'] = len(sorted(self.uf_dict[p_id]))
                    try:
                        node_list = html.xpath('//div[@id="detailBullets_feature_div"]')[1].xpath('ul/li')
                        for node in node_list:
                            key = node.xpath('span/span[1]/text()')[0].split(':')[0].strip()
                            if 'Actors' in key:
                                self.get_actors(node, 1)
                            if 'Release date' in key:
                                self.get_release_time(node, 1)
                            if 'Director' in key:
                                self.get_director(node, 1)
                        self.add_movie()
                    except IndexError as e:
                        print(e)
                        fo = open(pages_check, "a", encoding="utf-8")
                        fo.write(p_id + '\n')
                        fo.close()
                        self.add_movie()

                if index % 1000 == 0:
                    print('[index]:', index)
                if index % 10000 == 0:
                    self.movie_df.to_csv(self.target_path, mode='a', index=False, header=False)
                    self.init_movie_df()
            self.movie_df.to_csv(self.target_path, mode='a', index=False, header=False)
            break

        # 过滤labelExtract中去掉的非电影数据
        pid_use_target_path = '../.././data/unusepid.csv'
        unuse_list = []
        with open(pid_use_target_path, "r") as f:
            reader = csv.DictReader(f)
            have = 0
            for row in reader:
                unuse_list.append(row['pid'])

    def get_actors(self, node, page_type):
        """
        从一个网页中抽取所有演员信息
        """
        if page_type == 1:
            self.movie_dict['actor_list'] = [actor.strip() for actor in node.xpath('span/span[2]/text()')[0].split(',')]
        elif page_type == 2:
            self.movie_dict['actor_list'] = [actor for actor in node.xpath('dd/a/text()')]

    def get_release_time(self, node, page_type=1):
        """
        从一个网页中抽取电影上映时间
        """
        if page_type == 1:
            release_time = node.xpath('span/span[2]/text()')[0]
            year = int(release_time.split(',')[1].strip())
            month_str = release_time.split(',')[0].strip().split(' ')[0].strip()
            month = int(list(calendar.month_name).index(month_str))
            day = int(release_time.split(',')[0].strip().split(' ')[1].strip())
            dt = datetime(year, month, day)
            self.movie_dict['release_time'] = dt.strftime('%Y-%m-%d')
        elif page_type == 2:
            # 由于PrimeVideo页面比较特殊（时间不在信息栏中），直接在run()内处理
            pass

    def get_director(self, node, page_type):
        """
         从一个网页中抽取导演信息
        """
        if page_type == 1:
            self.movie_dict['director'] = node.xpath('span/span[2]/text()')[0].strip().strip('\"').split(',')
        elif page_type == 2:
            self.movie_dict['director'] = [director for director in node.xpath('dd/a/text()')]

    def get_labels(self, p_id):
        """
        获取电影风格
        """
        try:
            data = self.label_df.loc[self.label_df['p_id'] == p_id]
            self.movie_dict['label_list'] = eval(data.iloc[0]['labels'])
        except KeyError as e:
            pass;

    def get_title(self, html):
        """
        获取电影名称
        """
        # self.movie_dict['title'] = html.xpath('/span[@id="productTitle"]')
        data = html.xpath('//span[@id="productTitle"]/text()')
        if len(data) == 0:
            data = html.xpath('//h1[@class="_1GTSsh _2Q73m9"]/text()')
            self.movie_dict['title'] = '' if len(data) == 0 else data[0].split('[')[0].split('(')[0].strip()
        else:
            self.movie_dict['title'] = data[0].split('[')[0].split('(')[0].strip()

    def get_starring(self):
        """
        从一个网页中抽取电影的所有主演
        """
        pass

    def get_version(self):
        """
        从一个网页中抽取电影的版本
        """
        pass

    def init_uf_dict(self):
        with open(self.uf_path, 'rb') as uf_file:
            self.uf_dict = pickle.load(uf_file)

    def init_movie_df(self):
        self.movie_df = pd.DataFrame(
            columns=[
                'p_id',
                'title',
                'label_list',
                'director',
                'actor_list',
                'release_time',
                'version_count',
                'starring_list',
            ],
            index=[]
        )

    def add_movie(self):
        """
        将保存单个电影信息的 dict 插入到 data frame 中
        """
        self.movie_df.loc[self.movie_df.size] = self.movie_dict
        self.movie_dict = {}
