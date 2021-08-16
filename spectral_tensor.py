# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:32:58 2020

@author: Sohom
"""

import numpy as np
import matplotlib.pyplot as plt

def symmetrize_arr(x):
  l=len(x)
  L=2*(l-1)
  x_symm=[x[np.abs(l-1-i)] for i in range(L)]
  return x_symm
  
N=10000
N_symm_max=86401
Nmax=2*(N_symm_max-1)
N_symm=2*(N-1)



corr_arr=np.genfromtxt('correlation_tensor.txt')

corr_tensor=corr_arr[:,3].reshape(3,3,N)
'''
#Normalizing the correlation tensor
for i in range(3):
  for j in range(3):
    corr_tensor[i,j]/=corr_tensor[i,j,0]

'''
#Padding zeros to the correlation tensor
corr_tensor_padded=np.zeros((3,3,N_symm_max))

for i in range(3):
  for j in range(3):
    for k in range(N):
      corr_tensor_padded[i,j,k]=corr_tensor[i,j,k]


#Symmetrizing the correlation tensor
corr_tensor_symm=np.zeros((3,3,Nmax))

for i in range(3):
  for j in range(3):
    corr_tensor_symm[i,j]=symmetrize_arr(corr_tensor_padded[i,j])


#Computing the spectral tensor

S=np.zeros((3,3,Nmax),dtype=complex)

freq=np.fft.fftfreq(Nmax,d=1)
logfreq=np.log10(freq)

f=open('Spec_Blackman_Tukey.txt','w')
for i in range(3):
  for j in range(3):
    S[i,j]=np.fft.fft(corr_tensor_symm[i,j,:])
    for k in range(Nmax):
      f.write(str(i)+' '+str(j)+' '+str(S[i,j,k])+'\n')
      
f.close()

freq=np.fft.fftfreq(Nmax,d=1)
logfreq=np.log10(freq)

logS=np.log10(np.abs(S))

logfreq_fit=logfreq[150:3000]
logS_fit=logS[0,0,150:3000]

m,b=np.polyfit(logfreq_fit,logS_fit,1)
'''
plt.figure(figsize=(20,12))
plt.plot(logfreq[:N//2],logS[0,0,:N//2],'-', label='Spectrum')
plt.plot(logfreq[:N//2],m*logfreq[:N//2]+b, label='Slope = '+format(m,'.2f')+', Intercept = '+format(b,'.2f'))
plt.xlabel('Log Frequency(in Hz)',fontsize=20)
plt.ylabel('$log(S_{00})$',fontsize=20)
plt.legend(fontsize=20)

plt.show()
'''
arr=np.genfromtxt('spectral_tensor.txt')

#plt.plot(np.log10(arr[0:43200,3]),np.log10(arr[0:43200,4]))

t_arr=np.arange(-Nmax/2,Nmax/2,1)

fs=15

fig,axs=plt.subplots(2)
axs[0].plot(t_arr,corr_tensor_symm[0,0,:])
axs[0].set_title('Symmetrized auto-correlation function of $B_{r}$',fontsize=fs)
axs[0].set_xlabel('Lag,$\\tau$(in s)',fontsize=fs)
axs[0].set_ylabel('$R_{rr}(\\tau)$',fontsize=fs)
axs[0].grid(True)
axs[1].plot(freq[:Nmax//2],np.abs(S[0,0,:Nmax//2]),'-', label='Spectrum of $R_{rr}(\\tau)$')
axs[1].plot(freq[:Nmax//2],10**(m*logfreq[:Nmax//2]+b), label='Slope = '+format(m,'.2f')+', Intercept = '+format(b,'.2f'))
axs[1].set_xscale('log')
axs[1].set_yscale('log')
axs[1].set_xlabel('Frequency(in Hz)',fontsize=fs)
axs[1].set_ylabel('$S_{rr}$',fontsize=fs)
axs[1].grid(True)
axs[1].legend(fontsize=fs)

