import pandas as pd
import json
from pathlib import Path
from scraper.precios_justos import obtener_precios_por_ean


def procesar_archivo_excel(data: pd.DataFrame) -> pd.DataFrame:
    if isinstance(data, str):
        df = pd.read_excel(data)
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        raise ValueError("Se esperaba una ruta o un DataFrame.")

    filas_finales = []

    for _, fila in df.iterrows():
        eans = str(fila["ean"]).replace("'", "").split(";")
        eans = [e.strip() for e in eans if e.strip()]
        hubo_resultado = False

        for ean in eans:
            resultado = obtener_precios_por_ean(ean)

            if resultado["precio_min"] is not None:
                precio_venta = fila.get("precio_venta_futuro")
                precio_min = resultado["precio_min"]
                precio_max = resultado["precio_max"]
                precio_promedio = resultado["precio_promedio"]

                desvio_min = ((precio_venta - precio_min) /
                              precio_min * 100) if precio_min else None
                desvio_max = ((precio_venta - precio_max) /
                              precio_max * 100) if precio_max else None

                if precio_venta is None or precio_min is None or precio_max is None:
                    alerta_precio = ""
                elif precio_venta < precio_min:
                    alerta_precio = "BAJOS"
                elif precio_venta > precio_max:
                    alerta_precio = "ALTOS"
                else:
                    alerta_precio = "EN PRECIO"

                fila_nueva = fila.copy()
                fila_nueva["precio competencia bajo"] = precio_min
                fila_nueva["precio competencia alto"] = precio_max
                fila_nueva["precio promedio"] = precio_promedio
                fila_nueva["desvio vs min"] = round(
                    desvio_min, 2) if desvio_min is not None else None
                fila_nueva["desvio vs max"] = round(
                    desvio_max, 2) if desvio_max is not None else None
                fila_nueva["alerta precio"] = alerta_precio
                fila_nueva["datos_competencia"] = json.dumps(
                    resultado, ensure_ascii=False)

                filas_finales.append(fila_nueva)
                hubo_resultado = True

        if not hubo_resultado:
            fila_nueva = fila.copy()
            fila_nueva["precio competencia bajo"] = None
            fila_nueva["precio competencia alto"] = None
            fila_nueva["precio promedio"] = None
            fila_nueva["desvio vs min"] = None
            fila_nueva["desvio vs max"] = None
            fila_nueva["alerta precio"] = ""
            fila_nueva["datos_competencia"] = ""
            filas_finales.append(fila_nueva)

    df_final = pd.DataFrame(filas_finales)

    columnas_renombradas = {
        "codigo": "codigo",
        "cod_fac": "codigo fact.",
        "descripcion": "descripcion",
        "ean": "ean",
        "costo_final": "costo final",
        "precio_venta_actual": "precio venta actual",
        "margen_actual": "margen actual",
        "precio_venta_futuro": "precio venta futuro",
        "margen_futuro": "margen futuro"
    }
    df_final.rename(columns=columnas_renombradas, inplace=True)

    return df_final


def guardar_resultado(df: pd.DataFrame, ruta_salida: str):
    Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(ruta_salida, index=False)
