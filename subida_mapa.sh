#!/bin/bash
PROTOCOL="ftp"
URL="10.20.1.2"
#URL="10.30.1.4"
LOCALDIR="/home/data-science/mapaClima/mapa/"


USER="joel"
PASS="abcd1234+"
REGEX="*.gif"



cd $LOCALDIR/

lftp  $PROTOCOL://$URL <<- UPLOAD
	user $USER "$PASS"
	cd Estaciones_Met/
	mput -E index.html

UPLOAD

