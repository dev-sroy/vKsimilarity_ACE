# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 16:20:49 2021

@author: Sohom
"""

import numpy as np
import pandas as pd
import os
from init import *

from itertools import repeat

dir = r'C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Elsasser variables(detrended)'
corr_dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables"

corr_f = 'corr_lengths_elsasser.txt'
corr_fname = os.path.join(corr_dir, corr_f)

corr_len_df = pd.read_fwf(corr_fname)

def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')

def autocorr(dfin,dfout, var, comp):
  dfout[var+comp+comp] = [corr_func(dfin[var+comp], dfin[var+comp], lag) for lag in lag_arr]

def crosscorr(x,y):
  return [corr_func(x, y, lag) for lag in lag_arr]

def trace(df, s):
  df[s + '_tr(unnormalized)'] = df[s + 'RR'] + df[s + 'TT'] + df[s + 'NN']
  
def first_norm(df, s):
  df[s + '_tr'] = df[s + '_tr(unnormalized)'] / df[s + '_tr(unnormalized)'][0]

for f in os.listdir(dir):
  try:
    
    df = pd.read_fwf(os.path.join(dir,f))
    
    #Processing DataFrame
    df = df.rename(columns = {'Unnamed: 0':'Datetime'})
    df['Datetime'] +=  ' ' + df['Unnamed: 1']
    df = df.drop(columns = ['Unnamed: 1'])
    df = df.drop(index = 0)
    
    df = df.set_index('Datetime')
    df.index = pd.to_datetime(df.index)
    
    df = df.rename(columns = {'x_dot_RTN_detrended': 'vR', 'y_dot_RTN_detrended': 'vT', 'z_dot_RTN_detrended': 'vN'})
    
    #Finding average velocity for the day
    vavg = df['vmag'].mean()
    
    #Computing autocorrelations of the Elsasser variables
    corr_df = pd.DataFrame()
    lag_arr = np.array(range(480))
    
    corr_df.index.name = 'Lag_minutes'
    corr_df['Lag_spatial'] = lag_arr*vavg*60
    
   #Correlations of Elsasser variables  
    for var in ['z+', 'z-', 'B', 'v']:
      for comp in ['R', 'T', 'N']:
        autocorr(df, corr_df, var, comp)
  
      trace(corr_df, var)
      first_norm(corr_df, var)
    
  
    
    corr_df.reset_index()
    
    outfile = rf'C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\corr_{convert_date(df.index[0])}.txt'
    
    corr_df.to_string(outfile, index = False)
    
    #Computing correlation length
    
    
    print(df.index[0])
    
  except:
    continue
  
