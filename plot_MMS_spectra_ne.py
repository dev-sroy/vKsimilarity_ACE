# -*- coding: utf-8 -*-
"""
Created on Sat May 22 10:21:52 2021

@author: Sohom
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def symmetrize(x):
  l=len(x)
  L=2*(l-1)
  x_symm=[x[np.abs(l-1-i)] for i in range(L)]
  return x_symm

def smooth(x,num_iter):
  y=np.zeros(len(x))
  if(num_iter):
    y[0]=x[0]
    y[-1]=x[-1]
    for i in range(1,len(x)-1):
      y[i]=(x[i-1]+x[i]+x[i+1])/3.
    x=y
    return smooth(x,num_iter-1)
  return x

def ref_line(m,b,freq):
  x=np.linspace(freq[0],freq[-1],100)
  y=m*np.log10(x)+b
  plt.plot(x,10**y,'--k',label="Reference line of slope = "+str(m))

plt.rcParams['axes.grid'] = True
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20

electrondir = r'/home/sohom/MMS/MMS_DATA/ascii/20160124/233614/electrons'

df1 = pd.read_csv(os.path.join(electrondir, r'Ne_1_resNe_1.dat'), delim_whitespace = True, names = ['Datetime', 'ne'])

df1['Datetime'] = [datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S:%f') for date in df1['Datetime'].values]
df1['Datetime'] = pd.to_datetime(df1['Datetime'], format =  ('%Y-%m-%d %H:%M:%S:%f'))

df1 = df1.set_index('Datetime')

#df1['vmag'] = np.sqrt(df1['v1x']**2 + df1['v1y']**2 + df1['v1z']**2)

#Symmetrize magnitude of magnetic field
#vs = df1['vmag'].dropna()

N = len(df1)

#Compute FFT
FB = np.fft.fft(df1['ne'].values)

#Compute spectrum


dt = df1.index[1]-df1.index[0]
freq = np.fft.fftfreq(N, d = dt.total_seconds())
values = {freq[i]:FB[i] for i in range(N)}
S=np.zeros(N)
for i in range(N//2):
  S[i]=np.abs(values[-freq[i]]*values[freq[i]])



num_iter=10
S_smooth=smooth(S,num_iter)
plt.plot(freq[:N//2], S_smooth[:N//2])
#ref_line(-5/3.0, -4.5,np.logspace(-1,0,100))
#ref_line(-8/3.0, -4.5, np.logspace(0.2,1.2,100))
#plt.text(10**-0.5,10**-3.7, r'$f^{-5/3}$', fontsize = 20)
#plt.text(10**0.7,10**-6.4,r'$f^{-8/3}$', fontsize = 20)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'Frequency, $f$(Hz)', fontsize = 20)
plt.ylabel(r'$P(f)\quad(m^2s^{-2}/Hz)$', fontsize = 20)
interval_str = df1.index[0].strftime('%Y-%m-%d %H:%M:%S') + '  -  ' + df1.index[-1].strftime('%Y-%m-%d %H:%M:%S')
plt.suptitle(interval_str, fontsize = 30)

