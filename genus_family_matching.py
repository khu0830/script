#!/bin/python3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

target_genus = '/home/khu0830/Analysis/target_genus.tsv'
gg_13_5_taxonomy = '/home/khu0830/Analysis/gg_13_5_taxonomy.tsv'

df_target = pd.read_csv(target_genus, sep='\t', header=0)
print(df_target.head())





df_gg = pd.read_csv(gg_13_5_taxonomy, sep='\t', header=None, names=['line', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'])
# species column removed
df_gg = df_gg.drop(['species'], axis=1)
#print('df_gg')
#print(df_gg.shape)
#print(df_gg.head())
df_gg['genus'] = df_gg['genus'].str.lstrip()
df_gg_new = df_gg.drop_duplicates(subset='genus')
print('df_gg_new')
print(df_gg_new.shape)
print(df_gg_new.head())

# two dataframe merge
df_merge = pd.merge(df_target, df_gg_new, on='genus', how='outer')
df_merge_new = df_merge[['genus', 'family']]
print('df_merge')
print(df_merge_new.head(15))

df_merge.to_csv('/home/khu0830/Analysis/df_merge.csv', sep=',')