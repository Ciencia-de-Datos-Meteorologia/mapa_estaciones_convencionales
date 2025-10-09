import pandas as pd
import os

'''
Script encargado de generar los archivos HTML que se muestran al momento de presionar el botón 'Todas las variables'
'''

## Directorio de salida de los HTML
directory = '/var/www/html/mapas/mapa_convencionales/output_dashboard/'
## Enlace que conecta a la carpeta de la página
url = 'https://insivumeh.gob.gt/img/Estaciones_Met/output_csv_page/'

## Leer el csv
df = pd.read_csv('database.csv', delimiter=',', header=0)
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%Y-%m-%d')
df = df.dropna(thresh=df.shape[1]*0.2)
df = df.sort_values("FECHA")

df[['NOMBRE_ESTACIÓN']] = df[['NOMBRE_ESTACIÓN']].replace('_', ' ', regex=True)

## Obtener el listado de estaciones
estaciones = df["NOMBRE_ESTACIÓN"].unique()
data = df.groupby(['NOMBRE_ESTACIÓN'])

## Generar un archivo HTML por estación
for estacion in estaciones:
    ## Extraer los datos necesarios
    data_estacion = data.get_group((estacion,))
    lluvia = str(data_estacion['PRECIPITACIÓN'].iloc[-2])
    tmax = str(data_estacion['TEMPERATURA_MÁXIMA'].iloc[-1])
    tseca = str(data_estacion['TEMPERATURA_MEDIA'].iloc[-1])
    tmin = str(data_estacion['TEMPERATURA_MÍNIMA'].iloc[-1])
    eva_tan = str(data_estacion['EVAPORACIÓN_TANQUE'].iloc[-1])
    hum_rel = str(data_estacion['HUMEDAD_RELATIVA'].iloc[-1])
    bri_solar = str(data_estacion['BRILLO_SOLAR'].iloc[-1])
    nub = str(data_estacion['NUBOSIDAD'].iloc[-1])
    vel_viento = str(data_estacion['VELOCIDAD_VIENTO'].iloc[-1])
    dir_vient = str(data_estacion['DIRECCIÓN_VIENTO'].iloc[-1])
    pre_atmos = str(data_estacion['PRESIÓN_ATMOSFÉRICA'].iloc[-1])
    rad_solar = str(data_estacion['RADIACIÓN'].iloc[-1])
    ID = str(data_estacion['CODIGO'].iloc[-1])

## Plantilla HTML para cada estación
    html = '''
        <!DOCTYPE html>
        <meta http-equiv="content-type" content="text/html;charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <html>
        <head>
            <title>ESTACIÓN ''' + estacion + '''</title>
            <style type="text/css">
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }
                header {
                    background-color: #117ce7;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }
                h1 {
                    margin: 0;
                    font-size: 2em;
                }
                .container {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    grid-gap: 20px;
                    margin: 20px;
                }
                .card {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                    text-align: center;
                }
                .card h2 {
                    margin-top: 0;
                    font-size: 1.2em;
                    color: #333;
                }
                .card .value {
                    font-size: 1.8em;
                    font-weight: bold;
                    color: #117ce7;
                    margin-bottom: 10px;
                }
                .card .label {
                    font-size: 0.9em;
                    color: #777;
                }
                .button {
                    background-color: #117ce7;
                    border: none;
                    color: white;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 20px;
                    cursor: pointer;
                    border-radius: 5px;
                }
                .button:hover {
                    background-color: #0f6ac7;
                }
            </style>
        </head>
        <body>
            <header><h1>ESTACIÓN ''' + estacion + '''. DATOS PRELIMINARES.</h1></header>
            <div class="container">
                <div class="card"><h2>Precipitación 24hrs</h2><p class="value">''' + lluvia + ''' mm</p><p class="label">Últimas 24 horas</p></div>
                <div class="card"><h2>Temperatura Mínima</h2><p class="value">''' + tmin + ''' °C</p><p class="label">Hoy</p></div>
                <div class="card"><h2>Temperatura Media</h2><p class="value">''' + tseca + ''' °C</p><p class="label">Hoy</p></div>
                <div class="card"><h2>Temperatura Máxima</h2><p class="value">''' + tmax + ''' °C</p><p class="label">Hoy</p></div>
                <div class="card"><h2>Evaporación de Tanque</h2><p class="value">''' + eva_tan + ''' mm</p><p class="label">Últimas 24 horas</p></div>
                <div class="card"><h2>Humedad Relativa</h2><p class="value">''' + hum_rel + '''%</p><p class="label">Hoy</p></div>
                <div class="card"><h2>Brillo Solar</h2><p class="value">''' + bri_solar + ''' horas</p><p class="label">Hoy</p></div>
                <div class="card"><h2>Velocidad del Viento</h2><p class="value">''' + vel_viento + ''' km/h</p><p class="label">Hoy</p></div>
                <div class="card"><h2>Dirección del Viento</h2><p class="value">''' + dir_vient + ''' °</p><p class="label">Hoy</p></div>
                <div class="card"><h2>Presión Atmosférica</h2><p class="value">''' + pre_atmos + ''' mmHg</p><p class="label">Hoy</p></div>
                <div class="card"><h2>Radiación Solar</h2><p class="value">''' + rad_solar + '''</p><p class="label">Hoy</p></div>
            </div>
            <a href="''' + os.path.join(url, ID) + '''.html" target="_blank" class="button">Datos Mensuales</a>
        </body>
        </html>
    '''

    # Guardar el archivo HTML
    with open(f'{os.path.join(directory, ID)}.html', 'w') as f:
        f.write(html)
