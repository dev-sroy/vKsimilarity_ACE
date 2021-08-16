# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 14:12:18 2021

@author: Sohom
"""

import pandas as pd
import numpy as np
import os
from init import *

def corr_time(df, var):
  tc = np.where(df[var].values < np.exp(-1))[0][0]
  return tc

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables"
corr_dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\Second normalization"
corr_f = 'corr_lengths_elsasser.txt'
corr_fname = os.path.join(dir, corr_f)

corr_len_df = pd.read_fwf(corr_fname)

for f in os.listdir(dir):
  
  if f!=corr_f:
    try:
      
      fname = os.path.join(dir, f)
      new_fname = os.path.join(corr_dir, f)
      df = pd.read_csv(fname, delim_whitespace = True)
      
      
      date = f[5:13]
        
      corr_len = corr_len_df.loc[corr_len_df['Datetime'] == int(date)]['Corr_len_linfit_z+'].values
      df['Lag_2norm_z+'] = df['Lag_spatial']/corr_len
      
      corr_len2 = corr_len_df.loc[corr_len_df['Datetime'] == int(date)]['Corr_len_linfit_z-'].values
      df['Lag_2norm_z-'] = df['Lag_spatial']/corr_len2
      
      
      df['Sum_z(unnormalized)'] = df['z+_tr(unnormalized)'] + df['z-_tr(unnormalized)']
      df['Sum_z'] = df['Sum_z(unnormalized)']/df['Sum_z(unnormalized)'][0]
      
      tc = corr_time(df, 'Sum_z')
      p = np.polyfit(df['Lag_spatial'][:tc//2], df['Sum_z'][:tc//2], 1)
      corr_len_linfit = -1/p[0]
      
      df['Lag_2norm_sum_z'] = df['Lag_spatial']/corr_len_linfit
      
      df = df[['Lag_spatial', 'Lag_2norm_z+', 'Lag_2norm_z-', 'Lag_2norm_sum_z', 'z+RR', 'z+TT', 'z+NN', 'z+_tr(unnormalized)', 'z+_tr', 'z-RR', 'z-TT', 'z-NN', 'z-_tr(unnormalized)', 'z-_tr', 'Sum_z(unnormalized)', 'Sum_z', 'BRR', 'BTT', 'BNN', 'B_tr(unnormalized)', 'B_tr', 'vRR', 'vTT', 'vNN', 'v_tr(unnormalized)', 'v_tr']]
    
      df.to_string(new_fname)
    except:
      continue
  
  print(f)