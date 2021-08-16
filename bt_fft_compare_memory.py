# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 03:11:36 2020

@author: Sohom
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N=10000

#Generate N uncorrelated random numbers with 0 mean and unit variance

r=np.random.normal(0,1,N)
m=0.9

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
  
def symmetrize_arr(x):
  l=len(x)
  L=2*(l-1)
  x_symm=[x[np.abs(l-1-i)] for i in range(L)]
  return x_symm

def pad(arr,N):
  arr_padded=np.zeros(N)
  for i in range(len(arr)):
    arr_padded[i]=arr[i]
  return arr_padded

def smooth(x,num_iter):
  y=np.zeros(len(x))
  if(num_iter!=0):
    print(num_iter)
    y[0]=x[0]
    y[-1]=x[-1]
    for i in range(1,len(x)-1):
      y[i]=(x[i-1]+x[i]+x[i+1])/3.
    x=y
    print(y)
    return smooth(x,num_iter-1)
  return x

   
x=np.zeros(N)
corr_arr=np.zeros(1000)

for i in range(N-1):
    next_val(x,m,r,i)
    

for lag in range(1000):
    corr_arr[lag]=corr_func(x,x,lag)
    
corr_arr/=corr_arr[0]

#Computing the spectrum

corr_pad=pad(corr_arr,len(x))

#Symmetrizing the correlation function
corr_arr_symm=symmetrize_arr(corr_pad)
x_symm=symmetrize_arr(x)

S_BT=np.fft.fft(corr_arr_symm)
freq=np.fft.fftfreq(len(x_symm))
Fx=np.fft.fft(x_symm)

values={freq[i]:Fx[i] for i in range(len(x_symm))}
S=np.zeros(len(freq))

for k in range(len(freq)//2):                 #Range has been halved to avoid f=0.5 error  
      S[k]=np.abs(values[-freq[k]]*values[freq[k]])

num_iter=10

S_smooth=smooth(S,num_iter)
S_smooth/=S_smooth[0]
S_BT/=S_BT[0]
S/=S[0]

#plt.plot(freq[:N//2],np.abs(S[:N//2]),"gray", alpha=0.5, label='Original')
plt.plot(freq[:N//2],np.abs(S_BT[:N//2]),"black",alpha=0.5,label='Blackman-Tukey')
plt.plot(freq[:N//2],np.abs(S_smooth[:N//2]),"blue", label='Smoothed FFT spectrum')
plt.grid(True)
plt.yscale('log')
plt.xscale('log')     
plt.xlabel('Frequency(in Hz)',fontsize=15)
plt.ylabel('Spectrum',fontsize=15)
plt.legend(fontsize=20)
plt.show()
