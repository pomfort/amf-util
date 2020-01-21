#!/bin/bash

# /Users/ptr/Development/ACES/amf-util/scripts/../Material/amf/LogCEI800-Rec.709100nitsdim.amf
# created by amf-util 0.0.2
# transforms:
#   IDT: IDT.ARRI.Alexa-v3-logC-EI800.a1.v2 (ACES 1.0 Input - ARRI V3 LogC (EI800))
#   RRT: RRT.a1.0.3 (ACES 1.0 - RRT)
#   ODT: ODT.Academy.Rec709_100nits_dim.a1.0.3 (ACES 1.0 Output - Rec.709)

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
     -ctl /Users/ptr/Development/ACES/amf-util/scripts/../../ACES-LUTs/aces-dev-1.2.0/transforms/ctl/odt/rec709/ODT.Academy.Rec709_100nits_dim.ctl \
     -param1 aIn 1.0 \
     -force \
     "$INPUTIMAGEPATH" \
     "$OUTPUTIMAGEPATH"

