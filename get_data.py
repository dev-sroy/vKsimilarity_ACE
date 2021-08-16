# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 14:00:26 2020

@author: Sohom
"""

import urllib.request
import pandas as pd


print('Beginning file download with urllib2...')

def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')
  
year_list=range(1998,2009)

for year in year_list:
  if year==1998:
    dr=pd.date_range('02/05/'+str(year),'12/31/'+str(year))
  else:
    dr=pd.date_range('01/01/'+str(year),'12/31/'+str(year))
  dts=convert_date(dr)
  #To retrieve magnetic field data
  for dt in dts:
    fname='/ac_h3_mfi_'+dt+'_v01.cdf'
    url = r'https://spdf.gsfc.nasa.gov/pub/data/ace/mag/level_2_cdaweb/mfi_h3/'+str(year)+fname
    #print(fname)
    urllib.request.urlretrieve(url, r'C:/Users/Sohom Roy/Desktop/Research/ACE data/Magnetic field data/'+str(fname))
    
  #To retrieve velocity data
  # for dt in dts:
  #   count=6
  #   while (count<=10):
  #     fname='/ac_h2_swe_'+dt+'_v'+format(count,'02d')+'.cdf'
  #     url=r'https://spdf.gsfc.nasa.gov/pub/data/ace/swepam/level_2_cdaweb/swe_h2/'+str(year)+fname
  #     try:
  #       urllib.request.urlretrieve(url,r"C:/Users/Sohom Roy/Desktop/Research/ACE data/Velocity data/"+str(fname))
  #       print(fname)
  #       break
  #     except:
  #       pass
  #     count+=1
    