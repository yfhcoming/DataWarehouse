import argparse
from extract.reviewExtract import ReviewExtract
import pandas as pd
import os
import pickle


def get_args():
    # 创建一个解析器，即ArgumentParser对象
    parser = argparse.ArgumentParser(description='Extract review information from source data, ',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # 添加参数——调用 add_argument() 方法添加参数
    parser.add_argument('--movie_path', type=str, default='F:/Movies_and_TV_5.json',
                        help='path of movies', dest='raw_data_path')
    parser.add_argument('--uf_path', type=str, default='../data/UFMap/component_mapping.pickle',
                        help='path of union find data', dest='uf_path')
    parser.add_argument('--label_path', type=str, default='../data/labels.csv',
                        help='path of movie label', dest='label_path')
    parser.add_argument('--review-extract', dest='review_extract', action='store_true', help='extract review data from movie')
    # 解析参数——使用 parse_args() 解析添加的参数
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    print(args.raw_data_path)
    print(args.uf_path)
    print(args.review_extract)
    if args.review_extract:
        assert os.path.exists('F:/Movies_and_TV_5.json')
        print('will extract review data from ' + args.raw_data_path)
        review_extract = ReviewExtract(args.raw_data_path, args.uf_path)
        review_extract.run()

