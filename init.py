# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 17:00:03 2020

@author: Sohom
"""

import pandas as pd
import julian
from datetime import datetime
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

v_fname=r"C:\Users\Sohom Roy\Desktop\Research\PSP_SPC_1sec_Hampel20181031_20181219.csv"
B_fname=r"C:\Users\Sohom Roy\Desktop\Research\PSP_MAG_1sec20181006_20181219.csv"

def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')

def load_velocity_data():
    vel_df=pd.read_csv(v_fname)
    t=vel_df.iloc[:,0].values
    vr=vel_df.iloc[:,3].values
    vt=vel_df.iloc[:,4].values
    vn=vel_df.iloc[:,5].values
    
    return t,vr,vt,vn
    
# def load_magnetic_field_data():
#     mag_df=pd.read_csv(B_fname)
#     t=mag_df.iloc[:,0].values
#     br=mag_df.iloc[:,1].values
#     bt=mag_df.iloc[:,2].values
#     bn=mag_df.iloc[:,3].values
    
#     return t,br,bt,bn

def load_magnetic_field_data():
    mag_df = pd.read_csv(B_fname)
    t = mag_df[mag_df.columns[0]]
    B = mag_df[mag_df.columns[1:4]]
    
    return t,B

def jd_to_date(jd):
    dt=julian.from_jd(jd,fmt='jd')
    str_dt=dt.strftime('%x')
    return str_dt

def date_to_jd(dt):
    jd=julian.to_jd(dt,fmt='jd')
    return jd
  
def slice_arr(arr,t,dt1,dt2,time1="00:00:00",time2="00:00:00"):
    date1=dt1+' '+time1
    date2=dt2+' '+time2
    dt_obj1=datetime.strptime(date1,'%m/%d/%y %H:%M:%S') 
    dt_obj2=datetime.strptime(date2,'%m/%d/%y %H:%M:%S')
    jd1=date_to_jd(dt_obj1)
    jd2=date_to_jd(dt_obj2)
    index1=np.abs(t-jd1).argmin()+1
    index2=np.abs(t-jd2).argmin()+2
    slice_arr=arr[index1:index2]
    t_arr=pd.date_range(date1,date2,freq='S')
    return slice_arr,t_arr

def get_day(arr,t,dt1,time1="00:00:00"):
    date1=dt1+' '+time1
    dt_obj1=datetime.strptime(date1,'%m/%d/%y %H:%M:%S') 
    dt_obj2=dt_obj1+dt.timedelta(days=1)
    date2=dt_obj2.strftime('%m/%d/%y')+' '+time1
    jd1=date_to_jd(dt_obj1)
    jd2=date_to_jd(dt_obj2)
    index1=np.abs(t-jd1).argmin()+1
    index2=np.abs(t-jd2).argmin()+2
    slice_arr=arr[index1:index2]
    t_arr=pd.date_range(date1,date2,freq='S')
    return slice_arr,t_arr

def corr_func(arr1,arr2,lag):
    l1=len(arr1)
    l2=len(arr2)
    data1=pd.Series(arr1[0:l1-lag])
    data2=pd.Series(arr2[lag:l2])
    mean1=data1.mean()
    mean2=data2.mean()
    corr=np.nanmean(data1.values*data2.values)-mean1*mean2
    return corr

def corr_func2(arr1,arr2,lag):
    l1=len(arr1)
    l2=len(arr2)
    mean1=arr1.mean()
    mean2=arr2.mean()
    delta1=arr1.values-mean1
    delta2=arr2.values-mean2
    corr=np.nanmean(delta1[:l1-lag]*delta2[lag:])
    return corr

def corr_func3(arr1,arr2,lag):
    l1=len(arr1)
    l2=len(arr2)
    data1=pd.Series(arr1[0:l1-lag])
    data2=pd.Series(arr2[lag:l2])
    mean1=data1.mean()
    mean2=data2.mean()
    delta1=data1.values-mean1
    delta2=data2.values-mean2
    corr=np.nanmean(delta1*delta2)
    return corr
  
def symmetrize_arr(x):
  l=len(x)
  L=2*(l-1)
  x_symm=[x[np.abs(l-1-i)] for i in range(L)]
  return x_symm  

def plot_labels(xlabel, ylabel):
  plt.xticks(fontsize=40)
  plt.yticks(fontsize=40)
  plt.xlabel(xlabel,fontsize=40)
  plt.ylabel(ylabel,fontsize=40)
  plt.legend(fontsize=40)
  plt.grid(True)
  

    