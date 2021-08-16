# -*- coding: utf-8 -*-
"""
Created on Sat May  8 10:34:58 2021

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

df2 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\ions\Ni_1_resNi_1.dat", delim_whitespace = True, names = ['Datetime', 'Ni'])

df2['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in df2['Datetime'].values]
df2['Datetime'] = pd.to_datetime(df2['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

df2 = df2.set_index('Datetime')

df3 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\ions\Ti_1_resNi_1.dat", delim_whitespace = True, names = ['Datetime', 'Ti'])

df3['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in df3['Datetime'].values]
df3['Datetime'] = pd.to_datetime(df3['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

df3 = df3.set_index('Datetime')

df4 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\ions\Vi_1_resNi_1.dat", delim_whitespace = True, names = ['Datetime', 'vi1x', 'vi1y', 'vi1z'])

df4['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in df4['Datetime'].values]
df4['Datetime'] = pd.to_datetime(df4['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

df4 = df4.set_index('Datetime')

#Plot magnetic field components
fig, axs = plt.subplots(4,1, sharex = True)

axs[0].plot(df1.index, df1['B1x'], 'k', label = r'$B_x$')
axs[0].plot(df1.index, df1['B1y'], 'b', label = r'$B_y$')
axs[0].plot(df1.index, df1['B1z'], 'r', label = r'$B_z$')
axs[1].plot(df2.index, df2['Ni'], 'k')
axs[2].plot(df3.index, df3['Ti'], 'k')
axs[3].plot(df4.index, df4['vi1x'], 'k', label = r'$v_{i, x}$')
axs[3].plot(df4.index, df4['vi1y'], 'b', label = r'$v_{i, y}$')
axs[3].plot(df4.index, df4['vi1z'], 'r', label = r'$v_{i, z}$')

axs[0].set_ylabel('B(nT)', fontsize = 20)
axs[1].set_ylabel(r'$N_i$(cm$^{-3}$)', fontsize = 20)
axs[2].set_ylabel(r'$T_i$(eV)', fontsize = 20)
axs[3].set_ylabel(r'$V_i$(km/s)', fontsize = 20)

axs[0].legend(loc = 'best', fontsize = 15)
axs[3].legend(loc = 'best', fontsize = 15)

plt.xlabel('2017-01-18', fontsize = 20)
#plt.grid(True)

interval_str = df1.index[0].strftime('%Y-%m-%d %H:%M:%S') + '  -  ' + df1.index[-1].strftime('%Y-%m-%d %H:%M:%S')
