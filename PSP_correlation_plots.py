# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 17:38:53 2021

@author: Sohom
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

filelist = os.listdir(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\PSP correlations\\")

size = len(filelist)

for i in range(size):
  fname = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\PSP correlations\\"+filelist[i]
  data = pd.read_csv(fname, sep='\t')
  
  x = data.iloc[:,0].values
  y = data.iloc[:,1].values
  
  plt.plot(x,y)
  plt.xlabel('Lag(in s)')
  plt.ylabel(r'$R(\tau)$')
  plt.grid(True)
  
  img_fname = os.path.splitext(r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\PSP correlation plots\\"+filelist[i])[0]+'.jpg'
  plt.savefig(img_fname)
  plt.gca().clear()