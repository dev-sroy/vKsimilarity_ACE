# -*- coding: utf-8 -*-
"""
Created on Fri May 28 13:58:46 2021

@author: Sohom
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def corr_f(s):
  return 'corr_'+s+'.txt'

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\SF_Elsasser\\"

exclude_list = ['199802027', '19980310', '19980820', '19980821', '19980822', '19990227', '19990323', '19990626', '19990718', '19990815', '20000915', '20000930', '20001022', '20001028', '20001124', '20010115', '20010116', '20010523', '20010616', '20010617', '20010618', '20011105', '20011107', '20020107', '20020119', '20020125', '20020228', '20020409', '20020417', '20020607', '20020608', '20020903', '20021214', '20021219', '20030110', '20031205', '20031220', '20040227', '20040309', '20040324', '20040528', '20040613', '20040624', ',20040707', '20040824', '20040927', '20041002', '20041107', '20041205', '20041221', '20050108', '20050121', '20050206', '20050214', '20050403', '20050528', '20050612', '20050623', '20050813', '20050930', '20051016', '20051111', '20051127', '20051216', '20060105', '20060203', '20060309', '20060326', '20060331', '20060408', '20060420', '20060505', '20060518', '20060704', '20060806', '20060807', '20060818', '20060930', '20061011', '20061028', '20070129', '20070206', '20070304', '20070311', '20070422', '20070518', '20070609', '20070723', '20070919', '20071013', '20080207', 'lengths_elsasser']
ex_f = list(map(corr_f, exclude_list))

fig, axs = plt.subplots(2, 1, figsize = (40, 60), sharex = True)

plt.rcParams['xtick.labelsize'] = 80
plt.rcParams['ytick.labelsize'] = 80

lag = np.linspace(0, 10, 480)

corr_interp_df = pd.DataFrame()

# axs[0].set_xscale('log')
# axs[0].set_yscale('log')
# axs[1].set_xscale('log')
# axs[1].set_yscale('log')

for f in os.listdir(dir):
  try:
    if f not in ex_f:
      
      interp_df = pd.DataFrame(columns = ['Vmag', 'Lag_z+','Lag_z-', 'S2_z+', 'S2_z-', 'S2_z'])
      
      fname = os.path.join(dir,f)
      
      if not os.path.isdir(fname):
        
      
        df = pd.read_csv(fname, delim_whitespace = True)
        
        vmag = df['Vmag'][1]
        
        if vmag>=500:
          axs[0].plot(df['Lag_z+'], df['S2_z+'], color='peru', alpha = 0.2)
          axs[1].plot(df['Lag_z-'], df['S2_z-'], color='peru', alpha = 0.2)
          
          intf = interp1d(df['Lag_z+'], df['S2_z+'], bounds_error = False)
          intf2 = interp1d(df['Lag_z-'], df['S2_z-'], bounds_error = False)
          
          interp_df['Lag_z+'] = lag
          interp_df['Lag_z-'] = lag
          interp_df['S2_z+'] = intf(lag)
          interp_df['S2_z-'] = intf2(lag)
          
          corr_interp_df = corr_interp_df.append(interp_df)
          print(f)
  except:
    continue
          
zplus_mean = corr_interp_df.groupby(['Lag_z+'])['S2_z+'].mean()
zminus_mean = corr_interp_df.groupby(['Lag_z-'])['S2_z-'].mean()

zplus_std = corr_interp_df.groupby(['Lag_z+'])['S2_z+'].std()
zminus_std = corr_interp_df.groupby(['Lag_z-'])['S2_z-'].std()

axs[0].set_xlim(0, 10)
axs[1].set_xlim(0, 10)

#axs[0].set_ylim(0.1, 3.5)
#axs[1].set_ylim(0.1, 3.5)

cond = lag>0

cond2 = np.logical_and(np.logical_and(zplus_mean<1, zplus_mean>0.1), lag>0.2)
cond3 = np.logical_and(np.logical_and(zminus_mean<1, zminus_mean>0.1), lag>0.2)

axs[0].plot(lag, zplus_mean, 'k', linewidth = 2.0, zorder = 25, label = 'Mean')
axs[0].fill_between(lag, (zplus_mean - zplus_std), (zplus_mean + zplus_std), color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
axs[0].fill_between(lag, (zplus_mean - 2*zplus_std), (zplus_mean + 2*zplus_std), color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')

axs[1].plot(lag, zminus_mean,'k', linewidth = 2.0, zorder = 25, label = 'Mean')
axs[1].fill_between(lag, (zminus_mean - zminus_std), (zminus_mean + zminus_std), color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
axs[1].fill_between(lag, (zminus_mean - 2*zminus_std), (zminus_mean + 2*zminus_std), color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')


# p1 = np.polyfit(np.log10(lag[cond2]), np.log10(zplus_mean[cond2]), 1)
# p2 = np.polyfit(np.log10(lag[cond3]), np.log10(zminus_mean[cond3]), 1)

# axs[0].plot(lag, zplus_mean, 'k', linewidth = 2.0, zorder = 25, label = 'Mean, slope = ' + str(round(p1[0], 2)))
# axs[0].fill_between(lag[cond], (zplus_mean - zplus_std)[cond], (zplus_mean + zplus_std)[cond], color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
# axs[0].fill_between(lag[cond], (zplus_mean - 2*zplus_std)[cond], (zplus_mean + 2*zplus_std)[cond], color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')

# axs[1].plot(lag, zminus_mean,'k', linewidth = 2.0, zorder = 25, label = 'Mean, slope = ' + str(round(p2[0], 2)))
# axs[1].fill_between(lag[cond], (zminus_mean - zminus_std)[cond], (zminus_mean + zminus_std)[cond], color = 'blue', alpha = 0.5, zorder = 10, label = r'$1\sigma$')
# axs[1].fill_between(lag[cond], (zminus_mean - 2*zminus_std)[cond], (zminus_mean + 2*zminus_std)[cond], color = 'dodgerblue', alpha = 0.5, zorder = 20, label = r'$2\sigma$')



axs[0].tick_params(axis='x', pad=25)
axs[1].tick_params(axis='x', pad=25)

plt.xlabel(r'Spatial lag, $r/\lambda$', fontsize =80)
axs[0].set_ylabel(r'$\hat{S}^{(2)}_{z^+}(r/\lambda)$', fontsize = 80)
axs[1].set_ylabel(r'$\hat{S}^{(2)}_{z^-}(r/\lambda)$', fontsize = 80)

axs[0].grid()
axs[1].grid()




#axs[0].set_yticks(np.arange(0, 3.5, step = 0.5))
#axs[1].set_yticks(np.arange(0, 3.5, step = 0.5))
#axs[0].set_xticks(np.arange(0, 4, step = 0.2))
#axs[1].set_xticks(np.arange(0, 4, step = 0.2))



#Plotting on loglog scale
#x=np.logspace(-1.15,-0.2,50)
#y=(x**(2/3.))*4
#axs[0].plot(x,y,'r--',label='Slope=2/3='+str(round(2/3.,2)))
#axs[1].plot(x,y,'r--',label='Slope=2/3='+str(round(2/3.,2)))
# axs[0].set_xscale('log')
# axs[0].set_yscale('log')

# axs[1].set_xscale('log')
# axs[1].set_yscale('log')

axs[0].legend(fontsize = 80, loc = 'best')
axs[1].legend(fontsize = 80, loc = 'best')

plt.subplots_adjust(hspace = 0)
plt.tight_layout()

axs[0].grid(True)
axs[1].grid(True)

plt.savefig(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\Plots\sf2_zplus_zminus_1norm_fast_1e7.pdf")
