# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 23:08:29 2021

@author: Sohom
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from functools import reduce

plt.rcParams['axes.grid'] = True

df1 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\B\Ni_1_resB1.dat", delim_whitespace = True, names = ['Datetime', 'Ni_1'])
df2 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\B\Ni_1_resB1.dat", delim_whitespace = True, names = ['Datetime', 'Ni_2'])
df3 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\B\Ni_1_resB1.dat", delim_whitespace = True, names = ['Datetime', 'Ni_3'])
df4 = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\MMS_DATA\ascii\20170118\004553\B\Ni_1_resB1.dat", delim_whitespace = True, names = ['Datetime', 'Ni_4'])

data_frames = [df1, df2, df3, df4]

df = reduce(lambda left, right: pd.merge(left, right, on=['Datetime'], how = 'outer'), data_frames)

df['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in df['Datetime'].values]
df['Datetime'] = pd.to_datetime(df['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

df = df.set_index('Datetime')

fig, axs = plt.subplots(4,1)

axs[0].plot(df.index, df['Ni_1'])
axs[1].plot(df.index, df['Ni_2'])
axs[2].plot(df.index, df['Ni_3'])
axs[3].plot(df.index, df['Ni_4'])

axs[0].set_ylabel(r'$N_{i, 1}$', fontsize = 20)
axs[1].set_ylabel(r'$N_{i, 2}$', fontsize = 20)
axs[2].set_ylabel(r'$N_{i, 3}$', fontsize = 20)
axs[3].set_ylabel(r'$N_{i, 4}$', fontsize = 20)
plt.xlabel('Datetime', fontsize = 20)
