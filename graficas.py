from bokeh.models import Range1d, LinearAxis
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, output_file
import pandas as pd
from bokeh.io import export_png, save
import os

'''
Script encargado de generar los archivos HTML que se muestran dentro de la pestaña 'Gráficas' de cada estación.
'''

## Ruta de salida de los HTML
directory_html = "/var/www/html/mapas/mapa_convencionales/output_graficas/html/"
## Ruta de salida de los PNG
directory_img = "/var/www/html/mapas/mapa_convencionales/output_graficas/img/"

# Leer el archivo CSV 
df = pd.read_csv('database.csv', header=0, delimiter=',')

# Convertir la columna FECHA a formato datetime y ordenar el dataframe
df['FECHA'] = pd.to_datetime(df['FECHA'], format="%Y-%m-%d")

# Obtener la lista de códigos de estación 
codigos_estacion = df["CODIGO"].unique()

# Crear un gráfico y un archivo HTML para cada código de estación
for codigo in codigos_estacion:
    # Filtrar los datos para el código de estación actual
    data = df[df['CODIGO'] == codigo]
    
    # Obtener el nombre de la estación para el título del gráfico
    nombre_estacion = data['NOMBRE_ESTACIÓN'].iloc[0]
    
    # Extraer los datos necesarios
    lluvia = data['PRECIPITACIÓN']
    tmin = data['TEMPERATURA_MÍNIMA']
    tseca = data['TEMPERATURA_MEDIA']
    tmax = data['TEMPERATURA_MÁXIMA']
    fecha = data['FECHA']

    # Crear la figura de Bokeh
    fig = figure(
        x_axis_type='datetime',
        title=f"{nombre_estacion} (Código: {codigo})",  # Título con nombre y código
        plot_height=400,
        plot_width=800,
        toolbar_location='below',
        y_axis_label="Precipitación (mm)",
        y_range=(-5, max(lluvia) * 1.3),
        background_fill_color='white',
        background_fill_alpha=0.6,
        tools="save,pan,box_zoom,reset,wheel_zoom"
    )

    fig.yaxis.axis_label_text_font_size = "8pt"
    fig.title.text_font_size = '8pt'
    fig.left[0].formatter.use_scientific = False

    # Agregar el segundo eje para la temperatura
    fig.extra_y_ranges = {"temp_range": Range1d(start=-5, end=40)}
    fig.add_layout(LinearAxis(y_range_name="temp_range", axis_label="Temperatura (°C)"), 'right')

    # Agregar las líneas y los círculos
    fig.line(fecha, lluvia, line_color='navy', line_width=1, legend_label='Precipitación', name='lluvia')
    fig.line(fecha, tseca, line_color='seagreen', line_width=1, line_dash='dashed', legend_label='Temperatura media', 
             name='tseca', y_range_name='temp_range')
    fig.circle(fecha, tmin, fill_color='deepskyblue', line_color='blue', size=3,
               legend_label='Temperatura min', name='tmin', y_range_name='temp_range')
    fig.circle(fecha, tmax, fill_color='firebrick', line_color='red', size=3,
               legend_label='Temperatura max', name='tmax', y_range_name='temp_range')

    fig.legend.location = 'top_left'
    fig.title.text_font_size = '10pt'
    fig.yaxis.axis_label_text_font_size = "10pt"

    # Agregar etiquetas a las líneas y los círculos
    tooltips = [
        ("Valor", "@y"),
        ("Fecha", "@x{%F}")
    ]
    formatters = {
        '@x': 'datetime'
    }
    
    hover = HoverTool(names=['lluvia', 'tseca', 'tmin', 'tmax'], tooltips=tooltips, formatters=formatters)
    fig.add_tools(hover)

    # Generar el archivo HTML y la imagen PNG
    output_file(f'{directory_html}{codigo}.html', title=f"{nombre_estacion} (Código: {codigo})")  # Título en la pestaña
    fig.legend.background_fill_alpha = 0.5
    fig.legend.label_text_font_size = "8pt"
    fig.legend.spacing = 1
    save(fig)
    export_png(fig, filename=f"{os.path.join(directory_img,codigo)}.png")  # Usar el código para nombrar la imagen
