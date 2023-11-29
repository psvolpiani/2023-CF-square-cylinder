#! /usr/bin/env python
# -*- coding:utf-8 -*-

##############################################################################80
# GRANiTA : General Reynolds Avereged Navier sTokes eqs Assimilation algorithm #
##############################################################################80

# system libraies
import sys
import os
import time
from datetime import datetime

# optimisation library
import numpy as np
from scipy.optimize import minimize


# ==============================
# Hardcoded Numerical parameters
# ==============================

# BFGS parameters
verbose       = 2             # verbosity parameter
opttoll       = 1.e-6         # optimization tolerance (def. 1.e-4)
ftoll         = 1.e-8         # optimization tolerance on obj function
gtoll         = 1.e-8         # optimization tolerance on projected gradients
maxlinsear    = 15            # (15) max. iterations for line search algo.
maxiter       = 500           # (~200-500) max. global iterations
applyBounds   = False         # apply constraints or not
initParamRANS = False         # initialize parameter by RANS data (or by zero)

# Mesh parameters
Ndof          = 30576*2       # total number of elements in the mesh
useSlurm4Jobs = False         # use Slurm job scheduling (or sends job manually)

# Paths and file names
dir           = "./results/"
outJ          = dir+"solution-mesh"
outDJ         = dir+"gradient-mesh"
fileIn        = dir+"field_param"

# Commands
commandsJ     = "FreeFem++ solver_J4.edp -nw" #-nw nowindow
commandsDJ    = "FreeFem++ solver_DJ4.edp"

try: os.mkdir('./results')
except OSError as error: print(error)

print('--- Start GRANiTA')
if (verbose>0):
    print('Initial parameters')
    print('Ndof         =',Ndof)
    print('opttoll      =',opttoll)
    print('ftloo        =',ftoll)
    print('gtoll        =',gtoll)
    print('maxlinsear   =',maxlinsear)
    print('maxiter      =',maxiter)
    print('applyBounds  =',applyBounds)
    print('initParamRANS=',initParamRANS)


# initialize by zero or read initialization RANS files
v0       = np.zeros(Ndof)
filename = fileIn+".txt"
#v0         = np.loadtxt(filename)
np.savetxt(filename,v0)
#if(initParamRANS):
#    filename   = " "
#    v0         = np.loadtxt(filename)

filename2 = open(dir+"hist-J.txt","w")
filename2.close()
filename3 = open("report.txt","w")
filename3.close()


# local iterators on getJ and getDJ calls
iterJ      = 1
iterDJ     = 1


###################################################
### Define function(s) for optimisation library ###
###################################################

def getJ(v):
    global iterJ, commandsJ
    if (verbose>9): print("  -- call to getJ:  v = ",v)
    
    # write variables as exchange file
    filename = fileIn+".txt"
    np.savetxt(filename,v)
            
    filename = fileIn+"-iter%04d.txt"%iterJ
    np.savetxt(filename,v)
    
    # --- run solver: ---
    os.system(commandsJ+" -iterJ %04d"%iterJ)
    commands = ("cp "+outJ+".txt "+outJ+"-iter%04d.txt"%iterJ)
    os.system(commands)
    print(datetime.now())

    # load newly obtained data from file
    filename = dir+"J.txt"
    J = np.loadtxt(filename)
    if (verbose>1): print("  -- J = ",J)
    filename = open(dir+"hist-J.txt","a")
    filename.write(str(iterJ)+" "+str(J)+"\n")
    filename.close()
    
    time.sleep(1)
    
    iterJ = iterJ + 1
    # output
    return J

def getdJ(v):
    global iterDJ, commandsDJ
    if (verbose>9): print("  -- call to getdJ: v = ",v)
    
    # --- run solver for the gradient (adjoint, etc...) ---
    os.system(commandsDJ)
    commands = ("cp "+outDJ+".txt "+outDJ+"-iter%04d.txt"%iterDJ)
    os.system(commands)

    # load newly generated data from file(s)
    filename   = outDJ+"-iter%04d.txt"%iterDJ
    dJ         = np.loadtxt(filename)
        
    iterDJ = iterDJ + 1
    # output
    return dJ


# ============
# Optimisation
# ============

if (verbose>0): print(); print('Start optimisation:')

res = minimize(getJ, v0, method='L-BFGS-B',jac=getdJ, tol=opttoll, bounds=None,
	    options={'maxls': maxlinsear, 'maxiter': maxiter, 'ftol': ftoll, 'gtol': gtoll, 'disp': (verbose>1)})
v = res.x

# display result
if (verbose>0): print("Optimal parameters: ")
if (verbose>9): print(v)
if (verbose>0): print(); print('End of Optimisation:')

# write variables as exchange file
filename = fileIn+"_opt.txt"
np.savetxt(filename,v)

print("--- End GRANiTA")
