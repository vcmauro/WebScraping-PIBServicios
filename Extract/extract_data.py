import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup

# ------------------------
# 1. Cargar HTML local
# ------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(script_dir, 'tradingeconomics.html')

with open(html_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file.read(), 'html.parser')

# ------------------------
# 2. Extraer primera tabla (TABLA 1)
# ------------------------
tabla_1 = []
referencia_servicios = None  # Para usarla en la tabla 2

tabla1 = soup.find('table', class_='table')
if tabla1:
    filas = tabla1.find_all('tr')[1:]
    for fila in filas:
        celdas = fila.find_all('td')
        if len(celdas) >= 5:
            indicador = celdas[0].text.strip()
            actual = celdas[1].text.strip()
            anterior = celdas[2].text.strip()
            unidad = celdas[3].text.strip()
            referencia = celdas[4].text.strip()

            fila_data = {
                "Indicador": indicador,
                "Valor_actual": actual,
                "Valor_anterior": anterior,
                "Unidad": unidad,
                "Referencia": referencia
            }

            tabla_1.append(fila_data)

            if indicador.lower() == "pib de servicios":
                referencia_servicios = referencia

# ------------------------
# 3. Extraer segunda tabla (TABLA 2) emparejando claves dinámicamente
# ------------------------
tabla_2 = {}
todas_las_tablas = soup.find_all('table')

# Mapeo de nombres amigables
claves_deseadas = {
    "real": "Valor_actual",
    "anterior": "Valor_anterior",
    "mayor": "Mayor",
    "menor": "Menor",
    "fechas": "Fechas",
    "unidad": "Unidad",
    "frecuencia": "Frecuencia"
}

for tabla in todas_las_tablas:
    ths = tabla.find_all('th')
    encabezados = [th.text.strip().lower() for th in ths]

    if set(claves_deseadas.keys()).issubset(set(encabezados)):
        filas = tabla.find_all('tr')
        if len(filas) > 1:
            celdas = filas[1].find_all('td')
            for idx, encabezado in enumerate(encabezados):
                clave_limpia = encabezado.lower()
                if clave_limpia in claves_deseadas and idx < len(celdas):
                    tabla_2[claves_deseadas[clave_limpia]] = celdas[idx].text.strip()
            tabla_2["Referencia"] = referencia_servicios if referencia_servicios else "no disponible"
        break

# ------------------------
# 4. Construir JSON final
# ------------------------
json_final = {
    "tabla_1": tabla_1,
    "tabla_2": tabla_2
}

# ------------------------
# 5. Guardar en EXTRACT/<fecha-hoy>/pib_data.json
# ------------------------
fecha = datetime.now(ZoneInfo("America/Lima")).strftime('%d-%m-%Y')
carpeta_salida = os.path.join(script_dir, '..', 'EXTRACT', fecha)
os.makedirs(carpeta_salida, exist_ok=True)

ruta_salida = os.path.join(carpeta_salida, 'pib_data.json')
with open(ruta_salida, 'w', encoding='utf-8') as f:
    json.dump(json_final, f, indent=4, ensure_ascii=False)

print(f"✅ JSON guardado exitosamente en: {ruta_salida}")