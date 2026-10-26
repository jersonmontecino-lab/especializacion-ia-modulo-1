# Especialización en Desarrollo con IA Generativa — Módulo 1

Repositorio de trabajo del Módulo 1 del programa de especialización en
Desarrollo con IA Generativa.

Incluye la configuración del entorno de Python y un módulo para consultar
la API de Google Gemini, procesar su respuesta y manejar errores.

## Requisitos

- Python instalado. Versión utilizada: 3.14.7.
- Git instalado.
- Una clave de API de Gemini.
- Acceso a internet para realizar las consultas.

Los comandos siguientes están preparados para Windows PowerShell.

## Instalación

### 1. Clonar el repositorio

```powershell
git clone https://github.com/jersonmontecino-lab/especializacion-ia-modulo-1.git plantilla-repositorio-base
cd plantilla-repositorio-base
```

### 2. Crear el entorno virtual

```powershell
python -m venv venv
```

### 3. Activar el entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución del script, permite su ejecución
durante la sesión actual y vuelve a activar el entorno:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

Al activarse, la terminal muestra `(venv)` al principio de la línea.

### 4. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### 5. Verificar el entorno

```powershell
python -c "import requests; from google import genai; from dotenv import load_dotenv; print('Entorno configurado correctamente')"
```

Este comando comprueba que las dependencias pueden importarse.
No realiza una consulta a Gemini.

### 6. Configurar la clave de API

Copia la plantilla de configuración:

```powershell
Copy-Item .env.example .env
```

Este paso se realiza en una instalación nueva. Si ya tienes un archivo
`.env` configurado, conserva ese archivo.

Abre `.env` en un editor y reemplaza el valor de ejemplo:

```dotenv
API_KEY=tu_llave_aqui
```

La clave real se guarda únicamente en `.env`. Este archivo está excluido
del control de versiones mediante `.gitignore`.

## Ejecutar una consulta

Desde la raíz del proyecto, con el entorno virtual activado:

```powershell
python src/consumir_api.py
```

Cuando aparezca `Escribe tu pregunta:`, escribe una pregunta y presiona Enter.

Ejemplo:

```text
Escribe tu pregunta: Explica qué es una API en una sola frase.

Respuesta:
[Texto generado por Gemini]
```

El texto generado puede variar en cada ejecución.

El programa realiza una consulta por ejecución. Para hacer otra pregunta,
ejecuta nuevamente el mismo comando.

## Organización del código

El archivo principal es `src/consumir_api.py`.

| Función | Responsabilidad |
|---|---|
| `obtener_clave()` | Obtiene y valida la clave de API desde las variables de entorno. |
| `armar_peticion(pregunta)` | Valida la pregunta y prepara la URL, los encabezados y el cuerpo de la petición. |
| `enviar_peticion(url, encabezados, cuerpo)` | Envía la petición HTTP, comprueba su estado y convierte la respuesta JSON; maneja errores de comunicación y formato. |
| `extraer_texto(datos)` | Reúne el texto generado y maneja campos faltantes, estructuras inesperadas o respuestas sin texto. |
| `consultar_modelo(pregunta)` | Coordina la construcción de la petición, su envío y la extracción del resultado. |

Las funciones devuelven sus resultados mediante `return`.
La entrada por teclado y la impresión del resultado se realizan en el
bloque `if __name__ == "__main__":`.

Esto permite importar las funciones desde otro archivo sin ejecutar
automáticamente una consulta.

## Validaciones y manejo de errores

El programa contempla los siguientes casos:

- Preguntas que no sean texto.
- Preguntas vacías o formadas únicamente por espacios.
- Clave de API ausente o sin configurar.
- Tiempo de espera agotado.
- Errores de conexión.
- Estados HTTP de error.
- Respuestas que no contienen JSON válido.
- Campos o candidatos faltantes en la respuesta.
- Estructuras inesperadas o respuestas sin texto generado.

La validación de entrada se realiza antes de preparar la petición.

Los errores se manejan dentro de la función responsable de cada operación.
El bloque principal captura `ValueError` y `RuntimeError` para mostrar un
mensaje comprensible al usuario.

## Verificaciones realizadas

Durante el desarrollo se comprobó:

- Reconstrucción del entorno desde una copia nueva del repositorio.
- Importación de las dependencias.
- Exclusión de `.env` y `venv/` mediante `.gitignore`.
- Petición autenticada desde Thunder Client.
- Consulta real a Gemini desde Python.
- Construcción de la petición y extracción de texto con datos de prueba.
- Rechazo de preguntas vacías y valores que no sean texto.
- Extracción de una respuesta dividida en varias partes.
- Detección de una respuesta sin texto.
- Manejo de errores simulados de conexión, JSON inválido y campos faltantes.
- Rechazo de una credencial inválida mediante una petición real.
- Consulta exitosa con la credencial correcta después de las pruebas.

## Estructura del repositorio

- `src/`: código fuente del proyecto.
- `docs/`: documentación y evidencias.
- `tests/`: carpeta reservada para pruebas del proyecto.
- `requirements.txt`: dependencias y versiones del entorno.
- `.env.example`: plantilla de configuración sin credenciales reales.
- `.gitignore`: archivos y carpetas excluidos del control de versiones.
- `README.md`: instrucciones de instalación, uso y verificación.

El archivo `.env` y el entorno virtual `venv/` se crean localmente y
no forman parte del repositorio.

## Evidencias

### Unidad 1.2

- [Documentación de la petición autenticada](docs/prueba_api.md).
- [Captura de la petición autenticada](docs/evidencia_peticion_autenticada.png).

### Unidad 1.3

- [Consulta desde Python](docs/evidencia_consulta_python.png).
- [Credencial inválida, entrada vacía y consulta exitosa](docs/evidencia_validaciones_python.png).
- [Commit y sincronización final](docs/evidencia_commit_final_u13.png).

## Protección de credenciales

- La clave se carga desde `.env` mediante `python-dotenv`.
- La autenticación se envía mediante el encabezado `x-goog-api-key`.
- No se escribe la clave directamente en el código.
- No se incluye la clave en capturas ni en documentación.
- `.env.example` conserva únicamente un valor de ejemplo.

Para comprobar que Git ignora el archivo local:

```powershell
git check-ignore -v .env
```

Para comprobar que no está registrado en el repositorio:

```powershell
git ls-files -- .env
```

El segundo comando no debe mostrar ningún archivo.

## Información adicional

### Configuración utilizada

El módulo utiliza el modelo `gemini-3.8-flash` con
`thinkingLevel` configurado en `low`.

La petición utiliza:

```python
timeout=(10, 360)
```

Esto establece 10 segundos para conectar y 360 segundos de espera de
lectura. No representa un límite total exacto de duración de la operación.

Durante las pruebas se observaron respuestas que tardaron varios minutos.
Ampliar la espera permite tolerar esa demora, pero no acelera el servicio.

### Datos en tiempo real

Esta implementación no incorpora búsqueda web ni una fuente externa de
datos en tiempo real. Por ello, no garantiza respuestas actuales sobre
clima, noticias u otros datos que cambien constantemente.

### Actualizar las dependencias

Si instalas nuevas dependencias, registra el entorno en UTF-8 con:

```powershell
python -c "import subprocess, sys; from pathlib import Path; paquetes=subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True); Path('requirements.txt').write_text(paquetes, encoding='utf-8')"
```

### Desactivar el entorno virtual

Al terminar de trabajar:

```powershell
deactivate
```