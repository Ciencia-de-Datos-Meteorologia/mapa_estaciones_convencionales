 #!/bin/bash
PROTOCOL="ftp"
URL="10.20.1.2"
#URL="10.30.1.4"
LOCALDIR="/var/www/html/mapaMet/"


USER="joel"
PASS="abcd1234+"


cd $LOCALDIR/output_csv_page/

lftp  $PROTOCOL://$URL <<- UPLOAD
	user $USER "$PASS"
	cd Estaciones_Met/output_csv_page/
	mput -E *.html

UPLOAD


cd $LOCALDIR/output_csv_estacion/

lftp  $PROTOCOL://$URL <<- UPLOAD
	user $USER "$PASS"
	cd Estaciones_Met/output_csv_estacion/
	mput -E *.csv

UPLOAD


cd $LOCALDIR/output_dashboard/

lftp  $PROTOCOL://$URL <<- UPLOAD
	user $USER "$PASS"
	cd Estaciones_Met/output_dashboard/
	mput -E *.html

UPLOAD


cd $LOCALDIR/output_graficas/html/

lftp  $PROTOCOL://$URL <<- UPLOAD
	user $USER "$PASS"
	cd Estaciones_Met/output_graficas/html/
	mput -E *.html

UPLOAD


cd $LOCALDIR/output_graficas/img/

lftp  $PROTOCOL://$URL <<- UPLOAD
	user $USER "$PASS"
	cd Estaciones_Met/output_graficas/img/
	mput -E *.png

UPLOAD


cd $LOCALDIR/output_variables/

lftp  $PROTOCOL://$URL <<- UPLOAD
	user $USER "$PASS"
	cd Estaciones_Met/output_variables/
	mput -E *.html

UPLOAD

