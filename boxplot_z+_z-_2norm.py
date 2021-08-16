# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 16:07:21 2021

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

plot_fname = r"z+_z-_unnorm_data.pdf"

lag = np.linspace(0, 10, 480)

corr_interp_df = pd.DataFrame()

plt.rcParams['xtick.labelsize'] = 80
plt.rcParams['ytick.labelsize'] = 80

fig, axs = plt.subplots(2, 1, figsize  = (40, 60), sharex = True)

for f in os.listdir(dir):
  
  if f!='corr_lengths_elsasser.txt':
    try:
      
      fname = os.path.join(dir, f)
      df = pd.read_csv(fname, delim_whitespace = True)
      vmag = df['Lag_spatial'][1]/60
      
      if vmag >= 500:
      
        interp_df = pd.DataFrame(columns = ['Lag_2norm_z+', 'z+_tr', 'z-_tr'])
        
        intf = interp1d(df['Lag_2norm_z+'], df['z+_tr'], bounds_error = False)
        intf2 = interp1d(df['Lag_2norm_z-'], df['z-_tr'], bounds_error = False)
        
        interp_df['Lag_2norm_z+'] = lag
        interp_df['z+_tr'] = intf(lag)
        
        interp_df['Lag_2norm_z-'] = lag
        interp_df['z-_tr'] = intf2(lag)
        
        axs[0].plot(df['Lag_2norm_z+'], df['z+_tr'], color ='peru', alpha = 0.2)
        axs[1].plot(df['Lag_2norm_z-'], df['z-_tr'], color = 'peru', alpha = 0.2)
        
        corr_interp_df = corr_interp_df.append(interp_df)
      
        print(f)
    except:
      continue

xticks = np.arange(0, 4, 1)
yticks = np.arange(-0.4, 1.2, 0.2)

corr_interp_df.boxplot(column = 'z+_tr', by = 'Lag_2norm_z+', ax = axs[0], showfliers = False, positions = lag, widths = 0.015, medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})
corr_interp_df.boxplot(column = 'z-_tr', by = 'Lag_2norm_z-', ax = axs[1], showfliers = False, positions = lag, widths = 0.015, medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})
axs[0].set_xlim(0, 4)
axs[0].set_ylim(-0.4, 1.0)

axs[1].set_xlim(0, 4)
axs[1].set_ylim(-0.4, 1.0)

plt.xticks(xticks)

axs[0].set_yticks(yticks)
axs[1].set_yticks(yticks)
plt.gca().xaxis.set_major_formatter(ScalarFormatter())
plt.gca().ticklabel_format(axis = 'x', style = 'sci', useOffset = True)
plt.yticks(yticks)
axs[0].tick_params(axis = 'x', pad = 25)
axs[1].tick_params(axis = 'x', pad = 25)
#plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%0.0e'))
plt.xlabel(r'Spatial lag, $r/\lambda$', fontsize = 80)
axs[0].set_ylabel(r'$\hat{R_+}(r/\lambda)$', fontsize = 80) 
axs[1].set_ylabel(r'$\hat{R_-}(r/\lambda)$', fontsize = 80) 
#plt.xscale('log')
#plt.yscale('log')

plt.title('')
plt.suptitle('')
plt.savefig(os.path.join(plot_dir, plot_fname), dpi=600)