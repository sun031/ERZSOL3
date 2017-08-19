
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
	
PR : float
	Reduced slowness
	
STMIN : float
	starting reduced time
	
TCAL : float
	Reduced time, STMIN+PR*XS(JX)

	
