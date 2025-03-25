import pandas as pd
import os 

'''
Script encargado de generar los archivos CSV de los datos mensuales de cada estación.
'''

## Ruta de salida de los csv de cada estación
directory = '/var/www/html/mapaMet/output_csv_estacion/'


## Leer csv 
df = pd.read_csv('database.csv', delimiter=',', header=0)
## Eliminar las columnas no necesarias
df.drop(columns=['CODIGO_INSIVUMEH','CODIGO','LATITUD','LONGITUD','ALTITUD','FUENTE'], inplace=True)
## Renombrar el nombre de las columnas
df.rename(columns={'FECHA':'Fecha',
                    'PRECIPITACIÓN':'Lluvia',
                    'TEMPERATURA_MÍNIMA':'Temperatura Minima',
                    'TEMPERATURA_MÁXIMA':'Temperatura Maxima',
                    'TEMPERATURA_MEDIA':'Temperatura Media',
                    'EVAPORACIÓN_TANQUE':'Evaporacion Tanque',
                    'HUMEDAD_RELATIVA':'Humedad Relativa',
                    'NUBOSIDAD':'Nubosidad',
                    'VELOCIDAD_VIENTO':'Velocidad Viento',
                    'DIRECCIÓN_VIENTO':'Direccion Viento',
                    'PRESIÓN_ATMOSFÉRICA':'Presion Atmosferica',
                    'BRILLO_SOLAR':'Brillo Solar',
                    'EVAPORACIÓN_PICHE':'Evaporacion Piche',
                    'TEMPERATURA_SUELO_5CM':'Temperatura Suelo 5cm',
                    'TEMPERATURA_SUELO_50CM':'Temperatura Suelo 50cm',
                    'TEMPERATURA_SUELO_100CM':'Temperatura Suelo 100cm',
                    'RADIACIÓN':'Radiacion'
                    }, inplace=True)

## Tener el listado de las estaciones
estaciones = df["NOMBRE_ESTACIÓN"].unique()
 
## Filtrar los datos para cada estación
for estacion in estaciones:
    data_estacion = df[df['NOMBRE_ESTACIÓN'] == estacion]
    data_estacion = data_estacion.dropna(axis=1, how='all')
    data_estacion = data_estacion.reset_index(drop=True)
    data_estacion.drop(columns=['NOMBRE_ESTACIÓN'], inplace=True)
    data_estacion.sort_values("Fecha", inplace=True)
    data_estacion.to_csv(f"{os.path.join(directory,estacion)}.csv",index=False)
