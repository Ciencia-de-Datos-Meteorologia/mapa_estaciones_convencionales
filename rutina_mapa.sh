#!/bin/bash

entorno="/home/data-science/.python_envs/mapaClima/bin"


# Directorio de entrada donde se encuentran los archivos .tex
dir="/home/data-science/mapaClima/"

source "$entorno/activate" && cd $dir && python consulta_database.py && python dashboard.py && python variables.py && python graficas.py && python csv_page.py && python csv_estacion.py

