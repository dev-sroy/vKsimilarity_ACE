# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:18:33 2020

@author: Sohom
"""

import numpy as np
import matplotlib.pyplot as plt

data=np.genfromtxt(r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor\ACE_corr_trace_19980208.txt")

plt.plot(data[:,0],data[:,1])
plt.grid(True)
plt.ylabel('R(r)',fontsize=15)
plt.xlabel('Spatial lag, r(in km)', fontsize=15)