# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import os
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from spacepy import pycdf

dir=r'C:\Users\Sohom Roy\Desktop\Research\ACE data\Velocity data'
filelist=os.listdir(dir)
v_avg=np.zeros(len(filelist))
for i in range(len(filelist)):
  fname=os.path.join(dir,filelist[i])
  cdf=pycdf.CDF(fname)
  v_arr=cdf['V_RTN'][...]
  v_mag=[np.linalg.norm(v_arr[j]) for j in range(24)]
  v_avg[i]=np.mean(v_mag)


stat_df=pd.read_csv(r"C:\Users\Sohom Roy\Desktop\Research\Statistical weight.txt",sep=" ",header=None)
stat_df[1]/=1441

#Initialisations
date_len=[]
R=[]
size=1000
corr_arr=np.empty(len(stat_df),dtype=object)
corr_arr_new=np.zeros((len(stat_df),2,480))
corr_arr2_new=np.zeros((len(stat_df),2,size))
corr_mean=np.zeros(480)
corr_mean2=np.zeros(size)
corr_mean_fast=np.zeros(size)
corr_arr_fast=np.empty(987,dtype=object)
corr_arr2_fast=np.zeros((len(corr_arr_fast),2,size))
corr_len=np.zeros(len(corr_arr))
corr_len_fast=np.zeros(len(corr_arr_fast))
lag=np.logspace(0,7.4,480)

lag_new=np.zeros((len(corr_arr),480))
lag_new_fast=np.zeros((len(corr_arr_fast),480))
lag2=np.linspace(0,70,size)
stdev_arr=np.zeros(size)
stdev_arr_fast=np.zeros(size)
for i in range(len(stat_df)):
  if(stat_df[1][i]<=0.3):
      date=stat_df[0][i]
      date=date[0:4]+date[5:7]+date[8:10]
      fname=r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor\ACE_corr_trace_"+date+".txt"
      corr_arr[i]=pd.read_csv(fname,sep=" ",header=None)
      f=interp1d(corr_arr[i][0],corr_arr[i][1],bounds_error=False)
      corr_arr_new[i,0]=lag
      corr_arr_new[i,1]=f(lag)
      print(date)

for i in range(480):
  corr_mean[i]=np.nanmean(corr_arr_new[:,1,i])

# corr_per_min=np.zeros(480)
# corr_per_max=np.zeros(480)
# for i in range(480):
#     corr_per_min[i]=np.percentile(corr_arr_new[:,1,i],10)
#     corr_per_max[i]=np.percentile(corr_arr_new[:,1,i],90)

#Compute correlation length

for i in range(len(corr_arr)):
  if corr_arr[i] is not None:
    tc=np.where(corr_arr[i][1]<np.exp(-1))[0][0]
    if np.isnan(corr_arr[i][1][:tc]).sum()==0 and np.isinf(corr_arr[i][0][:tc]).sum()==0:
      log_corr=np.log(corr_arr[i][1][:tc])
      p=np.polyfit(corr_arr[i][0][:tc],log_corr,1)
      corr_len[i]=-1/p[0]


for i in range(len(lag_new)):
  if corr_arr[i] is not None:
    lag_new[i]=corr_arr[i][0]/corr_len[i]



for i in range(len(stat_df)):
  if(stat_df[1][i]<=0.3):
      f=interp1d(lag_new[i],corr_arr[i][1],bounds_error=False)
      corr_arr2_new[i,0]=lag2
      corr_arr2_new[i,1]=f(lag2)

for i in range(480):
  corr_mean2[i]=np.nanmean(corr_arr2_new[:,1,i])


for i in range(480):
  stdev_arr[i]=np.nanstd(corr_arr2_new[:,1,i])


j=0
for i in range(len(stat_df)):
  if(stat_df[1][i]<=0.3 and v_avg[i]>=500 and v_avg[i]!=np.inf):
    corr_arr_fast[j]=corr_arr[i].copy(deep=True)
    j+=1


#Computing correlation length for fast solar wind

for i in range(len(corr_arr_fast)):
  tc=np.where(corr_arr_fast[i][1]<np.exp(-1))[0][0]//2
  log_corr_fast=np.log(corr_arr_fast[i][1][:tc])
  p=np.polyfit(corr_arr_fast[i][0][:tc],log_corr_fast,1)
  corr_len_fast[i]=-1/p[0]

corr_len_fast_avg=np.nanmean(corr_len_fast)
for i in range(len(lag_new_fast)):
  lag_new_fast[i]=corr_arr_fast[i][0]/corr_len_fast[i]
#Fast solar wind
for i in range(len(corr_arr_fast)):
  f=interp1d(lag_new_fast[i],corr_arr_fast[i][1],bounds_error=False)
  corr_arr2_fast[i,0]=lag2
  corr_arr2_fast[i,1]=f(lag2)

for i in range(size):
  corr_mean_fast[i]=np.nanmean(corr_arr2_fast[:,1,i])
  
for i in range(size):
  stdev_arr_fast[i]=np.nanstd(corr_arr2_fast[:,1,i])

cond3=lag2<=10.03

for i in range(len(corr_arr_fast)):
  cond2=lag_new_fast[i]<10
  plt.plot(lag_new_fast[i][cond2],corr_arr_fast[i][1][cond2],'peru',alpha=0.2)
#plt.xlim(0,lag2[-1])  
plt.plot(lag2[cond3],corr_mean_fast[cond3],'k',linewidth=2.0,label='Mean',zorder=25)
y1=corr_mean_fast-stdev_arr_fast
y2=corr_mean_fast+stdev_arr_fast
y3=corr_mean_fast-2*stdev_arr_fast
y4=corr_mean_fast+2*stdev_arr_fast
#plt.plot(lag2,corr_mean_fast+stdev_arr_fast,'r--',linewidth=2.0,label='1 standard deviation')
#plt.plot(lag2,corr_mean_fast-stdev_arr_fast,'r--',linewidth=2.0)
#plt.plot(lag2,corr_mean_fast+2*stdev_arr_fast,'b--',linewidth=2.0,label='2 standard deviations')
#plt.plot(lag2,corr_mean_fast-2*stdev_arr_fast,'b--',linewidth=2.0)
plt.fill_between(lag2[cond3],y1[cond3],y2[cond3],color='blue',alpha=0.5,label='1 standard deviation',zorder=10)
plt.fill_between(lag2[cond3],y3[cond3],y4[cond3],color='dodgerblue',alpha=0.5, label='2 standard deviations',zorder=20)
plt.xlabel(r'Spatial lag,$\frac{r}{\lambda}$',fontsize=20)
plt.ylabel(r'R$\left(\frac{r}{\lambda}\right)$',fontsize=20)
plt.legend(fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid(True)


sf2_arr_fast=2-2*corr_arr2_fast
sf2_mean_fast=np.zeros(size)
sf2_std_fast=np.zeros(size)
sf_arr_fast=2-2*corr_arr_fast
for i in range(size):
  sf2_mean_fast[i]=np.nanmean(sf2_arr_fast[:,1,i])
for i in range(size):
  sf2_std_fast[i]=np.nanstd(sf2_arr_fast[:,1,i])
  
cond=np.logical_and(sf2_mean_fast<1,sf2_mean_fast!=0)
p=np.polyfit(np.log10(lag2[cond]),np.log10(sf2_mean_fast[cond]),1)


for i in range(len(sf2_arr_fast)):
  cond2=np.logical_and(lag_new_fast[i]<=10.03,lag_new_fast[i]>7e-2)
  #cond2=lag_new_fast[i]<=10.03
  plt.plot(lag_new_fast[i][cond2],sf_arr_fast[i][1][cond2],'peru',alpha=0.2)


cond3=np.logical_and(lag2<=10.03,lag2>0)
#cond3=lag2<=10.03
plt.xlim(lag2[1],1)
plt.plot(lag2[cond3],sf2_mean_fast[cond3],'k',label='Mean, slope='+str(round(p[0],2)),zorder=25)
#plt.plot(lag2[cond3],sf2_mean_fast[cond3],'k',label='Mean',zorder=25)
y1=sf2_mean_fast-sf2_std_fast
y2=sf2_mean_fast+sf2_std_fast
y3=sf2_mean_fast-2*sf2_std_fast
y4=sf2_mean_fast+2*sf2_std_fast
#plt.plot(lag2,sf2_mean_fast+sf2_std_fast,'r--')
#plt.plot(lag2,sf2_mean_fast-sf2_std_fast,'r--')
#plt.plot(lag2,sf2_mean_fast+2*sf2_std_fast,'b--')
#plt.plot(lag2,sf2_mean_fast-2*sf2_std_fast,'b--')
plt.fill_between(lag2[cond3],y1[cond3],y2[cond3],color='blue',alpha=0.5,label='1 standard deviation',zorder=10)
plt.fill_between(lag2[cond3],y3[cond3],y4[cond3],color='dodgerblue',alpha=0.5,label='2 standard deviations',zorder=10)
x=np.logspace(-1.15,-0.2,50)
y=(x**(2/3.))*4
plt.plot(x,y,'r--',label='Slope=2/3='+str(round(2/3.,2)))
plt.xscale('log')
plt.yscale('log')
plt.xticks(fontsize=40)
plt.yticks(fontsize=40)
plt.legend(fontsize=40)
plt.xlabel(r'Spatial lag, $r/\lambda$',fontsize=40)
plt.ylabel(r'$\hat{S}^{(2)}\left(r/\lambda\right)$',fontsize=40)
plt.grid(True)






#Plotting the entire dataset, irrespective of velocity
#plt.xlim(0,lag2[-1])  
#for i in range(len(stat_df)):
#  if corr_arr[i] is not None:
#    plt.plot(lag_new[i],corr_arr[i][1],'gray',alpha=0.5)
#plt.plot(lag2,corr_mean2,'k',linewidth=2.0,label='Mean')
#plt.plot(lag2,corr_mean2+stdev_arr,'r--',linewidth=2.0,label='1 standard deviation')
#plt.plot(lag2,corr_mean2-stdev_arr,'r--',linewidth=2.0)
#plt.plot(lag2,corr_mean2+2*stdev_arr,'b--',linewidth=2.0,label='2 standard deviations')
#plt.plot(lag2,corr_mean2-2*stdev_arr,'b--',linewidth=2.0)
#plt.xlabel('Lag(in km),r',fontsize=15)
#plt.ylabel('R(r)',fontsize=15)
#plt.legend(fontsize=15)
#plt.grid(True)



