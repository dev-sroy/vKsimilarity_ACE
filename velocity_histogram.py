# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 14:46:14 2020

@author: Sohom
"""

import numpy as np
import matplotlib.pyplot as plt
from spacepy import pycdf
import os
dir=r'C:\Users\Sohom Roy\Desktop\Research\ACE data\Velocity data'
filelist=os.listdir(dir)
v_avg=np.zeros(len(filelist))
for i in range(len(filelist)):
  fname=os.path.join(dir,filelist[i])
  cdf=pycdf.CDF(fname)
  v_arr=cdf['V_RTN'][...]
  v_mag=[np.linalg.norm(v_arr[j]) for j in range(24)]
  v_avg[i]=np.mean(v_mag)

plt.hist(v_avg[v_avg!=np.inf],color='b',bins=200)
plt.xlabel('Velocity(in km/s)')
plt.ylabel('Counts')
plt.grid(True)