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
N=86401                      #Length of magnetic field slice

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
  x_symm=np.array(x_symm)
  return x_symm

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

def ref_line(m,b,freq):
  x=np.linspace(freq[0],freq[-1],100)
  y=m*np.log10(x)+b
  plt.plot(x,10**y,'--k',label="Reference line of slope = "+str(m))


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
corr_win=corr_rr*cos_taper_window

#3. Padding the correlation function with zeros 
corr_pad=pad(corr_win,N//2)

#4. Symmetrize the correlation function
corr_symm=symmetrize(corr_pad)
#B_symm=[symmetrize(B[i]) for i in range(3)]
B_symm=np.copy(B)

#5. Taking FFT of the correlation function
spec=np.fft.fft(symmetrize(corr_win))
freq=np.fft.fftfreq(len(spec))
spec_bt=np.fft.fft(corr_symm)
spec/=spec[0]
spec_bt/=spec_bt[0]

N_symm=len(spec_bt)
#6. Taking FFT of the magnetic field
FB=np.fft.fft(B_symm)

freq=np.fft.fftfreq(N_symm,d=1)

#7. Computing spectrum using FFT technique

S=np.zeros((3,3,N_symm))

values={freq[i]:FB[:,i] for i in range(N_symm)}

f=open('spectral_tensor.txt','w')

for i in range(3):
  for j in range(3):
    for k in range(len(freq)//2):      
      S[i,j,k]=np.abs(values[-freq[k]][i])*np.abs(values[freq[k]][j])
      f.write(str(i)+' '+str(j)+' '+str(k)+' '+str(freq[k])+' '+str(S[i,j,k])+'\n')

f.close()
S_trace=S[0,0,:]+S[1,1,:]+S[2,2,:]
#Smoothing the Spectrum

num_iter=10
S_smooth=smooth(S_trace[1:],num_iter)
S_smooth/=S_smooth.max()
#9. Plotting spectra
plt.plot(freq[:N_symm//2],np.abs(spec_bt[:N_symm//2]),label='Blackman-Tukey')
plt.plot(freq[:N_symm//2:],np.abs(S_smooth[:N_symm//2]),alpha=0.5,label='Smoothed FFT')
ref_line(-1.5,-5,freq[:N_symm//2])
plt.xscale('log')
plt.yscale('log')
plt.title('Comparison of FFT spectra and Blackman-Tukey spectrum',fontsize=20)
plt.xlabel('Frequency',fontsize=20)
plt.ylabel('Spectrum', fontsize=20)
plt.legend(fontsize=20)
plt.grid(True)

corr_rr=corr_tensor[0,0,:]
corr_tt=corr_tensor[1,1,:]
corr_nn=corr_tensor[2,2,:]

#Performing the above correlations using the trace
'''
N_symm=86401
acorr=corr_rr+corr_tt+corr_nn
corr_symm=symmetrize_arr(acorr)
cos_taper_window=sig.windows.tukey(len(corr_symm),alpha=0.1,sym=True)
corr_win=corr_symm*cos_taper_window
l=len(corr_symm)
corr_pad=np.zeros(N_symm)
for i in range(l):
  corr_pad[N_symm//2-l//2+i]=corr_win[i]
  
spec_bt=np.fft.fft(corr_pad)
spec_bt/=spec_bt[0]

freq=np.fft.fftfreq(N_symm,d=1)

S=np.zeros((3,3,N_symm),dtype=complex)

f=open('spectral_tensor.txt','w')

for i in range(3):
  for j in range(3):
    for k in range(len(freq)):
      S[i,j,k]=FB[i][-k]*FB[j][k]
      f.write(str(i)+' '+str(j)+' '+str(k)+' '+str(freq[k])+' '+str(S[i,j,k])+'\n')

f.close()
S_trace=S[0,0,:]+S[1,1,:]+S[2,2,:]
#Smoothing the Spectrum

num_iter=10
S_smooth=np.zeros(N_symm,dtype=complex)
S_smooth[0]=1
S_smooth[1:]=smooth(S_trace[1:],num_iter)
S_smooth/=S_smooth.max()
'''


