# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 13:28:41 2020

@author: Sohom
"""

import numpy as np
import os
from datetime import datetime

dir=r'C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor'
f=open("Correlation lengths_linfit.txt",'w+')
f.write('Date'+'\t'+'Correlation length'+'\n')
for fname in os.listdir(dir):
  try:
    full_fname=os.path.join(dir,fname)
    r_lag,corr_arr=np.genfromtxt(full_fname,unpack=True)
    tc=np.abs(corr_arr-1/np.exp(1)).argmin()+1
    log_corr=np.log(corr_arr[:tc])
    p=np.polyfit(r_lag[:tc],log_corr,1)
    print(-1/p[0])
    date_string=fname[-12:-4]
    date=datetime.strptime(date_string,'%Y%m%d')
    date_fmt=datetime.strftime(date,'%d-%b-%Y')
    f.write(date_fmt+'\t'+str(-1/p[0])+'\n')
  except:
    continue
f.close()