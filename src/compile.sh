#!/bin/sh

g95 -o erzsol3  erzsol3.f qbessel.f qfcoolr.f
g95 -o zst-s    zst.f ps_rpost.f bpltlib.f

mv erzsol3 ../bin
mv zst-s ../bin