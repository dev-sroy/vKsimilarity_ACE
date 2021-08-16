# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 02:19:50 2020

@author: Sohom
"""

import pandas as pd
import matplotlib.pyplot as plt
import julian
import numpy as np
import datetime


def get_date(dt):
    return dt.strftime('%d')+' '+dt.strftime('%b')+' '+dt.strftime('%Y')

def get_time(dt):
    return dt.strftime('%I')+':'+dt.strftime('%M')+':'+dt.strftime('%S')

def get_hms(t):
    h=int(t)
    m=int((t-h)*60)
    s=int(((t-h)*60)-m)*60)

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

br0=np.nanmean(br_arr)
delta_br_arr=br_arr-br0

bt0=np.nanmean(bt_arr)
delta_bt_arr=bt_arr-bt0

bn0=np.nanmean(bn_arr)
delta_bn_arr=bn_arr-bn0

print("The mean magnetic field is "+str(br0)+" nT.")

#Computing autocorrelation

correlation_arr_rr=np.zeros(len(delta_br_arr))
correlation_arr_nn=np.zeros(len(delta_bn_arr))
correlation_arr_tt=np.zeros(len(delta_bt_arr))
correlation_arr=np.zeros(len(delta_br_arr))

for i in range(0,len(delta_br_arr),10000):
    for j in range(len(delta_br_arr)-i):
        if(~np.isnan(delta_br_arr[j]) and ~np.isnan(delta_br_arr[j+i])):
            correlation_arr_rr[i]+=delta_br_arr[j]*delta_br_arr[j+i]
        if(~np.isnan(delta_bn_arr[j]) and ~np.isnan(delta_bn_arr[j+i])):
            correlation_arr_nn[i]+=delta_bn_arr[j]*delta_bn_arr[j+i]
        if(~np.isnan(delta_bt_arr[j]) and ~np.isnan(delta_bt_arr[j+i])):
            correlation_arr_tt[i]+=delta_bt_arr[j]*delta_bt_arr[j+i]
    correlation_arr[i]=correlation_arr_rr[i]+correlation_arr_nn[i]+correlation_arr_tt[i]
    correlation_arr[i]/=len(delta_br_arr)-i
    if(correlation_arr[i]<=correlation_arr[0]/np.exp(1)):
        break
    print(i,correlation_arr[i])

corr_arr=[]
time_arr=[]

for i in range(len(correlation_arr)):
    if correlation_arr[i]!=0:
        corr_arr.append(correlation_arr[i])
        time_arr.append(jt_arr[i])

time_arr=time_arr-time_arr[0]

time_lag_arr=np.linspace(time_arr[0], time_arr[-1],8)
label_arr=

plt.figure(figsize=(20,12))
plt.plot(jt_arr[i],corr_arr[i])
plt.xticks(time_lag_arr,label_arr)

plt.show()
