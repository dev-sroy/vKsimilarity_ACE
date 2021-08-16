# -*- coding: utf-8 -*-
"""
Created on Mon May 10 10:51:14 2021

@author: Sohom
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\\"

def corr_f(s):
  return 'corr_'+s+'.txt'

def corr_time(df, var):
  tc = np.where(df[var].values < np.exp(-1))[0][0]
  return tc

corr_len_df = pd.DataFrame(columns = ['Datetime', 'Corr_time_z+', 'Corr_len_1e_z+', 'Corr_len_linfit_z+', 'Corr_time_z-', 'Corr_time_B', 'Corr_time_v', 'Corr_len_1e_z-', 'Corr_len_linfit_z-', 'Corr_len_linfit_B', 'Corr_len_linfit_v'], dtype = None)

exclude_list = ['199802027', '19980310', '19980820', '19980821', '19980822', '19990227', '19990323', '19990626', '19990718', '19990815', '20000915', '20000930', '20001022', '20001028', '20001124', '20010115', '20010116', '20010523', '20010616', '20010617', '20010618', '20011105', '20011107', '20020107', '20020119', '20020125', '20020228', '20020409', '20020417', '20020607', '20020608', '20020903', '20021214', '20021219', '20030110', '20031205', '20031220', '20040227', '20040309', '20040324', '20040528', '20040613', '20040624', ',20040707', '20040824', '20040927', '20041002', '20041107', '20041205', '20041221', '20050108', '20050121', '20050206', '20050214', '20050403', '20050528', '20050612', '20050623', '20050813', '20050930', '20051016', '20051111', '20051127', '20051216', '20060105', '20060203', '20060309', '20060326', '20060331', '20060408', '20060420', '20060505', '20060518', '20060704', '20060806', '20060807', '20060818', '20060930', '20061011', '20061028', '20070129', '20070206', '20070304', '20070311', '20070422', '20070518', '20070609', '20070723', '20070919', '20071013', '20080207']
ex_f = list(map(corr_f, exclude_list))

for f in os.listdir(dir):
  
  if f not in ex_f:
    
    fname = os.path.join(dir,f)
    
    if not os.path.isdir(fname):
      df = pd.read_csv(fname, delim_whitespace = True)
      
      try:
        
      #Calculate correlation length of z+ using the 1/e method
        tc = corr_time(df, 'z+_tr')
        corr_len = df['Lag_spatial'][tc]
        
        #Calculate correlation length of z+ using the linear fit method
        
        p = np.polyfit(df['Lag_spatial'][:tc//2], df['z+_tr'][:tc//2], 1)
        corr_len_linfit = -1/p[0]
        
        #Calculate correlation length of z- using the 1/e method
        tc2 = corr_time(df, 'z-_tr')
        corr_len2 = df['Lag_spatial'][tc2]
        
        #Calculate correlation length of z- using the linear fit method
        
        p2 = np.polyfit(df['Lag_spatial'][:tc2//2], df['z-_tr'][:tc2//2], 1)
        corr_len_linfit2 = -1/p2[0]
        
        tc3 = corr_time(df, 'B_tr')
        p3 = np.polyfit(df['Lag_spatial'][:tc3//2], df['B_tr'][:tc3//2], 1) 
        corr_len_linfitB = -1/p3[0]
        
        tc4 = corr_time(df, 'v_tr')
        p4 = np.polyfit(df['Lag_spatial'][:tc4//2], df['v_tr'][:tc4//2], 1)
        corr_len_linfitv = -1/p4[0]
        
        row = {'Datetime': os.path.splitext(f)[0][5:], 'Corr_time_z+': tc, 'Corr_len_1e_z+': corr_len, 'Corr_len_linfit_z+': corr_len_linfit,  'Corr_time_z-': tc2, 'Corr_time_B': tc3, 'Corr_time_v': tc4, 'Corr_len_1e_z-': corr_len2, 'Corr_len_linfit_z-': corr_len_linfit2, 'Corr_len_linfit_B': corr_len_linfitB, 'Corr_len_linfit_v': corr_len_linfitv}
        corr_len_df = corr_len_df.append(row, ignore_index = True)
        print(f)
        
      except:
        continue
      
corr_outfile = rf'C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\corr_lengths_elsasser.txt'
corr_len_df.to_string(corr_outfile, index = False)