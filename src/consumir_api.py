import os
from pathlib import Path

import requests
from dotenv import load_dotenv


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
load_dotenv(RAIZ_PROYECTO / ".env")


def obtener_clave():
    clave = os.getenv("API_KEY", "").strip()

    if not clave or clave == "tu_llave_aqui":
        raise ValueError("Falta configurar API_KEY en el archivo .env.")

    return clave


def armar_peticion(pregunta):
    if not isinstance(pregunta, str):
        raise ValueError("La pregunta debe ser un texto.")

    pregunta = pregunta.strip()

    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía.")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.8-flash:generateContent"
    )

    encabezados = {
        "x-goog-api-key": obtener_clave(),
        "Content-Type": "application/json",
    }

    cuerpo = {
        "contents": [
            {
                "parts": [
                    {"text": pregunta}
                ]
            }
        ],
        "generationConfig": {
            "thinkingConfig": {
                "thinkingLevel": "low"
            }
        },
    }

    return url, encabezados, cuerpo


def enviar_peticion(url, encabezados, cuerpo):
    try:
        respuesta = requests.post(
            url,
            headers=encabezados,
            json=cuerpo,
            timeout=(10, 360),
        )

        respuesta.raise_for_status()

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "Se agotó el tiempo de espera sin recibir respuesta del servicio."
        ) from error

    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "No se pudo establecer o mantener la conexión con el servicio."
        ) from error

    except requests.exceptions.HTTPError as error:
        estado = error.response.status_code

        if estado in (401, 403):
            mensaje = (
                f"Error HTTP {estado}: la credencial fue rechazada "
                "o no tiene permisos para esta operación."
            )
        elif estado == 400:
            mensaje = (
                "Error HTTP 400: la API rechazó la petición. "
                "Revisa los parámetros y la credencial configurada."
            )
        elif estado == 429:
            mensaje = (
                "Error HTTP 429: se alcanzó un límite de solicitudes "
                "o de cuota del servicio."
            )
        else:
            mensaje = f"La API devolvió un error HTTP {estado}."

        raise RuntimeError(mensaje) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            "Ocurrió un error al enviar la petición HTTP."
        ) from error

    try:
        return respuesta.json()

    except requests.exceptions.JSONDecodeError as error:
        raise RuntimeError(
            "La respuesta del servicio no tiene un formato JSON válido."
        ) from error


def extraer_texto(datos):
    try:
        partes = datos["candidates"][0]["content"]["parts"]

        textos = [
            parte["text"]
            for parte in partes
            if isinstance(parte.get("text"), str)
            and not parte.get("thought", False)
        ]

        texto = "".join(textos).strip()

    except KeyError as error:
        raise RuntimeError(
            f"Falta el campo {error} en la respuesta del servicio."
        ) from error

    except IndexError as error:
        raise RuntimeError(
            "La respuesta del servicio no contiene candidatos para leer."
        ) from error

    except (TypeError, AttributeError) as error:
        raise RuntimeError(
            "La estructura de la respuesta del servicio no es la esperada."
        ) from error

    if not texto:
        raise RuntimeError(
            "La respuesta del servicio no contiene texto generado."
        )

    return texto


def consultar_modelo(pregunta):
    url, encabezados, cuerpo = armar_peticion(pregunta)
    datos = enviar_peticion(url, encabezados, cuerpo)

    return extraer_texto(datos)


if __name__ == "__main__":
    pregunta = input("Escribe tu pregunta: ")

    try:
        resultado = consultar_modelo(pregunta)

        print("\nRespuesta:")
        print(resultado)

    except (ValueError, RuntimeError) as error:
        print(f"No se pudo realizar la consulta: {error}")