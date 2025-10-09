import pandas as pd
import datetime
import os

'''
Script encargado de generar los archivos HTML que se muestran dentro de la pestaña 'Variables' de cada estación.
'''

current=datetime.datetime.now()

## Ruta de salida de los HTML
directory='/var/www/html/mapas/mapa_convencionales/output_variables/'
## Enlace que dirige hacia la página de insivumeh donde se almacenan los dashboard de todas las variables
url='https://insivumeh.gob.gt/img/Estaciones_Met/output_dashboard/'

## Leer el csv y extraer los datos necesarios
df = pd.read_csv('database.csv', delimiter=',', header=0)
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%Y-%m-%d')
df= df.dropna(thresh=df.shape[1]*0.2)
df = df.sort_values("FECHA")

df[['NOMBRE_ESTACIÓN']] = df[['NOMBRE_ESTACIÓN']].replace('_', ' ', regex=True)
estaciones = df['NOMBRE_ESTACIÓN'].unique()
data=df.groupby(['NOMBRE_ESTACIÓN'])


## Iterar sobre cada estacion de la lista estaciones
for estacion in estaciones:
        data_estacion=data.get_group((estacion,))
        lluvia=str(data_estacion['PRECIPITACIÓN'].iloc[-2])
        tmax=str(data_estacion['TEMPERATURA_MÁXIMA'].iloc[-1])
        tseca=str(data_estacion['TEMPERATURA_MEDIA'].iloc[-1])
        tmin=str(data_estacion['TEMPERATURA_MÍNIMA'].iloc[-1])
        hum_rel=str(data_estacion['HUMEDAD_RELATIVA'].iloc[-1])
        FECHA_current=current.strftime("%Y-%m-%d %H:%M")
        FECHA = str(df['FECHA'].iloc[-1].date())
        ID=str(data_estacion['CODIGO'].iloc[-1])
       
## Plantilla HTML para cada estación
        html = '''
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>ESTACIÓN</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    color: #224f94;
                    margin: 0;
                    padding: 20px;
                    background-color: #f9f9f9;
                }

                .header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }

                h2 {
                    margin: 0;
                    font-size: 24px;
                    color: #224f94;
                }

                p {
                    margin: 5px 0;
                    font-size: 14px;
                    color: #555;
                }

                table {
                    border-collapse: collapse;
                    width: 100%;
                    max-width: 500px;
                    margin-top: 20px;
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }

                table th, table td {
                    border: 1px solid #007bff;
                    padding: 10px;
                    text-align: center;
                }

                table th {
                    background-color: #007bff;
                    color: white;
                    font-weight: bold;
                }

                button {
                    padding: 8px 16px;
                    border: 1px solid #007bff;
                    border-radius: 4px;
                    background-color: #007bff;
                    color: white;
                    font-size: 14px;
                    cursor: pointer;
                    transition: background-color 0.3s, color 0.3s;
                    
                }

                button:hover {
                    background-color: #0056b3;
                    border-color: #0056b3;
                }

                button:active {
                    background-color: #004080;
                    border-color: #004080;
                }

                @media (max-width: 600px) {
                    .header {
                        flex-direction: column;
                        align-items: flex-start;
                    }

                    h2 {
                        font-size: 20px;
                    }

                    button {
                        margin-top: 10px;
                    }
                }
            </style>
        </head>
        <body>
            <!-- Encabezado con título y botón -->
            <div class="header">
                <h2>''' + estacion + '''</h2>
                <a href="''' + os.path.join(url, ID) + '''.html" target="_blank">
                    <button>Todas las variables</button>
                </a>
            </div>


            <!-- Tabla de datos -->
            <table>
                <tr>
                    <th>LLUVIA 24H</th>
                    <th>TMIN</th>
                    <th>TMEDIA</th>
                    <th>TMAX</th>
                </tr>
                <tr>
                    <td>''' + lluvia + '''</td>
                    <td>''' + tmin + '''</td>
                    <td>''' + tseca + '''</td>
                    <td>''' + tmax + '''</td>
                </tr>
            </table>
            <!-- Información de fecha -->
            <p>Último reporte: ''' + FECHA + ''' -PRELIMINAR-</p>
            <p>Última actualización: ''' + FECHA_current + ''' -PRELIMINAR-</p>

        </body>
        </html>
'''

    # Imprimir el código HTML
        with open(f'{os.path.join(directory,ID)}.html', 'w') as f:
            f.write(html)
    

