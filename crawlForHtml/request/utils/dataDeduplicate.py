
if __name__ == '__main__':

    path = '/media/googlecamp/Teclast_S301/zips/_unzip'  # 待读取文件的文件夹绝对地址
    id_file_path = 'data/id_list.csv'
    error_path = 'data'
    save_path = 'data/UFMap'
    f_list = os.listdir(path)  # 获得文件夹中所有文件的名称列表
    mp = MoviePreProcess(file_list=f_list, file_path=path, id_list_file=id_file_path, error_path=error_path, save_path=save_path)
    mp.build_cor_id()