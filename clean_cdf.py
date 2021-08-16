# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 17:59:48 2020

@author: Sohom
"""


from spacepy import pycdf
import pandas as pd
import numpy as np

def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')
  
start_dt='02/05/1998'
end_dt='03/30/2008'

dr=pd.date_range(start_dt,end_dt,freq='D')
dts=convert_date(dr)

for dt in dts:
  #fname=r'C:\Users\Sohom Roy\Desktop\Research\Ace data\ac_h3s_mfi_19980205000000_19980205235959.cdf'
  fname=r'C:\Users\Sohom Roy\Desktop\Research\Ace data'+'\\ac_h3_mfi_'+dt+'_v01.cdf'
  cdf=pycdf.CDF(fname)
  print(fname+" loaded!")
  time=pd.Series(cdf['Epoch'][...])
  B_arr=pd.DataFrame(cdf['BRTN'][...])
  
  cdfnew=pycdf.CDF(r'C:\Users\Sohom Roy\Desktop\Research\Ace data\Cleaned data'+'\\ac_h3_mfi_'+dt+'_v01_cleaned.cdf','')
  
  threshold=1e2
  
  B_arr[np.abs(B_arr[0])>threshold]=np.nan
  
  cdfnew['Epoch']=cdf['Epoch'].copy()
  cdfnew['BRTN']=B_arr.values
  
  print ('Cleaned data saved! '+dt)
  
  cdfnew.close()
  cdf.close()





