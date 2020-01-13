#!/bin/bash


### config ###

# root folder auto config
ROOTFOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

DOALL=0
DOTEST=1

NOWDATE="test-first" #`date +%Y-%m-%d-%H%M`
#NOWDATE=`date +%Y-%m-%d-%H%M`


### preparation ###

SOURCEFOLDER="$ROOTFOLDER/Material/source"
AMFFOLDER="$ROOTFOLDER/Material/amf"

AMFUTIL="$ROOTFOLDER/amf-util.py"
CTLROOTPATH="$ROOTFOLDER/../ACES-LUTs/aces-dev-1.1.0/transforms/ctl"

IMAGEPATH="$ROOTFOLDER/Images/Samples-$NOWDATE"

mkdir -p $IMAGEPATH

### functions ###

# function: render_frame
# parameter: 
#  sourcefilename (without ".dpx"), e.g. "Lowkey.0090350"
#  amf name (without ".amf"), e.g. "example2"

function render_frame
{
    SOURCENAME=$1
    AMFNAME=$2

	SOURCEPATH="$SOURCEFOLDER/$SOURCENAME.dpx"
	AMFPATH="$AMFFOLDER/$AMFNAME.amf"
	DESTINATIONPATH=$IMAGEPATH/${AMFNAME}__${SOURCENAME}.tiff
	
	echo "render_frame $SOURCENAME $AMFNAME"
	#echo "  source: $SOURCEPATH"
	#echo "     amf: $AMFPATH"
	echo "         ctls: $CTLROOTPATH"

	SCRIPTPATH=$IMAGEPATH/$AMFNAME.sh
	ERRORPATH=$IMAGEPATH/logs/${AMFNAME}__${SOURCENAME}__log.txt
	mkdir -p $IMAGEPATH/logs/

	echo 
    echo "  printing amf info..."
    $AMFUTIL info $AMFPATH 2>$ERRORPATH

	echo 
    echo "  creating render script..."
    $AMFUTIL render $AMFPATH $CTLROOTPATH > $SCRIPTPATH 2>>$ERRORPATH
	chmod 755 $SCRIPTPATH

	echo 
    echo "  executing render script..."
    echo "         source: $SOURCEPATH"
    echo "    destination: $DESTINATIONPATH"
	$SCRIPTPATH $SOURCEPATH $DESTINATIONPATH
	
    #echo "  copy source..."
	#SOURCEDESTPATH=$IMAGEPATH/$SOURCEFILENAME
    #if [ ! -f $SOURCEDESTPATH ]
    #then
	#    cp -rf $SOURCEPATH $SOURCEDESTPATH
	#fi

	echo 
}


### TEST

if [ $DOTEST -eq 1 ]
then
	echo "DOTEST"
	render_frame ArriAlexa.LowKey.0090350 amf_minimal
	#render_frame ArriAlexa.Portrait.0177143 example2
fi


### ALL

if [ $DOALL -eq 1 ]
then
	echo "DOALL: TBD"
fi
