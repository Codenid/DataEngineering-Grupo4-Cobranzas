from datetime import datetime
import os
import pandas as pd

def add_date_suffix(filename, date=None):
    """
    Appends _YYYYMMDD to the filename before the extension.
    
    Args:
        filename (str): Original filename (e.g. 'data.csv')
        date (datetime, optional): Date to use; defaults to today.
    
    Returns:
        str: Modified filename (e.g. 'data_20250501.csv')
    """
    if date is None:
        date = datetime.today()
        
    name, ext = os.path.splitext(filename)
    date_str = date.strftime("%Y%m%d")
    return f"{name}_{date_str}{ext}"

def leer_datos(path):
    return pd.read_csv(path)

def transformar_datos(df):
    df['total'] = df['cantidad'] * df['precio']
    return df

def resumir_datos(df):
    resumen = df.groupby('producto')['total'].sum().reset_index()
    return resumen

def guardar_datos(df, path):
    df.to_csv(path, index=False)

##########################################
# Funciones para obtener fechas y lotes
##########################################

def get_fecha_proceso():
    return datetime.now().strftime("%Y-%m-%d")


def get_fecha_proceso_compacta():
    return datetime.now().strftime("%Y%m%d")


def get_lote_id():
    return f"COB_{get_fecha_proceso_compacta()}"


###########################################
# New
###########################################

import json
import logging

from scripts.azure_upload import upload_to_adls

##########################################
# Cobranzas
##########################################

def crear_contexto_lote():
    return {
        "fecha_proceso": get_fecha_proceso(),
        "lote_id": get_lote_id()
    }

def validar_archivos(files):
    for file_path in files:
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Archivo no encontrado: {file_path}"
            )

    return True

def obtener_metadata_archivo(
    dataset,
    file_path
):
    return {
        "dataset": dataset,
        "archivo": os.path.basename(file_path),
        "registros": len(pd.read_csv(file_path)),
        "tamano_mb": round(os.path.getsize(file_path)/ (1024 * 1024),2),
        "estado": "SUCCESS"
    }


def obtener_nombre_archivo_lote(
    dataset,
    fecha_proceso
):
    fecha = fecha_proceso.replace("-", "")
    return f"{dataset}_{fecha}.csv"


def cargar_dataset_raw(
    dataset,
    file_path,
    container_name,
    grupo,
    contexto,
    conexion
):
    logging.info(f"Subiendo dataset={dataset}")

    lote_id = contexto["lote_id"]

    logging.info(f"Lote={lote_id}")

    nombre_archivo = obtener_nombre_archivo_lote(
        dataset,
        contexto["fecha_proceso"]
    )

    blob_name = (
        f"raw/{grupo}/"
        f"{lote_id}/"
        f"{nombre_archivo}"
    )

    logging.info(f"Destino={blob_name}")

    upload_to_adls(
        local_file_path=file_path,
        container_name=container_name,
        blob_name=blob_name,
        wasb_conn_id=conexion
    )

    metadata = obtener_metadata_archivo(
        dataset,
        file_path
    )

    logging.info(metadata)

    return metadata

def generar_auditoria(
    path,
    contexto,
    datasets
):

    os.makedirs(
        path,
        exist_ok=True
    )

    audit_file = (
        f"{path}/"
        f"audit_{contexto['fecha_proceso'].replace('-','')}.json"
    )

    auditoria = {
        "lote_id": contexto["lote_id"],
        "fecha_proceso": contexto["fecha_proceso"],
        "execution_timestamp": datetime.now().isoformat(),
        "datasets": datasets
    }

    with open(
        audit_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            auditoria,
            file,
            indent=4,
            ensure_ascii=False
        )

    logging.info(f"Auditoría generada: {audit_file}")

    return audit_file