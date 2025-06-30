import requests
from time import sleep

API_KEY = "zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96"
BASE_URL = "https://d3e6htiiul5ek9.cloudfront.net/prod"

SUCURSALES_TUCUMAN = [
    "10-2-176", "9-1-71", "10-2-177", "9-1-659", "9-1-125",
    "9-1-134", "9-1-660", "10-1-46", "9-1-727", "9-1-958",
    "9-1-73", "16-1-802", "16-1-702", "9-1-72", "9-3-5227",
    "9-1-70", "10-2-601", "9-1-728", "9-1-903", "9-1-904",
    "9-1-906", "15-1-825", "9-1-730", "16-1-1002", "9-1-13",
    "2005-1-73", "9-1-887", "15-1-8014", "9-1-242", "9-1-243"
]

HEADERS = {
    "x-api-key": API_KEY,
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.preciosclaros.gob.ar",
    "Referer": "https://www.preciosclaros.gob.ar/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}


def obtener_precios_por_ean(ean):
    resultados = []

    # Dividimos en bloques de 20 sucursales (según cómo opera la web oficial)
    for i in range(0, len(SUCURSALES_TUCUMAN), 20):
        bloque = SUCURSALES_TUCUMAN[i:i + 20]
        params = {
            "id_producto": ean,
            "array_sucursales": ",".join(bloque),
            "limit": 30
        }

        try:
            response = requests.get(
                f"{BASE_URL}/producto", headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            for s in data.get("sucursales", []):
                if "message" in s:
                    continue  # sucursal sin stock
                precio = s.get("preciosProducto", {}).get("precioLista")
                nombre_sucursal = s.get("sucursalNombre", "")
                comercio = s.get("banderaDescripcion", "")
                if precio:
                    resultados.append(
                        (f"{comercio} {nombre_sucursal}", precio))

        except requests.exceptions.HTTPError as err:
            print(f"⚠️ Error 403 (bloque): {err}")
        except Exception as e:
            print(f"⚠️ Otro error: {e}")

        sleep(0.5)  # Pausa corta para evitar rate limit

    return procesar_resultados(ean, resultados)


def procesar_resultados(ean, resultados):
    precios = [p[1] for p in resultados]
    if not precios:
        return {
            "coincidencias": [],
            "precio_promedio": None,
            "precio_min": None,
            "precio_max": None,
            "ean_usado": ean
        }

    return {
        "coincidencias": resultados,
        "precio_promedio": round(sum(precios) / len(precios), 2),
        "precio_min": min(precios),
        "precio_max": max(precios),
        "ean_usado": ean
    }


if __name__ == "__main__":
    resultado = obtener_precios_por_ean("7790895006418")
    print("🧾 Resultado:")
    print(resultado)
