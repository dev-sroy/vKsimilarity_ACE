import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd

#Compute all correlation lengths from Ruiz data files

R_arr=np.zeros((3196,480))
r_arr=np.zeros((3196,480))

corr_len=np.zeros(3180)
corr_len2=np.zeros(3180)
date=np.empty(3196,dtype=object)

df=pd.read_csv(r"C:\Users\Sohom Roy\Desktop\Research\Correlation lengths(3).txt",sep='\t',index_col=0)
f=open('Correlation length_compare3.txt','w+')
for i in range(3196):
  try:
    date[i]=str(np.genfromtxt(r"C:\Users\Sohom Roy\Downloads\R_universal_from_Sergio_Dasso_2_Bill\ascii_Rbb_Univ_ACE_thesis_Maria_Emilia_Ruiz\startdate_"+str(i)+".txt",usecols=0,dtype=str))
    corr_len2[i]=df.at[date[i],'Correlation length']
    R_fname=r"C:\Users\Sohom Roy\Downloads\R_universal_from_Sergio_Dasso_2_Bill\ascii_Rbb_Univ_ACE_thesis_Maria_Emilia_Ruiz\R_bb_"+str(i)+".txt"
    r_fname=r"C:\Users\Sohom Roy\Downloads\R_universal_from_Sergio_Dasso_2_Bill\ascii_Rbb_Univ_ACE_thesis_Maria_Emilia_Ruiz\r_lag_"+str(i)+".txt"
    
    R_arr[i]=np.genfromtxt(R_fname,max_rows=480)
    r_arr[i]=np.genfromtxt(r_fname,max_rows=480)
    
    R_arr[i]/=R_arr[i,0]
    corr_index=np.abs(R_arr[i]-1/np.exp(1)).argmin()
    
    corr_len[i]=r_arr[i,corr_index]
    
    if(corr_len2[i]!=np.inf):
      f.write(date[i]+'\t'+format(corr_len[i],'.2f')+'\t'+format(corr_len2[i],'.2f')+'\n')
  except:
    continue
f.close()
    
    
    
    
    
    

