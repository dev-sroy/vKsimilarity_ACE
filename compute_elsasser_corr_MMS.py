# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 13:16:27 2021

@author: Sohom
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from init import *

mu0 = 4*np.pi*1e-7
mp = 1.67e-27

def autocorr(dfin,dfout, var, comp):
  dfout[var+comp+comp] = [corr_func(dfin[var+comp], dfin[var+comp], lag) for lag in lag_arr]
  
def trace(df, s):
  df[s + '_tr(unnormalized)'] = df[s + '_x_x'] + df[s + '_y_y'] + df[s + '_z_z']
  
def first_norm(df, s):
  df[s + '_tr'] = df[s + '_tr(unnormalized)'] / df[s + '_tr(unnormalized)'][0]
  
def compute_e1_plus(Zplus, Zminus, Lplus, alpha = 1):
  return alpha * Zplus ** 2 * Zminus/Lplus

def compute_e1_minus(Zplus, Zminus, Lminus, alpha = 1):
  return alpha * Zminus ** 2 * Zplus/Lminus



B_df = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\004553\ions\B1_resNi_1.dat", delim_whitespace = True, names = ['Datetime', 'B1x', 'B1y', 'B1z'])

v_df = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\004553\ions\Vi_1_resNi_1.dat", delim_whitespace = True, names = ['Datetime', 'v1x', 'v1y', 'v1z'])

rho_df = pd.read_csv(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\MMS_MATLAB\004553\ions\Ni_1_resNi_1.dat", delim_whitespace = True, names = ['Datetime', 'Ni'])

B_df['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in B_df['Datetime'].values]
B_df['Datetime'] = pd.to_datetime(B_df['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

B_df = B_df.set_index('Datetime')

v_df['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in v_df['Datetime'].values]
v_df['Datetime'] = pd.to_datetime(v_df['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

v_df = v_df.set_index('Datetime')

v_df['vmag'] = np.sqrt(v_df['v1x']**2 + v_df['v1y']**2 + v_df['v1z']**2)

V = np.mean(v_df['vmag'])

rho_df['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in rho_df['Datetime'].values]
rho_df['Datetime'] = pd.to_datetime(rho_df['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

rho_df = rho_df.set_index('Datetime')

freq = 1/((B_df.index[1] - B_df.index[0]).total_seconds())

lag_arr = np.arange(0, len(B_df)//5, 1)

B_df['B1x_Alfven'] =  B_df['B1x']*1e-9/np.sqrt(mu0*rho_df['Ni']*1e6*mp)*1e-3
B_df['B1y_Alfven'] =  B_df['B1y']*1e-9/np.sqrt(mu0*rho_df['Ni']*1e6*mp)*1e-3
B_df['B1z_Alfven'] =  B_df['B1z']*1e-9/np.sqrt(mu0*rho_df['Ni']*1e6*mp)*1e-3

z_df  = pd.DataFrame(columns = ['Datetime', 'z+_x', 'z+_y', 'z+_z', 'z-_x', 'z-_y', 'z-_z'])

z_df['z+_x'] = v_df['v1x'] + B_df['B1x_Alfven']
z_df['z+_y'] = v_df['v1y'] + B_df['B1y_Alfven']
z_df['z+_z'] = v_df['v1z'] + B_df['B1z_Alfven']
z_df['z-_x'] = v_df['v1x'] - B_df['B1x_Alfven']
z_df['z-_y'] = v_df['v1y'] - B_df['B1y_Alfven']
z_df['z-_z'] = v_df['v1z'] - B_df['B1z_Alfven']


corr_df = pd.DataFrame()

z_df['delta_z+_x'] = z_df['z+_x'] - np.mean(z_df['z+_x'])
z_df['delta_z+_y'] = z_df['z+_y'] - np.mean(z_df['z+_y'])
z_df['delta_z+_z'] = z_df['z+_z'] - np.mean(z_df['z+_z'])

z_df['delta_z-_x'] = z_df['z-_x'] - np.mean(z_df['z-_x'])
z_df['delta_z-_y'] = z_df['z-_y'] - np.mean(z_df['z-_y'])
z_df['delta_z-_z'] = z_df['z-_z'] - np.mean(z_df['z-_z'])

z_df['delta_z+_mag'] = np.sqrt(z_df['delta_z+_x'] ** 2 + z_df['delta_z+_y'] ** 2 + z_df['delta_z+_z'] ** 2)
z_df['delta_z-_mag'] = np.sqrt(z_df['delta_z-_x'] ** 2 + z_df['delta_z-_y'] ** 2 + z_df['delta_z-_z'] ** 2)


corr_df['Lag(s)'] = lag_arr/freq

for var in ['delta_z+', 'delta_z-']:
  for comp in ['_x', '_y', '_z']:
    autocorr(z_df, corr_df, var, comp)
  trace(corr_df, var)
  first_norm(corr_df, var)


#Compute correlation time
tc_index_zplus = np.where(corr_df['delta_z+_tr'] < np.exp(-1))[0][0]
tc_zplus = corr_df['Lag(s)'][tc_index_zplus]

tc_index_zminus = np.where(corr_df['delta_z-_tr'] < np.exp(-1))[0][0]
tc_zminus = corr_df['Lag(s)'][tc_index_zminus]

Lplus = V * tc_zplus
Lminus = V * tc_zminus

Zplus = np.sqrt(np.mean(z_df['delta_z+_mag']**2))
Zminus = np.sqrt(np.mean(z_df['delta_z-_mag']**2))

eps1_plus = compute_e1_plus(Zplus, Zminus, Lplus)
eps1_minus = compute_e1_minus(Zplus, Zminus, Lminus)


#Third-Order Law

#Computing time increments of Z_\pm

lag_arr = np.arange(0, len(B_df)//2 , 1)

dz_df = pd.DataFrame(columns = ['Lag', 'Y+', 'Y-'])

L = len(z_df)

for lag in lag_arr:
  # zplus_x_inc = z_df['delta_z+_x'][lag:].values - z_df['delta_z+_x'][:L-lag].values
  # zplus_y_inc = z_df['delta_z+_y'][lag:].values - z_df['delta_z+_y'][:L-lag].values
  # zplus_z_inc = z_df['delta_z+_x'][lag:].values - z_df['delta_z+_z'][:L-lag].values
  # zminus_x_inc = z_df['delta_z-_x'][lag:].values - z_df['delta_z-_x'][:L-lag].values
  # zminus_y_inc = z_df['delta_z-_y'][lag:].values - z_df['delta_z-_y'][:L-lag].values
  # zminus_z_inc = z_df['delta_z-_z'][lag:].values - z_df['delta_z-_z'][:L-lag].values
  
  zplus_x_inc = z_df['z+_x'][lag:].values - z_df['z+_x'][:L-lag].values
  zplus_y_inc = z_df['z+_y'][lag:].values - z_df['z+_y'][:L-lag].values
  zplus_z_inc = z_df['z+_z'][lag:].values - z_df['z+_z'][:L-lag].values
  zminus_x_inc = z_df['z-_x'][lag:].values - z_df['z-_x'][:L-lag].values
  zminus_y_inc = z_df['z-_y'][lag:].values - z_df['z-_y'][:L-lag].values
  zminus_z_inc = z_df['z-_z'][lag:].values - z_df['z-_z'][:L-lag].values
  
  zplus_inc_mag = np.sqrt(zplus_x_inc ** 2 + zplus_y_inc ** 2 + zplus_z_inc ** 2)
  zminus_inc_mag = np.sqrt(zminus_x_inc ** 2 + zminus_y_inc ** 2 + zminus_z_inc ** 2)
  
  Yplus = np.nanmean(zplus_inc_mag ** 2 * zminus_x_inc)
  Yminus = np.nanmean(zminus_inc_mag ** 2 * zplus_x_inc)
  
  dz_df = dz_df.append({'Lag': lag / freq, 'Y+': Yplus, 'Y-': Yminus}, ignore_index = True)
  
  
#Computing ion inertial length
ni = np.mean(rho_df.values)
di = 2.28*1e7/np.sqrt(ni)*1e-5


cond = dz_df['Lag']!=0
#Plotting Y+ and Y-

ax = plt.gca()


fac = 1.1

lag_left = np.log10(10 * di)
lag_right = np.log10(Lplus)
x = np.logspace(lag_left, lag_right, 50)
y = (x**1)*10
plt.plot(V * dz_df['Lag'], np.abs(dz_df['Y+']))
plt.plot(x, y, '--')
plt.axvline(di, linewidth = 2, color='k')
plt.axvline(10*di, linewidth = 2, color = 'k')
plt.axvline(Lplus, linewidth = 2, color = 'k')
plt.text(di * fac, 15, r'$d_i = $' + str(round(di, 2)) + ' km', fontsize = 25)
plt.text(Lplus * fac, 15, r'$\lambda^+_c = $' + str(round(Lplus, 2)) + ' km', fontsize = 25)
plt.text(10 * di * fac, 15, r'$10d_i$', fontsize =25) 
plt.text(250, 5000, r'$\sim r$', fontsize = 40)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'Spatial lag, $r$(km)', fontsize = 40)
plt.ylabel(r'$Y^+(r) (km^3/s^3)$', fontsize = 40)
plt.xticks(fontsize = 40)
plt.yticks(fontsize = 40)
#plt.legend(fontsize = 40)
plt.grid(True)

# cond = np.logical_and(dz_df['Lag']>1e-2, dz_df['Lag']<1e-1)

# p = np.polyfit(np.log10(dz_df['Lag'][cond]), np.log10(dz_df['Y-'][cond]), 1)
# slope = p[0]


lag_left = np.log10(10 * di)
lag_right = np.log10(Lminus)
x = np.logspace(lag_left, lag_right, 50)
y = (x**1)*13
plt.plot(dz_df['Lag'] * V, np.abs(dz_df['Y-']))
plt.plot(x, y, '--')
plt.axvline(di, linewidth = 2, color='k')
plt.axvline(10*di, linewidth = 2, color = 'k')
plt.axvline(Lminus, linewidth = 2, color = 'k')
plt.text(di * fac, 25, r'$d_i = $' + str(round(di, 2)) + ' km', fontsize = 25)
plt.text(Lminus * fac, 25, r'$\lambda^-_c = $' + str(round(Lminus, 2)) + ' km', fontsize = 25)
plt.text(10 * di * fac, 25, r'$10d_i$', fontsize = 25) 
plt.text(300, 7000, r'$\sim r$', fontsize = 40)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'Spatial lag, $r$(km)', fontsize = 40)
plt.ylabel(r'$Y^-(r) (km^3/s^3)$', fontsize = 40)
plt.xticks(fontsize = 40)
plt.yticks(fontsize = 40)
#plt.legend(fontsize = 40)
plt.grid(True)


#Computing cascade rate from Y+ and Y- using third order law
r = dz_df['Lag'] * V
eps_3ord_plus = - (dz_df['Y+'] / r) * (3/4.0)
eps_3ord_minus = -(dz_df['Y-'] / r) * (3/4.0)
eps_3ord_avg = (eps_3ord_plus + eps_3ord_minus)/2.0

plt.plot(r, np.abs(eps_3ord_avg)*1e6)
cond_eps_avg = np.logical_and(r > 10 * di, r < Lplus)
eps_3ord_plateau = eps_3ord_avg[cond_eps_avg]
eps_3ord_mean = np.mean(np.abs(eps_3ord_plateau))
plt.axvline(10 * di, linewidth = 2, color = 'k')
plt.axvline(Lplus, linewidth = 2, color = 'k')
plt.axvline(Lminus, linewidth = 2, color = 'k')
plt.axhline(eps_3ord_mean * 1e6, linewidth = 2, color = 'r', linestyle = '--')
#plt.axvline(Lminus, linewidth = 2, color = 'k')
plt.text(10 * di * fac, 5500, r'$10d_i$', fontsize  = 25)
plt.text(Lplus * fac, 5500, r'$\lambda^+_c$', fontsize = 25)
plt.text(Lminus / 1.3, 5500, r'$\lambda^-_c$', fontsize = 25)
plt.text(20, eps_3ord_mean * 1e6 * fac, r'$\epsilon$ = ' +'{:.2e}'.format(eps_3ord_mean * 1e6) + ' $ J.kg^{-1}.s^{-1}$', fontsize = 25)
plt.xlabel(r'Spatial lag, $r$(km)', fontsize = 40)
plt.ylabel(r'$\overline{\epsilon} = (\epsilon^+ + \epsilon^-)/2(J.kg^{-1}.s^{-1})$', fontsize = 40)
plt.xscale('log')
plt.yscale('log')
plt.show()