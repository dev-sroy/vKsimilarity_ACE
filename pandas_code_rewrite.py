# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 15:42:49 2021

@author: Sohom
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from spacepy import pycdf

dir = r"C:\Users\Sohom Roy\Dropbox\My PC (LAPTOP-SLR6UBDE)\Desktop\Research\ACE data\Resampled data\\"

B_max = pd.DataFrame(columns = ['Bx', 'By', 'Bz'])
B = pd.DataFrame()

for f in os.listdir(dir):
  
  fname = os.path.join(dir, f)

  cdf = pycdf.CDF(fname)

  Bx, By, Bz = cdf['BRTN'][...].T
  epoch = cdf['Epoch'][...]

  B_df = pd.DataFrame(data = [epoch, Bx, By, Bz], index = ['Datetime', 'Bx', 'By', 'Bz']).T

  B_df = B_df.set_index('Datetime')
  
  B = B.append(B_df, ignore_index = True)
  
  print(fname)

