# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 14:20:27 2020

@author: Sohom
"""


import numpy as np
import matplotlib.pyplot as plt
import datetime as datetime

def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')

dt=datetime.date(1998,2,7)
dts=convert_date(dt)

fname=r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Correlation tensor\ACE_corr_tensor_"+dts+".txt"

corr_tensor=np.genfromtxt(fname,usecols=3)

corr_tensor=corr_tensor.reshape((3,3,144))

corr_trace=(corr_tensor[0,0]+corr_tensor[1,1]+corr_tensor[2,2])/3.0
corr_trace/=corr_trace[0]

plt.plot(corr_trace)
plt.xlabel(r'Lag, $\tau$(in minutes)',fontsize=15)
plt.ylabel(r'R($\tau$)',fontsize=15)
plt.grid(True)
plt.show()
