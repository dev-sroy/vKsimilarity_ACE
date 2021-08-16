# -*- coding: utf-8 -*-
"""
Created on Tue May 11 17:47:01 2021

@author: Sohom
"""

import numpy as np
import pandas as pd
import os
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\Second Normalization\\"

lag = np.linspace(0, 10, 480)

corr_interp_df = pd.DataFrame()

fig, axs = plt.subplots(2, 1, figsize = (40, 60), sharex = True)

plt.rcParams['xtick.labelsize'] = 90
plt.rcParams['ytick.labelsize'] = 90

for f in os.listdir(dir):
  
  if f!='corr_lengths_elsasser.txt':
    
    interp_df = pd.DataFrame(columns = ['Lag_2norm_z+', 'Lag_2norm_z-', 'z+_tr', 'z-_tr'])
    
    fname = os.path.join(dir, f)
    
    df = pd.read_csv(fname, delim_whitespace = True)
    
    intf = interp1d(df['Lag_2norm_z+'], df['z+_tr'], bounds_error = False)
    intf2= interp1d(df['Lag_2norm_z-'], df['z-_tr'], bounds_error = False)
    
    interp_df['Lag_2norm_z+'] = lag
    interp_df['Lag_2norm_z-'] = lag
    interp_df['z+_tr'] = intf(lag)
    interp_df['z-_tr'] = intf2(lag)
    
    axs[0].plot(df['Lag_2norm_z+'], df['z+_tr'], color ='peru', alpha = 0.2)
    axs[1].plot(df['Lag_2norm_z-'], df['z-_tr'], color ='peru', alpha = 0.2)
    
    corr_interp_df = corr_interp_df.append(interp_df)
    
    print(f)

zplus_mean = corr_interp_df.groupby(['Lag_2norm_z+'])['z+_tr'].mean()
zminus_mean = corr_interp_df.groupby(['Lag_2norm_z-'])['z-_tr'].mean()

zplus_std = corr_interp_df.groupby(['Lag_2norm_z+'])['z+_tr'].std()
zminus_std = corr_interp_df.groupby(['Lag_2norm_z-'])['z-_tr'].std()


axs[0].plot(lag, zplus_mean.values,'k', linewidth = 2.0, zorder = 25, label = 'Mean')
axs[0].fill_between(lag, zplus_mean - zplus_std, zplus_mean + zplus_std, color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
axs[0].fill_between(lag, zplus_mean - 2*zplus_std, zplus_mean + 2*zplus_std, color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')

axs[1].plot(lag, zminus_mean,'k', linewidth = 2.0, zorder = 25, label = 'Mean')
axs[1].fill_between(lag, zminus_mean - zminus_std, zminus_mean + zminus_std, color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
axs[1].fill_between(lag, zminus_mean - 2*zminus_std, zminus_mean + 2*zminus_std, color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')

axs[0].set_xlim(0, 4)
axs[1].set_xlim(0, 4)
axs[0].set_ylim(-0.6, 1.2)
axs[1].set_ylim(-0.6, 1.2)

axs[0].tick_params(axis='x', pad=25)
axs[1].tick_params(axis='x', pad=25)

plt.xlabel(r'Spatial lag, $r/\lambda$', fontsize = 80)
axs[0].set_ylabel(r'$\hat{R}_{+}(r/\lambda)$', fontsize = 80)
axs[1].set_ylabel(r'$\hat{R}_{-}(r/\lambda)$', fontsize = 80)

axs[0].grid()
axs[1].grid()

axs[0].legend(fontsize = 80, loc = 'best')
axs[1].legend(fontsize = 80, loc = 'best')

axs[0].set_yticks(np.arange(-0.4, 1.2, step = 0.2))
axs[1].set_yticks(np.arange(-0.4, 1.2, step = 0.2))
#axs[0].set_xticks(np.arange(0, 4, step = 0.2))
#axs[1].set_xticks(np.arange(0, 4, step = 0.2))


plt.subplots_adjust(hspace = 0)
plt.tight_layout()

plt.savefig(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\Plots\corr_zplus_zminus_2norm_fast.pdf")



