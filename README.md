# Productor de datos para S3

Este proyecto contiene un productor en Python que genera eventos simulados de sensores y los guarda como archivos JSON en un bucket de Amazon S3.

## Objetivo

Simular el envio periodico de datos en tiempo real hacia S3 para usarlos en practicas de procesamiento, almacenamiento o analitica de datos en AWS.

Cada evento incluye:

- ID del evento
- Tipo de sensor: temperatura, humedad o presion
- Valor numerico simulado
- Timestamp
- Fecha en formato legible
- Ubicacion simulada

Los archivos se guardan en la carpeta `raw/` del bucket configurado.

## Requisitos

Para ejecutar el proyecto necesitas:

- Python 3 instalado
- La libreria `boto3`, instalada desde `requirements.txt`
- Credenciales de AWS configuradas
- Un bucket de S3 existente
- Permisos para escribir objetos en ese bucket

Antes de ejecutar el productor, cambia el valor de `BUCKET` en `productor.py` por el nombre de tu bucket:

```python
BUCKET = "coloca-el-nombre-de-tu-bucket-aqui"
```

## Instalacion

Desde la carpeta del proyecto, crea un entorno virtual:

```powershell
python -m venv .venv
```

Activa el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias del proyecto:

```powershell
pip install -r requirements.txt
```

Si necesitas desactivar el entorno virtual al terminar, ejecuta:

```powershell
deactivate
```

## Configuracion de AWS

El script usa las credenciales disponibles para `boto3`. Puedes configurarlas con AWS CLI:

```powershell
aws configure
```

Debes ingresar:

- AWS Access Key ID
- AWS Secret Access Key
- Region por defecto
- Formato de salida, por ejemplo `json`

La cuenta configurada debe tener permisos para ejecutar `s3:PutObject` sobre el bucket.

## Como se ejecuta

Ejecuta el productor con:

```powershell
python productor.py
```

El programa empezara a generar un evento cada 30 segundos y lo subira a S3 en una ruta similar a:

```text
raw/evento_1716040000_0.json
```

Para detenerlo, presiona:

```text
Ctrl + C
```

Al detenerse, mostrara el total de eventos enviados.

## Que hace el codigo

El archivo `productor.py`:

- Genera eventos simulados con `generar_evento()`
- Construye el nombre del archivo con `crear_nombre_archivo()`
- Envia el JSON a S3 con `enviar_evento()`
- Ejecuta el ciclo principal desde `main()`

La ejecucion inicia desde:

```python
if __name__ == "__main__":
    main()
```

Esto permite que el archivo tambien pueda importarse desde otro script sin iniciar automaticamente el productor.
