# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 00:06:11 2020

@author: Sohom
"""


from spacepy import pycdf
import pandas as pd
import numpy as np
from init import *
from scipy import signal
import os

def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')
  
start_dt='02/05/1998'
end_dt='03/30/2008'

dr=pd.date_range(start_dt,end_dt,freq='D')
#dts=convert_date(dr)
dts=['20000316']
detrend=True

v_mag=np.zeros(len(dts))

filelist=os.listdir(r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Velocity data\\")

stat_df=pd.read_csv(r"C:\Users\Sohom Roy\Desktop\Research\Statistical weight.txt",sep=" ",header=None)
stat_df[1]/=1441

for r in range(len(dts)):
  if stat_df[1][r]<=0.30:
    
    v_fname=r'C:\Users\Sohom Roy\Desktop\Research\ACE data\Velocity data\\'+filelist[r]
    v_cdf=pycdf.CDF(v_fname)
    v_arr=v_cdf['V_RTN'][...]
    v_mag[r]=np.sqrt(np.sum(v_arr**2,axis=1)).mean()
    
    fname=r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Resampled data\ac_h3_mfi_"+dts[r]+"_v01_resampled_1min.cdf"
    #fname=r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Cleaned data\ac_h3_mfi_19980205_v01_cleaned.cdf"
    print(fname)
    cdf=pycdf.CDF(fname)
    time=cdf['Epoch'][...]
    B_arr=cdf['BRTN'][...]
    df=pd.DataFrame(B_arr,time)
    #df_windowed=df.copy()
    #f=open(r'C:\Users\Sohom Roy\Desktop\Research\ACE data\Correlation tensor(2)\ACE_corr_tensor_'+dts[r]+'.txt','w')
    f2=open(r'C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor(unnormalized)\ACE_corr_trace_'+dts[r]+'.txt','w')
    #f.write(str(dr[r].date())+' '+str(df[0].isna().sum())+'\n')
    
    #window=signal.tukey(len(df[0]),alpha=0.1)
    
    if(detrend==True):
      for i in range(3):
        x=np.array(range(len(df[i])))
        mask=~df[i].isna()
        p=np.polyfit(x[mask],df[i][mask],1)
        y=np.polyval(p,x)
        df[i]-=y
        #df_windowed[i]=df[i]*window
    
  
    
    
    lag_arr=np.array([(time[i]-time[0]).days*86400+(time[i]-time[0]).seconds for i in range(len(time)//3)])
    corr_arr=np.zeros((3,3,len(lag_arr)))
    d=lag_arr*v_mag[r]
    for lag in lag_arr//60:
      for i in range(3):
        for j in range(3):
          corr_arr[i,j,lag]=corr_func(df[i],df[j],lag)
          #f.write(str(i)+' '+str(j)+' '+str(lag)+' '+str(d[lag])+' '+str(corr_arr[i,j,lag])+'\n')
          #print(lag,d[lag],i,j,corr_arr[i,j,lag])
    
    corr_trace=(corr_arr[0,0]+corr_arr[1,1]+corr_arr[2,2])
    #corr_trace/=corr_trace[0]
    
    for lag in lag_arr//60:
      f2.write(str(d[lag])+' '+str(corr_trace[lag])+'\n')
    
    #f.close()  
    f2.close()

  
  
 