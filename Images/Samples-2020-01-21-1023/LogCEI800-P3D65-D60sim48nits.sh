#!/bin/bash

# /Users/ptr/Development/ACES/amf-util/scripts/../Material/amf/LogCEI800-P3D65-D60sim48nits.amf
# created by amf-util 0.0.2
# transforms:
#   IDT: IDT.ARRI.Alexa-v3-logC-EI800.a1.v2 (ACES 1.0 Input - ARRI V3 LogC (EI800))
#   RRT: RRT.a1.0.3 (ACES 1.0 - RRT)
#   ODT: ODT.Academy.P3D65_D60sim_48nits.a1.1.0 (ACES 1.0 Output - P3D65 (D60 simulation))

CTLRENDER=`which ctlrender`

if [ -z "$1" ] || [ -z "$2" ]
then
     echo "Usage: [script name] path/to/input-file.[tiff|dpx|exr] path/to/output-file.[tiff|dpx|exr]"
     echo
     exit 200
fi

INPUTIMAGEPATH=$1
OUTPUTIMAGEPATH=$2

export CTL_MODULE_PATH="/Users/ptr/Development/ACES/amf-util/scripts/../../ACES-LUTs/aces-dev-1.2.0/transforms/ctl/utilities/"

$CTLRENDER \
     -ctl /Users/ptr/Development/ACES/amf-util/scripts/../../ACES-LUTs/aces-dev-1.2.0/transforms/ctl/idt/vendorSupplied/arri/alexa/v3/EI800/IDT.ARRI.Alexa-v3-logC-EI800.ctl \
     -param1 aIn 1.0 \
     -ctl /Users/ptr/Development/ACES/amf-util/scripts/../../ACES-LUTs/aces-dev-1.2.0/transforms/ctl/rrt/RRT.ctl \
     -param1 aIn 1.0 \
     -ctl /Users/ptr/Development/ACES/amf-util/scripts/../../ACES-LUTs/aces-dev-1.2.0/transforms/ctl/odt/p3/ODT.Academy.P3D65_D60sim_48nits.ctl \
     -param1 aIn 1.0 \
     -force \
     "$INPUTIMAGEPATH" \
     "$OUTPUTIMAGEPATH"

