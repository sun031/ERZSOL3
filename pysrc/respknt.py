#!/usr/bin/env python

import numpy as np
from obspy.io.sac import SACTrace
import os

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





if __name__=="__main__":
    tosac(filename="../example/ew1.tx.z", outpath="../example/sac",  parfile="../example/ew1.cmd")