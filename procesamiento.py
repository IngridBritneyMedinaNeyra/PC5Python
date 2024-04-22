import pandas as pd
import requests

def limpiar_columnas(df):
    # Renombrar columnas eliminando espacios y tildes
    # Convertir nombres de columna a minúsculas
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    
    # Eliminar columnas ID y TipoMoneda repetidas
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Eliminar la coma de la columna 'DISPOSITIVO_LEGAL' si existe
    if 'DISPOSITIVO_LEGAL' in df.columns:
        df['DISPOSITIVO_LEGAL'] = df['DISPOSITIVO_LEGAL'].str.replace(',', '')

    return df

def dolarizar_valores(df):
    try:
        # Obtener el valor actual del dólar desde la API de Sunat
        valor_dolar = requests.get('http://pc4.sunat.gob.pe:8080/ol-ti-itconsultadws/ConsultarTC').json()['TCs'][0]['Compra']

        # Dolarizar los valores de montos de inversión y montos de transferencia
        df['MONTO_INVERSION_USD'] = df['MONTO_INVERSION'] / valor_dolar
        df['MONTO_TRANSFERENCIA_USD'] = df['MONTO_TRANSFERENCIA'] / valor_dolar
    except requests.exceptions.RequestException as e:
        print("Error al obtener el valor del dólar:", e)

    return df

def mapear_estado(estado):
    if estado == 'ACTOS_PREVIOS':
        return 1
    elif estado == 'RESUELTO':
        return 0
    elif estado == 'EJECUCION':
        return 2
    elif estado == 'CONCLUIDO':
        return 3
    else:
        return None

def puntuar_estado(df):
    if 'ESTADO' in df.columns:
        df['PUNTUACION_ESTADO'] = df['ESTADO'].apply(mapear_estado)
    else:
        print("La columna 'ESTADO' no se encuentra en el DataFrame.")

    return df

def almacenar_ubigeos(df):
    if all(col in df.columns for col in ['UBIGEO', 'REGION', 'PROVINCIA', 'DISTRITO']):
        ubigeos_df = df[['UBIGEO', 'REGION', 'PROVINCIA', 'DISTRITO']].drop_duplicates()
    else:
        print("Las columnas 'UBIGEO', 'REGION', 'PROVINCIA' y 'DISTRITO' no se encuentran en el DataFrame.")

def generar_reportes_regionales(df):
    if 'REGION' in df.columns:
        regiones = df['REGION'].unique()
        for region in regiones:
            region_df = df[df['REGION'] == region]
    else:
        print("La columna 'REGION' no se encuentra en el DataFrame.")

if __name__ == "__main__":
    df = pd.read_excel('/workspaces/PC5Python/Data/reactiva.xlsx')
    df = limpiar_columnas(df)
    df = dolarizar_valores(df)
    df = puntuar_estado(df)
    generar_reportes_regionales(df)
    almacenar_ubigeos(df)
