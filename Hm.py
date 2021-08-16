# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 16:17:00 2020

@author: Sohom
"""

import pandas as pd
import matplotlib.pyplot as plt
import julian
import numpy as np
import datetime
import scipy.integrate as sp

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

au_to_km=1.496e8

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

def mag_helicity(dt1,dt2):
    start_dt=datetime.datetime(2018,11,dt1,0,0,0,0)
    end_dt=datetime.datetime(2018,11,dt2,0,0,0,0)
    
    start_jd=julian.to_jd(start_dt,fmt='jd')
    end_jd=julian.to_jd(end_dt,fmt='jd')
    
    start_index=np.abs(jt_arr_mag-start_jd).argmin()
    end_index=np.abs(jt_arr_mag-end_jd).argmin()
    
    start_index_v=np.abs(jt_arr-start_jd).argmin()
    end_index_v=np.abs(jt_arr-end_jd).argmin()
    
    vr_arr_slice=pd.Series(vr_arr[start_index_v:end_index_v])
    
    vr_mean=vr_arr_slice.mean()
    
    br_arr_slice=br_arr[start_index:end_index]
    bn_arr_slice=bn_arr[start_index:end_index]
    bt_arr_slice=bt_arr[start_index:end_index]
    
    N=10000
    
    integrand=np.zeros(N)
    r_lag=np.zeros(N)
    for lag in range(N):
        #Computing off-diagonal terms in the correlation tensor
        corr_tn=corr_func(bt_arr_slice,bn_arr_slice,lag)
        corr_nt=corr_func(bn_arr_slice,bt_arr_slice,lag)
        #Computing the difference 
        integrand[lag]=corr_tn-corr_nt
        r_lag[lag]=(lag*vr_mean)/au_to_km
        #print(r_lag[lag],integrand[lag])
        
    #Integrating to get the magnetic helicity
    Hm=sp.trapz(integrand,r_lag)
    return Hm
    
Hm_arr=np.zeros(30)
for dt in range(1,30):
    Hm_arr[dt]=mag_helicity(dt,dt+1)
    print(dt,Hm_arr[dt])
        
