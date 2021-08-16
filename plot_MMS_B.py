# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 01:26:17 2021

@author: Sohom
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

plt.rcParams['axes.grid'] = True

df1 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\B\B1_resB1.dat", delim_whitespace = True, names = ['Datetime', 'B1x', 'B1y', 'B1z'])

df1['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in df1['Datetime'].values]
df1['Datetime'] = pd.to_datetime(df1['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

df1 = df1.set_index('Datetime')
#Plot magnetic field components
fig, axs = plt.subplots(3,1)

axs[0].plot(df1.index, df1['B1x'])
axs[1].plot(df1.index, df1['B1y'])
axs[2].plot(df1.index, df1['B1z'])
axs[0].set_ylabel(r'$B_{1x}$', fontsize = 20)
axs[1].set_ylabel(r'$B_{1y}$', fontsize = 20)
axs[2].set_ylabel(r'$B_{1z}$', fontsize = 20)
plt.xlabel('Datetime', fontsize = 20)
#plt.grid(True)

interval_str = df1.index[0].strftime('%Y-%m-%d %H:%M:%S') + '  -  ' + df1.index[-1].strftime('%Y-%m-%d %H:%M:%S')
fig.suptitle(f'B-field components measured by MMS1 for interval {interval_str}', fontsize = 20)

df2 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\B\B2_resB1.dat", delim_whitespace = True, names = ['Datetime', 'B2x', 'B2y', 'B2z'])

df2['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in df2['Datetime'].values]
df2['Datetime'] = pd.to_datetime(df2['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

df2 = df2.set_index('Datetime')
#Plot magnetic field components
fig, axs = plt.subplots(3,1)

axs[0].plot(df2.index, df2['B2x'])
axs[1].plot(df2.index, df2['B2y'])
axs[2].plot(df2.index, df2['B2z'])
axs[0].set_ylabel(r'$B_{2x}$', fontsize = 20)
axs[1].set_ylabel(r'$B_{2y}$', fontsize = 20)
axs[2].set_ylabel(r'$B_{2z}$', fontsize = 20)
plt.xlabel('Datetime', fontsize = 20)
#plt.grid(True)

interval_str = df2.index[0].strftime('%Y-%m-%d %H:%M:%S') + '  -  ' + df2.index[-1].strftime('%Y-%m-%d %H:%M:%S')
fig.suptitle(f'B-field components measured by MMS2 for interval {interval_str}', fontsize = 20)

df3 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\B\B3_resB1.dat", delim_whitespace = True, names = ['Datetime', 'B3x', 'B3y', 'B3z'])

df3['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in df3['Datetime'].values]
df3['Datetime'] = pd.to_datetime(df3['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

df3 = df3.set_index('Datetime')
#Plot magnetic field components
fig, axs = plt.subplots(3,1)

axs[0].plot(df3.index, df3['B3x'])
axs[1].plot(df3.index, df3['B3y'])
axs[2].plot(df3.index, df3['B3z'])
axs[0].set_ylabel(r'$B_{3x}$', fontsize = 20)
axs[1].set_ylabel(r'$B_{3y}$', fontsize = 20)
axs[2].set_ylabel(r'$B_{3z}$', fontsize = 20)
plt.xlabel('Datetime', fontsize = 20)
#plt.grid(True)

interval_str = df3.index[0].strftime('%Y-%m-%d %H:%M:%S') + '  -  ' + df3.index[-1].strftime('%Y-%m-%d %H:%M:%S')
fig.suptitle(f'B-field components measured by MMS3 for interval {interval_str}', fontsize = 20)

df4 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\B\B4_resB1.dat", delim_whitespace = True, names = ['Datetime', 'B4x', 'B4y', 'B4z'])

df4['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in df4['Datetime'].values]
df4['Datetime'] = pd.to_datetime(df4['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

df4 = df4.set_index('Datetime')
#Plot magnetic field components
fig, axs = plt.subplots(3,1)

axs[0].plot(df4.index, df4['B4x'])
axs[1].plot(df4.index, df4['B4y'])
axs[2].plot(df4.index, df4['B4z'])
axs[0].set_ylabel(r'$B_{4x}$', fontsize = 20)
axs[1].set_ylabel(r'$B_{4y}$', fontsize = 20)
axs[2].set_ylabel(r'$B_{4z}$', fontsize = 20)
plt.xlabel('Datetime', fontsize = 20)
#plt.grid(True)

interval_str = df4.index[0].strftime('%Y-%m-%d %H:%M:%S') + '  -  ' + df4.index[-1].strftime('%Y-%m-%d %H:%M:%S')
fig.suptitle(f'B-field components measured by MMS4 for interval {interval_str}', fontsize = 20)