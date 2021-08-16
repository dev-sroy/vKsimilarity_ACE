# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 15:23:17 2021

@author: Sohom
"""

from init import *
import os
import pandas as pd

folder = r'C:\\Users\\Sohom Roy\\Dropbox\\My PC (LAPTOP-SLR6UBDE)\\Desktop\Research\\PSP correlations\\'
filelist = os.listdir(folder)

f = open(r'C:\\Users\\Sohom Roy\\Dropbox\\My PC (LAPTOP-SLR6UBDE)\\Desktop\Research\\PSP_correlation_lengths_1e.txt','w')
f2 = open(r'C:\\Users\\Sohom Roy\\Dropbox\\My PC (LAPTOP-SLR6UBDE)\\Desktop\Research\\PSP_correlation_lengths_linfit.txt','w')

f.write('Date\tCorrelation length\n')
f2.write('Date\tCorrelation length\n')

for file in filelist:
  fname = folder+file
  
  corr_arr = pd.read_csv(fname, sep = '\t')
  
  lags = corr_arr.iloc[:,0].values
  R = corr_arr.iloc[:,1].values
  
  tc = np.where(R<np.exp(-1))[0][0]
  
  corr_len = lags[tc]
  
  f.write(f'{file}\t{lags[tc]}\n')
  
  if np.isnan(lags[:tc].sum())==0:
    log_corr = np.log(R[:tc//2])
    p = np.polyfit(lags[:tc//2],log_corr,1)
    corr_len_linfit = -1/p[0]
  else:
    corr_len_linfit = np.nan
  
  f2.write(f'{file}\t{corr_len_linfit}\n')
  
f.close()
f2.close()
  
  
  
  