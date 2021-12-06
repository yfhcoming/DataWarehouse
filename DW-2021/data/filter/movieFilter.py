import csv
import pandas as pd

label_un_use_target_path = './data/unuselabels.csv'
label_use_target_path = './data/uselabels.csv'
pid_un_use_target_path = './data/unusepid.csv'
pid_use_target_path = './data/usepid.csv'
label_un_use_df = pd.DataFrame(
            columns=[
                'pid',
                'labels',
            ],
            index=[]
        )
label_un_use_dict = {}
label_use_df = pd.DataFrame(
            columns=[
                'pid',
                'labels',
            ],
            index=[]
        )
label_use_dict = {}
pid_un_use_df = pd.DataFrame(
            columns=[
                'pid',
            ],
            index=[]
        )
pid_un_use_dict = {}
pid_use_df = pd.DataFrame(
            columns=[
                'pid',
            ],
            index=[]
        )
pid_use_dict = {}
if __name__ == '__main__':
  with open("./data/labels.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # print(row['labels'])
        if ( row['labels'] == "['Movies & TV', 'TV']" or row['labels'] == "['Movies & TV', 'Boxed Sets', 'Television']"):
            label_un_use_dict['pid'] = row['pid']
            label_un_use_dict['labels'] = row['labels']
            label_un_use_df.loc[label_un_use_df.size] = label_un_use_dict
            label_un_use_dict = {}
            print("hello")
            pid_un_use_dict['pid'] = row['pid']
            pid_un_use_df.loc[pid_un_use_df.size] = pid_un_use_dict
            pid_un_use_dict = {}
        elif (row['labels'] == "[]"):
            label_un_use_dict['pid'] = row['pid']
            label_un_use_dict['labels'] = row['labels']
            label_un_use_df.loc[label_un_use_df.size] = label_un_use_dict
            label_un_use_dict = {}
            print("empty")
            pid_un_use_dict['pid'] = row['pid']
            pid_un_use_df.loc[pid_un_use_df.size] = pid_un_use_dict
            pid_un_use_dict = {}
        else:
            label_use_dict['pid'] = row['pid']
            label_use_dict['labels'] = row['labels']
            label_use_df.loc[label_use_df.size] = label_use_dict
            label_use_dict = {}
            pid_use_dict['pid'] = row['pid']
            pid_use_df.loc[pid_use_df.size] = pid_use_dict
            pid_use_dict = {}

  label_un_use_df.to_csv(label_un_use_target_path, mode='a', index=False, header=False)
  label_use_df.to_csv(label_use_target_path, mode='a', index=False, header=False)
  pid_un_use_df.to_csv(pid_un_use_target_path, mode='a', index=False, header=False)
  pid_use_df.to_csv(pid_use_target_path, mode='a', index=False, header=False)
