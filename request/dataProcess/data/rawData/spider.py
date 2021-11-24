# -*- coding:UTF-8 -*-
import jsonlines as jsonlines
from bs4 import BeautifulSoup
import requests


asinSet = set()
with open("Movies.json") as movies , open('pid.txt', 'w', encoding="utf-8") as f:

    for line in jsonlines.Reader(movies):
        try:
            asin = line['asin']
            if asin not in asinSet:
                asinSet.add(asin)
                f.write(asin+'\n')
        except:
            pass

print("Done. {len(asinSet)} asin in total")

# if __name__ == "__main__":