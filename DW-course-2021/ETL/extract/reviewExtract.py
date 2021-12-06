import pickle
import csv
import pandas as pd
import jsonlines as jsonlines
from _cffi_backend import string

pid_use_target_path = 'D:/2021-2022/DataWareHouse/Extract/data/unusepid.csv'
class ReviewExtract:

    def __init__(self, raw_data_path, uf_path, target_path='F:/reviews.csv'):
        """
        初始化
        """
        self.raw_data_path = raw_data_path  #存放的原始路径
        self.uf_path = uf_path  # 并查集文件路径
        self.uf_dict = {}  # 并查集数据结构
        self.df = pd.DataFrame()
        self.init_df()
        self.target_path = target_path  # big table的存储路径
        self.df.to_csv(self.target_path, index=False)

    def run(self):
        self.init_uf_dict()
        block_num = 0
        sum=0
        n=0
        with open(self.raw_data_path, 'r', encoding='iso-8859-1', errors='replace') as file:
                try:
                    # if block_num % 5000 == 0:
                    #     print('[block_num]:', block_num)

                    for line in jsonlines.Reader(file):
                        sum+=1
                        if ('asin' in line):
                            new_asin = line['asin']
                            with open(pid_use_target_path, "r") as f:
                                reader = csv.DictReader(f)
                                have = 0
                                for row in reader:
                                        if row['pid'] == new_asin:
                                            have = 1
                                            break
                                if(have==0):
                                    n += 1
                                    buffer = []
                                    while len(buffer) < 7 and line:
                                        if len(buffer) == 0:
                                            if ('asin' in line):
                                                asin = line['asin']
                                            else:
                                                asin = ''
                                            buffer.append(asin)
                                        elif len(buffer) == 1:
                                            if ('reviewerID' in line):
                                                reviewerID = line['reviewerID']
                                            else:
                                                reviewerID = ''
                                            buffer.append(reviewerID)
                                        elif len(buffer) == 2:
                                            if ('reviewerName' in line):
                                                reviewerName = line['reviewerName']
                                            else:
                                                reviewerName = ''
                                            buffer.append(reviewerName)
                                        elif len(buffer) == 3:
                                            if ('overall' in line):
                                                overall = line['overall']
                                            else:
                                                overall = ''
                                            buffer.append(overall)
                                        elif len(buffer) == 4:
                                            if ('reviewTime' in line):
                                                reviewTime = line['reviewTime']
                                            else:
                                                reviewTime = ''
                                            buffer.append(reviewTime)
                                        elif len(buffer) == 5:
                                            if ('summary' in line):
                                                summary = line['summary']
                                            else:
                                                summary = ''
                                            buffer.append(summary)
                                        elif len(buffer) == 6:
                                            if ('reviewText' in line):
                                                reviewText = line['reviewText']
                                            else:
                                                reviewText = ''
                                            buffer.append(reviewText)
                                    block_num += 1
                                    block = buffer
                                    if sorted(self.uf_dict[block[0]])[0] == block[0]:
                                        self.df.loc[self.df.size] = block
                                    if block_num % 10000 == 0:
                                        self.df.to_csv(self.target_path, mode='a', index=False, header=False)
                                        self.init_df()
                        if(sum%1000==0):
                            print(sum)
                            print(n)
                except:
                    pass
        print(block_num)
        print(n)
        print("结束！！！！")
        self.df.to_csv(self.target_path, mode='a', index=False, header=False)

    def init_uf_dict(self):
        with open(self.uf_path, 'rb') as uf_file:
            self.uf_dict = pickle.load(uf_file)

    def init_df(self):
        self.df = pd.DataFrame(
            columns=[
                'asin',
                'reviewerID',
                'reviewerName',
                'overall',
                'reviewTime',
                'summary',
                'reviewText',
            ],
            index=[]
        )
