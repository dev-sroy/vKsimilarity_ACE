# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import julian
import time

def get_date(dt):
    return dt.strftime('%d')+' '+dt.strftime('%b')+' '+dt.strftime('%Y')

start=time.time()

#julian_time_arr=np.genfromtxt('PSP_SPC_1sec_Hampel20181031_20181219.csv',usecols=0,skip_header=1,delimiter=',')
#vr_arr=np.genfromtxt('PSP_SPC_1sec_Hampel20181031_20181219.csv',usecols=3,skip_header=1,delimiter=',')
#vt_arr=np.genfromtxt('PSP_SPC_1sec_Hampel20181031_20181219.csv',usecols=4,skip_header=1,delimiter=',')
#vn_arr=np.genfromtxt('PSP_SPC_1sec_Hampel20181031_20181219.csv',usecols=5,skip_header=1,delimiter=',')
br_arr=np.genfromtxt('PSP_MAG_1sec20181006_20181219.csv',usecols=1,skip_header=1,delimiter=',')

end=time.time()
print("Array of magnetic field values loaded")
print(end-start)
julian_time_arr_mag=np.genfromtxt('PSP_MAG_1sec20181006_20181219.csv',usecols=0,skip_header=1,delimiter=',')
#Convert Julian date to Gregorian date
date_arr=[julian.from_jd(jd,fmt='jd') for jd in julian_time_arr_mag]
#date_labels=[get_date(julian.from_jd(jd,fmt='jd')) for jd in np.linspace(julian_time_arr.min(),julian_time_arr.max()+1,5)]
date_labels_mag=[get_date(julian.from_jd(jd,fmt='jd')) for jd in np.linspace(julian_time_arr_mag.min(),julian_time_arr_mag.max()+1,5)]

plt.figure(figsize=(20,12))
plt.plot(julian_time_arr_mag,br_arr,'-k')
plt.xticks(np.linspace(julian_time_arr_mag.min(),julian_time_arr_mag.max()+1,5),date_labels_mag)

plt.show()

