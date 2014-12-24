#!/bin/sh
# create  inkscope location conf and scripts

INKPATHETC='/opt/inkscope/etc'
INKPATHBIN='/opt/inkscope/bin'

mkdir -pv $INKPATHETC $INKPATHBIN
cp inkscope-template.conf $INKPATHETC/inkscope.conf
cp inkscopeProbe/cephprobe.py $INKPATHBIN
cp inkscopeProbe/sysprobe.py  $INKPATHBIN
cp inkscopeProbe/daemon.py  $INKPATHBIN