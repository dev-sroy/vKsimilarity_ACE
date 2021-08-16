# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 17:12:03 2020

@author: Sohom
"""


import numpy as np
import matplotlib.pyplot as plt
import os

corr_func_arr=np.zeros((3682,2,480))
corr_mean=np.zeros(480)
corr_std=np.zeros(480)

dir=r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor"
for i in range(len(os.listdir(dir))):
  fname=os.listdir(dir)[i]
  full_fname=os.path.join(dir,fname)
  corr_func_arr[i,0],corr_func_arr[i,1]=np.genfromtxt(full_fname,unpack=True)
  print(i)
  
for i in range(480):
  corr_mean[i]=corr_func_arr[:,1,i].mean()
  corr_std[i]=np.std(corr_func_arr[:,1,i])
  