#!/bin/bash


### config ###

# root folder auto config
ROOTFOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

# DOALL=1	# not needed any more, if DOTEST is 1, no full set is done
DOTEST=0

DOZIP=1

#NOWDATE="Test-EXR"
NOWDATE=`date +%Y-%m-%d-%H%M`


### preparation ###

SOURCEFOLDER="$ROOTFOLDER/Material/source"
AMFFOLDER="$ROOTFOLDER/Material/amf"

AMFUTIL="$ROOTFOLDER/amf-util.py"
CTLROOTPATH="$ROOTFOLDER/../ACES-LUTs/aces-dev-1.2.0/transforms/ctl"

IMAGEFOLDER="Samples-$NOWDATE"
IMAGEPATH="$ROOTFOLDER/Images/$IMAGEFOLDER"
TEMPROOT="$ROOTFOLDER/tmp/"
TEMPPATH="$TEMPROOT/$IMAGEFOLDER"


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
	FORMAT=$3
	
	if [ -z "$FORMAT" ]
	then
		FORMAT="tiff"
	fi

	SOURCEPATH="$SOURCEFOLDER/$SOURCENAME.$FORMAT"
	AMFPATH="$AMFFOLDER/$AMFNAME.amf"
	DESTINATIONFILENAME=${AMFNAME}__${SOURCENAME}.tiff
	DESTINATIONPATH=$IMAGEPATH/$DESTINATIONFILENAME
	
	echo "render_frame $SOURCENAME $AMFNAME $FORMAT"
	#echo "  source: $SOURCEPATH"
	#echo "     amf: $AMFPATH"
	echo "         ctls: $CTLROOTPATH"

	SCRIPTFILENAME=$AMFNAME.sh
	SCRIPTPATH=$IMAGEPATH/$SCRIPTFILENAME
	#ERRORPATH=$IMAGEPATH/logs/${AMFNAME}__${SOURCENAME}__log.txt
	#mkdir -p $IMAGEPATH/logs/

	echo 
    echo "  printing amf info..."
    $AMFUTIL info $AMFPATH

	echo 
    echo "  creating render script..."
    $AMFUTIL render $AMFPATH $CTLROOTPATH > $SCRIPTPATH
    #echo "$AMFUTIL render $AMFPATH $CTLROOTPATH > $SCRIPTPATH"
	chmod 755 $SCRIPTPATH

	echo 
    echo "  executing render script..."
    echo "         source: $SOURCEPATH"
    echo "    destination: $DESTINATIONPATH"
	$SCRIPTPATH $SOURCEPATH $DESTINATIONPATH
	
	if [ $DOZIP -eq 1 ]
	then
		mkdir -p $TEMPPATH/source-frames/
		SOURCEDESTPATH=$TEMPPATH/source-frames/$SOURCEFILENAME
	    if [ ! -f $SOURCEDESTPATH ]
	    then
		    echo "  copy source..."
		    cp $SOURCEPATH $SOURCEDESTPATH
		fi
		READMEDESTPATH=$TEMPPATH/source-frames/README.md
	    if [ ! -f $READMEDESTPATH ]
	    then
		    echo "  copy readme..."
		    cp "${SOURCEFOLDER}/README.md" $READMEDESTPATH
		fi

		mkdir -p $TEMPPATH/amf
		AMFDESTPATH=$TEMPPATH/amf/$AMFNAME.amf
	    if [ ! -f $AMFDESTPATH ]
	    then
		    echo "  copy amf..."
		    cp $AMFPATH $AMFDESTPATH
		fi

		mkdir -p $TEMPPATH/output-frames
		OUTPUTDESTPATH=$TEMPPATH/output-frames/$DESTINATIONFILENAME
	    if [ ! -f $OUTPUTDESTPATH ]
	    then
		    echo "  copy output..."
		    cp $DESTINATIONPATH $OUTPUTDESTPATH
		fi
		
		mkdir -p $TEMPPATH/scripts
		SCRIPTDESTPATH=$TEMPPATH/scripts/$SCRIPTFILENAME
	    if [ ! -f $SCRIPTDESTPATH ]
	    then
		    echo "  copy script..."
		    cp $SCRIPTPATH $SCRIPTDESTPATH
		fi
	fi
	
	echo 
}


### TEST

if [ $DOTEST -eq 1 ]
then
	echo "DOTEST"
	#render_frame ArriAlexa.LowKey.0090350 amf_minimal
	#render_frame ArriAlexa.Portrait.0177143 example2

	#render_frame A003C001_190625_R24Y LogCEI800-Rec.709100nitsdim__skip-IDT exr
	#render_frame A003C001_190625_R24Y LogCEI800-Rec.709100nitsdim

	#render_frame M001_C001_06198Y_001 REDlog3G10-Rec.709100nitsdim
	#render_frame A003C001_190625_R24Y LogCEI800-P3D65-D60sim48nits
	
	render_frame A003C001_190625_R24Y__Rec709 Rec.709-Rec.709100nitsdim

fi


### ALL

if [ $DOTEST -eq 0 ]
then
	echo "DOALL"

	# ACES sources (ARRI)
	
#	render_frame ArriAlexa.HighKey.0101699 LogCEI800-Rec.709100nitsdim
#	render_frame ArriAlexa.HighKey.0101699 LogCEI800-P3D65-D60sim48nits
#	render_frame ArriAlexa.HighKey.0101699 LogCEI800-Rec.2020ST20841000nits
#
#	render_frame ArriAlexa.LowKey.0090350 LogCEI800-Rec.709100nitsdim
#	render_frame ArriAlexa.LowKey.0090350 LogCEI800-P3D65-D60sim48nits
#	render_frame ArriAlexa.LowKey.0090350 LogCEI800-Rec.2020ST20841000nits
#
#	render_frame ArriAlexa.LowLight.0117185 LogCEI800-Rec.709100nitsdim
#	render_frame ArriAlexa.LowLight.0117185 LogCEI800-P3D65-D60sim48nits
#	render_frame ArriAlexa.LowLight.0117185 LogCEI800-Rec.2020ST20841000nits
#
#	render_frame ArriAlexa.Portrait.0177143 LogCEI800-Rec.709100nitsdim
#	render_frame ArriAlexa.Portrait.0177143 LogCEI800-P3D65-D60sim48nits
#	render_frame ArriAlexa.Portrait.0177143 LogCEI800-Rec.2020ST20841000nits
#
#	render_frame ArriAlexa.StillLife.0181284 LogCEI800-Rec.709100nitsdim
#	render_frame ArriAlexa.StillLife.0181284 LogCEI800-P3D65-D60sim48nits
#	render_frame ArriAlexa.StillLife.0181284 LogCEI800-Rec.2020ST20841000nits
	
	# ACES sources (Sony F35?)

	# ...

	# Netflix sources

	render_frame A003C001_190625_R24Y LogCEI800-Rec.709100nitsdim
	render_frame A003C001_190625_R24Y LogCEI800-P3D65-D60sim48nits
	render_frame A003C001_190625_R24Y LogCEI800-Rec.2020ST20841000nits

	# render_frame M001_C001_06198Y_001 REDlog3G10-Rec.709100nitsdim

	render_frame A004C002_190619J4 S-Log3S-Gamut3-Rec.709100nitsdim
	render_frame A004C002_190619J4 S-Log3S-Gamut3-Rec.2020ST20841000nits	
	
	# Rec.709

	render_frame A003C001_190625_R24Y__Rec709 Rec.709-Rec.709100nitsdim

	# OpenEXR in ACES AP0 for VFX	
	
	render_frame A003C001_190625_R24Y__ACES LogCEI800-Rec.709100nitsdim__skip-IDT exr
	

	# sRGB
	# ADSM ? 
	# DCDM (16-bit tiff) ? DCP ?
	
	
fi

if [ $DOZIP -eq 1 ] && [ $DOTEST -eq 0 ]
then
	echo "DOZIP"
	
	CURRENTPATH=`pwd`
	cd $TEMPROOT
	zip -r "${IMAGEFOLDER}.zip" $IMAGEFOLDER
	cd $CURRENTPATH

	#rm -rf $TEMPROOT
fi
	