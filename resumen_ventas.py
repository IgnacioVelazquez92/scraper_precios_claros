import pandas as pd
import os

# Crear carpeta de resultados si no existe
os.makedirs("resultados", exist_ok=True)

# Leer archivo Excel
archivo_entrada = "data/ventas_articulos.xlsx"
df = pd.read_excel(archivo_entrada)

# Limpiar nombres de columnas
df.columns = df.columns.str.strip()

# Verificar columnas necesarias
columnas_esperadas = ["Fecha", "Código", "Descripción", "Cantidad"]
faltantes = [col for col in columnas_esperadas if col not in df.columns]
if faltantes:
    raise ValueError(f"Faltan columnas necesarias: {faltantes}")

# Normalización de tipos
df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce")
df["Código"] = df["Código"].astype(str)
df["Descripción"] = df["Descripción"].astype(str)

# -------- VENTAS DIARIAS (pivot) --------
pivot_diario = pd.pivot_table(
    df,
    values="Cantidad",
    index=["Código", "Descripción"],
    columns=df["Fecha"].dt.date,
    aggfunc="sum",
    fill_value=0
).sort_index()

# -------- VENTAS SEMANALES (pivot) --------
df["Semana"] = df["Fecha"].dt.to_period("W").apply(
    lambda r: f"{r.start_time.date()} → {r.end_time.date()}")
pivot_semanal = pd.pivot_table(
    df,
    values="Cantidad",
    index=["Código", "Descripción"],
    columns="Semana",
    aggfunc="sum",
    fill_value=0
).sort_index()

# -------- VENTAS MENSUALES (pivot) --------
df["Mes"] = df["Fecha"].dt.to_period(
    "M").dt.strftime("%B %Y")  # Ej: Enero 2025
pivot_mensual = pd.pivot_table(
    df,
    values="Cantidad",
    index=["Código", "Descripción"],
    columns="Mes",
    aggfunc="sum",
    fill_value=0
).sort_index()

# -------- EXPORTAR A EXCEL --------
archivo_salida = "resultados/resumen_ventas.xlsx"
with pd.ExcelWriter(archivo_salida, engine="openpyxl") as writer:
    pivot_diario.to_excel(writer, sheet_name="Ventas Diarias")
    pivot_semanal.to_excel(writer, sheet_name="Ventas Semanales")
    pivot_mensual.to_excel(writer, sheet_name="Ventas Mensuales")

print(f"✅ Archivo generado con reportes pivot: {archivo_salida}")
