# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 01:26:16 2021

@author: Sohom
"""

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

#Directory where the correlations of the Elsasser variables are stored
dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Correlations of Elsasser variables\Second Normalization\\"

#Directory where plots are saved
plot_dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\Plots\Box_plots_ApJ"

#Filenames for the plots
plot_fname_plus = r"z+_data.pdf"
plot_fname_minus = r"z-_data.pdf"

lag = np.linspace(0, 1e7, 480)                                                 #Uniform grid for raw spatial lags (without normalizations)
lag_2norm = np.linspace(0, 10, 480)                                            #Uniform grid for spatial lags after 2nd normalization

corr_interp_df = pd.DataFrame()

#Setting font sizes for xticks and yticks
plt.rcParams['xtick.labelsize'] = 80
plt.rcParams['ytick.labelsize'] = 80

#Creating figures for plots
fig_plus, axs_plus = plt.subplots(3, 1, figsize  = (40, 90))
fig_minus, axs_minus = plt.subplots(3, 1, figsize = (40, 90))

for f in os.listdir(dir):
  
  if f!='corr_lengths_elsasser.txt':
    try:
      
      fname = os.path.join(dir, f)
      df = pd.read_csv(fname, delim_whitespace = True)
      vmag = df['Lag_spatial'][1]/60
      
      #Checking whether velocities are greater than 500 km/s
      if vmag >= 500:
        #Creating DataFrame to store interpolated correlation functions
        interp_df = pd.DataFrame(columns = ['Lag_spatial', 'Lag_2norm_z+', 'Lag_2norm_z-', 'z+_tr(unnormalized)', 'z+_tr_1norm', 'z+_tr_2norm', 'z-_tr(unnormalized)', 'z-_tr_1norm', 'z-_tr_2norm'])
        
        #Defining the interpolations for the z+ and z- variables
        intf_unnorm_plus = interp1d(df['Lag_spatial'], df['z+_tr(unnormalized)'], bounds_error = False)
        intf_1norm_plus = interp1d(df['Lag_spatial'], df['z+_tr'], bounds_error = False)
        intf_2norm_plus = interp1d(df['Lag_2norm_z+'], df['z+_tr'], bounds_error = False)
        
        intf_unnorm_minus = interp1d(df['Lag_spatial'], df['z-_tr(unnormalized)'], bounds_error = False)
        intf_1norm_minus = interp1d(df['Lag_spatial'], df['z-_tr'], bounds_error = False)
        intf_2norm_minus = interp1d(df['Lag_2norm_z-'], df['z-_tr'], bounds_error = False)
        
        #Interpolating the correlation functions using the interpolations defined above
        interp_df['Lag_spatial'] = lag
        
        interp_df['z+_tr(unnormalized)'] = intf_unnorm_plus(lag)
        interp_df['z+_tr_1norm'] = intf_1norm_plus(lag)
        interp_df['z+_tr_2norm'] = intf_2norm_plus(lag_2norm)
        
        interp_df['z-_tr(unnormalized)'] = intf_unnorm_minus(lag)
        interp_df['z-_tr_1norm'] = intf_1norm_minus(lag)
        interp_df['z-_tr_2norm'] = intf_2norm_minus(lag_2norm)
        
        #Plotting the uninterpolated correlation functions at each stage of the normalization for the given date
        axs_plus[0].plot(df['Lag_spatial'], df['z+_tr(unnormalized)'], color ='peru', alpha = 0.2)
        axs_plus[1].plot(df['Lag_spatial'], df['z+_tr'], color = 'peru', alpha = 0.2)
        axs_plus[2].plot(df['Lag_2norm_z+'], df['z+_tr'], color = 'peru', alpha = 0.2)
        
        axs_minus[0].plot(df['Lag_spatial'], df['z-_tr(unnormalized)'], color = 'peru', alpha = 0.2)
        axs_minus[1].plot(df['Lag_spatial'], df['z-_tr'], color = 'peru', alpha = 0.2)
        axs_minus[2].plot(df['Lag_2norm_z-'], df['z-_tr'], color = 'peru', alpha = 0.2)
        
        #Appending the DataFrame containing the interpolated correlation function to the DataFrame containing all the interpolated correlation functions
        corr_interp_df = corr_interp_df.append(interp_df)
      
        print(f)
    except:
      continue
    
#Setting ranges of xticks and yticks for unnormalized correlation functions
xticks_unnorm = np.arange(0, 1.2e7, 2e6)
yticks_unnorm = np.arange(-20000, 30000, 10000)

#Setting ranges of xticks and yticks for 1st normalized correlation functions
xticks_1norm = np.arange(0, 1.2e7, 2e6)
yticks_1norm = np.arange(-0.6, 1.2, 0.2)

#Setting ranges of xticks and yticks for 2nd normalized correlation functions
xticks_2norm = np.arange(0, 4, 1)
yticks_2norm = np.arange(-0.4, 1.2, 0.2)

#Boxplots for the unnormalized correlation functions for z+ and z-
corr_interp_df.boxplot(column = 'z+_tr(unnormalized)', by = 'Lag_spatial', ax = axs_plus[0], showfliers = False, positions = lag, widths = 20000, medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})
corr_interp_df.boxplot(column = 'z-_tr(unnormalized)', by = 'Lag_spatial', ax = axs_minus[0], showfliers = False, positions = lag, widths = 20000, medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})

#Boxplots for the 1st normalized correlation functions for z+ and z-
corr_interp_df.boxplot(column = 'z+_tr_1norm', by = 'Lag_spatial', ax = axs_plus[1], showfliers = False, positions = lag, widths = 20000, medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})
corr_interp_df.boxplot(column = 'z-_tr_1norm', by = 'Lag_spatial', ax = axs_minus[1], showfliers = False, positions = lag, widths = 20000,medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})

#Boxplots for the 2nd normalized correlation functions for z+ and z-
corr_interp_df.boxplot(column = 'z+_tr_2norm', by = 'Lag_2norm_z+', ax = axs_plus[2], showfliers = False, positions = lag, widths = 0.015, medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})
corr_interp_df.boxplot(column = 'z-_tr_2norm', by = 'Lag_2norm_z-', ax = axs_minus[2], showfliers = False, positions = lag, widths = 0.015, medianprops = {'linewidth' : 5.0, 'color' : 'k'}, patch_artist = True, boxprops = {'facecolor' : 'blue', 'alpha' : 0.2})

#Setting xlim and ylim for unnormalized correlation functions
axs_plus[0].set_xlim(0, 1e7)
axs_plus[0].set_ylim(-20000, 30000)
axs_minus[0].set_xlim(0, 1e7)
axs_minus[0].set_ylim(-20000, 30000)

#Setting xlim and ylim for 1st normalized correlation functions
axs_plus[1].set_xlim(0, 1e7)
axs_plus[1].set_ylim(-0.4, 1.0)
axs_minus[1].set_xlim(0, 1e7)
axs_minus[1].set_ylim(-0.4, 1.0)

#Setting xlim and ylim for 2nd normalized correlation functions
axs_plus[2].set_xlim(0, 4)
axs_plus[2].set_ylim(-0.4, 1.0)
axs_minus[2].set_xlim(0, 4)
axs_minus[2].set_ylim(-0.4, 1.0)

#Showing xticks and yticks for the plots
axs_plus[0].set_xticks(xticks_unnorm)
axs_plus[1].set_xticks(xticks_1norm)
axs_plus[2].set_xticks(xticks_2norm)
axs_minus[0].set_xticks(xticks_unnorm)
axs_minus[1].set_xticks(xticks_1norm)
axs_minus[2].set_xticks(xticks_2norm)

axs_plus[0].set_yticks(yticks_unnorm)
axs_plus[1].set_yticks(yticks_1norm)
axs_plus[2].set_yticks(yticks_2norm)
axs_minus[0].set_yticks(yticks_unnorm)
axs_minus[1].set_yticks(yticks_1norm)
axs_minus[2].set_yticks(yticks_2norm)


plt.gca().xaxis.set_major_formatter(ScalarFormatter())
plt.gca().ticklabel_format(axis = 'x', style = 'sci', useOffset = True)

#Padding the x-axis 
axs_plus[0].tick_params(axis ='x', pad = 25)
axs_plus[1].tick_params(axis ='x', pad = 25)
axs_plus[2].tick_params(axis ='x', pad = 25)
axs_minus[0].tick_params(axis ='x', pad = 25)
axs_minus[1].tick_params(axis ='x', pad = 25)
axs_minus[2].tick_params(axis ='x', pad = 25)

#plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%0.0e'))

#Setting xlabels and ylabels for the plots
#Setting xlabels

fs = 80

axs_plus[0].set_xlabel(r'Spatial lag, $r$(km)', fontsize = fs)
axs_plus[1].set_xlabel(r'Spatial lag, $r$(km)', fontsize = fs)
axs_plus[2].set_xlabel(r'Spatial lag, $r/\lambda$', fontsize = fs)

axs_minus[0].set_xlabel(r'Spatial lag, $r$(km)', fontsize = fs)
axs_minus[1].set_xlabel(r'Spatial lag, $r$(km)', fontsize = fs)
axs_minus[2].set_xlabel(r'Spatial lag, $r/\lambda$', fontsize = fs)

#Setting ylabels
axs_plus[0].set_ylabel(r'R_+(r)(km^2s^{-2})', fontsize = fs)
axs_plus[1].set_ylabel(r'R_+(r)', fontsize = fs)
axs_plus[2].set_ylabel(r'\hat{R}_+(r/\lambda)', fontsize = fs)

axs_minus[0].set_ylabel(r'R_-(r)(km^2s^{-2})', fontsize = fs)
axs_minus[1].set_ylabel(r'R_-(r)', fontsize = fs)
axs_minus[2].set_ylabel(r'\hat{R}_-(r/\lambda)', fontsize = fs)

plt.title('')
plt.suptitle('')
fig_plus.savefig(os.path.join(plot_dir, plot_fname_plus), dpi=600)
fig_minus.savefig(os.path.join(plot_dir, plot_fname_minus), dpi=600)
