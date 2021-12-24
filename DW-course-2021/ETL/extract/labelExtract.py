import os

from lxml import etree
import pandas as pd
import csv


class labelExtract:

    def __init__(self, page_dir_path):
        self.page_dir_path = page_dir_path
        self.target_path = '../.././data/labels.csv'
        self.pid_use_target_path = '../.././data/unusepid.csv'

    def run(self):
        label_df = pd.DataFrame(
            columns=[
                'pid',
                'labels',
            ],
            index=[]
        )
        label_dict = {}
        unuse_list = []
        with open(self.pid_use_target_path, "r") as f:
            reader = csv.DictReader(f)
            have = 0
            for row in reader:
                unuse_list.append(row['pid'])
        for root_path, _, file_names in os.walk(self.page_dir_path):
            for index, file_name in enumerate(file_names):
                if index % 10 == 0:
                    print('[index]: ', index)
                pid = file_name.split('.')[0][-10:]
                if pid not in unuse_list:
                    try:
                        html = etree.parse(os.path.join(root_path, file_name), etree.HTMLParser())
                        label_list = html.xpath(
                            '//*[@id="wayfinding-breadcrumbs_feature_div"]//span[@class="a-list-item"]')
                    except Exception as e:
                        print(file_name)
                        break
                else:
                    continue
                # print(label_list)
                label_names = []
                for label in label_list:
                    label_name = label.xpath('./a/text()')[0].replace('\n', '').replace('\r', '').strip()
                    label_names.append(label_name)
                label_dict['pid'] = pid
                label_dict['labels'] = label_names

                label_df.loc[label_df.size] = label_dict
                label_dict = {}
                if index % 20 == 0:
                    label_df.to_csv(target_path, mode='a', index=False, header=False)
                    label_df = label_df.drop(index=label_df.index)

            label_df.to_csv(target_path, mode='a', index=False, header=False)
            break
