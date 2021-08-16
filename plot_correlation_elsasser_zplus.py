# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 12:57:45 2021

@author: Sohom
"""

import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def corr_f(s):
  return 'corr_'+s+'.txt'

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\Second Normalization\\"

exclude_list = ['199802027', '19980310', '19980820', '19980821', '19980822', '19990227', '19990323', '19990626', '19990718', '19990815', '20000915', '20000930', '20001022', '20001028', '20001124', '20010115', '20010116', '20010523', '20010616', '20010617', '20010618', '20011105', '20011107', '20020107', '20020119', '20020125', '20020228', '20020409', '20020417', '20020607', '20020608', '20020903', '20021214', '20021219', '20030110', '20031205', '20031220', '20040227', '20040309', '20040324', '20040528', '20040613', '20040624', ',20040707', '20040824', '20040927', '20041002', '20041107', '20041205', '20041221', '20050108', '20050121', '20050206', '20050214', '20050403', '20050528', '20050612', '20050623', '20050813', '20050930', '20051016', '20051111', '20051127', '20051216', '20060105', '20060203', '20060309', '20060326', '20060331', '20060408', '20060420', '20060505', '20060518', '20060704', '20060806', '20060807', '20060818', '20060930', '20061011', '20061028', '20070129', '20070206', '20070304', '20070311', '20070422', '20070518', '20070609', '20070723', '20070919', '20071013', '20080207', 'lengths_elsasser']
ex_f = list(map(corr_f, exclude_list))

fig, axs = plt.subplots(3, 1, figsize = (40, 90))
fig2, axs2 = plt.subplots(3, 1, figsize = (40, 90))

plt.rcParams['xtick.labelsize'] = 80
plt.rcParams['ytick.labelsize'] = 80

lag_max = 1e7
lag = np.linspace(0, lag_max, 480)
lag_2norm = np.linspace(0, 10, 480)

corr_interp_df = pd.DataFrame()

for f in os.listdir(dir):
  if f not in ex_f:
    
    interp_df = pd.DataFrame(columns = ['Lag_spatial', 'Lag_2norm_z+', 'Lag_2norm_z-', 'z+_tr(unnormalized)', 'z-_tr(unnormalized)', 'z+_tr', 'z-_tr', 'z+_tr(2norm)', 'z-_tr(2norm)'])
    
    fname = os.path.join(dir,f)
    
    if not os.path.isdir(fname):
      
    
      df = pd.read_csv(fname, delim_whitespace = True)
      
      vmag = df['Lag_spatial'][1]/df.index[1]/60
      
      if vmag>=500:
        try:
          
          
          intfplus_unnorm = interp1d(df['Lag_spatial'], df['z+_tr(unnormalized)'], bounds_error = False)
          intfminus_unnorm = interp1d(df['Lag_spatial'], df['z-_tr(unnormalized)'], bounds_error = False)
          
          intfplus_1norm = interp1d(df['Lag_spatial'], df['z+_tr'], bounds_error = False)
          intfminus_1norm = interp1d(df['Lag_spatial'], df['z-_tr'], bounds_error = False)
          
          intfplus_2norm = interp1d(df['Lag_2norm_z+'], df['z+_tr'], bounds_error = False)
          intfminus_2norm = interp1d(df['Lag_2norm_z-'], df['z-_tr'], bounds_error = False)
          
          #Not normalized
          interp_df['Lag_spatial'] = lag
          interp_df['z+_tr(unnormalized)'] = intfplus_unnorm(lag)
          interp_df['z-_tr(unnormalized)'] = intfminus_unnorm(lag)
          
          #1st normalized
          interp_df['z+_tr'] = intfplus_1norm(lag)
          interp_df['z-_tr'] = intfminus_1norm(lag)
          
          #2nd normalized
          interp_df['Lag_2norm_z+'] = lag_2norm
          interp_df['Lag_2norm_z-'] = lag_2norm
          interp_df['z+_tr(2norm)'] = intfplus_2norm(lag_2norm)
          interp_df['z-_tr(2norm)'] = intfminus_2norm(lag_2norm)
          
          corr_interp_df = corr_interp_df.append(interp_df)
          print(f)
          
          axs[0].plot(df['Lag_spatial'], df['z+_tr(unnormalized)'], color = 'peru', alpha = 0.2)
          axs[1].plot(df['Lag_spatial'], df['z-_tr'], color = 'peru', alpha = 0.2)
          axs[2].plot(df['Lag_2norm_z+'], df['z+_tr'], color = 'peru', alpha = 0.2)
          
          axs2[0].plot(df['Lag_spatial'], df['z-_tr(unnormalized)'], color = 'peru', alpha = 0.2)
          axs2[1].plot(df['Lag_spatial'], df['z-_tr'], color = 'peru', alpha = 0.2)
          axs2[2].plot(df['Lag_2norm_z-'], df['z-_tr'], color = 'peru', alpha = 0.2)
          
          
        except:
          continue
        
zplus_mean_unnorm = corr_interp_df.groupby(['Lag_spatial'])['z+_tr(unnormalized)'].mean()
zminus_mean_unnorm = corr_interp_df.groupby(['Lag_spatial'])['z-_tr(unnormalized)'].mean()

zplus_std_unnorm = corr_interp_df.groupby(['Lag_spatial'])['z+_tr(unnormalized)'].std()
zminus_std_unnorm = corr_interp_df.groupby(['Lag_spatial'])['z-_tr(unnormalized)'].std()

zplus_mean_1norm = corr_interp_df.groupby(['Lag_spatial'])['z+_tr'].mean()
zminus_mean_1norm = corr_interp_df.groupby(['Lag_spatial'])['z-_tr'].mean()

zplus_std_1norm = corr_interp_df.groupby(['Lag_spatial'])['z+_tr'].std()
zminus_std_1norm = corr_interp_df.groupby(['Lag_spatial'])['z-_tr'].std()

zplus_mean_2norm = corr_interp_df.groupby(['Lag_2norm_z+'])['z+_tr(2norm)'].mean()
zminus_mean_2norm = corr_interp_df.groupby(['Lag_2norm_z-'])['z-_tr(2norm)'].mean()

zplus_std_2norm = corr_interp_df.groupby(['Lag_2norm_z+'])['z+_tr(2norm)'].std()
zminus_std_2norm = corr_interp_df.groupby(['Lag_2norm_z-'])['z-_tr(2norm)'].std()

#Plotting mean and standard deviations

axs[0].plot(lag, zplus_mean_unnorm.values,'k', linewidth = 2.0, zorder = 25, label = 'Mean')
axs[0].fill_between(lag, zplus_mean_unnorm - zplus_std_unnorm, zplus_mean_unnorm + zplus_std_unnorm, color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
axs[0].fill_between(lag, zplus_mean_unnorm - 2*zplus_std_unnorm, zplus_mean_unnorm + 2*zplus_std_unnorm, color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')

axs[1].plot(lag, zplus_mean_1norm,'k', linewidth = 2.0, zorder = 25, label = 'Mean')
axs[1].fill_between(lag, zplus_mean_1norm - zplus_std_1norm, zplus_mean_1norm + zplus_std_1norm, color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
axs[1].fill_between(lag, zplus_mean_1norm - 2*zplus_std_1norm, zplus_mean_1norm + 2*zplus_std_1norm, color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')

axs[2].plot(lag_2norm, zplus_mean_2norm.values,'k', linewidth = 2.0, zorder = 25, label = 'Mean')
axs[2].fill_between(lag_2norm, zplus_mean_2norm - zplus_std_2norm, zplus_mean_2norm + zplus_std_2norm, color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
axs[2].fill_between(lag_2norm, zplus_mean_2norm - 2*zplus_std_2norm, zplus_mean_2norm + 2*zplus_std_2norm, color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')

axs2[0].plot(lag, zminus_mean_unnorm.values,'k', linewidth = 2.0, zorder = 25, label = 'Mean')
axs2[0].fill_between(lag, zminus_mean_unnorm - zminus_std_unnorm, zminus_mean_unnorm + zminus_std_unnorm, color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
axs2[0].fill_between(lag, zminus_mean_unnorm - 2*zminus_std_unnorm, zminus_mean_unnorm + 2*zminus_std_unnorm, color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')

axs2[1].plot(lag, zminus_mean_1norm,'k', linewidth = 2.0, zorder = 25, label = 'Mean')
axs2[1].fill_between(lag, zminus_mean_1norm - zminus_std_1norm, zminus_mean_1norm + zminus_std_1norm, color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
axs2[1].fill_between(lag, zminus_mean_1norm - 2*zminus_std_1norm, zminus_mean_1norm + 2*zminus_std_1norm, color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')

axs2[2].plot(lag_2norm, zminus_mean_2norm.values,'k', linewidth = 2.0, zorder = 25, label = 'Mean')
axs2[2].fill_between(lag_2norm, zminus_mean_2norm - zminus_std_2norm, zminus_mean_2norm + zminus_std_2norm, color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
axs2[2].fill_between(lag_2norm, zminus_mean_2norm - 2*zminus_std_2norm, zminus_mean_2norm + 2*zminus_std_2norm, color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')

#Setting proper x limits and axis labels

axs[0].set_xlim(0, 1e7)
axs[1].set_xlim(0, 1e7)
axs[2].set_xlim(0, 4)

axs[0].set_ylim(-20000, 30000)
axs2[0].set_ylim(-20000, 30000)
axs[1].set_ylim(-0.6, 1.2)
axs2[1].set_ylim(-0.6, 1.2)
axs[2].set_ylim(-0.6, 1.2)
axs2[2].set_ylim(-0.6, 1.2)

axs2[0].set_xlim(0, 1e7)
axs2[1].set_xlim(0, 1e7)
axs2[2].set_xlim(0, 4)

xlabel_1norm = r'Spatial lag, $r$(km)'
xlabel_2norm = r'Spatial lag, $r/\lambda$'

ylabel_unnorm_plus = r'$R_+(r) (km^2s^{-2})$'
ylabel_unnorm_minus = r'$R_-(r) (km^2s^{-2})$'
ylabel_1norm_plus = r'$R_+(r)$'
ylabel_1norm_minus = r'$R_-(r)$'
ylabel_2norm_plus = r'$\hat{R}_{+}(r/\lambda)$'
ylabel_2norm_minus = r'$\hat{R}_{-}(r/\lambda)$'

axs[0].set_xlabel(xlabel_1norm, fontsize = 80)
axs[1].set_xlabel(xlabel_1norm, fontsize = 80)
axs[2].set_xlabel(xlabel_2norm, fontsize = 80)

axs2[0].set_xlabel(xlabel_1norm, fontsize = 80)
axs2[1].set_xlabel(xlabel_1norm, fontsize = 80)
axs2[2].set_xlabel(xlabel_2norm, fontsize = 80)

axs[0].set_ylabel(ylabel_unnorm_plus, fontsize = 80)
axs[1].set_ylabel(ylabel_1norm_plus, fontsize = 80)
axs[2].set_ylabel(ylabel_2norm_plus, fontsize = 80)

axs2[0].set_ylabel(ylabel_unnorm_minus, fontsize = 80)
axs2[1].set_ylabel(ylabel_1norm_minus, fontsize = 80)
axs2[2].set_ylabel(ylabel_2norm_minus, fontsize = 80)

axs[0].tick_params(axis = 'x', pad = 25)
axs[1].tick_params(axis = 'x', pad = 25)
axs[2].tick_params(axis = 'x', pad = 25)
axs2[0].tick_params(axis = 'x', pad = 25)
axs2[1].tick_params(axis = 'x', pad = 25)
axs2[2].tick_params(axis = 'x', pad = 25)

for i in range(3):
  axs[i].grid()
  axs[i].legend(fontsize = 80, loc = 'best')
  axs2[i].grid()
  axs2[i].legend(fontsize = 80, loc = 'best')

fig.tight_layout()
fig2.tight_layout()

fig.savefig(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\Plots\corr_zplus_fast_1e7.pdf")
fig2.savefig(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\Plots\corr_zminus_fast_1e7.pdf")
