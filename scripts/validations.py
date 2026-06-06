import os

def validate_file_exists(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"Archivo no encontrado: {file_path}"
        )

    return True