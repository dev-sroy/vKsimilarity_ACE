# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 20:04:30 2021

@author: Sohom
"""

import h5py
import numpy as np
import datetime
import pandas as pd

def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')

for y in range(1998,2009):
  fname = rf"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Downloads\swepam_data_64sec_year{y}.h5"

  f = h5py.File(fname,'r')
  keys = list(f.keys())
  
  data = f[keys[0]]
  vel_keys = list(f[keys[0]].keys())
  
  v_dset = data[vel_keys[1]]
  vel_arr = np.array(v_dset)
  
  
  df = pd.DataFrame(columns = ['Datetime', 'rho', 'vmag', 'x_dot_RTN','y_dot_RTN','z_dot_RTN'])
  
  for i in range(len(vel_arr)):
    year = vel_arr[i][0]
    day = vel_arr[i][1]
    h = int(vel_arr[i][2])
    m = int(vel_arr[i][3])
    s = int(vel_arr[i][4])
    dt = datetime.datetime(year, 1, 1, 0, 0, 0) + datetime.timedelta(days = int(day-1), hours = h, minutes = m, seconds = s)
    rho = vel_arr[i][8]
    vproton = vel_arr[i][11]
    xdot, ydot, zdot = [vel_arr[i][15], vel_arr[i][16], vel_arr[i][17]]
    
    if day==vel_arr[i-1][1] or i==0:
      df.loc[i] = [dt,rho,vproton, xdot, ydot, zdot]
      df.set_index('Datetime')
    else:
      dtnew = dt-datetime.timedelta(days=1)
      outfile = r'C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Velocity data_64s//'+convert_date(dtnew)+'.txt'
      df.to_string(outfile)
      df=df[0:0]
      print(dt, dtnew)

      
  dtnew = dt
  outfile = r'C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Velocity data_64s//'+convert_date(dtnew)+'.txt'
  df.to_string(outfile)
  df=df[0:0]
  print(dt, dtnew)
    
    
  
  
  
  
  
  

