# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 15:52:16 2020

@author: Sohom
"""


import pandas as pd
import matplotlib.pyplot as plt
import julian
import datetime 
import numpy as np

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

t=pd.date_range('11/4/2018','11/7/2018',freq='S')

start_jd=julian.to_jd(datetime.datetime(2018,11,4,0,0,0,0),fmt='jd')
end_jd=julian.to_jd(datetime.datetime(2018,11,7,0,0,0,0),fmt='jd')

start_index=np.abs(jt_arr-start_jd).argmin()
end_index=np.abs(jt_arr-end_jd).argmin()

br_arr_slice=br_arr[start_index-1:end_index]
bn_arr_slice=bn_arr[start_index-1:end_index]
bt_arr_slice=bt_arr[start_index-1:end_index]

data_rr=pd.Series(br_arr_slice,t)
data_nn=pd.Series(bn_arr_slice,t)
data_tt=pd.Series(bt_arr_slice,t)

mean_rr=data_rr['2018-11-05 00:00:00':'2018-11-06 00:00:00'].rolling(3600).mean()
mean_nn=data_nn['2018-11-05 00:00:00':'2018-11-06 00:00:00'].rolling(3600).mean()
mean_tt=data_tt['2018-11-05 00:00:00':'2018-11-06 00:00:00'].rolling(3600).mean()

delta_data_rr=data_rr-mean_rr
delta_data_nn=data_nn-mean_nn
delta_data_tt=data_tt-mean_tt

corr_arr=np.zeros(10000)

for i in range(10000):
    corr_arr[i]=(delta_data_rr.autocorr(lag=i)+delta_data_nn.autocorr(lag=i)+delta_data_tt.autocorr(lag=i))/3
    
    
plt.figure(figsize=(20,12))
plt.plot(corr_arr)    
plt.show()

