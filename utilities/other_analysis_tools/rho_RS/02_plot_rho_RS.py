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
file1 = directory1+'boussinesq_rho.dat'
header1 = 3
nvar1 = 3
label1 = 'DNS'




data1 = Data()
data1.read(file1, header1, nvar1)
data1.grid(h,4000,4000)
data1.label = label1



# -----------------------------------------------------------------------------------------
# Plot
# -----------------------------------------------------------------------------------------
print('\n Plotting rho_RS... \n')

ri1 = data1.interp(data1.r)



filename = '../../figures/rhors.png'

plot_contour(data1,ri1, ref_length = C, filename = filename, vmin = 0, vmax = 1.0, nlevels = 11)
