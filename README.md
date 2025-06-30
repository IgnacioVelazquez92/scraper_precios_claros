# 📊 Comparador de Precios - Precios Justos Argentina

Este proyecto permite comparar precios propios contra los precios publicados en la plataforma **Precios Justos** del gobierno argentino. A partir de un Excel con artículos, el sistema scrapeará los precios de la competencia por EAN y detectará si hay desvíos de precio relevantes.

---

## 🚀 ¿Qué hace este programa?

- Lee un Excel (`data/articulos.xlsx`) con artículos a analizar.
- Scrapea el precio por EAN en varias sucursales de San Miguel de Tucumán y alrededores.
- Compara tus precios (actuales y futuros) contra el **precio mínimo, máximo y promedio** de la competencia.
- Informa si hay un desvío mayor al permitido (ej: 10%, 15%, etc.).
- Devuelve un nuevo Excel con el análisis completo y un JSON serializado con los datos de competencia por cada artículo.

---

## 📁 Estructura esperada del archivo `data/articulos.xlsx`

Debe tener las siguientes columnas:

| columna               | descripción                      |
| --------------------- | -------------------------------- |
| `codigo`              | Código interno o SKU             |
| `descripcion`         | Descripción del producto         |
| `ean`                 | Uno o más EANs separados por `;` |
| `costo_final`         | Costo total del producto         |
| `precio_venta_actual` | Precio de venta actual           |
| `margen_actual`       | Margen actual (%)                |
| `precio_venta_futuro` | Precio de venta proyectado       |
| `margen_futuro`       | Margen futuro (%)                |

---

## ✅ Cómo usar

1. Activá tu entorno virtual:

   ```bash
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

2. Ejecutá el script principal:

   ```bash
   python main.py
   ```

3. El programa te pedirá una **tolerancia de desvío** (ej: `15` para 15%).

4. Se generará:
   - Un archivo con los resultados finales: `resultados/final.xlsx`
   - Un archivo de respaldo por si falla: `resultados/progreso_parcial.xlsx`

---

## 🧠 Consideraciones técnicas

- El scraping se hace por lotes de hasta 100 artículos para evitar bloqueos.
- Si el programa se interrumpe, los datos procesados hasta ese momento se guardan.
- Si un artículo no se encuentra en la API, las celdas de análisis quedan vacías.

---

## 🛠 Dependencias principales

- `requests`
- `pandas`
- `openpyxl`

Instalación rápida:

```bash
pip install -r requirements.txt
```

---

## 📍 Ámbito geográfico

Este comparador está diseñado para **San Miguel de Tucumán y alrededores**, usando sucursales seleccionadas (Jumbo, Vea, Carrefour, Libertad, Market, Día, etc.).

---

## 🧾 Licencia

Uso interno y experimental. Datos públicos extraídos de [preciosclaros.gob.ar](https://www.preciosclaros.gob.ar).

---

Desarrollado con 🧉 y un poco de IA.
