import json
import random
import time
from datetime import datetime

import boto3


BUCKET = "gio76-bucket-datalke-ia"
CARPETA_DESTINO = "raw"
INTERVALO_SEGUNDOS = 30
SENSORES = ("temperatura", "humedad", "presion")
UBICACIONES = ("Norte", "Sur", "Este", "Oeste")


def generar_evento():
    """Genera un evento simulado de sensor."""
    return {
        "evento_id": random.randint(1000, 9999),
        "sensor": random.choice(SENSORES),
        "valor": round(random.uniform(15, 40), 2),
        "timestamp": int(time.time()),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ubicacion": random.choice(UBICACIONES),
    }


def crear_nombre_archivo(contador):
    """Crea el nombre del archivo donde se guardara el evento."""
    timestamp = int(time.time())
    return f"{CARPETA_DESTINO}/evento_{timestamp}_{contador}.json"


def enviar_evento(s3_client, evento, nombre_archivo):
    """Envia un evento serializado como JSON a S3."""
    s3_client.put_object(
        Bucket=BUCKET,
        Key=nombre_archivo,
        Body=json.dumps(evento, indent=2),
    )


def mostrar_inicio():
    print("=" * 50)
    print(" PRODUCTOR DE DATOS EN TIEMPO REAL")
    print("=" * 50)
    print(f" Bucket destino: {BUCKET}")
    print(f" Carpeta: {CARPETA_DESTINO}/")
    print(f" Enviando cada {INTERVALO_SEGUNDOS} segundos")
    print(" Presiona Ctrl+C para detener")
    print("=" * 50)


def mostrar_evento_enviado(contador, evento):
    print(
        f" [{contador}] {evento['sensor']}: "
        f"{evento['valor']} - {evento['ubicacion']}"
    )


def mostrar_cierre(contador):
    print("\n" + "=" * 50)
    print(" Productor detenido")
    print(f" Total de eventos enviados: {contador}")
    print("=" * 50)


def ejecutar_productor(s3_client):
    contador = 0

    try:
        while True:
            evento = generar_evento()
            nombre_archivo = crear_nombre_archivo(contador)

            enviar_evento(s3_client, evento, nombre_archivo)
            mostrar_evento_enviado(contador, evento)

            contador += 1
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        mostrar_cierre(contador)


def main():
    s3_client = boto3.client("s3")

    mostrar_inicio()
    ejecutar_productor(s3_client)


if __name__ == "__main__":
    main()
