# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 14:11:15 2020

@author: Sohom
"""


import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')
plt.figure(figsize=(20,12))
for i in range(3196):
  date=datetime.strptime(str(np.genfromtxt(r"C:\Users\Sohom Roy\Downloads\R_universal_from_Sergio_Dasso_2_Bill\ascii_Rbb_Univ_ACE_thesis_Maria_Emilia_Ruiz\startdate_"+str(i)+".txt",usecols=0,dtype=str)),"%d-%b-%Y")
  dt=convert_date(date)
  print(dt)
  fname1=r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor\ACE_corr_trace_"+dt+".txt"
  fname2=r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor(2)\ACE_corr_trace_"+dt+".txt"
  fname3=r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor(3)\ACE_corr_trace_"+dt+".txt"
  try:
    r_lag1,R1=np.genfromtxt(fname1,unpack=True)
    r_lag2,R2=np.genfromtxt(fname2,unpack=True)
    r_lag3,R3=np.genfromtxt(fname3,unpack=True)
    
    R_Ruiz=np.genfromtxt(r"C:\Users\Sohom Roy\Downloads\R_universal_from_Sergio_Dasso_2_Bill\ascii_Rbb_Univ_ACE_thesis_Maria_Emilia_Ruiz\R_bb_"+str(i)+".txt",max_rows=480)
    r_lag_Ruiz=np.genfromtxt(r"C:\Users\Sohom Roy\Downloads\R_universal_from_Sergio_Dasso_2_Bill\ascii_Rbb_Univ_ACE_thesis_Maria_Emilia_Ruiz\r_lag_"+str(i)+".txt",max_rows=480)
    
    R_Ruiz/=R_Ruiz[0]
    
    plt.gca().clear()
    plt.plot(r_lag1,R1,label='Sohom,Method 1')
    plt.plot(r_lag3,R3,label='Sohom, Method 2')
    plt.plot(r_lag2,R2,label='Sohom,Method 3')
    
    plt.plot(r_lag_Ruiz,R_Ruiz,label='Ruiz')
    plt.title(dt,fontsize=20)
    plt.legend(fontsize=20)
    plt.xlabel('Lag(in km)',fontsize=20)
    plt.ylabel('Autocorrelation',fontsize=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.grid(True)
    plt.savefig(r'C:\Users\Sohom Roy\Desktop\Research\Plots of correlation functions(4)\\'+dt)
    #plt.draw()
    #plt.pause(0.2)
  except:
    print('File not found')