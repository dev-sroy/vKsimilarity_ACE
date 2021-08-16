# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 15:30:49 2021

@author: Sohom
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 15:14:37 2021

@author: Sohom
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import ScalarFormatter

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\Second Normalization\\"
plot_dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\Plots\Box_plots_ApJ"

plot_fname = r"B_sf_2norm_data.pdf"

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
      
      df['B_sf'] = 2 - 2 * df['B_tr']
      
      if vmag >= 500:
      
        interp_df = pd.DataFrame(columns = ['Lag_2norm_B', 'B_sf'])
        
        intf = interp1d(df['Lag_2norm_B'], df['B_sf'], bounds_error = False)
        
        interp_df['Lag_2norm_B'] = lag
        interp_df['B_sf'] = intf(lag)
        
        plt.loglog(df['Lag_2norm_B'], df['B_sf'], color ='peru', alpha = 0.2)
        
        corr_interp_df = corr_interp_df.append(interp_df)
      
        print(f)
    except:
      continue

xticks = np.arange(0, 12, 2)
yticks = np.arange(0.5, 4.0, 0.5)

corr_interp_df = corr_interp_df.sort_values(by = 'Lag_2norm_B')

corr_interp_df[2008:].boxplot(column = 'B_sf', by = 'Lag_2norm_B', ax = axs, showfliers = False, positions = lag[2:], widths = np.diff(np.log10(lag[1:])), medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})
plt.xscale('log')
plt.yscale('log')
#plt.xlim(1e-2, 1.0)
#plt.ylim(1e-2, 10)
#plt.xlim(0, 10.0)
#plt.ylim(0, 4.0)
#plt.xticks(xticks)
#plt.gca().xaxis.set_major_formatter(ScalarFormatter())
#axs.ticklabel_format(axis = 'x', style = 'sci', useOffset = True)
#plt.yticks(yticks)
plt.gca().tick_params(axis = 'x', pad = 25)
#plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%0.0e'))
plt.xlabel(r'Spatial lag, $r/\lambda$', fontsize = 80)
plt.ylabel(r'$\hat{S}^{(2)}(r/\lambda)$', fontsize = 80) 
#plt.xscale('log')
#plt.yscale('log')

plt.title('')
plt.suptitle('')

#plt.savefig(os.path.join(plot_dir, plot_fname), dpi=600)