#!/usr/bin/env python

# script for calculating stress tensor and Pi-D using curlometer

import numpy as np
import sys
import os
import readline
import pandas as pd

#===============================================================

def cross(ax,ay,az,bx,by,bz): 	# Cross pdt of a and b vector

	cx = (ay*bz - az*by)
	cy = -(ax*bz - az*bx)
	cz = (ax*by - ay*bx)

	return cx,cy,cz

def dot(ax,ay,az,bx,by,bz):	# Dot pdt of a and b vector

	return ax*bx + ay*by + az*bz	

def grad(x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4,bx1,by1,bz1,bx2,by2,bz2,bx3,by3,bz3,bx4,by4,bz4):   # From data file

   x12=x2-x1; y12=y2-y1; z12=z2-z1
   x13=x3-x1; y13=y3-y1; z13=z3-z1
   x14=x4-x1; y14=y4-y1; z14=z4-z1
   x23=x3-x2; y23=y3-y2; z23=z3-z2
   x24=x4-x2; y24=y4-y2; z24=z4-z2
   x34=x4-x3; y34=y4-y3; z34=z4-z3

   x2324,y2324,z2324 = cross(x23,y23,z23,x24,y24,z24)
   kx1,ky1,kz1 = cross(x23,y23,z23,x24,y24,z24)/\
   dot(-x12,-y12,-z12,x2324,y2324,z2324)

   x3431,y3431,z3431 = cross(x34,y34,z34,-x13,-y13,-z13)
   kx2,ky2,kz2 = cross(x34,y34,z34,-x13,-y13,-z13)/\
   dot(-x23,-y23,-z23,x3431,y3431,z3431)

   x4142,y4142,z4142 = cross(-x14,-y14,-z14,-x24,-y24,-z24)
   kx3,ky3,kz3 = cross(-x14,-y14,-z14,-x24,-y24,-z24)\
   /dot(-x34,-y34,-z34,x4142,y4142,z4142)

   x1213,y1213,z1213 = cross(x12,y12,z12,x13,y13,z13)

   kx4,ky4,kz4 = cross(x12,y12,z12,x13,y13,z13)/\
   dot(x14,y14,z14,x1213,y1213,z1213)

   divb = dot(kx1,ky1,kz1,bx1,by1,bz1)+dot(kx2,ky2,kz2,bx2,by2,bz2)\
   +dot(kx3,ky3,kz3,bx3,by3,bz3)+dot(kx4,ky4,kz4,bx4,by4,bz4)

   dxbx = kx1*bx1 + kx2*bx2 + kx3*bx3 + kx4*bx4
   dxby = kx1*by1 + kx2*by2 + kx3*by3 + kx4*by4		# D_ij = d_i(b_j)
   dxbz = kx1*bz1 + kx2*bz2 + kx3*bz3 + kx4*bz4	
   dybx = ky1*bx1 + ky2*bx2 + ky3*bx3 + ky4*bx4
   dyby = ky1*by1 + ky2*by2 + ky3*by3 + ky4*by4
   dybz = ky1*bz1 + ky2*bz2 + ky3*bz3 + ky4*bz4
   dzbx = kz1*bx1 + kz2*bx2 + kz3*bx3 + kz4*bx4
   dzby = kz1*by1 + kz2*by2 + kz3*by3 + kz4*by4
   dzbz = kz1*bz1 + kz2*bz2 + kz3*bz3 + kz4*bz4

   return divb,dxbx,dxby,dxbz,dyby,dybx,dybz,dzbx,dzby,dzbz

pi = np.pi

def readFile(var):

	#print "Pl. enter the file to read %s"%(var)
	#f = raw_input(readline.parse_and_bind("tab: complete"))
	d = np.loadtxt('%s_resNi_1.dat'%(var))
	n = len(d[:,0])
	print(n)
	b = np.zeros((4,n)) 	# Time and all 3 components in 1 array

	b[0][:] = d[:,0]
	b[1][:] = d[:,1]
	b[2][:] = d[:,2]
	b[3][:] = d[:,3]
	#print b
	return b

base_dir = r'/data/MMS_ANALYSIS/MMS_DATA/ywwang_data_50int'
date_arg = sys.argv[1]
interval_arg = sys.arg[2]

b1 = readFile('Vi_1')
b2 = readFile('Vi_2')
b3 = readFile('Vi_3')
b4 = readFile('Vi_4')

r1 = readFile('R1')
r2 = readFile('R2')
r3 = readFile('R3')
r4 = readFile('R4')

# D_ij calculation from V
# Input:  v, positions from all 4 s/c
# Output: divU and other derivs

tb1=b1[0]; bx1=b1[1]; by1=b1[2]; bz1=b1[3]
tr1=r1[0]; x1=r1[1]; y1=r1[2]; z1=r1[3]

tb2=b2[0]; bx2=b2[1]; by2=b2[2]; bz2=b2[3]
tr2=r2[0]; x2=r2[1]; y2=r2[2]; z2=r2[3]

tb3=b3[0]; bx3=b3[1]; by3=b3[2]; bz3=b3[3]
tr3=r3[0]; x3=r3[1]; y3=r3[2]; z3=r3[3]

tb4=b4[0]; bx4=b4[1]; by4=b4[2]; bz4=b4[3]
tr4=r4[0]; x4=r4[1]; y4=r4[2]; z4=r4[3]

# Check if all time arrays are identical
if np.array_equal(tb1,tr1)==True and np.array_equal(tb1,tb2)==True and np.array_equal(tb1,tr2)==True and np.array_equal(tb1,tb3)==True and np.array_equal(tb1,tr3)==True and np.array_equal(tb1,tb4)==True and np.array_equal(tb1,tr4)==True:

   print("All time arrays compatible")
   n_tot = len(tb1)
   divB = np.zeros(n_tot)
   dxux = np.zeros(n_tot)
   dxuy = np.zeros(n_tot)
   dxuz = np.zeros(n_tot)
   dyux = np.zeros(n_tot)
   dyuy = np.zeros(n_tot)
   dyuz = np.zeros(n_tot)
   dzux = np.zeros(n_tot)
   dzuy = np.zeros(n_tot)
   dzuz = np.zeros(n_tot)

   for j in range(n_tot):
      divB[j],dxux[j],dxuy[j],dxuz[j],dyux[j],dyuy[j],dyuz[j],dzux[j],dzuy[j],dzuz[j] \
      = grad(x1[j],y1[j],z1[j],x2[j],y2[j],z2[j],x3[j],\
		y3[j],z3[j],x4[j],y4[j],z4[j],bx1[j],by1[j],bz1[j],bx2[j],by2[j],\
      bz2[j],bx3[j],by3[j],bz3[j],bx4[j],by4[j],bz4[j])

else:
   print("Time arrays not compatible")

tP = tb1

# Read pressure tensor
f = 'Pi_tensor_1_resNi_1.dat'
Ptensor = np.loadtxt(f)
Pxx1 = Ptensor[:,1]; Pxy1 = Ptensor[:,2]; Pxz1 = Ptensor[:,3]
Pyx1 = Ptensor[:,4]; Pyy1 = Ptensor[:,5]; Pyz1 = Ptensor[:,6]
Pzx1 = Ptensor[:,7]; Pzy1 = Ptensor[:,8]; Pzz1 = Ptensor[:,9]

f = 'Pi_tensor_2_resNi_1.dat'
Ptensor = np.loadtxt(f)
Pxx2 = Ptensor[:,1]; Pxy2 = Ptensor[:,2]; Pxz2 = Ptensor[:,3]
Pyx2 = Ptensor[:,4]; Pyy2 = Ptensor[:,5]; Pyz2 = Ptensor[:,6]
Pzx2 = Ptensor[:,7]; Pzy2 = Ptensor[:,8]; Pzz2 = Ptensor[:,9]

f = 'Pi_tensor_3_resNi_1.dat'
Ptensor = np.loadtxt(f)
Pxx3 = Ptensor[:,1]; Pxy3 = Ptensor[:,2]; Pxz3 = Ptensor[:,3]
Pyx3 = Ptensor[:,4]; Pyy3 = Ptensor[:,5]; Pyz3 = Ptensor[:,6]
Pzx3 = Ptensor[:,7]; Pzy3 = Ptensor[:,8]; Pzz3 = Ptensor[:,9]

f = 'Pi_tensor_4_resNi_1.dat'
Ptensor = np.loadtxt(f)
Pxx4 = Ptensor[:,1]; Pxy4 = Ptensor[:,2]; Pxz4 = Ptensor[:,3]
Pyx4 = Ptensor[:,4]; Pyy4 = Ptensor[:,5]; Pyz4 = Ptensor[:,6]
Pzx4 = Ptensor[:,7]; Pzy4 = Ptensor[:,8]; Pzz4 = Ptensor[:,9]

Pxx = (Pxx1+Pxx2+Pxx3+Pxx4)/4.
Pxy = (Pxy1+Pxy2+Pxy3+Pxy4)/4.
Pxz = (Pxz1+Pxz2+Pxz3+Pxz4)/4.
Pyx = (Pyx1+Pyx2+Pyx3+Pyx4)/4.
Pyy = (Pyy1+Pyy2+Pyy3+Pyy4)/4.
Pyz = (Pyz1+Pyz2+Pyz3+Pyz4)/4.
Pzx = (Pzx1+Pzx2+Pzx3+Pzx4)/4.
Pzy = (Pzy1+Pzy2+Pzy3+Pzy4)/4.
Pzz = (Pzz1+Pzz2+Pzz3+Pzz4)/4.

Dxx = dxux-(divB/3.0); Dxy = 0.5*(dxuy+dyux); Dyx = Dxy
Dyy = dyuy-(divB/3.0); Dxz = 0.5*(dxuz+dzux); Dzx = Dxz
Dzz = dzuz-(divB/3.0); Dyz = 0.5*(dyuz+dzuy); Dzy = Dyz

t01 = pd.to_datetime(tP[0],unit='s')
t02 = pd.to_datetime(tP[-1],unit='s')

np.savetxt('./Pi_tensor_resNi_1.dat', np.c_[tP, Pxx, Pxy, Pxz, Pyx, Pyy, Pyz, Pzx, Pzy, Pzz])
np.savetxt('./DijDij_i_resNi_1_%s-%s-%s_%02d%02d%02d.dat'%(t01.year,t01.month,t01.day,t01.hour,t01.minute,t01.second), np.c_[tP, Dxx, Dxy, Dxz, Dyx, Dyy, Dyz, Dzx, Dzy, Dzz])

p = (Pxx+Pyy+Pzz)/3.0
ptheta = p*divB
PiD = (Pxx-p)*Dxx+(Pyy-p)*Dyy+(Pzz-p)*Dzz+\
     Pxy*Dxy+Pxz*Dxz+Pyx*Dyx+Pyz*Dyz+Pzx*Dzx+Pzy*Dzy

np.savetxt('./thi_resNi_1_%s-%s-%s_%02d%02d%02d.dat'%(t01.year,t01.month,t01.day,t01.hour,t01.minute,t01.second), np.c_[tP, divB])
np.savetxt('./pthi_resNi_1_%s-%s-%s_%02d%02d%02d.dat'%(t01.year,t01.month,t01.day,t01.hour,t01.minute,t01.second), np.c_[tP, ptheta])
np.savetxt('./pidi_resNi_1_%s-%s-%s_%02d%02d%02d.dat'%(t01.year,t01.month,t01.day,t01.hour,t01.minute,t01.second), np.c_[tP, PiD])





