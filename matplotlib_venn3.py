#!/bin/python3
from matplotlib_venn import venn3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, argparse, datetime
#import venn
"""
Three group comparison within one individual venn diagram만드는 모듈


#example
---------
#set1 = set(['A', 'B', 'C', 'D'])
#set2 = set(['B', 'C', 'D', 'E'])
#set3 = set(['C', 'D',' E', 'F', 'G'])
#venn3([set1, set2, set3], ('Set1', 'Set2', 'Set3'))
#plt.savefig('test_matplotlib_venn.png')

Parameters
----------
input_file: file path
	벤다이어그램 그릴 tsv file path

	FTB_ALL	PTB_ALL	FTB_VDS	PTB_VDS	FTB_AF	PTB_AF	FTB_AOF	PTB_AOF
	Ralstonia_pickettii_group		Lactobacillus_gasseri_group	Mycoplasma_hominis	Actinomyces_oris	Streptococcus_pneumoniae_group	Streptococcus_salivarius_group	Streptococcus_pneumoniae_group
	Faecalibacterium_prausnitzii_group	Atopobium_parvulum	Lactobacillus_helveticus_group	Pluralibacter_gergoviae	Streptococcus_pneumoniae_group		Streptococcus_pneumoniae_group	
individual_name: str
	one sample name
type1: str
	sample type 1
type2: str
	sample type 2
type3: str
	sample type 3   
output_dir: file path
	venn diagram plot file path
"""
#date
dt = datetime.datetime.now()
today_full = dt.strftime('%Y-%m-%d-%H%M')	#2023-06-21 16:34
today_date = dt.strftime('%Y%m%d')	#20230621

#argument
parser = argparse.ArgumentParser(description='')
parser.add_argument('--input', '-i', required=True, help='Input file path')
parser.add_argument('--individual_name', '-n', required=True, help='one sample name')
parser.add_argument('--type1', '-t1', required=True, help='sample type 1')
parser.add_argument('--type2', '-t2', required=True, help='sample type 2')
parser.add_argument('--type3', '-t3', required=True, help='sample type 3')
parser.add_argument('--output_dir', '-o', required=True, help='output directory')

args = parser.parse_args()
args_input = os.path.abspath(args.input_file)	#~/venn_list_individual.tsv
args_individual_name = str(args.individual_name)	#PT10
args_type1 = str(args.type1)	#VDS
args_type2 = str(args.type2)	#AF
args_type3 = str(args.type3)	#AOF
args_output_dir = os.path.abspath(args.output_dir)

## load data
df_input = pd.read_csv(args_input, sep='\t', header=0)

## set group
venn_group1 = f'{args_individual_name}_{args_type1}'
venn_group2 = f'{args_individual_name}_{args_type2}'
venn_group3 = f'{args_individual_name}_{args_type3}'

set_venn_group1 = set(df_input[venn_group1].dropna().tolist())
set_venn_group2 = set(df_input[venn_group2].dropna().tolist())
set_venn_group3 = set(df_input[venn_group3].dropna().tolist())

## Venn diagram
plot_out = f'{args_output_dir}/matplotlib_venn_{args_individual_name}_{args_type1}vs{args_type2}vs{args_type3}_{today_date}.png'
venn3([set_venn_group1, set_venn_group2, set_venn_group3], (venn_group1, venn_group2, venn_group3), set_colors=('green', 'blue', 'purple'))
plt.savefig(plot_out)

inter_update = set_venn_group1.intersection_update(set_venn_group2, set_venn_group3)
print('inter_update')
print(inter_update)


inter_12 = set_venn_group1.intersection(set_venn_group2)
df_inter12 = pd.DataFrame(inter_12)
print('inter_12')
print(inter_12)
exit()
inter_name = f'{venn_group1}_{venn_group2}_intersection'
df_inter12.columns = ['intersection']
df_inter12['Category'] = inter_name
df_inter12 = df_inter12[['Category', 'intersection']]

inter_23 = set_venn_group2.intersection(set_venn_group3)
df_inter23 = pd.DataFrame(inter_23)
inter_name = f'{venn_group2}_{venn_group3}_intersection'
df_inter23.columns = ['intersection']
df_inter23['Category'] = inter_name
df_inter23 = df_inter23[['Category', 'intersection']]

print(f'\n\n{venn_group1}_{venn_group2}_intersection\tn={df_inter12.count()}\n')
print(df_inter12.head())

df_con = pd.concat([df_inter12, df_inter23], axis=0)
print(f'\n\ndf_concat\tn={df_con.count()}\n')
print(df_con)
intersection_gene_lst_file = f'{output_dir}/intersection_venn_list_{individual}_{type1}vs{type2}vs{type3}_{today_date}.tsv'
df_con.to_csv(intersection_gene_lst_file, sep='\t', index=False)

