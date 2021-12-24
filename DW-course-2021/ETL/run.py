import argparse
import pandas as pd
import os
import pickle


def get_args():
    # 创建一个解析器，即ArgumentParser对象
    parser = argparse.ArgumentParser(description='Extract review information from source data, ',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # 添加参数——调用 add_argument() 方法添加参数
    parser.add_argument('--webpage_path', default='/Users/spica/data/webPages/',
                        help='path of web pages dir', dest='page_dir_path')
    parser.add_argument('--movie_path', default='/Users/spica/data/Movies_and_TV_5.json',
                        help='path of movies', dest='raw_data_path')
    parser.add_argument('--uf_path', default='.././data/UFMap/component_mapping.pickle',
                        help='path of union find data', dest='uf_path')
    parser.add_argument('--label_path', default='.././data/labels.csv',
                        help='path of movie label', dest='label_path')
    # 从网页抽取标签进行筛选，得到label.csv
    parser.add_argument('--label-extract', dest='label_extract', action='store_true', help='extract label data')
    # 从网页抽取评论，并结合标签进行筛选得到reviews.csv
    parser.add_argument('--review-extract', dest='review_extract', action='store_true', help='extract review data')
    # 从网页抽取电影相关数据，筛选得到movies.csv
    parser.add_argument('--movie-extract', dest='movie_extract', action='store_true', help='extract movie data')
    parser.add_argument('--review-transform', dest='review_transform', action='store_true', help='transform review data')
    parser.add_argument('--movie-transform', dest='movie_transform', action='store_true', help='transform review data')
    # 解析参数——使用 parse_args() 解析添加的参数
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    print(args.page_dir_path)
    print(args.raw_data_path)
    print(args.uf_path)
    if args.label_extract:
        # 检查若路径不存在则退出
        assert os.path.exists(args.page_dir_path)
        print('Extract label Data from' + args.page_dir_path)
        label_extract = labelExtract(args.page_dir_path)
        label_extract.run()

    if args.review_extract:
        assert os.path.exists(args.raw_data_path)
        assert os.path.exists(args.uf_path)
        print('Extract review data from ' + args.raw_data_path)
        review_extract = ReviewExtract(args.raw_data_path, args.uf_path)
        review_extract.run()

    if args.movie_extract:
        assert os.path.exists(args.page_dir_path)
        assert os.path.exists(args.uf_path)
        print('Extract movie data from ' + args.page_dir_path)
        movie_extract = MovieExtract(args.page_dir_path, args.uf_path)
        movie_extract.run()

    if args.review_transform:
        assert os.path.exists('.././data/reviews.csv')
        review_transform = ReviewTransform()

    if args.movie_transform:
        assert os.path.exists('.././data/reviews.csv')
        movie_transform = MovieTransform()

