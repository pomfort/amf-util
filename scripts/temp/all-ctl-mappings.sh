#!/bin/bash

# call from root amf-util root directory as 
# $ ./scripts/temp/all-ctl-mappings.sh

mkdir -p Material/mappings
mkdir -p Material/mappings/logs

./amf-util.py ctls ../ACES-LUTs/aces-dev-1.0.0/ > Material/mappings/aces-dev-1.0.0.txt 2> Material/mappings/logs/aces-dev-1.0.0.log
./amf-util.py ctls ../ACES-LUTs/aces-dev-1.0.1/ > Material/mappings/aces-dev-1.0.1.txt 2> Material/mappings/logs/aces-dev-1.0.1.log
./amf-util.py ctls ../ACES-LUTs/aces-dev-1.0.2/ > Material/mappings/aces-dev-1.0.2.txt 2> Material/mappings/logs/aces-dev-1.0.2.log
./amf-util.py ctls ../ACES-LUTs/aces-dev-1.0.3/ > Material/mappings/aces-dev-1.0.3.txt 2> Material/mappings/logs/aces-dev-1.0.3.log
./amf-util.py ctls ../ACES-LUTs/aces-dev-1.1.0/ > Material/mappings/aces-dev-1.1.0.txt 2> Material/mappings/logs/aces-dev-1.1.0.log
