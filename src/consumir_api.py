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


def consultar_modelo(pregunta):
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
        }
    }   

    respuesta = requests.post(
        url,
        headers=encabezados,
        json=cuerpo,
        timeout=(10, 240),
    )

    respuesta.raise_for_status()
    datos = respuesta.json()

    return datos["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == "__main__":
    pregunta = "Explica qué es una API en una sola frase."
    resultado = consultar_modelo(pregunta)
    print(resultado)