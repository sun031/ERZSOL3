#!/usr/bin/env python

import numpy as np
from obspy.io.sac import SACTrace
import os
import subprocess

def tosac(filename, outpath, parfile="None"):
    """
    Convert to SAC format

    Parameters
    ----------
    filename : string
        the filename of waveform data

    outpath : string
        the path name saving sac file, no back slash

    parfile : string
        input pararameter file for calculating response


    """

    with open(filename, "r") as fp:
        lst = fp.readlines()

    row = lst[0].split()
    # print row

    npx = int(row[0])
    ncomp = int(row[1])

    try:
        os.makedirs(outpath)
    except:
        pass

    k = -1
    for i in range(1, npx*ncomp*2+1, 2):

        k += 1
        stno = k/ncomp + 1

        row = lst[i].split()
        # XS(JX)
        stlo = float(row[0])
        stla = 0.0
        az = float(row[1])
        kcmpnm = row[2]
        delta = float(row[3])
        npts = int(row[4])
        # reduced slowness, unit is
        pr = float(row[5])
        # reduced time, STMIN+PR*XS(JX), where STMIN is starting reduced time
        tcal = float(row[6])
        # not clear what smp mean
        smp = float(row[7])

        evla = 0.0
        evlo = 0.0

        # print stlo, az, kcmpnm, delta, npts, pr, tcal, smp

        row = lst[i+1].split()
        data = np.array(row)
        data = data.astype(np.float32)

        if parfile=="None":
            evdp = -12345.0
        else:
            with open(parfile, "r") as fp:
                parlst = fp.readlines()
                row = parlst[20].split()[0]
                evdp = float(row)

        knetwk = "S"
        kstnm = str(stno).zfill(3)
        header = {"kcmpnm":kcmpnm, "knetwk":knetwk, "kstnm":kstnm,
                  "stlo":stlo, "stla":stla,
                  "delta":delta, "npts":npts,
                  "evlo":evlo, "evla":evla, "evdp":evdp}
        sac = SACTrace(data=data, **header)
        fn = outpath + "/" + ".".join([knetwk, kstnm, "", kcmpnm, "sac"])
        # print fn
        sac.write(dest=fn)

def run_slowness(slomin, slomax, nslo, parfile):
    """
    Synthesize waveforms for each single slowness ranging from slomin to slomax

    Parameters
    ----------
    slomin : float
        minimum of slowness

    slomax : float
        maximum of slowness

    nslo : int
        number of slowness

    parfile : string
        filename of input parameters

    """

    with open(parfile, "r") as fp:
        lst = fp.readlines()

    wavfile = lst[1].split()[0]
    wavfile = wavfile[1:-1]

    # print wavfile

    for slowness in np.linspace(slomin, slomax, num=nslo, endpoint=True):

        if slomax==slomin:
            slomax = slomin + 1.0e-6

        if slomax==0.0:
            slomax = 1.0e-6

        lst[4] = "  1\n"
        lst[5] = "  %s\n" % (str(slomin))
        lst[6] = "  %s\n" % (str(slomax))

        fp = open("par.cmd", "w")
        fp.writelines(lst)
        fp.close()

        child = subprocess.Popen("erzsol3 < par.cmd > par.out", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        child.wait()

        # build directory
        outpath = str(slowness)
        try:
            os.makedirs(outpath)
        except:
            pass

        tosac(filename=wavfile, outpath=outpath, parfile="par.cmd")


if __name__=="__main__":
    # tosac(filename="../example/ew1.tx.z", outpath="../example/sac",  parfile="../example/ew1.cmd")
    # run_slowness(0.0, 0.0, nslo=1, parfile="../example/ew1.cmd")
    pass