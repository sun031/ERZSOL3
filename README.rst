*******************************************************
Calculating the elastic response of a stratified medium
*******************************************************

I have changed the code to run more flexible and easier.

Weijia Sun

Updated on 19 August 2017

Changes
-------
1. Change line 136 of qbessel.f from

>>> COMPLEX FUNCTION BESHS0*16(X, IFAIL)

to

>>> COMPLEX FUNCTION BESHS0(X, IFAIL)

, so that the compilation could be successful.

2. Change the output seismogram from unformatted to text format.

3. Add some python scripts convert the wavefroms into SAC format.

Notes
-----
sac.user0 : 

sac.user1 : 

Parameters
----------
XS : float, array_like
	XS -- Station position, ranges in km
	
AZ : float, array_like
	Azimuth from North (X-axis) in degree
	
CZC : character*4
	: "Z"
	
CRC : character*4
	: "R"

CTC : character*4
	: "T"
	
DELT: float
	Time sampling interval in second

NT : int
	Sampling number, must be FFT length, e.g., 1024, 2048, 4096
	
PR : float, unit might be s/km
	Reduced slowness
	
STMIN : float
	starting reduced time
	
TCAL : float
	Reduced time, STMIN+PR*XS(JX)

	
