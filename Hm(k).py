# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 14:12:28 2020

@author: Sohom
"""


from init import *

N=86401

def E(i,j,k):
  if i==j or i==k or j==k:
    return 0
  if (i<j and j<k) or (j<k and k<i) or (k<i and i<j):
    return 1
  else:
    return -1

e=np.zeros((3,3,3))
for i in range(3):
  for j in range(3):
    for k in range(3):
      e[i,j,k]=E(i,j,k)

def smooth(x,num_iter):
  y=np.zeros(len(x),dtype=complex)
  if(num_iter):
    y[0]=x[0]
    y[-1]=x[-1]
    for i in range(1,len(x)-1):
      y[i]=(x[i-1]+x[i]+x[i+1])/3.
    x=y
    return smooth(x,num_iter-1)
  return x

data=np.genfromtxt('spectral_tensor.txt',dtype=complex)

jt_arr,vr_arr,vt_arr,vn_arr=load_velocity_data()

start_dt='11/05/18'
end_dt='11/06/18'

v=np.zeros((3,N))

v[0],vtr = slice_arr(vr_arr,jt_arr,start_dt,end_dt)  #Array containing the radial velocity values in the given date range
v[1],vtt = slice_arr(vt_arr,jt_arr,start_dt,end_dt)  #Array containing the tangential velocity values in the given date range
v[2],vtn = slice_arr(vn_arr,jt_arr,start_dt,end_dt)  #Array containing the normal velocity values in the given date range

S=data[:,4].reshape(3,3,N)
S[1,2]/=S[1,2,0]


freq=np.fft.fftfreq(N,d=1)
freq=freq[1:]

#k1=2*np.pi*freq/v[0]

num_iter=10
S_smooth=smooth(S[1,2,1:],num_iter)

Hm_r=np.zeros(len(S[1,2]-1))
Hm_r=2*S_smooth.imag/freq
Hm=Hm_r[Hm_r>0]
pfreq=freq[Hm_r>0]

#Sorting the frequencies and magnetic helicity spectra properly
values={pfreq[i]:Hm[i] for i in range(len(pfreq))}
items=values.items()
s=np.array(sorted(items))

plt.plot(s[:,0],s[:,1])
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.xlabel('Frequency, f(in Hz)',fontsize=20)
plt.ylabel('$H_m(f)$',fontsize=20)
plt.show()



