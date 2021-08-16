# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 15:29:49 2020

@author: Sohom
"""


from init import *

def smoothing(x):
  y=np.zeros(len(x))
  y[0]=x[0]
  y[-1]=x[-1]
  for i in range(1,len(x)-1):
    y[i]=(x[i-1]+x[i]+x[i+1])/3.
    
  return y

def symmetrize_arr(x):
  l=len(x)
  L=2*(l-1)
  x_symm=[x[np.abs(l-1-i)] for i in range(L)]
  return x_symm

jt_arr_mag,br_arr,bt_arr,bn_arr=load_magnetic_field_data()

start_dt='11/05/18'
end_dt='11/06/18'

N=86401
N_symm=2*(N-1)

b1=np.zeros((3,N))
b1[0],tr = slice_arr(br_arr,jt_arr_mag,start_dt,end_dt)  #Array containing the radial magnetic field values in the given date range
b1[1],tt = slice_arr(bt_arr,jt_arr_mag,start_dt,end_dt)  #Array containing the tangential magnetic field values in the given date range
b1[2],tn = slice_arr(bn_arr,jt_arr_mag,start_dt,end_dt)  #Array containing the normal magnetic field values in the given date range

#Computing the Fourier transforms

b1_symm=np.zeros((3,N_symm))

for i in range(3):
  b1_symm[i]=symmetrize_arr(b1[i])

fb1=np.fft.fft(b1_symm)

freq1=np.fft.fftfreq(N_symm,d=1)

#Computing the spectrum

S=np.zeros((3,3,N_symm))

values={freq1[i]:fb1[:,i] for i in range(N_symm)}
f=open('spectral_tensor.txt','w')

for i in range(3):
  for j in range(3):
    for k in range(len(freq1)//2):      
      S[i,j,k]=np.abs(values[-freq1[k]][i])*np.abs(values[freq1[k]][j])
      f.write(str(i)+' '+str(j)+' '+str(k)+' '+str(freq1[k])+' '+str(S[i,j,k])+'\n')

f.close()

S[0,0,:]/=S[0,0,1]
#Smoothing the Spectrum

num_iter=5

S_smooth=np.copy(S)

for i in range(3):
  for j in range(3):
    for n in range(num_iter):
      S_smooth[i,j,1:]=smoothing(S_smooth[i,j,1:])
    print(i,j,n)
    
dt=1
T=dt*N_symm
df=1/T
dw=2*np.pi/T

freq=freq1*N_symm*df
omega=freq1*N_symm*dw

f=np.genfromtxt('Spec_Blackman_Tukey.txt',dtype=complex)

S_BT=f[:,2].reshape(3,3,N_symm)
S_BT[0,0,:]/=S_BT[0,0,0]

logomega_fit=np.log10(omega[150:3000])
logS_smooth_fit=np.log10(S_smooth[0,0,150:3000])
logS_BT_fit=np.log10(np.abs(S_BT[0,0,150:3000]))

m1,b1=np.polyfit(logomega_fit,logS_smooth_fit,1)
m2,b2=np.polyfit(logomega_fit,logS_BT_fit,1)

#plt.plot(omega[:N_symm//2],np.abs(S[0,0,:N_symm//2]),"gray", alpha=0.5, label='Original')
plt.plot(omega[:N_symm//2],np.abs(S_BT[0,0,:N_symm//2]),"black",alpha=0.5,label='Blackman-Tukey')
plt.plot(omega[:N_symm//2],S_smooth[0,0,:N_symm//2],"blue", label='Smoothed FFT spectrum')

plt.plot(omega[:N_symm//2],10**(m1*np.log10(omega[:N_symm//2])+b1),'-k', label='Smoothed spectrum slope = '+format(m1,'.2f')+', Intercept = '+format(b1,'.2f'))
plt.plot(omega[:N_symm//2],10**(m2*np.log10(omega[:N_symm//2])+b2),'--k', label='Blackman-Tukey slope = '+format(m2,'.2f')+', Intercept = '+format(b2,'.2f'))
plt.grid(True)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Angular frequency, $\omega$',fontsize=20)
plt.ylabel('$S_{00}(\omega)$',fontsize=20)   
plt.legend(fontsize=20)             