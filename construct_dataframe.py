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
    #只选取前15篇文章
    for p_path in [j_path + '/' + x for x in os.listdir(j_path)][:15]:
      with open(p_path, encoding='utf-8') as paper_pointer:
        paper = json.load(paper_pointer)
        #有些文件没有issue这个key，在此情况下issue的默认值为0
        paper = defaultdict(int,paper)

        journal_name = j_path.split('/')[2]
        journal_discipline = {'Annual Review of Sociology': 'sociology', 'Cell' : 'biology',\
           'Digital Humanities Quarterly':'digital humanities', 'Journal of Financial Economics':'economics',\
             'Living Reviews in Relativity':'physics','Nature Cell Biology':'biology','Nature Physics':'physics',
             'Sociology':'sociology','The Quarterly Journal of Economics':'economics','Digital Scholarship in the Humanities': 'digital humanities'}

        datum = {'discipline':journal_discipline[journal_name], 'journal':journal_name, 'volume': paper['volume'],\
           'issue' : paper['issue'], 'date': paper['date'],\
          'title':paper['title'], 'author': paper['author']}
        for chapter in paper.keys():
          if chapter not in datum:
            datum_p = datum
            datum_p['heading'] = chapter.lower()
            for para in paper[chapter].split('\n'):
              if len(para) < 50:
                continue
              datum_p['paragraph'] = para.strip()
              # 这里deepcopy很重要，要是不做deepcopy就会让每个datum_p共享内存地址，因此上一句会改变所有data_p的paragraph值
              data.append(copy.deepcopy(datum_p))
  df = pd.DataFrame(data)
  return df

def filter_df(df):
  data = []
  for index, row in df.iterrows():
    heading = row['heading'].lower()
    para = row['paragraph']

    flag = False

    #小标题若包含 method, data, abstract, 则包含当前段落
    include = ['method','data','abstract']
    for keyword in include:
      if keyword in heading:
        flag = True

    #段落内容包含data，则包含当前段落
    if 'data' in para:
      flag = True
      
    #段落小标题包含下列关键词，则移除当前段落
    exclude = ['related','literature','previous','background']
    for keyword in exclude:
      if keyword in heading:
        flag = False

    if flag == True:
      data.append(row)  
  df = pd.DataFrame(data)
  return df

df = construct_df(j_paths)
df_2 = filter_df(df)
df_2.to_excel('./df_filtered.xlsx')




