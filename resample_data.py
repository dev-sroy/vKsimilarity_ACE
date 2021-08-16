# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:34:04 2020

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
  fname=r'C:\Users\Sohom Roy\Desktop\Research\Ace data\Cleaned data'+'\\ac_h3_mfi_'+dt+'_v01_cleaned.cdf'
  cdf=pycdf.CDF(fname)
  print(fname+" loaded!")

  df=pd.DataFrame(cdf['BRTN'][...],cdf['Epoch'][...])
  df_rs=df.resample('1min',base=0.5,loffset='30s').mean()

  cdfnew=pycdf.CDF(r'C:\Users\Sohom Roy\Desktop\Research\Ace data\Resampled data\ac_h3_mfi_'+dt+'_v01_resampled_1min.cdf','')
  cdfnew['Epoch']=df_rs.index.to_pydatetime()
  cdfnew['BRTN']=df_rs.values
  
  cdfnew.close()
  cdf.close()
