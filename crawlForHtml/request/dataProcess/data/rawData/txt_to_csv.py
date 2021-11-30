import pandas as pd


df = pd.read_csv("pid.txt",delimiter="\n")

df.to_csv("id_list.csv", encoding='utf-8', index=True)
