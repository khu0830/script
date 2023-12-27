#!/bin/python3
# writed 2023.12.27
from matplotlib_venn import venn2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, argparse, datetime
#import venn
"""
venn diagram만드는 모듈


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
group1: str
	control group name
group2: str
	case group name
subgroup: str
	sample type이 다양할 경우 설정.
    VDS, AF, AOF ...etc.
output_dir: file path
	벤다이어그램 plot file path
    
"""
#date
dt = datetime.datetime.now()
today_full = dt.strftime('%Y-%m-%d-%H%M')	#2023-06-21 16:34
today_date = dt.strftime('%Y%m%d')	#20230621

#argument
parser = argparse.ArgumentParser(description='')
parser.add_argument('--input', '-i', required=True, help='Input file path')
parser.add_argument('--group_1', '-g1', required=True, help='control group name')
parser.add_argument('--group_2', '-g2', required=True, help='case group name')
parser.add_argument('--subgroup', '-sg', required=False, help='if data include various sample type, use this option')
parser.add_argument('--output_dir', '-o', required=True, help='output directory')

args = parser.parse_args()
args_input = os.path.abspath(args.input_file)	#~/venn_list_FTB_PTB_subgroup_willCompare.tsv
args_group_1 = str(args.group_1)	#FTB
args_group_2 = str(args.group_2)	#PTB
args_subgroup = str(args.subgroup)	#VDS, AF, AOF
args_output_dir = os.path.abspath(args.output_dir)

## load data
df_input = pd.read_csv(args_input, sep='\t', header=0)

## set group
venn_group1 = f'{args_group_1}_{args_subgroup}'
venn_group2 = f'{args_group_2}_{args_subgroup}'
set_venn_group1 = set(df_input[venn_group1].dropna().tolist())
print(set_venn_group1)
set_venn_group2 = set(df_input[venn_group2].dropna().tolist())

## Venn diagram
plot_out = f'{args_output_dir}/matplotlib_venn2_{args_group_1}vs{args_group_2}_{args_subgroup}_{today_date}.png'

venn2([set_venn_group1, set_venn_group2], (venn_group1, venn_group2), set_colors=('grey', 'red'))
plt.savefig(plot_out)

ser_AOF = set_venn_group1.intersection(set_venn_group2)
df_inter = pd.DataFrame(ser_AOF)
inter_name = f'{args_subgroup}_intersection'
df_inter.columns = [inter_name]
df_inter['Category'] = inter_name
df_inter = df_inter[['Category', inter_name]]
print(f'\n\n{args_subgroup}_intersection\tn={df_inter.count()}\n')
print(df_inter.head())

intersection_taxa_lst_file = f'{args_output_dir}/intersection_taxa_list_venn_{args_group_1}vs{args_group_2}_{args_subgroup}_{today_date}.tsv'
df_inter.to_csv(intersection_taxa_lst_file, sep='\t', index=False)
