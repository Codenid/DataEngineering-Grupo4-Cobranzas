from airflow.decorators import dag, task
from pendulum import timezone
from datetime import datetime, timedelta
import logging

from scripts.helpers import (
    crear_contexto_lote,
    validar_archivos,
    cargar_dataset_raw,
    generar_auditoria
)

LOCAL_CARTERA = "/opt/airflow/data/cobranzas/cartera_diaria.csv"
LOCAL_GESTIONES = "/opt/airflow/data/cobranzas/gestiones_diarias.csv"
LOCAL_RECUPEROS = "/opt/airflow/data/cobranzas/recuperos_diarios.csv"

CONTAINER_NAME = "airflow"
GRUPO = "G4"

AUDIT_PATH = "/opt/airflow/logs/audit"

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

@dag(
    dag_id="cobranzas_raw_ingestion",
    description="Carga diaria de datasets de cobranzas hacia ADLS RAW.",
    default_args=default_args,
    start_date=datetime(2026,1,1,tzinfo=timezone("America/Lima")),
    schedule="0 8 * * *",
    catchup=False,
    tags=["cobranzas","adls","raw"],
)
def dag_cobranzas_raw():

    @task
    def crear_contexto():
        logging.info("==> Creando contexto de lote")
        return crear_contexto_lote()

    @task
    def validar_archivos_fuente(contexto):
        logging.info("==> Validando archivos fuente")

        validar_archivos([
            LOCAL_CARTERA,
            LOCAL_GESTIONES,
            LOCAL_RECUPEROS
        ])

        return contexto

    @task
    def cargar_cartera(contexto):
        logging.info("==> Cargando cartera a RAW")

        return cargar_dataset_raw(
            dataset="cartera",
            file_path=LOCAL_CARTERA,
            container_name=CONTAINER_NAME,
            grupo=GRUPO,
            contexto=contexto
        )

    @task
    def cargar_gestiones(contexto):
        logging.info("==> Cargando gestiones a RAW")

        return cargar_dataset_raw(
            dataset="gestiones",
            file_path=LOCAL_GESTIONES,
            container_name=CONTAINER_NAME,
            grupo=GRUPO,
            contexto=contexto
        )

    @task
    def cargar_recuperos(contexto):
        logging.info("==> Cargando recuperos a RAW")

        return cargar_dataset_raw(
            dataset="recuperos",
            file_path=LOCAL_RECUPEROS,
            container_name=CONTAINER_NAME,
            grupo=GRUPO,
            contexto=contexto
        )

    @task
    def generar_auditoria_task(
        contexto,
        metadata_cartera,
        metadata_gestiones,
        metadata_recuperos
    ):
        logging.info("==> Generando auditoría")

        generar_auditoria(
            AUDIT_PATH,
            contexto,
            [
                metadata_cartera,
                metadata_gestiones,
                metadata_recuperos
            ]
        )

    contexto = crear_contexto()
    contexto_validado = validar_archivos_fuente(contexto)
    metadata_cartera = cargar_cartera(contexto_validado)
    metadata_gestiones = cargar_gestiones(contexto_validado)
    metadata_recuperos = cargar_recuperos(contexto_validado)

    generar_auditoria_task(
        contexto_validado,
        metadata_cartera,
        metadata_gestiones,
        metadata_recuperos
    )

dag = dag_cobranzas_raw()