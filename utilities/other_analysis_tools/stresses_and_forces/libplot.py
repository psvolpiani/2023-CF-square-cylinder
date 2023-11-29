import numpy as np
import operator
from scipy.interpolate import griddata
from math import *
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import ticker as tk 


rc('text', usetex=True)
rc('font', family='serif')
rc('lines', linewidth=1.)
rc('font', size=16)
plt.rc('legend',**{'fontsize':10})
plt.rc({'axes.labelsize': 20})

#===============================================================
# PROFILE FUNCTION
#===============================================================

def bump(x,nummesh):
    C      = 305.0 /1000.0;
    L      = C - 2.0 * ( C / 12.0 );
    R1     = 0.323 * C;
    hp     = R1 - sqrt( R1**2 - ((C-L)/2.0)**2 );
    hoC    = nummesh / 305.0;
    h      = hoC * C;
    hpp    = h - hp;
    R2     = ( hpp**2 + (L/2.0)**2 ) / ( 2.0 * hpp ) ;
      
    if (x<0. ):
      y = 0.
    elif (x>=0.  and x<C/12.0 ):
      y = (R1-sqrt(R1**2-x**2))
    elif (x>=C/12.0 and x<L+C/12.0 ):
      y = (-R2+h+sqrt(R2**2-(C/2.0-x)**2))
    elif (x>=L+C/12.0 and x<C ):
      x = x-C
      y = (R1-sqrt(R1**2-x**2))
    else: y=0.
    
    return y
 
        
#===============================================================
# DATASET CLASS
#===============================================================
class Data:
    
    def read(self, file, header_size, nvar, connectivity = False):
        print('Loading data...\n')
        
        data            = []            # Initialize data array
        connect         = []
        
        print('File: '+ file)
        
        eof = False
        i = 0
        nodes = 1
        elements = 1
            
        with open(file) as f:
            while eof == False:
                line = f.readline()
                if (i == header_size - 1):
                    nodes = int(line[line.find('N=')+2:line.find('E=')-1])
                    elements = int(line[line.find('E=')+2:line.find(',',line.find('E='))])
                    
                elif (i > header_size - 1 and i < header_size + nodes):
                    myarray = np.fromstring(line, dtype=float, sep=' ')
                    data = np.concatenate([data , myarray])
                
                elif (i >= header_size + nodes and i < header_size + nodes + elements) :
                    if connectivity:
                        myarray = np.fromstring(line, dtype=int, sep=' ')
                        connect = np.concatenate([connect,myarray])
                    else:
                        break
                elif (i == header_size + nodes + elements):
                    break
                
                i+=1
                    
        # Reshape data so that we have blocks of lines corresponding to each case 
        self.size       = nodes    # Total size of data with all the cases
        self.base       = np.reshape(data, (self.size,nvar))
        if connectivity:
            self.connectivity    = np.reshape(connect,(elements,3))
        self.nvar       = nvar
        
        self.x = self.base[:,0]
        self.y = self.base[:,1]
        self.u = self.base[:,2]
        self.v = self.base[:,3]
        
   
        
    def grid(self, h, nx, ny):
        # Create grid values first.
        self.xi = np.linspace(min(self.x), max(self.x), nx)
        self.yi = np.linspace(min(self.y), max(self.y), ny)
        self.h  = h
        


    def interp(self, var):
        # Perform linear interpolation of the data (x,y) on a grid defined by (xi,yi)
        vari = griddata((self.x, self.y), var, (self.xi[None,:], self.yi[:,None]), method='linear')
        
        for i in range (0,len(self.xi)):
          for j in range (0,len(self.yi)):
            if (self.yi[j] <= self.h/2 and self.yi[j] >= -self.h/2 and self.xi[i] <= self.h/2 and self.xi[i] >= -self.h/2):
                vari[j,i] = np.nan
                
        return vari
        
        
        
    def interpdns(self, var):
        # Perform linear interpolation of the data (x,y) on a grid defined by (xi,yi)
        vari = griddata((self.x, self.y), var, (self.xi[None,:], self.yi[:,None]), method='linear')
        
        for i in range (0,len(self.xi)):
          for j in range (0,len(self.yi)):
            if (self.yi[j] >= 0):
                vari[j,i] = np.nan
                            
            elif (self.xi[i] >= -0.5 and self.xi[i] <= 0.5 and self.yi[j] >= -0.5):
                vari[j,i] = np.nan
                
        return vari
        
  
    
def plot_contour_compared(data1, vari1, data2 = None, vari2 = None, data3 = None, vari3 = None, ref_length = 1.0, filename = 'countour.png', vmin = -0.2, vmax = 1.4, nlevels = 17, title=None):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot([-10,15],[0, 0],linewidth=1.5,color='gray')

    cntr = ax.contourf(data1.xi/ref_length,data1.yi/ref_length,vari1, np.linspace(vmin,vmax,nlevels), cmap="jet", vmin = vmin, vmax = vmax, extend='both')
    

    
    
    if data2 is not None:
        cntr = ax.contourf(data2.xi/ref_length,data2.yi/ref_length,vari2, np.linspace(vmin,vmax,nlevels), cmap="jet", vmin = vmin, vmax = vmax, extend='both')

    if data3 is not None:
        plt.contour(data3.xi/ref_length,data3.yi/ref_length,vari3,np.linspace(vmin,vmax,nlevels),linewidths=0.5,colors='k', linestyles = 'dashdot', vmin = vmin, vmax = vmax)
        
    

    ax.set_ylim([-1.5, 1.5])
    ax.set_xlim([-1, 2])
    
    bounds = [vmin, 0, vmax]
    fig.colorbar(cntr, ax=ax, format='%.1f',ticks=bounds)
    
    if title is not None:
    
        ax.set_title(title,fontsize=17)
    
        
    ax.text(-0.8,1.2,'DA',fontsize=14)
    #ax.text(-2.8,2.5,'RANS',fontsize=14)
        
    ax.text(-0.8,-1.4,'DNS',fontsize=14)
    
    
    
    
    ax.set_xlabel( r"$x/L$",fontsize=17)
    ax.set_ylabel( r"$y/L$",fontsize=17)
    fig.subplots_adjust(bottom=0.18)
    fig.savefig(filename, dpi=600, bbox_inches='tight')
    plt.show()

