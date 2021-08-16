# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 15:41:14 2021

@author: Sohom
"""

import numpy as np
import pandas as pd
from spacepy import pycdf
import datetime as dt
from datetime import timedelta
from init import *

#Defining constants
mu0 = 4*np.pi*1e-7
mp = 1.67e-27

def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')

def str_to_date(dt):
  return datetime.strptime(dt, '%Y%m%d%h%m%s')

def detrend(df, colstr):
  x = np.array(range(len(df)))
  mask = ~df[colstr].isna()
  p = np.polyfit(x[mask],df[colstr][mask],1)
  y = np.polyval(p,x)
  df[colstr+'_detrended'] = df[colstr] - y
  
def convert_to_Alfven(df, colstr):
  df[colstr+'_Alfven'] = df[colstr]*1e-9/np.sqrt(mu0*df['rho_smoothed']*1e6*mp)*1e-3

start_dt = '02/05/1998'
end_dt = '03/31/2008'

dr = pd.date_range(start_dt,end_dt,freq='D')
dts = convert_date(dr)

for i in range(len(dts)):
    
  #Read magnetic field data
  B_fname = rf"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Resampled data\ac_h3_mfi_{dts[i]}_v01_resampled_1min.cdf"
  cdf = pycdf.CDF(B_fname)
  keys = list(cdf.keys())
  epoch = cdf[keys[0]][...]
  BR,BT,BN = cdf[keys[1]][...].T
  B_df = pd.DataFrame(columns = ['Datetime','BR','BT','BN'])
  
  for j in range(len(epoch)):
    B_df.loc[j] = [epoch[j],BR[j],BT[j],BN[j]]
  
  B_df = B_df.set_index('Datetime')
  
  #Read velocity and density data
  v_fname = rf"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Velocity data_64s\{dts[i]}.txt"
  v_df = pd.read_fwf(v_fname)
  v_df = v_df.drop(columns = ['Unnamed: 0'])
  v_df['Datetime'] = v_df['Unnamed: 1']+ ' ' + v_df['Datetime']
  v_df = v_df.drop(columns = ['Unnamed: 1'])
  v_df = v_df.set_index('Datetime')
  v_df.index = pd.to_datetime(v_df.index)
  
  idx = pd.date_range(dr[i],dr[i+1],freq='1T')
  
  #Set any value less than -9999 or greater than 9999 to NaN
  v_df[v_df<-9999] = np.nan
  v_df[v_df>9999] = np.nan
  
  v_df = v_df[~v_df.index.duplicated()]
  v_df = v_df.reindex(v_df.index.union(idx)).interpolate('index').reindex(idx)
  
  #Combine them in a dataframe
  df = v_df.join(B_df, how = 'outer')
  df.index.name = 'Datetime'
  
  
  #Check if a large percentage of the values for the v and B fields are NaNs
  vsum = df['vmag'].isna().sum()/1441
  BRsum = df['BR'].isna().sum()/1441
  BTsum = df['BT'].isna().sum()/1441
  BNsum = df['BN'].isna().sum()/1441
  rhosum = df['rho'].isna().sum()/1441
  
  if all([vsum<=0.3, BRsum<=0.3, BTsum<=0.3, BNsum<=0.3, rhosum<=0.3]):
    
    df['Bmag'] = np.sqrt(df['BR']**2 + df['BT']**2 + df['BN']**2)
    #Smooth the proton density to 1 hour resolution
    df['rho_smoothed'] = df['rho'].rolling(60,min_periods = 1).mean()
    
    #Detrend velocity and magnetic fields
    detrend(df, 'x_dot_RTN')
    detrend(df, 'y_dot_RTN')
    detrend(df, 'z_dot_RTN')
    detrend(df, 'BR')
    detrend(df, 'BT')
    detrend(df, 'BN')
    
    convert_to_Alfven(df, 'BR')
    convert_to_Alfven(df, 'BT')
    convert_to_Alfven(df, 'BN')
  
    
    #Compute Elsasser variables
    
    df['z+R'] = df['x_dot_RTN_detrended'] + df['BR_Alfven']
    df['z-R'] = df['x_dot_RTN_detrended'] - df['BR_Alfven']
    df['z+T'] = df['y_dot_RTN_detrended'] + df['BT_Alfven']
    df['z-T'] = df['y_dot_RTN_detrended'] - df['BT_Alfven']
    df['z+N'] = df['z_dot_RTN_detrended'] + df['BN_Alfven']
    df['z-N'] = df['z_dot_RTN_detrended'] - df['BN_Alfven']
    
    #Write output to file
    outfile = rf'C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Elsasser variables(detrended)\{dts[i]}.txt'
    df.to_string(outfile)
    
  print(dts[i])



