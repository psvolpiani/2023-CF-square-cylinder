#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys
from libplot import *
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------
C    = 1
Uref = 1.
h = 1
Pref=101325.


directory1 = './'
file1 = directory1+'forcedns.dat'
header1 = 3
nvar1 = 4
label1 = 'DNS'




case='f'

directory2 = './'
file2 = directory2+'forceda.dat'
header2 = 3
nvar2 = 4
label2 = 'DA - '+ case



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



# -----------------------------------------------------------------------------------------
# Plot forces/stresses
# -----------------------------------------------------------------------------------------
print('\n Plotting forces/stresses... \n')

ui1 = data1.interpdns(data1.u)
ui2 = data2.interp(data2.u)



filename = '../../figures/totalforcex-dns-f.png'


plot_contour_compared(data1,ui1,data2,ui2, ref_length = C, filename = filename, vmin = -1.5, vmax = 1.5, nlevels = 10)




