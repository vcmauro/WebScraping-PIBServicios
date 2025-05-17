import os
import json
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

# -----------------------
# 1. Rutas
# -----------------------
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'EXTRACT')
transform_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TRANSFORM')
os.makedirs(transform_path, exist_ok=True)

# -----------------------
# 2. Inicializar listas
# -----------------------
tabla1_list = []
tabla2_list = []

# -----------------------
# 3. Explorar archivos
# -----------------------
for root, dirs, files in os.walk(base_path):
    if 'pib_data.json' in files:
        try:
            ruta_json = os.path.join(root, 'pib_data.json')
            with open(ruta_json, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Fecha desde el nombre de carpeta
            fecha = os.path.basename(root)

            # Procesar tabla_1
            for fila in data.get("tabla_1", []):
                fila['fecha'] = fecha
                tabla1_list.append(fila)

            # Procesar tabla_2 (una sola fila)
            if "tabla_2" in data:
                fila2 = data["tabla_2"]
                fila2['fecha'] = fecha
                tabla2_list.append(fila2)

        except Exception as e:
            print(f"⚠️ Error al leer {ruta_json}: {e}")

# -----------------------
# 4. Guardar como CSV
# -----------------------
if tabla1_list:
    df1 = pd.DataFrame(tabla1_list)
    df1.to_csv(os.path.join(transform_path, 'pib_general.csv'), index=False)
    print("✅ Transformación completada: pib_general.csv")

if tabla2_list:
    df2 = pd.DataFrame(tabla2_list)
    df2.to_csv(os.path.join(transform_path, 'pib_servicios.csv'), index=False)
    print("✅ Transformación completada: pib_servicios.csv")

if not tabla1_list and not tabla2_list:
    print("❌ No se encontraron archivos válidos para transformar.")