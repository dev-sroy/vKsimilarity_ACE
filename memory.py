# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 09:20:57 2020

@author: Sohom
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N=10000

#Generate N uncorrelated random numbers with 0 mean and unit variance

r=np.random.normal(0,1,N)

def next_val(x,m,r,n):
    x[n+1]=m*x[n]+np.sqrt(1-m**2)*r[n+1]
    
def corr_func(arr1,arr2,lag):
    data1=pd.Series(arr1[0:-lag-1])
    data2=pd.Series(arr2[lag:-1])
    mean1=data1.mean()
    mean2=data2.mean()
    delta1=data1-mean1
    delta2=data2-mean2
    corr=(data1*data2).mean()-mean1*mean2
    #corr=(delta1*delta2).mean()
    return corr

plt.figure(figsize=(20,12))
plt.xlabel('Lag,'+'$\\tau$'+'(in s)',fontsize=20)
plt.ylabel('Correlation, $R(\\tau)$', fontsize=20)

for m in np.linspace(0.9,1,5):

    x=np.zeros(N)
    corr_arr=np.zeros(1000)
    
    for i in range(N-1):
        next_val(x,m,r,i)
        
    
    for lag in range(1000):
        corr_arr[lag]=corr_func(x,x,lag)
        
    corr_arr/=corr_arr[0]
        
    tc=np.abs(corr_arr-1/np.exp(1)).argmin()
    
    
    plt.plot(corr_arr,linewidth=2.0,label='$\\tau_c$ = '+str(tc)+', m = '+str(m))
    
    #plt.axvline(tc,0,1,color='k',linewidth=2.0)
    plt.plot(tc,corr_arr[tc],'r.',markersize=12)
    #plt.text(tc,corr_arr[tc],'('+str(tc)+', '+format(corr_arr[tc],'.2f')+')',fontsize=20)

plt.legend(fontsize=20)
plt.show()
