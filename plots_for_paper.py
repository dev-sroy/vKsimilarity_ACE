# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 03:04:34 2021

@author: Sohom
"""
#Figure 1: 




















#Figure 2: Correlation functions normalized by energy

plt.xlim(0,0.5e7)
corr_arr_fast_new=np.zeros((len(corr_arr_fast),2,480))
stdev_fast_new=np.zeros(480)
corr_mean_fast_new=np.zeros(480)
for i in range(len(corr_arr_fast)):
    plt.plot(corr_arr_fast[i][0],corr_arr_fast[i][1],'peru',alpha=0.2)
for i in range(len(corr_arr_fast)):
    f=interp1d(corr_arr_fast[i][0],corr_arr_fast[i][1],bounds_error=False)
    corr_arr_fast_new[i,0]=lag
    corr_arr_fast_new[i,1]=f(lag)
for i in range(len(lag)):
    corr_mean_fast_new[i]=np.nanmean(corr_arr_fast_new[:,1,i])
for i in range(len(lag)):
    stdev_fast_new[i]=np.nanstd(corr_arr_fast_new[:,1,i])
plt.plot(lag,corr_mean_fast_new,'k',label='Mean',zorder=25)
y1=corr_mean_fast_new-stdev_fast_new
y2=corr_mean_fast_new+stdev_fast_new
y3=corr_mean_fast_new-2*stdev_fast_new
y4=corr_mean_fast_new+2*stdev_fast_new
plt.fill_between(lag,y1,y2,color='blue',alpha=0.5,label='1 standard deviation',zorder=10)
plt.fill_between(lag,y3,y4,color='dodgerblue',alpha=0.5,label='2 standard deviations',zorder=10)
plt.xlabel('Spatial lag, r(km)',fontsize=40)
plt.ylabel('R(r)',fontsize=40)
plt.legend(fontsize=40)
plt.xticks(fontsize=40)
plt.yticks(fontsize=40)
t=plt.gca().xaxis.get_offset_text()
t.set_size(40)
plt.grid(True)

#Figure 3: Correlation functions normalized by energy and correlation scale
cond3=lag2<=10.03

for i in range(len(corr_arr_fast)):
  cond2=lag_new_fast[i]<10
  plt.plot(lag_new_fast[i][cond2],corr_arr_fast[i][1][cond2],'peru',alpha=0.2)
plt.xlim(0,4)  
plt.plot(lag2[cond3],corr_mean_fast[cond3],'k',linewidth=2.0,label='Mean',zorder=25)
y1=corr_mean_fast-stdev_arr_fast
y2=corr_mean_fast+stdev_arr_fast
y3=corr_mean_fast-2*stdev_arr_fast
y4=corr_mean_fast+2*stdev_arr_fast
#plt.plot(lag2,corr_mean_fast+stdev_arr_fast,'r--',linewidth=2.0,label='1 standard deviation')
#plt.plot(lag2,corr_mean_fast-stdev_arr_fast,'r--',linewidth=2.0)
#plt.plot(lag2,corr_mean_fast+2*stdev_arr_fast,'b--',linewidth=2.0,label='2 standard deviations')
#plt.plot(lag2,corr_mean_fast-2*stdev_arr_fast,'b--',linewidth=2.0)
plt.fill_between(lag2[cond3],y1[cond3],y2[cond3],color='blue',alpha=0.5,label='1 standard deviation',zorder=10)
plt.fill_between(lag2[cond3],y3[cond3],y4[cond3],color='dodgerblue',alpha=0.5, label='2 standard deviations',zorder=20)
plt.xlabel(r'Spatial lag,$r/\lambda$',fontsize=40)
plt.ylabel(r'R$\left(r/\lambda\right)$',fontsize=40)
plt.legend(fontsize=30)
plt.xticks(fontsize=40)
plt.yticks(fontsize=40)
plt.grid(True)
















#Supplementary figures
#Figure showing the distribution of correlations at 1 correlation length

bins=np.logspace(-0.9,0,100)
plt.hist(corr_arr2_fast[:,1,14],bins=bins,color='blue')
plt.xscale('log')
plt.gca().xaxis.set_minor_formatter(ScalarFormatter())
plt.gca().xaxis.get_minor_formatter().set_scientific(False)
plt.gca().xaxis.set_minor_locator(MultipleLocator(0.2))
plt.rc('font',size=40)
plot_labels(r'$R(\frac{r}{\lambda})$ at $r=\lambda$','Counts')