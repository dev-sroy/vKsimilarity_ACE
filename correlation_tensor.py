# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 17:32:21 2020

@author: Sohom
"""


from init import *

jt_arr_mag,br_arr,bt_arr,bn_arr=load_magnetic_field_data()

start_dt='11/05/18'
end_dt='11/06/18'

b1=np.zeros((3,86401))
b1[0],tr = slice_arr(br_arr,jt_arr_mag,start_dt,end_dt)  #Array containing the radial magnetic field values in the given date range
b1[1],tt = slice_arr(bt_arr,jt_arr_mag,start_dt,end_dt)  #Array containing the tangential magnetic field values in the given date range
b1[2],tn = slice_arr(bn_arr,jt_arr_mag,start_dt,end_dt)  #Array containing the normal magnetic field values in the given date range

b1.T

t_max=10000                     #Maximum lag time in seconds

lag_arr=np.arange(0,t_max,1)     #Array containing the lag times in seconds

#Computing the correlation tensor

corr_tensor=np.zeros((3,3,t_max))

for i in range(3):
    for j in range(3):
        for k in range(len(lag_arr)):
            corr_tensor[i,j,lag_arr[k]]=corr_func(b1[i],b1[j],lag_arr[k])
            print(i,j,lag_arr[k],corr_tensor[i,j,lag_arr[k]])
            
f=open('correlation_tensor_1.txt','w')
for i in range(3):
    for j in range(3):
        for k in range(len(lag_arr)):
            f.write(str(i)+' '+str(j)+' '+str(lag_arr[k])+' '+str(corr_tensor[i,j,k])+'\n')

f.close()