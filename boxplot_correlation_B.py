# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 04:38:22 2021

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

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\Second Normalization\\"
plot_dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\Plots\Box_plots_ApJ"

plot_fname = r"B_2norm_data.pdf"

#fig, axs = plt.subplots(1, 1, figsize = (40, 30), sharex = True)

lag = np.linspace(0, 10, 480)

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
      
        interp_df = pd.DataFrame(columns = ['Lag_2norm_B', 'B_tr'])
        
        intf = interp1d(df['Lag_2norm_B'], df['B_tr'], bounds_error = False)
        
        interp_df['Lag_2norm_B'] = lag
        interp_df['B_tr'] = intf(lag)
        
        plt.plot(df['Lag_2norm_B'], df['B_tr'], color ='peru', alpha = 0.2)
        
        corr_interp_df = corr_interp_df.append(interp_df)
      
        print(f)
    except:
      continue

xticks = np.arange(0, 4.5, 0.5)
yticks = np.arange(-0.4, 1.2, 0.2)


corr_interp_df.boxplot(column = 'B_tr', by = 'Lag_2norm_B', ax = axs, showfliers = False, positions = lag, widths = 0.015, medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})
plt.xticks(xticks)
plt.yticks(yticks)
plt.gca().tick_params(axis = 'x', pad = 25)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
plt.xlabel(r'Spatial lag, $r/\lambda$', fontsize = 80)
plt.ylabel(r'$\hat{R}(r/\lambda)$', fontsize = 80) 
plt.xlim(0, 4)
plt.ylim(-0.4, 1.0)
plt.title('')
plt.suptitle('')

plt.savefig(os.path.join(plot_dir, plot_fname), dpi=600)