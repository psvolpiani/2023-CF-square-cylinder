#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys
from libplot import *
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------
C    = 1.
Uref = 1.
h = 1.
Pref=101325.


directory1 = './solution_fields/DNS/'
file1 = directory1+'reference-solution-Re-22000.dat'
header1 = 3
nvar1 = 6
label1 = 'DNS'





directory2 = './solution_fields/RANS-SA/'
file2 = directory2+'baseline-solution-Re-22000.dat'
header2 = 3
nvar2 = 6
label2 = 'RANS - SA'



case='f'

directory3 = './solution_fields/DA/da-'+case+'/'
file3 = directory3+'da_'+case+'.dat'
header3 = 3
nvar3 = 8
label3 = 'DA - '+ case




# -----------------------------------------------------------------------------------------
# Read files
# -----------------------------------------------------------------------------------------


data1 = Data()
data1.read(file1, header1, nvar1)
data1.grid(h,4000,4000)
data1.label = label1

data2 = Data()
data2.read(file2, header2, nvar2)
data2.grid(h,4000,4000)
data2.label = label2


data3 = Data()
data3.read(file3, header3, nvar3)
data3.grid(h,4000,4000)
data3.label = label3


# -----------------------------------------------------------------------------------------
# Plot horizontal velocity contour
# -----------------------------------------------------------------------------------------
print('\n Plotting horizontal velocity contour... \n')

ui1 = data1.interpdns(data1.u)
ui2 = data2.interp(data2.u)
ui3 = data3.interp(data3.u)

filename = './figures/u-baseline.png'


plot_contour_u_baseline(data1,ui1/Uref, data2,ui2/Uref, ref_length = C, filename = filename, vmin = -0.5, vmax = 1.5, nlevels = 17)


filename = './figures/u-f.png'

plot_contour_u(data1,ui1/Uref, data3,ui3/Uref, ref_length = C, filename = filename, vmin = -0.5, vmax = 1.5, nlevels = 17)

