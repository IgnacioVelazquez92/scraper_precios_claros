import pandas as pd
from core.comparador import procesar_archivo_excel
from core.comparador import guardar_resultado
from pathlib import Path

ARCHIVO_ENTRADA = "data/articulos.xlsx"
ARCHIVO_SALIDA_FINAL = "resultados/final.xlsx"
ARCHIVO_SALIDA_TEMP = "resultados/progreso_parcial.xlsx"
TAMANO_LOTE = 100  # artículos por bloque
UMBRAL_PARCIAL = 300  # mínimo de artículos para guardar parciales

COLUMNAS_REQUERIDAS = {
    "codigo", "cod_fac", "descripcion", "ean", "costo_final",
    "precio_venta_actual", "margen_actual", "precio_venta_futuro", "margen_futuro"
}


def main():
    try:
        df = pd.read_excel(ARCHIVO_ENTRADA)
    except Exception as e:
        print(f"❌ Error leyendo el archivo: {e}")
        return

    if not COLUMNAS_REQUERIDAS.issubset(df.columns):
        print("❌ El archivo no contiene todas las columnas requeridas.")
        return

    total_filas = len(df)
    GUARDAR_PARCIAL = total_filas > UMBRAL_PARCIAL
    print(f"📦 Total de artículos a procesar: {total_filas}")
    print("📝 Guardado parcial activado." if GUARDAR_PARCIAL else "⚡ Ejecutando sin guardado parcial (proceso más rápido).")

    resultados = pd.DataFrame()

    for inicio in range(0, total_filas, TAMANO_LOTE):
        fin = min(inicio + TAMANO_LOTE, total_filas)
        bloque = df.iloc[inicio:fin]
        print(f"🔄 Procesando artículos {inicio + 1} a {fin}...")

        try:
            resultado_parcial = procesar_archivo_excel(bloque)
            resultados = pd.concat(
                [resultados, resultado_parcial], ignore_index=True)
            if GUARDAR_PARCIAL:
                guardar_resultado(resultados, ARCHIVO_SALIDA_TEMP)
        except Exception as e:
            print(f"⚠️ Error en el bloque {inicio}-{fin}: {e}")
            if GUARDAR_PARCIAL:
                print("💾 Guardando progreso parcial...")
                guardar_resultado(resultados, ARCHIVO_SALIDA_TEMP)
            return

    guardar_resultado(resultados, ARCHIVO_SALIDA_FINAL)
    print("✅ Proceso finalizado con éxito. Resultados en:", ARCHIVO_SALIDA_FINAL)


if __name__ == "__main__":
    main()
