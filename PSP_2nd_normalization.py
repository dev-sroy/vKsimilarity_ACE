# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 15:39:48 2021

@author: Sohom
"""

from init import *
import os
import pandas as pd
import matplotlib.pyplot as plt

folder = r'C:\\Users\\Sohom Roy\\Dropbox\\My PC (LAPTOP-SLR6UBDE)\\Desktop\Research\\PSP correlations\\'
filelist = os.listdir(folder)

corr_len_fname = r'C:\\Users\\Sohom Roy\\Dropbox\\My PC (LAPTOP-SLR6UBDE)\\Desktop\Research\\PSP_correlation_lengths_linfit.txt'

dict = {}

with open(corr_len_fname) as f:
  for line in f:
    (key,value) = line.strip('\n').split('\t')
    dict[key] = value

  
#corr_len = pd.read_csv(r'C:\\Users\\Sohom Roy\\Dropbox\\My PC (LAPTOP-SLR6UBDE)\\Desktop\Research\\PSP_correlation_lengths_linfit.txt')


#First normalization
# for file in filelist:
#   fname = folder + file
  
#   corr_arr = pd.read_csv(fname,sep='\t')
  
#   lags = corr_arr.iloc[:,0].values
#   R = corr_arr.iloc[:,1].values
  
#   plt.plot(lags,R,'b')
  
# plt.grid(True)
# plt.xlabel('Lag(in km)',fontsize=40)
# plt.ylabel('R',fontsize=40)
# plt.xticks(fontsize=40)
# plt.yticks(fontsize=40)
# plt.gca().xaxis.get_offset_text().set_size(40)

#Second normalization
for file in filelist:
  fname = folder + file
  
  corr_arr = pd.read_csv(fname, sep = '\t',names=['Lags','R'])
  
  lags = corr_arr.iloc[:,0].values
  R = corr_arr.iloc[:,1].values
  
  corr_len = float(dict[file])
  lags_2 = lags/corr_len
  
  plt.plot(lags_2,R,'b')

plt.grid(True)
plt.xlabel(r'Spatial lag, $r/\lambda$',fontsize=40)
plt.ylabel('R',fontsize=40)
plt.xticks(fontsize=40)
plt.yticks(fontsize=40)
plt.gca().xaxis.get_offset_text().set_size(40)

