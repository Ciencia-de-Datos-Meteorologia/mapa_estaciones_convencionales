import pandas as pd
import mysql.connector 
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yaml

'''
Script donde se genera el archivo 'database.csv' que contiene los datos meteorológicos de todas las estaciones de Climatología de los últimos 30 días.
'''

# Archivo de credenciales
archivo_configuracion = 'db_credentials.yaml'

# Leer las credenciales
with open(archivo_configuracion) as cred_f:
    user_conf = yaml.safe_load(cred_f)

host = user_conf['credentials']['host']
user = user_conf['credentials']['username']
password = user_conf['credentials']['password']
database = user_conf['credentials']['database']

# Conexion a la base de datos
conexion_database = mysql.connector.connect(
    host = host,
   user = user,
    password = password,
    auth_plugin = 'mysql_native_password',
    database = database
)

# Definir las fechas de inicio y final
inicio_fecha = datetime.today()
final_fecha = datetime.now() - relativedelta(months=1)

# Consulta a la base de datos de los últimos 30 días
query_database_completa = f'''SELECT * FROM CLIMATOLOGIA_INSIVUMEH_PROD.001_climatologia_ALFA_ICC WHERE FUENTE='CLIMATOLOGÍA' AND FECHA BETWEEN '{final_fecha.strftime('%Y-%m-%d')}' AND '{inicio_fecha.strftime('%Y-%m-%d')}' '''
df = pd.read_sql_query( sql = query_database_completa, con = conexion_database)
df['FECHA'] = pd.to_datetime(df['FECHA'],format='%Y-%m-%d')

# Generar la salida en formato csv
df.to_csv('database.csv',index=False)
