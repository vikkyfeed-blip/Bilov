import os
import pandas as pd
import numpy as np
from sklearn import preprocessing

mas_txt = []
attributes_names = ['class']
le = preprocessing.LabelEncoder()


def load_txt(file_name):
    project_roof = os.path.dirname(__file__)
    file_path = os.path.join(project_roof, 'data', file_name)
    data = open(str(file_path))
    data.readline()
    return data

def load_data(file_name):
    project_roof = os.path.dirname(__file__)
    file_path = os.path.join(project_roof, 'data', file_name)
    data = pd.read_csv(str(file_path), sep=';', header=0)
    return data

def uniq_means(df):
    for i in range(len(df.columns)):
        print(f'столбик {attributes_names[i]}: уник.знач. {df.iloc[:, i].unique().tolist()}, кол-во {len(df.iloc[:, i].unique().tolist())}\n')
    return ''

def delete_column(df):
    for col in df.columns:
        if len(df[col].unique()) == 1:
            print(f'Удаляем столбик {col}')
            df = df.drop(labels=col, axis=1)
    return df

def find_miss_means(df):
    miss_columns = []
    for col in df.columns:
        if '?' in df[col].unique():
            print(col, df[col].unique().tolist(),(df[col]=='?').sum())
            miss_columns.append(col)
    return miss_columns

def replace_values(df, miss_columns):
    for i in miss_columns:
        df.loc[df[i] == '?', i] = np.nan
        df[i] = df[i].fillna(value=0)
        print(df[i].unique())
    return df

def transform(df):
    df = df.astype(str)
    df_new = pd.DataFrame()
    for col in df.columns:
        data_transform = le.fit_transform(df[col])
        df_new[col] = data_transform
    return df_new


txt_file = load_txt('attribute_info.txt')

for line in txt_file:
    mas_txt.append(line)
for atr in mas_txt:
    name = atr[: atr.find(':')]
    name = name[atr.find('. ') + 2 :]
    attributes_names.append(name)
df = load_data('agaricus-lepiota.csv')
df.columns = attributes_names


print(uniq_means(df))
df = delete_column(df)
miss_columns = find_miss_means(df)
df = replace_values(df, miss_columns)
df.to_csv('data/new_dataset.csv', index=False, encoding='utf-8', sep=';')
transform(df).to_csv('data/transform_data.csv', index=False, encoding='utf-8', sep=';')






