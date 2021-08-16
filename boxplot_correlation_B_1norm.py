# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 10:29:25 2021

@author: Sohom
"""

import numpy as np
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import ScalarFormatter

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\Second Normalization\\"
plot_dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\Plots\Box_plots_ApJ"

plot_fname = r"B_1norm_data.pdf"

#fig, axs = plt.subplots(1, 1, figsize = (40, 30), sharex = True)

lag = np.linspace(0, 1e7, 480)

corr_interp_df = pd.DataFrame()

plt.rcParams['xtick.labelsize'] = 80
plt.rcParams['ytick.labelsize'] = 80

fig, axs = plt.subplots(1, 1, figsize  = (40, 30))

for f in os.listdir(dir):
  
  if f!='corr_lengths_elsasser.txt':
    try:
      
      fname = os.path.join(dir, f)
      df = pd.read_csv(fname, delim_whitespace = True)
      vmag = df['Lag_spatial'][1]/60
      
      if vmag >= 500:
      
        interp_df = pd.DataFrame(columns = ['Lag_spatial', 'B_tr'])
        
        intf = interp1d(df['Lag_spatial'], df['B_tr'], bounds_error = False)
        
        interp_df['Lag_spatial'] = lag
        interp_df['B_tr'] = intf(lag)
        
        plt.plot(df['Lag_spatial'], df['B_tr'], color ='peru', alpha = 0.2)
        
        corr_interp_df = corr_interp_df.append(interp_df)
      
        print(f)
    except:
      continue

xticks = np.arange(0, 6e6, 1e6)
yticks = np.arange(-0.4, 1.2, 0.2)


corr_interp_df.boxplot(column = 'B_tr', by = 'Lag_spatial', ax = axs, showfliers = False, positions = lag, widths = 20000, medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})
plt.xlim(0, 5e6)
plt.ylim(-0.4, 1.0)
plt.xticks(xticks)
plt.gca().xaxis.set_major_formatter(ScalarFormatter())
axs.ticklabel_format(axis = 'x', style = 'sci', useOffset = True)
plt.yticks(yticks)
plt.gca().tick_params(axis = 'x', pad = 25)
#plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%0.0e'))
plt.xlabel(r'Spatial lag, $r$ (km)', fontsize = 80)
plt.ylabel(r'$R(r)$', fontsize = 80) 

plt.title('')
plt.suptitle('')

plt.savefig(os.path.join(plot_dir, plot_fname), dpi=600)
