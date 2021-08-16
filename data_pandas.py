# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 18:15:41 2020

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

julian_time_arr=vel_df.iloc[:,0].values

vr_arr=vel_df.iloc[:,3].values
vt_arr=vel_df.iloc[:,4].values
vn_arr=vel_df.iloc[:,5].values

julian_time_arr_mag=mag_df.iloc[:,0].values
br_arr=mag_df.iloc[:,1].values
bt_arr=mag_df.iloc[:,2].values
bn_arr=mag_df.iloc[:,3].values

#Plotting the entire data
'''
date_arr=[julian.from_jd(jd,fmt='jd') for jd in julian_time_arr]
date_arr_mag=[julian.from_jd(jd,fmt='jd') for jd in julian_time_arr_mag]
date_labels=[get_date(julian.from_jd(jd,fmt='jd')) for jd in np.linspace(julian_time_arr.min(),julian_time_arr.max()+1,5)]
date_labels_mag=[get_date(julian.from_jd(jd,fmt='jd')) for jd in np.linspace(julian_time_arr_mag.min(),julian_time_arr_mag.max()+1,5)]

plt.figure(figsize=(20,12))
plt.plot(julian_time_arr_mag,br_arr,'-k')
plt.xticks(np.linspace(julian_time_arr_mag.min(),julian_time_arr_mag.max()+1,5),date_labels_mag)
'''

#Zooming in on the data between 1 and 10 November 2018

'''
dt1=datetime.datetime(2018,11,1,0,0,0,0)
dt2=datetime.datetime(2018,11,10,0,0,0,0)

jd1=julian.to_jd(dt1,fmt='jd')
jd2=julian.to_jd(dt2,fmt='jd')

#Finding the dates in the array

index1=np.abs(julian_time_arr_mag-jd1).argmin()
index2=np.abs(julian_time_arr_mag-jd2).argmin()

plt.figure(figsize=(20,12))
plt.plot(julian_time_arr_mag[index1:index2],br_arr[index1:index2],'-k')
label_arr=np.linspace(julian_time_arr_mag[index1],julian_time_arr_mag[index2],5)
date_labels_mag=[get_date(julian.from_jd(jd,fmt='jd')) for jd in label_arr]

plt.xticks(label_arr,date_labels_mag)
'''

#Plotting the data for 6 November 2018

dt1=datetime.datetime(2018,11,5,0,0,0,0)
dt2=datetime.datetime(2018,11,6,0,0,0,0)

jd1=julian.to_jd(dt1,fmt='jd')
jd2=julian.to_jd(dt2,fmt='jd')

index1=np.abs(julian_time_arr_mag-jd1).argmin()
index2=np.abs(julian_time_arr_mag-jd2).argmin()

time_label_arr=np.linspace(julian_time_arr_mag[index1],julian_time_arr_mag[index2],8)
time_arr=[get_time(julian.from_jd(jd,fmt='jd')) for jd in time_label_arr]

plt.figure(figsize=(20,12))
plt.plot(julian_time_arr_mag[index1:index2],br_arr[index1:index2],'-k')
plt.xticks(time_label_arr,time_arr)


plt.show()



