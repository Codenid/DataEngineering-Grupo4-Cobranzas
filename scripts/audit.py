import os
import json
import pandas as pd
from datetime import datetime


AUDIT_PATH = "/opt/airflow/audit"


def get_file_metadata(
    dataset,
    file_path
):

    file_size_mb = round(
        os.path.getsize(file_path) / (1024 * 1024),
        2
    )

    record_count = len(
        pd.read_csv(file_path)
    )

    return {
        "dataset": dataset,
        "file_name": os.path.basename(file_path),
        "record_count": record_count,
        "file_size_mb": file_size_mb,
        "status": "SUCCESS"
    }


def save_audit(
    lote_id,
    dag_id,
    fecha_proceso,
    datasets
):
    os.makedirs(
        AUDIT_PATH,
        exist_ok=True
    )

    audit_file = (
        f"{AUDIT_PATH}/"
        f"audit_{fecha_proceso.replace('-','')}.json"
    )

    payload = {
        "lote_id": lote_id,
        "dag_id": dag_id,
        "fecha_proceso": fecha_proceso,
        "execution_timestamp":
            datetime.now().isoformat(),
        "datasets":
            datasets
    }

    with open(
        audit_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            payload,
            f,
            indent=4,
            ensure_ascii=False
        )

    return audit_file