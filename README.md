## Proyecto del Módulo 1 — Unidad U1.2

Configuración de un entorno Python y ejecución de una primera petición autenticada a Gemini mediante Thunder Client.

### Requisitos previos

- Python instalado. Versión utilizada en este proyecto: 3.14.7.
- Git instalado.
- Visual Studio Code.
- Para repetir la prueba de API: Thunder Client y una clave propia de Gemini.

### Instalación en Windows con PowerShell

1. Clona el repositorio y entra en su carpeta:

```powershell
git clone https://github.com/jersonmontecino-lab/especializacion-ia-modulo-1.git
cd especializacion-ia-modulo-1
```

2. Crea el entorno virtual:

```powershell
python -m venv venv
```

3. Activa el entorno:

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecuta este comando y vuelve a intentar activarlo. El cambio se aplica únicamente a la terminal actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

4. Instala las dependencias registradas:

```powershell
python -m pip install -r requirements.txt
```

5. Comprueba que las librerías pueden importarse:

```powershell
python -c "import requests; from google import genai; from dotenv import load_dotenv; print('Entorno reconstruido correctamente')"
```

Resultado esperado:

```text
Entorno reconstruido correctamente
```

### Configuración de la credencial

Copia la plantilla:

```powershell
Copy-Item .env.example .env
```

Abre `.env` en el editor y reemplaza `tu_llave_aqui` por tu propia clave:

```dotenv
API_KEY=tu_llave_aqui
```

El archivo `.env` y la carpeta `venv/` están excluidos mediante `.gitignore`. Cada persona utiliza su propia credencial.

### Evidencia de la petición autenticada

La prueba se realizó con Thunder Client y el modelo `gemini-3.8-flash`.

Consulta los datos y la captura en [Documentación de la prueba](docs/prueba_api.md).

## Consultar Gemini desde Python

Con el entorno virtual activado y la variable `API_KEY` configurada
en el archivo `.env`, ejecuta:

```powershell
python src/consumir_api.py
```

Escribe una pregunta y presiona Enter. El programa realiza una consulta
a Gemini y muestra la respuesta en la terminal.

Ejemplo de pregunta:

> Explica con un ejemplo la diferencia entre una lista y un diccionario en Python.

### Organización del código

- `obtener_clave()`: obtiene y valida la clave de API.
- `armar_peticion()`: prepara la URL, los encabezados y el cuerpo.
- `enviar_peticion()`: envía la petición HTTP y devuelve el JSON decodificado.
- `extraer_texto()`: reúne el texto de la respuesta.
- `consultar_modelo()`: valida la pregunta y coordina la consulta.

### Validaciones y errores

El programa rechaza preguntas vacías o valores que no sean texto.
También muestra mensajes ante errores de conexión, tiempo de espera,
estado HTTP, JSON inválido o respuestas sin el texto esperado.

### Información adicional

Las respuestas pueden tardar varios minutos. La petición utiliza
`timeout=(10, 360)`: 10 segundos para conectar y 360 segundos de espera
de lectura.

Esta implementación no incorpora búsqueda web ni una fuente de datos
en tiempo real.