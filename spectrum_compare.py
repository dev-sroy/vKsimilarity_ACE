# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 12:02:18 2020

@author: Sohom
"""


from init import *
import scipy.signal as sig
'''
Steps
1. Read correlation tensor, and magnetic fields from file, reshape and slice the arrays appropriately
2. Window the correlation function, using a 10% cosine taper
3. Pad the correlation function with zeros to match the length of the magnetic field array
4. Symmetrize the correlation function
5. Take FFT of the correlation function
6. Take FFT of the magnetic field
7. Compute the spectrum using FFT technique( Fourier components of B)
'''
#Initializing values
L=10000                       #Maximum lag(in seconds)
N=86401                       #Length of magnetic field slice

#Defining functions
def pad(arr,N):
  arr_padded=np.zeros(N)
  for i in range(len(arr)):
    arr_padded[i]=arr[i]
  return arr_padded

def symmetrize(x):
  l=len(x)
  L=2*(l-1)
  x_symm=[x[np.abs(l-1-i)] for i in range(L)]
  return x_symm

def smooth(x,num_iter):
  y=np.zeros(len(x))
  if(num_iter):
    y[0]=x[0]
    y[-1]=x[-1]
    for i in range(1,len(x)-1):
      y[i]=(x[i-1]+x[i]+x[i+1])/3.
    x=y
    return smooth(x,num_iter-1)
  return x


#1. Reading and reshaping correlation tensor, and magnetic fields from file
corr_tensor=np.genfromtxt('correlation_tensor.txt')
jt_arr_mag,br_arr,bt_arr,bn_arr=load_magnetic_field_data()

corr_tensor=corr_tensor[:,3].reshape(3,3,L)

start_dt='11/05/18'
end_dt='11/06/18'

B=np.zeros((3,N))
B[0],tr = slice_arr(br_arr,jt_arr_mag,start_dt,end_dt)  #Array containing the radial magnetic field values in the given date range
B[1],tt = slice_arr(bt_arr,jt_arr_mag,start_dt,end_dt)  #Array containing the tangential magnetic field values in the given date range
B[2],tn = slice_arr(bn_arr,jt_arr_mag,start_dt,end_dt)  #Array containing the normal magnetic field values in the given date range

#2. Windowing the correlation function
cos_taper_window=sig.windows.tukey(L,alpha=0.1,sym=True)
corr_rr=corr_tensor[0,0,:]/corr_tensor[0,0,0]



#3. Padding the correlation function with zeros 
corr_pad=pad(corr_win,N)

#4. Symmetrize the correlation function
corr_symm=symmetrize(corr_pad)
Br_symm=symmetrize(B[0])

#5. Taking FFT of the correlation function
spec=np.fft.fft(symmetrize(corr_win))
freq1=np.fft.fftfreq(len(spec))
spec_bt=np.fft.fft(corr_symm)
spec/=spec[0]
spec_bt/=spec_bt[0]

N_symm=len(spec_bt)
#6. Taking FFT of the magnetic field
FB=np.fft.fft(Br_symm)

freq=np.fft.fftfreq(N_symm,d=1)

#7. Computing spectrum using FFT technique
values={freq[i]:FB[i] for i in range(N_symm)}

S=np.zeros(N_symm)
for i in range(N_symm//2):
  S[i]=np.abs(values[-freq[i]]*values[freq[i]])
  
S/=S[0]

#Smoothing FFT spectrum
num_iter=10
S_smooth=smooth(S,num_iter)

#9. Plotting spectra
plt.plot(freq[:N_symm//2],np.abs(spec_bt[:N_symm//2]))
plt.plot(freq[:N_symm//2],np.abs(S_smooth[:N_symm//2]))
plt.xscale('log')
plt.yscale('log')
