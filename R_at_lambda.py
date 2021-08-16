# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 17:49:31 2021

@author: Sohom
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\\"

R_arr = []
corr_len_arr = []
E_arr = []

for f in os.listdir(dir):
  print(f)
  try:
    fname = os.path.join(dir, f)
    
    df = pd.read_csv(fname, delim_whitespace = True)
    
    vmag = df['Lag_spatial'][1]/df.index[1]/60
    
    if vmag >= 500:
      
    
      B_df = pd.DataFrame(columns = ['Lag_spatial', 'Lag_2norm', 'B_tr'])
      
      B_df['Lag_spatial'] = df['Lag_spatial'].copy(deep = True)
      B_df['B_tr'] = df['B_tr'].copy(deep = True)
      
      E_arr.append(df['B_tr(unnormalized)'][0])
      
      tc  = np.where(B_df['B_tr'] < np.exp(-1))[0][0]
      
      corr_len_1e = B_df['Lag_spatial'][tc]
      
      p = np.polyfit(B_df['Lag_spatial'][0: tc//2], B_df['B_tr'][0: tc//2], 1)
      corr_len_linfit = -1/p[0]
      
      corr_len_arr.append(corr_len_linfit)
      
      B_df['Lag_2norm'] = B_df['Lag_spatial'] / corr_len_linfit
      
      R_at_lambda = B_df.loc[np.where(B_df['Lag_2norm']>1)[0][0], 'B_tr']
      
      R_arr.append(R_at_lambda)
    
  except:
    
    continue


#Creating the plots

#Distribution of correlations at 1 correlation length
bins = np.logspace(-2, 0, 150)
plt.hist(R_arr, bins = bins, color = 'b')
plt.xscale('log')
plt.xlim(0.1, 1)
plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))
plt.gca().set_xticks(major_ticks)
plt.minorticks_off()
plt.grid(True)
plt.xlabel(r'$R(r/\lambda)$ at $r = \lambda$', fontsize = 60)
plt.ylabel('Counts', fontsize = 60)
plt.xticks(fontsize = 60)
plt.yticks(fontsize = 60)

#Distribution of correlation lengths
l_bins = np.logspace(5, 7, 100)
plt.hist(corr_len_arr, bins = l_bins, color = 'b')
plt.xscale('log')
plt.xlabel(r'Correlation length(in km)', fontsize = 60)
plt.ylabel('Counts', fontsize = 60)
plt.grid(True)
plt.xticks(fontsize = 60)
plt.yticks(fontsize = 60)
plt.gca().tick_params(axis = 'x', pad = 20)

#Distribution of energies
E_bins = np.logspace(0, 3, 100)
plt.hist(E_arr, bins = E_bins, color = 'b')
plt.xscale('log')
plt.xlabel(r'Energy bins(in nT$^2$)', fontsize = 60)
plt.ylabel('Counts', fontsize = 60)
plt.grid(True)
plt.xticks(fontsize = 60)
plt.yticks(fontsize = 60)
plt.gca().tick_params(axis = 'x', pad = 20)