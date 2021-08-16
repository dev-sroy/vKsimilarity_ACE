# -*- coding: utf-8 -*-
"""
Created on Fri May 28 11:37:13 2021

@author: Sohom
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\Second normalization"
sf_dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\SF_Elsasser"
sf_df = pd.DataFrame(columns = ['Vmag', 'Lag_z+','Lag_z-', 'Lag_z', 'S2_z+', 'S2_z-', 'S2_z'])

corr_f = 'corr_lengths_elsasser.txt'

for f in os.listdir(dir):
  if f!=corr_f:
    try:
      
      fname = os.path.join(dir, f)
      
      if not os.path.isdir(fname):
        
        df = pd.read_csv(fname, delim_whitespace = True)
        
        # sf_df['Lag_z+'] = df['Lag_2norm_z+']
        # sf_df['Lag_z-'] = df['Lag_2norm_z-']
        # sf_df['Lag_z'] = df['Lag_2norm_sum_z']
        # sf_df['S2_z+'] = 2 - 2 * df['z+_tr']
        # sf_df['S2_z-'] = 2 - 2 *df['z-_tr']
        # sf_df['S2_z'] = 2 - 2 * df['Sum_z']
        sf_df['Vmag'] = df['Lag_spatial'][1:]/df.index[1:]/60
        
        sf_df['Lag_z+'] = df['Lag_2norm_z+']
        sf_df['Lag_z-'] = df['Lag_2norm_z-']
        sf_df['Lag_z'] = df['Lag_2norm_sum_z']
        sf_df['S2_z+'] = 2 - 2 * df['z+_tr']
        sf_df['S2_z-'] = 2 - 2 * df['z-_tr']
        
        sum_z_unnorm = df['z+_tr(unnormalized)'] + df['z-_tr(unnormalized)']
        sum_z_norm = sum_z_unnorm/sum_z_unnorm[0]
        
        sf_df['S2_z'] = 2 - 2 * sum_z_norm
        
        sf_fname = os.path.join(sf_dir, f)
        
        sf_df.to_string(sf_fname)
      
    except:
      continue
    
  print(f)