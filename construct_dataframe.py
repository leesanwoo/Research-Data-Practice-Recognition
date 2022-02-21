import pandas as pd
import numpy as np
import os
import json
from collections import defaultdict
import copy

path = './Journals/'
j_paths = [path + x + '/structuredText' for x in os.listdir(path)]


def construct_df(j_paths):
  #j_paths = list[] -> './Cell/structuredText' , ...
  data = []
  for j_path in j_paths:
    for p_path in [j_path + '/' + x for x in os.listdir(j_path)]:
      with open(p_path, encoding='utf-8') as paper_pointer:
        paper = json.load(paper_pointer)
        #有些文件没有issue这个key，在此情况下issue的默认值为0
        paper = defaultdict(int,paper)
        datum = {'title':paper['title'], 'authors': paper['authors'], 'journal':j_path.split('/')[2],\
          'volume': paper['volume'], 'issue' : paper['issue'], 'date': paper['date'] }
        for chapter in paper.keys():
          if chapter not in datum:
            datum_p = datum
            datum_p['heading'] = chapter
            for para in paper[chapter].split('\n'):
              if len(para) < 50:
                continue
              datum_p['paragraph'] = para
              # 这里deepcopy很重要，要是不做deepcopy就会让每个datum_p共享内存地址，因此上一句会改变所有data_p的paragraph值
              data.append(copy.deepcopy(datum_p))
  df = pd.DataFrame(data)
  return df

df = construct_df(j_paths)
df.to_excel('df_all.xlsx')



