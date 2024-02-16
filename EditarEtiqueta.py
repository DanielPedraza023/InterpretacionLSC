import os
import json

carpeta_json = "D:/Datos/Desktop/CODIGOS/TESIS/DATAHUGO/Letra_R"

def modificar_etiqueta_json(archivo_json):
    with open(archivo_json, 'r') as f:
        datos = json.load(f)

    # Modifica la etiqueta en cada objeto dentro de "shapes"
    for forma in datos.get("shapes", []):
        if "label" in forma:
            forma["label"] = forma["label"].replace("LETRA_R", "R")

    with open(archivo_json, 'w') as f:
        json.dump(datos, f, indent=2)

def procesar_archivos_json(carpeta):
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".json"):
            ruta_archivo = os.path.join(carpeta, archivo)
            modificar_etiqueta_json(ruta_archivo)
            print(f"Se modificó el archivo: {ruta_archivo}")

if __name__ == "__main__":
    procesar_archivos_json(carpeta_json)
