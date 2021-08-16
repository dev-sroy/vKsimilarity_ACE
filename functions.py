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



print("The mean magnetic field is "+str(br0)+" nT.")

#Computing autocorrelation

correlation_arr=np.zeros(len(delta_br_arr))

for i in range(0,len(delta_br_arr),10000):
    for j in range(len(delta_br_arr)-i):
        if(~np.isnan(delta_br_arr[j]) and ~np.isnan(delta_br_arr[j+i])):
            correlation_arr[i]+=delta_br_arr[j]*delta_br_arr[j+i]
    correlation_arr[i]/=len(delta_br_arr)-i
    if(correlation_arr[i]<=correlation_arr[0]/np.exp(1)):
        break
    print(i,correlation_arr[i])

    