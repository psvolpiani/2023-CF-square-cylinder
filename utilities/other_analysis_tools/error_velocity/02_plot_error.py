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



directory1 = './'
file1 = directory1+'error_field_baseline.dat'
header1 = 3
nvar1 = 3
label1 = 'RANS - SA'



case='f'
directory2 = './'
file2 = directory2+'error_field_f.dat'
header2 = 3
nvar2 = 3
label2 = 'DA - f'



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
# Plot 
# -----------------------------------------------------------------------------------------
print('\n Plotting error... \n')

ei1 = data1.interp(data1.e)
ei2 = data2.interp(data2.e)




min=0.;
max=0.3;
lev=6;

plot_contour(data1,ei1, ref_length = C, filename = '../../figures/error_field_baseline.png', vmin =0.0, vmax = 1.0, nlevels = lev)


min1=0.;
max1=0.03;
lev1=6;

plot_contour(data2,ei2, ref_length = C, filename = '../../figures/error_field_f.png', vmin =0., vmax = 1., nlevels = 6)






