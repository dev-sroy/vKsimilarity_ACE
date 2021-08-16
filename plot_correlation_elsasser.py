# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 14:43:04 2021

@author: Sohom
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\Second Normalization\\"
dir2 = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\\"
#img_dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\Plots\Elsasser_corr_plots\2norm"
corr_df = pd.DataFrame()
corr_df2 = pd.DataFrame()

def corr_f(s):
  return 'corr_'+s+'.txt'

def corr_len(df, var):
  tc = np.where(df[var].values < np.exp(-1))[0]
  return tc

exclude_list = ['199802027', '19980310', '19980820', '19980821', '19980822', '19990227', '19990323', '19990626', '19990718', '19990815', '20000915', '20000930', '20001022', '20001028', '20001124', '20010115', '20010116', '20010523', '20010616', '20010617', '20010618', '20011105', '20011107', '20020107', '20020119', '20020125', '20020228', '20020409', '20020417', '20020607', '20020608', '20020903', '20021214', '20021219', '20030110', '20031205', '20031220', '20040227', '20040309', '20040324', '20040528', '20040613', '20040624', ',20040707', '20040824', '20040927', '20041002', '20041107', '20041205', '20041221', '20050108', '20050121', '20050206', '20050214', '20050403', '20050528', '20050612', '20050623', '20050813', '20050930', '20051016', '20051111', '20051127', '20051216', '20060105', '20060203', '20060309', '20060326', '20060331', '20060408', '20060420', '20060505', '20060518', '20060704', '20060806', '20060807', '20060818', '20060930', '20061011', '20061028', '20070129', '20070206', '20070304', '20070311', '20070422', '20070518', '20070609', '20070723', '20070919', '20071013', '20080207', 'lengths_elsasser']
ex_f = list(map(corr_f, exclude_list))

fig = plt.figure(figsize = (20,15))
#fig, axs = plt.subplots(4, 1, figsize = (20,15))

plt.rcParams['xtick.labelsize'] = 40
plt.rcParams['ytick.labelsize'] = 40

#corr_len_df = pd.DataFrame(columns = {'Datetime', 'Corr_time', 'Corr_len_1e', 'Corr_len_linfit'})

for f in os.listdir(dir):
  if f not in ex_f:
    fname = os.path.join(dir,f)
    fname2 = os.path.join(dir2, f)
    df = pd.read_csv(fname, delim_whitespace = True)
    df2 =pd.read_csv(fname2, delim_whitespace = True)
    vmag = df['Lag_spatial'][1]/df.index[1]/60
    
    if vmag>=500:
      try:
    
        # axs[0].plot(df['Lag_spatial'], df['v_tr'], color= 'blue')
        # #axs[0].set_xlabel('Spatial lag(km)')
        # axs[0].set_ylabel(r'$R_v(r)$', fontsize = 40)
        # axs[1].plot(df['Lag_spatial'], df['B_tr'], color = 'darkgreen')
        # #axs[1].set_xlabel('Spatial lag(km)')
        # axs[1].set_ylabel(r'$R_B(r)$', fontsize = 40)
        # axs[2].plot(df['Lag_spatial'], df['z+_tr'], color = 'teal')
        # #axs[2].set_xlabel('Spatial lag(km)')
        # axs[2].set_ylabel(r'$R_{z+}(r)$', fontsize = 40)
        # axs[3].plot(df['Lag_spatial'], df['z-_tr'], color = 'crimson')
        # #axs[3].set_xlabel('Spatial lag(km)')
        # axs[3].set_ylabel(r'$R_{z-}(r)$', fontsize = 40)
        
        # axs[0].grid(True)
        # axs[1].grid(True)
        # axs[2].grid(True)
        # axs[3].grid(True)
        # plt.xlabel('Spatial lag(km)', fontsize = 40)
        # fig.tight_layout()
        #img_name = os.path.splitext(f)[0] + '_2norm.png'
        # plt.savefig(os.path.join(img_dir, img_name))
        
      
        # axs[0].clear()
        # axs[1].clear()
        # axs[2].clear()
        # axs[3].clear()
        # #df = df.set_index('Lag_minutes')
        
        #Compute correlation lengths
        
        #fig, axs = plt.subplots(2, 1)
        #plt.plot(df['Lag_spatial'], df['z+_tr'], color='peru', alpha = 0.2)
        
        #axs[0].plot(df['Lag_spatial'], df['z+_tr'], color='k')
        
        #plt.tight_layout()
        #plt.savefig(os.path.join(img_dir, img_name))
        #plt.gca().clear()
        corr_df = corr_df.append(df)
        corr_df2 = corr_df2.append(df2)
        print(f)
      except:
        continue

#bins = np.linspace(corr_df['Lag_spatial'].min(), corr_df['Lag_spatial'].max(), 480)

#zpos_mean, bin_edges, binnum = stats.binned_statistic(corr_df['Lag_spatial'],corr_df['z+_tr'], bins=480, statistic= 'mean')
#zpos_std, bin_edges, binnum = stats.binned_statistic(corr_df['Lag_spatial'], corr_df['z+_tr'], bins=480, statistic = 'std')

# zm_mean, bin_edges, binnum = stats.binned_statistic(corr_df['Lag_2norm,corr_df['z+_tr'], bins=1000, statistic= 'mean')
# zm_std, bin_edges, binnum = stats.binned_statistic(corr_df['Lag_spatial'], corr_df['z+_tr'], bins=1000, statistic = 'std')

# zm_mean, bin_edges, binnum = stats.binned_statistic(corr_df['Lag_spatial'],corr_df2['z+_tr'], bins=1000, statistic= 'mean')
# zm_std, bin_edges, binnum = stats.binned_statistic(corr_df['Lag_spatial'], corr_df2['z+_tr'], bins=1000, statistic = 'std')



zm_mean, bin_edges, binnum = stats.binned_statistic(corr_df['Lag_2norm'],corr_df2['z+_tr'], bins=1000, statistic= 'mean')
zm_std, bin_edges, binnum = stats.binned_statistic(corr_df['Lag_2norm'], corr_df2['z+_tr'], bins=1000, statistic = 'std')

# corr_df1 = corr_df.copy(deep = True)
# corr_df1['Lag_bins'] = pd.qcut(corr_df1['Lag_spatial'], 200)
# zpos_mean = corr_df1.groupby('Lag_bins')['z+_tr'].mean()
# zpos_std = corr_df1.groupby('Lag_bins')['z+_tr'].std()

# corr_df1 = corr_df1.groupby('Lag_bins').mean()
# bin_edges = [corr_df1.index[i].left for i in range(len(corr_df1))]

x = bin_edges[:-1]
x = x + (x[1]*0.5)
x = np.insert(x, 0, 0)
zm_mean = np.insert(zm_mean, 0, 1)
zm_std = np.insert(zm_std, 0, 0)
plt.plot(x,zm_mean,'k', linewidth = 2.0, zorder = 25, label = 'Mean')
plt.fill_between(x, zm_mean+zm_std, zm_mean-zm_std, color = 'blue', alpha = 0.5, zorder = 10, label = '1 standard deviation')
plt.fill_between(x, zm_mean+2*zm_std, zm_mean-2*zm_std, color = 'dodgerblue', alpha = 0.5, zorder = 20, label = '2 standard deviations')
plt.grid(True)
plt.xlim(0, 4)
plt.ylim(bottom=-0.5)
plt.xlabel(r'Spatial lag, r/$\lambda$', fontsize = 40)
plt.ylabel(r'$R(r)$', fontsize = 40)
plt.legend(fontsize = 40)

