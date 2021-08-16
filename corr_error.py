# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 13:49:46 2020

@author: Sohom
"""

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import scipy as sp
from datetime import datetime


def convert_date(dt):
  return dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d')

#Compute all correlation lengths from Ruiz data files

R_arr=np.zeros((3196,480))
r_arr=np.zeros((3196,480))
rs_arr=np.zeros((3196,480))
Rs_arr=np.zeros((3196,480))
rs_arr2=np.zeros((3196,480))
Rs_arr2=np.zeros((3196,480))

integ=[]
integ2=[]
date_corr=[]
date=np.empty(3196,dtype=object)
ctr=0
for i in range(3196):
  try:
    date[i]=str(np.genfromtxt(r"C:\Users\Sohom Roy\Downloads\R_universal_from_Sergio_Dasso_2_Bill\ascii_Rbb_Univ_ACE_thesis_Maria_Emilia_Ruiz\startdate_"+str(i)+".txt",usecols=0,dtype=str))
    dt=convert_date(datetime.strptime(date[i],"%d-%b-%Y"))
    fname=r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor\ACE_corr_trace_"+dt+".txt"
    fname2=r"C:\Users\Sohom Roy\Desktop\Research\ACE data\Trace of correlation tensor(2)\ACE_corr_trace_"+dt+".txt"
    R_fname=r"C:\Users\Sohom Roy\Downloads\R_universal_from_Sergio_Dasso_2_Bill\ascii_Rbb_Univ_ACE_thesis_Maria_Emilia_Ruiz\R_bb_"+str(i)+".txt"
    r_fname=r"C:\Users\Sohom Roy\Downloads\R_universal_from_Sergio_Dasso_2_Bill\ascii_Rbb_Univ_ACE_thesis_Maria_Emilia_Ruiz\r_lag_"+str(i)+".txt"
    
    R_arr[i]=np.genfromtxt(R_fname,max_rows=480)
    r_arr[i]=np.genfromtxt(r_fname,max_rows=480)
    
    R_arr[i]/=R_arr[i,0]
    
    rs_arr[i],Rs_arr[i]=np.genfromtxt(fname,unpack=True)
    rs_arr2[i],Rs_arr2[i]=np.genfromtxt(fname2,unpack=True)
    corr_index=np.abs(Rs_arr[i]-1/np.exp(1)).argmin()
    corr_index2=np.abs(Rs_arr2[i]-1/np.exp(1)).argmin()
    diff=np.abs(Rs_arr[i,:corr_index]-R_arr[i,:corr_index])
    diff2=np.abs(Rs_arr2[i,:corr_index2]-R_arr[i,:corr_index2])
    date_corr.append(date[i])
    integ.append(np.trapz(diff)/corr_index)
    integ2.append(np.trapz(diff)/corr_index2)
    ctr+=1
  except:
    continue

bins=np.logspace(-4,0,300)
plt.hist(integ,color='b',bins=bins,label='Method 1')
plt.hist(integ2,color='k',bins=bins,histtype='step',linewidth=2.0,label='Method 3')
plt.grid(True)
plt.legend(fontsize=20)
plt.xlabel(r'$\delta R$',fontsize=20)
plt.ylabel('Counts',fontsize=20)
plt.xscale('log')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.show()
