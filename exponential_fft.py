# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 14:46:13 2020

@author: Sohom
"""


import numpy as np
import matplotlib.pyplot as plt

def symmetrize_arr(x):
  l=len(x)
  L=2*(l-1)
  x_symm=[x[np.abs(l-1-i)] for i in range(L)]
  return x_symm

def lorentzian(k,k0):
  return k0/(np.pi*(k**2+k0**2))

k0=0.1
xmin=0

n=16       #Number of e-foldings
xmax=n/(2*np.pi*k0)

N=400

x=np.linspace(xmin,xmax,N)

x_symm=np.linspace(-xmax,xmax,2*(N-1))

step=x_symm[1]-x_symm[0]

y=np.exp(-2*np.pi*k0*x)

y_symm=symmetrize_arr(y)

Fy_symm=np.fft.fft(y_symm)
freq=np.fft.fftfreq(len(y_symm),d=step)

Fy_symm=Fy_symm*lorentzian(0,k0)/Fy_symm[0]

fig,axs=plt.subplots(2)
axs[0].plot(x_symm,y_symm,label='$k_0$ = '+str(k0)+', n = '+str(n)+' e-foldings')
axs[0].set_xlabel('x',fontsize=15)
axs[0].set_ylabel('$y=exp(-2\pi k_0|x|)$',fontsize=15)
axs[0].legend(fontsize=15)
axs[1].plot(freq,np.abs(Fy_symm),'.',label="Fourier transform")
axs[1].plot(freq,lorentzian(freq,k0),label="Lorentzian curve with "+'$k_0$ = '+str(k0))
axs[1].set_xlabel('k',fontsize=15)
axs[1].set_ylabel('$\mathcal{F}(y)$',fontsize=15)
axs[1].legend(fontsize=15)
