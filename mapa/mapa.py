#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:40:55 2023
Modficado el 26 de sep

@author: rainy
"""
import folium
import random
import pandas as pd
import branca
from folium.plugins import FloatImage
from folium.plugins import MarkerCluster, MiniMap, MousePosition, MeasureControl, Geocoder, FloatImage, LocateControl
from folium.plugins import GroupedLayerControl
#Linea de 233 a 240 aprox los hrefs
#Define coordinates of where we want to center our map
boulder_coords = [15.8, -90.5]
my_map = folium.Map(location = boulder_coords, zoom_start = 7, control_scale=True, tiles=None)
#my_map = folium.Map(location = boulder_coords, zoom_start = 8, control_scale=True)
#my_map = folium.Map(location = boulder_coords, zoom_start = 8, tiles="Stamen Terrain", control_scale=True)
tile_layer1 = folium.TileLayer(zoom_srart = 8,control_scale=True, min_zoom=7,name='OpenStreetMap',show=(True)).add_to(my_map)
tile_layer2 = folium.TileLayer(zoom_srart = 8,control_scale=True, tiles="cartodbpositron",name="OSM Carto",min_zoom=7,show=False).add_to(my_map)


loc = 'INFORMACIÓN PRELIMINAR DE LAS ESTACIONES CONVENCIONALES - Departamento de Investigación y Servicios Meteorológicos - INSIVUMEH'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(loc)   


marker_cluster = MarkerCluster(name="Estaciones Climáticas").add_to(my_map)
#marker_cluster2 = MarkerCluster(name="Estaciones Sinópticas", show=False).add_to(my_map)

#### Enlaces ####
regiones_clima='https://raw.githubusercontent.com/PeterArgueta/clima/main/rc.geojson'
departamentos='https://raw.githubusercontent.com/PeterArgueta/clima/main/deptos_gt.geojson'
#belice='https://raw.githubusercontent.com/carlossoto362/Hidrologia/main/data/Belice.geojson'
belice='data/Belice.geojson'

#### Style ####
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1,
                            'weight':0.1}


style_function2 = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1,
                            'weight':1,
                            "dashArray": "5, 5"}


def random_color(feature):
    return {'fillColor': f"#{random.randint(0, 0xFFFFFF):06x}", 'color': '#000000',
                            'fillOpacity': 0.4,
                            'weight':0.8}



#### Highlight ####

highlight_function = lambda x: {'fillColor': '#e78829', 
                                'color':'#000000', 
                                'fillOpacity': 0.5, 
                                'weight': 0.8}

#### REGIONES CLIMATICAS ####
R=folium.GeoJson(
    regiones_clima, name="Regiones Climáticas",
    style_function=style_function,
    highlight_function=random_color,
    show=(True), embed=True,
    tooltip=folium.features.GeoJsonTooltip(
        fields=['NOMBRE'],  # use fields from the json file
        aliases=[''],
        style=("background-color: white; color: #000000; font-family: arial; font-size: 12px; padding: 10px;") 
    ), 
).add_to(my_map)

folium.GeoJson(
    departamentos, name="Departamentos",
    style_function=style_function2,
    show=(True)
).add_to(my_map)


style_functionDiff = lambda x: {'fillColor': '#ffffff', 
                            'color':'red', 
                            'fillOpacity': 1,
                            'weight':1,
                            "dashArray": "5, 5"}

""" folium.GeoJson(
    belice, name="Diferendo Territorial y Marítimo",
    style_function=style_function2,
    show=(True),
    tooltip=folium.features.GeoJsonTooltip(
        fields=['Nombre'],  # use fields from the json file
        aliases=[''],
        style=("background-color: white; color: #000000; font-family: arial; font-size: 12px; padding: 10px;") 
    )
).add_to(my_map) """

######################################
#### Data frame ####

df_sino=(pd.read_csv('data/sinopticas.csv').dropna(subset=["Latitude","Longitude"]))
df_sino['Tipo']='sino' #se crea una columna para que a partir de este dato se elija el icono que se mostrará en la pantalla.

df_auto=(pd.read_csv('data/automaticas.csv').dropna(subset=["Latitude","Longitude"]))
df_auto['Tipo']='automática'

df_conv=(pd.read_csv('data/convencionales.csv').dropna(subset=["Latitude","Longitude"]))
df_conv['Tipo']='convencional'

#Se concatenan los 3 data frame para trabajar sólo con uno. 
#df=pd.concat([df_sino,df_auto,df_conv])

df=pd.concat([df_auto,df_conv])

####HTML###

def html_chilera(row):
    i = row
    
    Estación = df['Estación'].iloc[i]                             
    Departamento = df['Departamento'].iloc[i]                           
    Municipio = df['Municipio'].iloc[i]
    ID = df['Código'].iloc[i]                 
    Latitude=str(round(df['Latitude'].iloc[i],6))   
    Longitude=str(round(df['Longitude'].iloc[i],6))
    
    html = """<!DOCTYPE html>

<html>
<head>
  <meta charset="UTF-8">
  <style>
    /* Estilo de botones de pestañas */
    .tab button {
      background-color: #f2f2f2;
      border: none;
      outline: none;
      cursor: pointer;
      padding: 10px 20px;
      transition: 0.3s;
      font-size: 18px;
      color: #333; /* Color del texto por defecto */
    }

    /* Cambio de color de fondo al pasar el mouse */
    .tab button:hover {
      background-color: #ddd;
    }

    /* Estilo de botones activos */
    .tab button.active {
      background-color: #007bff; /* Color de fondo activo */
      color: white; /* Color del texto activo */
    }

    /* Estilo del contenido de pestañas */
    .tabcontent {
      display: none;
      padding: 10px;
    }

    /* Mostrar el contenido de la pestaña activa */
    .tabcontent.active {
      display: block;
    }

    body {
      margin: 0;
      padding: 0;
      font-family: Arial, sans-serif;
      font-size: 10px;
      color: #333;
      background-color: #f2f2f2;
    }

    h1 {
      font-size: 20px;
      font-weight: bold;
      margin: 10px;
      color: #224f94;
    }

    hr {
      margin: 20px;
      border: none;
      height: 1px;
      background-color: #d4d4d4;
    }

    p {
      margin: 20px;
      line-height: 1.6em;
    }

    a {
      color: #224f94;
      font-weight: bold;
      text-decoration: none;
    }

    a:hover {
      color: #1a3d73;
      text-decoration: underline;
    }
  </style>
  <title>iframe</title>
</head>

<body>
  <!-- Nombre de la estación arriba de las pestañas -->
  <h1>""" + Estación + """</h1>

  <!-- Pestañas -->
  <div class="tab">
    <button class="tablinks active" onclick="openTab(event, 'estacion')">Estación</button>
    <button class="tablinks" onclick="openTab(event, 'variables')">Variables</button>
    <button class="tablinks" onclick="openTab(event, 'contact')">Gráficas</button>
  </div>

  <!-- Contenido de las pestañas -->
  <div id="estacion" class="tabcontent active" style="font-size: 18px; line-height: 1.6;">
    <p><strong>ID: </strong><a href="https://insivumeh.gob.gt/img/Estaciones_Met/output_dashboard/"""+ID+""".html" target="_blank">""" + ID + """</a></p>
    <p><strong>Ubicación: </strong><span>Lat: """ + Latitude + """, Lon: """ + Longitude + """</span></p>
    <p><strong>"""+Municipio+""", """+Departamento+"""</span></p>
  </div>

  <div id="variables" class="tabcontent">
    <iframe src="https://insivumeh.gob.gt/img/Estaciones_Met/output_variables/"""+ID+""".html" frameborder="0" width="100%" height="400px"></iframe>
  </div>

  <div id="contact" class="tabcontent">
    <a href="https://insivumeh.gob.gt/img/Estaciones_Met/output_graficas/html/""" + ID + """.html" target="_blank">
      <img src="https://insivumeh.gob.gt/img/Estaciones_Met/output_graficas/img/""" + ID + """.png" alt="graph" width="430" height="250"> 
    </a>
  </div>

  <script>
    function openTab(evt, tabName) {
      // Obtener elementos con la clase "tabcontent" y ocultarlos
      var tabcontent = document.getElementsByClassName("tabcontent");
      for (var i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
      }

      // Obtener elementos con la clase "tablinks" y quitar la clase "active"
      var tablinks = document.getElementsByClassName("tablinks");
      for (var i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
      }

      // Mostrar la pestaña actual y marcar el botón como activo
      document.getElementById(tabName).classList.add("active");
      evt.currentTarget.classList.add("active");
    }
  </script>
</body>
</html>
      """
    return html



def icono_chilero(row):
    i=row
    
    Tipo=df['Tipo'].iloc[i]
    
    html="""<!DOCTYPE html>
    <html>

   ''<img src="https://github.com/PeterArgueta/clima/raw/main/"""+Tipo +""".svg" style="width:35px;height:35px;">'

    </html>
    """ 
    return html


#'<img src="https://github.com/PeterArgueta/clima/raw/main/"""+Tipo +""".png" style="width:35px;height:35px;">'
#'<img src="https://www.svgrepo.com/show/286488/pin.svg" style="width:30px;height:30px;">'

    
#### ICON SINOPTICAS ####
icono_sino=html='<img src="https://github.com/PeterArgueta/clima/raw/main/sino.png" style="width:35px;height:35px;">'


for i in range(0,len(df)):
    html = html_chilera(i)
    icono= icono_chilero(i)
    iframe = branca.element.IFrame(html=html,width=450,height=300)
    popup = folium.Popup(iframe,parse_html=True)
    folium.Marker([df['Latitude'].iloc[i],df['Longitude'].iloc[i]],
                  popup=popup, icon=folium.DivIcon(icono)).add_to(marker_cluster) 
    

""" for i in range(0,len(df_sino)):
    html = html_chilera(i)
    iframe = branca.element.IFrame(html=html,width=600,height=350)
    popup = folium.Popup(iframe,parse_html=True)
    folium.Marker([df_sino['Latitude'].iloc[i],df_sino['Longitude'].iloc[i]],
                  popup=popup, icon=folium.DivIcon(icono_sino)).add_to(marker_cluster2) 
  """
        
logo = ("https://raw.githubusercontent.com/PeterArgueta/clima/main/logo.png")


creditos_html = '''
<div style="
     position: fixed; 
     bottom: 10px; right: 10px; width: 250px; 
     background-color: rgba(255, 255, 255, 0.8);
     border-radius: 12px;
     box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
     padding: 10px;
     font-size: 12px;
     font-family: Arial, sans-serif;
     z-index: 9999;
     ">
     <p style="text-align: center; color: #333;"><b>Desarrollado por [Nombre de los Desarrolladores]</b></p>
</div>
'''




FloatImage(logo, bottom=5, left=1, width='120px').add_to(my_map)



folium.LayerControl(position="topright").add_to(my_map)
my_map.keep_in_front(R)


MousePosition( 
    position='topright', 
    separator=' | ', 
    prefix="Mouse:", 
    num_digits=3, 
    #lat_formatter=fmtr, 
    #lng_formatter=fmtr 
).add_to(my_map) 


grupo_diferendo=folium.GeoJson(
    belice, name="Diferendo Territorial y Marítimo",
    style_function=style_functionDiff, control=False,
    show=(True),
    tooltip=folium.features.GeoJsonTooltip(
        fields=['Nombre'],  # use fields from the json file
        aliases=[''],
        style=("background-color: white; color: #000000; font-family: arial; font-size: 12px; padding: 10px;") 
    )
).add_to(my_map)

icono = folium.features.DivIcon(
                          icon_size=(150,30),
                          icon_anchor=(5,14),
                          html=f"<p style='transform: rotate(-88deg);'>Diferendo Territorial Insular y Marítimo Pendiente de Resolver</p>",)

folium.Marker([17,-89.15], icon=icono).add_to(grupo_diferendo)

GroupedLayerControl(
    groups={'<b style="text-decoration: underline;">Estilo del mapa: </b>':[tile_layer1,tile_layer2]},
    collapsed=False,
    position='bottomright',
).add_to(my_map)


creditos_html = '''
<div style="
     position: fixed; 
     bottom: 10px; right: 10px; width: 250px; 
     background-color: rgba(255, 255, 255, 0.8);
     border-radius: 12px;
     box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
     padding: 10px;
     font-size: 12px;
     font-family: Arial, sans-serif;
     z-index: 9999;
     ">
     <p style="text-align: center; color: #333;"><b>Desarrollado por la sección de Climatología.</b></p>
</div>
'''


LocateControl().add_to(my_map)
#Geocoder().add_to(my_map)
my_map.get_root().html.add_child(folium.Element(title_html))
#my_map.get_root().html.add_child(folium.Element(creditos_html))

my_map.save("index.html")

