# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 14:11:43 2020

@author: Sohom
"""


import numpy as np
import matplotlib.pyplot as plt

f=np.genfromtxt('correlation.txt')


plt.figure(figsize=(20,12))
plt.plot(f[:,0],f[:,1],'k',label='explicitly computing delta')
plt.plot(f[:,0],f[:,2],'b',label='implicitly computing delta')
plt.xlabel('Lag(in s)',fontsize=20)
plt.ylabel('$\\frac{R(\\tau)}{R(0)}$',fontsize=30)
plt.legend()
plt.show()
