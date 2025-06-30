import pandas as pd
import json
from pathlib import Path
from scraper.precios_justos import obtener_precios_por_ean


def procesar_archivo_excel(data, tolerancia: float) -> pd.DataFrame:
    if isinstance(data, str):
        df = pd.read_excel(data)
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        raise ValueError("Se esperaba una ruta o un DataFrame.")

    nuevos_datos = []
    for _, fila in df.iterrows():
        descripcion = fila["descripcion"]
        eans = str(fila["ean"]).replace("'", "").split(";")
        resultado = None

        # Buscar precios por EAN hasta que alguno devuelva datos válidos
        for ean in eans:
            resultado = obtener_precios_por_ean(ean)
            if resultado["precio_min"] is not None:
                break

        if resultado is None or resultado["precio_min"] is None:
            # No se encontró ningún dato de la competencia
            nuevos_datos.append({
                "precio_competencia_bajo": None,
                "precio_competencia_alto": None,
                "precio_promedio": None,
                "desvio?": "",
                "datos_competencia": ""
            })
            continue

        # Sí se encontraron precios
        precio_min = resultado["precio_min"]
        precio_max = resultado["precio_max"]
        precio_promedio = resultado["precio_promedio"]
        json_serializado = json.dumps(resultado, ensure_ascii=False)

        precios_a_evaluar = [
            fila.get("precio_venta_actual"),
            fila.get("precio_venta_futuro")
        ]
        desvio = "NO"
        for precio_venta in precios_a_evaluar:
            if precio_venta and precio_min:
                diferencia_pct = abs(
                    precio_venta - precio_min) / precio_min * 100
                if diferencia_pct > tolerancia:
                    desvio = "SI"
                    break

        nuevos_datos.append({
            "precio_competencia_bajo": precio_min,
            "precio_competencia_alto": precio_max,
            "precio_promedio": precio_promedio,
            "desvio?": desvio,
            "datos_competencia": json_serializado
        })

    nuevos_df = pd.DataFrame(nuevos_datos)
    final_df = pd.concat([df.reset_index(drop=True), nuevos_df], axis=1)
    return final_df


def guardar_resultado(df: pd.DataFrame, ruta_salida: str):
    Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(ruta_salida, index=False)
