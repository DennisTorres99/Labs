import json
import re
from pathlib import Path

EMPRESA_EMAIL_REGEX = re.compile(r"^[\w\.-]+@empresa\.com$")


def cargar_json(ruta: Path) -> list[dict]:
    try:
        with ruta.open(encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    except json.JSONDecodeError as error:
        raise ValueError("El archivo no contiene JSON válido") from error


def filtrar_usuarios(datos: list[dict]) -> list[dict]:
    usuarios_filtrados: list[dict] = []

    for registro in datos:
        match registro:
            case {
                "id": int(id_usuario),
                "nombre": str(nombre),
                "email": str(email),
                "activo": True,
            } if EMPRESA_EMAIL_REGEX.match(email):
                usuarios_filtrados.append(
                    {
                        "id": id_usuario,
                        "nombre": nombre,
                        "email": email,
                    }
                )
            case _:
                continue

    return usuarios_filtrados
