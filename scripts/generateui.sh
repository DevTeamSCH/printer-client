#!/usr/bin/env bash
for i in ../design/*.ui; do
    [ -f "$i" ] || break
    basename=`basename $i .ui`
    pyuic5 $i > design/${basename}_ui.py
done
