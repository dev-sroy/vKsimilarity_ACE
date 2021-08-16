# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:03:41 2020

@author: Sohom
"""

import pandas as pd
import matplotlib.pyplot as plt
import julian
import numpy as np
import datetime

def corr_func(arr1,arr2,lag):
    data1=pd.Series(arr1[0:-lag-1])
    data2=pd.Series(arr2[lag:-1])
    mean1=data1.mean()
    mean2=data2.mean()
    #delta1=data1-mean1
    #delta2=data2-mean2
    corr=(data1*data2).mean()-(mean1*mean2)
    #corr=(delta1*delta2).mean()
    return corr

def get_date(dt):
    return dt.strftime('%d')+' '+dt.strftime('%b')+' '+dt.strftime('%Y')

def get_time(dt):
    return dt.strftime('%I')+':'+dt.strftime('%M')+':'+dt.strftime('%S')

def time(t):
    h=int(t)
    m=int((t-h)*60)
    s=int(((t-h)*60-m)*60)
    return str(h)+"h "+str(m)+"m "+str(s)+"s"

vel_df=pd.read_csv('PSP_SPC_1sec_Hampel20181031_20181219.csv')
mag_df=pd.read_csv('PSP_MAG_1sec20181006_20181219.csv')

jt_arr=vel_df.iloc[:,0].values

vr_arr=vel_df.iloc[:,3].values
vt_arr=vel_df.iloc[:,4].values
vn_arr=vel_df.iloc[:,5].values

jt_arr_mag=mag_df.iloc[:,0].values
br_arr=mag_df.iloc[:,1].values
bt_arr=mag_df.iloc[:,2].values
bn_arr=mag_df.iloc[:,3].values

start_dt=datetime.datetime(2018,11,5,0,0,0,0)
end_dt=datetime.datetime(2018,11,6,0,0,0,0)

start_jd=julian.to_jd(start_dt,fmt='jd')
end_jd=julian.to_jd(end_dt,fmt='jd')

start_index=np.abs(jt_arr_mag-start_jd).argmin()
end_index=np.abs(jt_arr_mag-end_jd).argmin()

br_arr_slice=br_arr[start_index:end_index]
bn_arr_slice=bn_arr[start_index:end_index]
bt_arr_slice=bt_arr[start_index:end_index]


corr_arr=np.zeros(10000)

for lag in range(10000):
    corr_rr=corr_func(br_arr_slice,br_arr_slice,lag)
    corr_nn=corr_func(bn_arr_slice,bn_arr_slice,lag)
    corr_tt=corr_func(bt_arr_slice,bt_arr_slice,lag)
    corr_arr[lag]=(corr_rr+corr_nn+corr_tt)/3.
    print(lag,corr_arr[lag]/corr_arr[0])
    
corr_arr/=corr_arr[0]

# f=open('correlation.txt','w')
# for i in range(len(corr_arr)):
#     f.write(str(i)+' '+str(corr_arr[i])+'\n')

# f.close()

tc=np.abs(corr_arr-1/np.exp(1)).argmin()

plt.figure(figsize=(20,12))
plt.plot(corr_arr,linewidth=2.0)
plt.xlabel('Lag,$\\tau$(in s)',fontsize=20)
plt.ylabel('$\\frac{1}{3}\\sum_{i}\\frac{R_{ii}(\\tau)}{R_{ii}(0)}$',fontsize=30)
plt.axvline(tc,0,1,color='k',linewidth=2.0)
plt.plot(tc,corr_arr[tc],'r.',markersize=12)
plt.text(tc,corr_arr[tc],'('+str(tc)+', '+format(corr_arr[tc],'.2f')+')',fontsize=20)

plt.show()
    

    