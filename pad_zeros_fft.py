# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 02:48:31 2020

@author: Sohom
"""


import numpy as np
import matplotlib.pyplot as plt

N=1000
Nmax=8000

freq=2

x=np.linspace(1,10,N)

y=np.sin(2*np.pi*freq*x)

Fy=np.fft.fft(y,Nmax)

dt=x[1]-x[0]
T=dt*N

f=np.fft.fftfreq(Nmax,d=dt)

plt.plot(f[0:Nmax//2],np.abs(Fy[0:Nmax//2]))

y_padded=np.zeros(Nmax)

for i in range(N):
  l=(Nmax-N)//2
  y_padded[l+i]=y[i]
  
Fy_padded=np.fft.fft(y_padded)

def symmetrize_arr(x):
  l=len(x)
  L=2*(l-1)
  x_symm=[x[np.abs(l-1-i)] for i in range(L)]
  return x_symm

