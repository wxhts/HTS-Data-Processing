#!/bin/bash
for f in /cygdrive/c/30KSet/*.csv
do
	sed -i '1d' $f
done 

