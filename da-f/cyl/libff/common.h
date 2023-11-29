include "getARGV.idp"
load "MUMPS_seq"
load "bfstream"

// physical parameters
real Re		= 22000;
real nu         = 1./Re;

bool waitplt    = false; // flag to wait after plot

// mesh and FEM spaces

int nummesh = 21; // Numero maillage reprise
mesh th     = readmesh("../../mesh/mesh.msh");
int k       = 1; // degree of the polynoms (2 for P2dc ...)
int kp      = 1; //Order of interpolation for the pressure
int qfo     = 3*k+1; //order of quadrature
real order  = 1.; // order in space
real dimensionTau = 2.; // number of dimension
real c1     = 4;
real c2     = sqrt(c1);

// Mesh Building

fespace f2212(th,[P1b,P1b,P1,P1]);
fespace f221(th,[P1b,P1b,P1]);
fespace f22(th,[P1b,P1b]);
fespace f11(th,[P1,P1]);
fespace f0(th,P0);
fespace f1(th,P1);
fespace f2(th,P2);

string fileoutput="report.txt";

