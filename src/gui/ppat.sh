#!/bin/sh -x
source /etc/profile.d/modules.sh
module load python/3.3

cd /Home/eic/PPAT/
python ppat.py PPATConfig_EiC.xml
