# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 09:31:37 2021

@author: Sohom
"""

import numpy as np
import pandas as pd
from spacepy import pycdf
import os

B_dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Magnetic field data"

B_df = pd.DataFrame()

for f in os.listdir(B_dir):
  
  fname = os.path.join(B_dir, f)
  
  cdf = pycdf.CDF(fname)
  
  keys = list(cdf.keys())
  
  df = pd.DataFrame(cdf[keys[3]][...], cdf[keys[0]][...], columns = ['Bx', 'By', 'Bz'])
  
  df = df.rename_axis(index = 'Datetime')
  
  B_df = B_df.append(df)
  
  print(f)