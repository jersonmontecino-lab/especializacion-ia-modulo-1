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