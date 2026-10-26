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
    respuesta = requests.post(
        url,
        headers=encabezados,
        json=cuerpo,
        timeout=(10, 360),
    )

    respuesta.raise_for_status()

    return respuesta.json()


def extraer_texto(datos):
    return datos["candidates"][0]["content"]["parts"][0]["text"]


def consultar_modelo(pregunta):
    if not isinstance(pregunta, str):
        raise ValueError("La pregunta debe ser un texto.")

    pregunta = pregunta.strip()

    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía.")

    url, encabezados, cuerpo = armar_peticion(pregunta)
    datos = enviar_peticion(url, encabezados, cuerpo)

    return extraer_texto(datos)


if __name__ == "__main__":
    pregunta = "Explica qué es una API en una sola frase."

    print("Consultando a Gemini...", flush=True)

    try:
        resultado = consultar_modelo(pregunta)

        print("\nRespuesta:")
        print(resultado)

    except requests.exceptions.Timeout:
        print(
            "Se agotó el tiempo de espera sin recibir respuesta. "
            "Intenta nuevamente más tarde."
        )

    except requests.exceptions.ConnectionError:
        print("No se pudo establecer o mantener la conexión con Gemini.")

    except requests.exceptions.HTTPError as error:
        print(
            "La API devolvió un error HTTP: "
            f"{error.response.status_code}."
        )

    except requests.exceptions.JSONDecodeError:
        print("La API devolvió una respuesta que no es JSON válido.")

    except requests.exceptions.RequestException:
        print("Ocurrió un error al enviar la petición HTTP.")

    except (KeyError, IndexError, TypeError):
        print("La respuesta no contiene el texto en la estructura esperada.")

    except ValueError as error:
        print(f"No se pudo realizar la consulta: {error}")