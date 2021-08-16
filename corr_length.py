# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:54:16 2020

@author: Sohom
"""


import numpy as np
import os
from datetime import datetime

dir=r'C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor(3)'
f=open("Correlation lengths(3).txt",'w+')
f.write('Date'+'\t'+'Correlation length'+'\n')
for fname in os.listdir(dir):
  try:
    full_fname=os.path.join(dir,fname)
    r_lag,corr_arr=np.genfromtxt(full_fname,unpack=True)
    tc=np.abs(corr_arr-1/np.exp(1)).argmin()
    date_string=fname[-12:-4]
    date=datetime.strptime(date_string,'%Y%m%d')
    date_fmt=datetime.strftime(date,'%d-%b-%Y')
    f.write(date_fmt+'\t'+str(r_lag[tc])+'\n')
  except:
    continue
f.close()