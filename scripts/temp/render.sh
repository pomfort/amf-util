
# -- start of script --

# /Users/ptr/Development/ACES/amf-util/scripts/../Material/amf/example2.amf
# created by amf-util 0.0.2
# transforms:
#   IDT: IDT.Acme.Camera.a1.v1 (IDT from Acme Camera Company)
#   RRT: RRT.a1.0.3 (ACES v1.0.3 RRT)
#   ODT: ODT.Academy.P3D60_48nits.a1.0.3 (P3D60 ODT)

CTLRENDER=`which ctlrender`


if [ -z "$1" ] || [ -z "$2" ]
then
	echo "Usage: [script name] path/to/input-file.[tiff|dpx|exr] path/to/output-file.[tiff|dpx|exr]"
	echo
	exit 200
fi

INPUTIMAGEPATH=$1
OUTPUTIMAGEPATH=$2

export CTL_MODULE_PATH="/Users/ptr/Development/ACES/amf-util/scripts/../../ACES-LUTs/aces-dev-1.1.0/transforms/ctl/utilities/"

$CTLRENDER \
     # skipping IDT.Acme.Camera.a1.v1 [applied="true"]
     -ctl /Users/ptr/Development/ACES/amf-util/scripts/../../ACES-LUTs/aces-dev-1.1.0/transforms/ctl/rrt/RRT.ctl \
     -ctl /Users/ptr/Development/ACES/amf-util/scripts/../../ACES-LUTs/aces-dev-1.1.0/transforms/ctl/odt/p3/ODT.Academy.P3D60_48nits.ctl \
     -force \
     "$INPUTIMAGEPATH" \
     "$OUTPUTIMAGEPATH"

# -- end of script --

