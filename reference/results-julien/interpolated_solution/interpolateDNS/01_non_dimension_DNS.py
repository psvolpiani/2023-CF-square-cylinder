#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys
import matplotlib.pyplot as plt
import numpy as np
from numpy import *


dimDNS = open('../../full_solution/moy_DNS_cyl_22k_point.dat')
print('Data opened...\n')
ndDNS = open('nd_moy_DNS_cyl_22k_point.dat','w')

data            = []

i=0

I=0
J=0

block=-1

nodes=0
cumulativenodes=0

header_size=40


Gamma = 1.4
Rgas = 287.
Reynolds = 22000 #4000
Pdon = 101325.
Tdon = 293.
Mach = 0.0969

# Compute reference quantities
TisT = 1.+0.5*(Gamma-1.)*Mach**2

Pinf=Pdon
Tinf=Tdon

Pi_inf=Pinf*(TisT**(Gamma/(Gamma-1.)))
Ti_inf=Tinf*TisT

rinf = Pinf/(Rgas*Tinf)

Ainf = (Gamma*Rgas*Tinf)**.5

Uinf = Mach*Ainf
     

#Uinf=34
#rinf=1.19402
#Pinf=Pdon


# Read in the file once and build a list of line offsets
#line_offset = []
#offset = 0
#for line in dimDNS:
#    line_offset.append(offset)
#    offset += len(line)
#dimDNS.seek(0)



for line in dimDNS:
        
    #if (i <= header_size - 1):
    
        #ndDNS.write(line)
        
        
    if 'K=1' in line:
        block=block+1
        I = int(line[line.find('I=')+2:line.find(', J')])
        J = int(line[line.find('J=')+2:line.find(', K')])
                
        cumulativenodes=cumulativenodes+nodes
       
        nodes=I*J
        
       
        
    #if (i > (header_size - 1) and i < (header_size + nodes) ):
    
    if (i > (header_size - 1)+cumulativenodes+block*7 and i < (header_size + nodes)+cumulativenodes+block*7 ):
     
        myarray = np.fromstring(line, dtype=float, sep=' ')
        
        
        ndX="{:e}".format(myarray[0]*100.0+0.5) #X
        ndY="{:e}".format(myarray[1]*100.0+0.5)  #Y
        ndZ="{:e}".format(myarray[2]*0.0)               #Z
        ndr="{:e}".format(myarray[3]/rinf)  #r
        ndu="{:e}".format(myarray[4]/Uinf)  #u
        ndv="{:e}".format(myarray[5]/Uinf) #v
        ndw="{:e}".format(myarray[6]/Uinf)  #w
        ndp="{:e}".format(myarray[7]/Pinf)  #p
        ndp2="{:e}".format(myarray[8]/(Pinf**2))   #p^2
        visceddy="{:e}".format(myarray[9])        #ViscEddy     CHECK DIMENSIONLESS (DIVIDE BY REYNOLDS)
        ndru="{:e}".format(myarray[10]/(rinf*Uinf))  #ru
        ndrv="{:e}".format(myarray[11]/(rinf*Uinf))  #rv
        ndrw="{:e}".format(myarray[12]/(rinf*Uinf))  #rw
        ndruu="{:e}".format(myarray[13]/(rinf*Uinf*Uinf))  #ru^2
        ndrvv="{:e}".format(myarray[14]/(rinf*Uinf*Uinf))  #rv^2
        ndrww="{:e}".format(myarray[15]/(rinf*Uinf*Uinf))  #rw^2
        ndruv="{:e}".format(myarray[16]/(rinf*Uinf*Uinf))  #ruv
        ndruw="{:e}".format(myarray[17]/(rinf*Uinf*Uinf))  #ruw
        ndrvw="{:e}".format(myarray[18]/(rinf*Uinf*Uinf))  #rvw
        ndurms="{:e}".format(myarray[19]/Uinf)  #urms
        ndvrms="{:e}".format(myarray[20]/Uinf)  #vrms
        ndwrms="{:e}".format(myarray[21]/Uinf)  #wrms
        ndutvt="{:e}".format(myarray[22]/(Uinf*Uinf))  #u'v'
        ndutwt="{:e}".format(myarray[23]/(Uinf*Uinf))  #u'w'
        ndvtwt="{:e}".format(myarray[24]/(Uinf*Uinf))  #v'w'
        
        
        data = np.concatenate([data , myarray])
        
        
        #str1=' '+ndX+' '+ndY+' '+ndZ+' '+ndr+' '+ndu+' '+ndv+' '+ndw+' '+ndp+' '+ndp2+' '+visceddy+' '+ndru+' '+ndrv+' '+ndrw+' '+ndruu+' '+ndrvv+' '+ndrww+' '+ndruv+' '+ndruw+' '+ndurms+' '+ndvrms+' '+ndwrms+' '+ndutvt+' '+ndutwt+' '+ndvtwt
        str1=' '+ndX+' '+ndY+' '+ndZ+' '+ndr+' '+ndu+' '+ndv+' '+ndw+' '+ndp+' '+ndp2+' '+visceddy+' '+ndru+' '+ndrv+' '+ndrw+' '+ndruu+' '+ndrvv+' '+ndrww+' '+ndruv+' '+ndruw+' '+ndrvw+' '+ndurms+' '+ndvrms+' '+ndwrms+' '+ndutvt+' '+ndutwt+' '+ndvtwt
        #str1=' '+ndX+' '+ndY
        ndDNS.write(str1+'\n')
        #ndDNS.write(line)
    
    else:
    
        ndDNS.write(line)
    
                
    #if (i >= (header_size + nodes) ):
    
     #   ndDNS.write(line)
    
    #if (i >= (header_size + nodes+6) ):
    
     #   break
    
    i+=1



ndDNS.close()
