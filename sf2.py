# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 18:43:12 2020

@author: Sohom
"""

sf2_arr_fast=2-2*corr_arr2_fast
sf2_mean_fast=np.zeros(size)
sf2_std_fast=np.zeros(size)
sf_arr_fast=2-2*corr_arr_fast
for i in range(size):
  sf2_mean_fast[i]=np.nanmean(sf2_arr_fast[:,1,i])
for i in range(size):
  sf2_std_fast[i]=np.nanstd(sf2_arr_fast[:,1,i])
for i in range(len(sf2_arr_fast)):
    plt.plot(lag_new_fast[i][1:],sf_arr_fast[i][1][1:],'peru',alpha=0.2)
plt.xlim(lag2[1],lag2[-1])
plt.plot(lag2[1:],sf2_mean_fast[1:],'k',label='Mean, slope='+str(round(p[0],2)),zorder=25)
y1=sf2_mean_fast-sf2_std_fast
y2=sf2_mean_fast+sf2_std_fast
y3=sf2_mean_fast-2*sf2_std_fast
y4=sf2_mean_fast+2*sf2_std_fast
#plt.plot(lag2,sf2_mean_fast+sf2_std_fast,'r--')
#plt.plot(lag2,sf2_mean_fast-sf2_std_fast,'r--')
#plt.plot(lag2,sf2_mean_fast+2*sf2_std_fast,'b--')
#plt.plot(lag2,sf2_mean_fast-2*sf2_std_fast,'b--')
plt.fill_between(lag2[1:],y1[1:],y2[1:],color='blue',alpha=0.5,label='1 standard deviation',zorder=10)
plt.fill_between(lag2[1:],y3[1:],y4[1:],color='dodgerblue',alpha=0.5,label='2 standard deviations',zorder=20)
x=np.logspace(-1,-0.2,50)
y=(x**(2/3.))*2
plt.plot(x,y,'r--',label='Slope=2/3='+str(round(2/3.,2)))
#plt.xscale('log')
#plt.yscale('log')
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
plt.xlabel(r'Spatial lag, $\frac{r}{\lambda}$',fontsize=15)
plt.ylabel(r'$S^2\left(\frac{r}{\lambda}\right)$',fontsize=15)
plt.grid(True)