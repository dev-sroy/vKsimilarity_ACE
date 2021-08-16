# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 12:47:31 2021

@author: Sohom
"""

from init import *

def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')

v_fname=r"C:\Users\Sohom Roy\Desktop\Research\PSP_SPC_1sec_Hampel20181031_20181219.csv"
B_fname=r"C:\Users\Sohom Roy\Desktop\Research\PSP_MAG_1sec20181006_20181219.csv"

vel_df = pd.read_csv(v_fname)
mag_df = pd.read_csv(B_fname)
mag_time = mag_df[mag_df.columns[0]]
vel_time = vel_df[vel_df.columns[0]]

start_dt=jd_to_date(vel_time[0])
end_dt=jd_to_date(vel_time.values[-1])


date_range=pd.date_range(start_dt,end_dt,freq='D',closed='left')

max_lag=10000                                #Maximum lag in seconds

#Compute trace of autocorrelation tensor for each day

for dt in date_range[1:]:
  date = dt.strftime('%m/%d/%y')
  B_df,t = get_day(mag_df,mag_time,date)
  v_df,t = get_day(vel_df, vel_time, date)
  B_df = B_df.drop(columns=['Time (Julian day)'])
  v_df = v_df.drop(columns=['Time (Julian day)','np (cm^-3)','wp (km/s)'])
  B_df.insert(loc=0,column='Time',value=t)
  v_df.insert(loc=0, column='Time', value=t)
  B_df=B_df.set_index('Time')
  v_df=v_df.set_index('Time')
  v_mag_sq = v_df.iloc[:,0].values**2+v_df.iloc[:,2].values**2+v_df.iloc[:,2].values**2
  v_mag=np.nanmean(np.sqrt(v_mag_sq))                               #Computing average velocity for the day
  
  corr_arr=np.zeros((3,3,max_lag))
  
  for lag in range(max_lag):
    for i in range(3):
      for j in range(3):
        corr_arr[i,j,lag]=corr_func(B_df.iloc[:,i],B_df.iloc[:,j],lag)
        
  corr_trace=corr_arr[0,0]+corr_arr[1,1]+corr_arr[2,2]
  corr_trace/=corr_trace[0]
  
  f2=open(r"C:\Users\Sohom Roy\Desktop\Research\PSP correlations\\"+convert_date(dt)+".txt",'w')
  
  for lag in range(max_lag):
    f2.write(str(v_mag*lag)+'\t'+str(corr_trace[lag])+'\n')
  
  print(date)