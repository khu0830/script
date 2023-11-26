#!/bin/python3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load tsv file
tsv_file_path = "genus_bar_chart.tsv"
data = pd.read_csv(tsv_file_path, sep='\t')

# id 별 Family의 비율을 계산합니다.
pivot_data = data.groupby(['id', 'Family']).size().unstack().div(data.groupby('id').size(), axis=0).fillna(0)

# Seaborn을 사용하여 바 차트를 그립니다.
plt.figure(figsize=(10, 6))
sns.barplot(data=pivot_data.reset_index(), x='id', y='Actinomycetaceae', color='skyblue', label='Actinomycetaceae')
sns.barplot(data=pivot_data.reset_index(), x='id', y='Streptococcaceae', color='salmon', label='Streptococcaceae')
sns.barplot(data=pivot_data.reset_index(), x='id', y='Pasteurellaceae', color='green', label='Pasteurellaceae')
# 필요한 만큼 다른 Family에 대해서도 추가합니다.

plt.xlabel('id')
plt.ylabel('Percentage')
plt.title('Taxonomic Composition by id')
plt.legend()
plt.tight_layout()

# 차트를 이미지 파일로 저장합니다.
plt.savefig('taxonomic_composition.png', dpi=300)  # 이미지 파일로 저장 (PNG 형식)