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

start_dt=datetime.datetime(2018,11,5,0,0,0,0)
end_dt=datetime.datetime(2018,11,6,0,0,0,0)

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


integrand=np.zeros(10000)
r_lag=np.zeros(10000)
for lag in range(10000):
    #Computing off-diagonal terms in the correlation tensor
    corr_tn=corr_func(bt_arr_slice,bn_arr_slice,lag)
    corr_nt=corr_func(bn_arr_slice,bt_arr_slice,lag)
    #Computing the difference 
    integrand[lag]=corr_tn-corr_nt
    r_lag[lag]=(lag*vr_mean)/au_to_km
    print(r_lag[lag],integrand[lag])
    
f=open('correlation.txt','w')
for i in range(len(integrand)):
    f.write(str(r_lag[i])+' '+str(integrand[i])+'\n')

f.close()

Hm_arr=np.zeros(10000)
#Integrating to get the magnetic helicity
Hm_arr=sp.trapz(integrand,r_lag)
    
#tc=np.abs(corr_arr-1/np.exp(1)).argmin()

fig=plt.figure(figsize=(20,12))
ax=fig.add_subplot(111)
ax.plot(r_lag,integrand,'-k')
ax.set_xlabel('Lag(in AU)',fontsize=20)
ax.set_ylabel('$R_{tn}(r,0,0,)-R_{nt}(r,0,0)$',fontsize=20)
ax.tick_params(labelsize=20)
plt.title('Integrand of the magnetic helicity averaged over 1 day(11/5/2018-11/6/2018)',fontsize=25)
#plt.axvline(tc,0,1,color='k',linewidth=2.0)
#plt.plot(tc,corr_arr1[tc],'r.',markersize=12)
#plt.text(tc,corr_arr1[tc],'('+str(tc)+', '+format(corr_arr1[tc],'.2f')+')',fontsize=20)

plt.show()
    
