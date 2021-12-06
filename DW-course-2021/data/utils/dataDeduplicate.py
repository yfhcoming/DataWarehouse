"""
find unique movie from web page data.
"""
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import pickle
import os
import csv

from unionFind import UnionFind


class MoviePreProcess(object):

    def __init__(self, file_list, file_path, error_path, id_list_file, save_path):
        self._id_list = np.array(pd.read_csv(id_list_file)['pid'])
        self._file_list = file_list
        self._uf_set = UnionFind(self._id_list)
        self._file_path = file_path
        self._error_path = error_path
        self._error_id_list = []
        self._save_path = save_path
        # self._break_point = -1

    def save_uf(self, save_path):
        save_file = open(save_path, 'wb')
        pickle.dump(self._uf_set.component_mapping(), save_file)

    # def load_break_point(self, load_data, break_point):
    #     new_uf = UnionFind([key for key in data])
    #
    #     for key in load_data:
    #         for cor_id in load_data[key]:
    #             new_uf.union(key, cor_id)
    #
    #     self._uf_set = new_uf
    #     self._break_point = break_point
    #     self._error_id_list = list(pd.read_csv(self._error_path + "/error_id_list.csv")['p_id'])

    def build_cor_id(self):

        for index, file_name in enumerate(self._file_list):
            # if index <= self._break_point:
            #     continue
            # if index % 10000 == 0:
            #     self.save_uf(self._save_path + '/component_mapping_' + str(index) + '.pickle')
            #     df = pd.DataFrame(self._error_id_list, index=None, columns=['p_id'])
            #     df.to_csv(error_path + "/error_id_list.csv")

            if index % 10 == 0:
                print('[index]: ', index, '[components]: ', self._uf_set.n_comps, '[elements]: ', self._uf_set.n_elts)
            ct_id = file_name.split('.')[0][-10:]
            if ct_id not in unuse_list:
                    # 解析html文件
                    try:
                        content = open(self._file_path + '/' + file_name, 'r',encoding="utf-8").read()
                        soup = BeautifulSoup(content, 'lxml')
                    except:
                        continue
                    try:
                        a_list = soup.find(id="MediaMatrix").find_all('a')

                        # 相同id列表
                        pre_id = ''

                        # 遍历a_list
                        for a_tag in a_list:
                            href = a_tag['href']
                            if len(href.split('/dp/')) > 1:
                                cor_id = href.split('/dp/')[1][0:10]
                                if cor_id != pre_id and cor_id in self._id_list:
                                    pre_id = cor_id
                                    self._uf_set.union(ct_id, cor_id)
                    except:
                        self._error_id_list.append(ct_id)
            else:
                continue

        print('[components]: ', self._uf_set.n_comps, '[elements]: ', self._uf_set.n_elts)
        self.save_uf(self._save_path + '/component_mapping.pickle')
        df = pd.DataFrame(self._error_id_list, index=None, columns=['pid'])
        df.to_csv(error_path + "/error_id_list.csv")


if __name__ == '__main__':
    path = '/Users/spica/data/webPages'  # 待读取文件的文件夹绝对地址
    id_file_path = '../data/id_list.csv'
    error_path = '../data'
    save_path = '../data/UFMap'

    pid_use_target_path = '../data/unusepid.csv'
    unuse_list = []
    with open(pid_use_target_path, "r") as f:
        reader = csv.DictReader(f)
        have = 0
        for row in reader:
            unuse_list.append(row['pid'])

    f_list = os.listdir(path)  # 获得文件夹中所有文件的名称列表

    mp = MoviePreProcess(file_list=f_list, file_path=path, id_list_file=id_file_path, error_path=error_path,
                         save_path=save_path)
    mp.build_cor_id()
