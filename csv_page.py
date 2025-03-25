import pandas as pd
import os

'''
Script encargado de generar los archivos HTML donde se muestran los datos mensuales de cada estación.
'''

## Ruta de salida de los HMTL, en este caso se sube directamente a la carpeta del servidor Apache de la computadora
directory = '/var/www/html/mapaMet/output_csv_page/'

## Leer csv y extraer datos necesarios
df = pd.read_csv('database.csv', delimiter=',', header=0)
df[['NOMBRE_ESTACIÓN']] = df[['NOMBRE_ESTACIÓN']].replace('_', ' ', regex=True)
df['NOMBRE_ESTACIÓN'] = df['NOMBRE_ESTACIÓN'].astype(str)

estaciones = df['CODIGO'].unique()

## Iterar sobre cada estación unica que se encuentra dentro del csv
for estacion in estaciones:
    data_estacion = df[df['CODIGO'] == estacion]
    nombre = data_estacion['NOMBRE_ESTACIÓN'].values[0]
    latitud = data_estacion['LATITUD'].values[0]
    longitud = data_estacion['LONGITUD'].values[0]
    
## Plantilla para el HTML de cada estación
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Datos mensuales - {nombre}</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 80%;
                max-width: 1200px;
                margin: 0 auto;
            }}
            table th, table td {{
                border: 1px solid #ccc;
                padding: 5px;
                text-align: center;
                width: 100px; /* Ancho fijo para las celdas */
            }}
            table th {{
                background-color: #0074D9;
                color: white;
                text-align: center;
                font-weight: bold;
            }}
            #button-container {{
                text-align: center;
                margin: 20px auto;
                width: 80%;
                max-width: 1200px;
            }}
            button {{
                background-color: #2980b9;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                padding: 10px 20px;
                font-size: 16px;
            }}
            button:hover {{
                background-color: #005ca9;
            }}
        </style>
    </head>
    <body>
        <h1 style="text-align: center;">ESTACIÓN {nombre}</h1>
        <h2 style="text-align: center;">Código: {estacion}</h2>
        <h2 style="text-align: center;">Latitud: {latitud} - Longitud: {longitud}</h2>

        
        <!-- Contenedor para el botón -->
        <div id="button-container">
            <button id="downloadBtn">Descargar CSV</button>
        </div>
        
        <div id="table-container"></div>

        <script type="text/javascript">
            function processData(csv) {{
                let data = csv.split(/\\r|\\n/).map(v => v.split(','));
                let headers = data.shift();
                let table = document.createElement('table');
                let thead = document.createElement('thead');
                table.appendChild(thead);
                thead.innerHTML = '<tr><th>' + headers.join('</th><th>') + '</th></tr>';
                let tbody = document.createElement('tbody');
                table.appendChild(tbody);
                for (let row of data) {{
                    if(row.length > 1) {{
                        tbody.innerHTML += '<tr><td>' + row.join('</td><td>') + '</td></tr>';
                    }}
                }}
                document.getElementById("table-container").appendChild(table);
                
                // Guardar el CSV en una variable para la descarga
                window.csvData = headers.join(",") + "\\n" + data.map(row => row.join(",")).join("\\n");
            }}

            document.getElementById("downloadBtn").addEventListener("click", function() {{
                if (!window.csvData) {{
                    alert("Los datos aún no se han cargado. Por favor, espera...");
                    return;
                }}
                const blob = new Blob([window.csvData], {{type: 'text/csv'}});
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = "Data_mensual_{nombre}.csv";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }});

            // Cargar datos desde el CSV remoto
            fetch("https://insivumeh.gob.gt/img/Estaciones_Met/output_csv_estacion/{nombre}.csv")
            .then(res => res.text())
            .then(text => processData(text))
            .catch(err => {{
                console.error("Error cargando datos:", err);
                alert("No se pudieron cargar los datos. Por favor, inténtalo más tarde.");
            }});
        </script>
    </body>
    </html>
    """

    # Imprimir el código HTML
    with open(f'{os.path.join(directory,estacion)}.html', 'w') as f:
        f.write(html)
