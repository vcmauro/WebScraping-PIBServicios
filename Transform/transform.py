import os
import json
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

# -----------------------
# 1. Rutas
# -----------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join(script_dir, '..', 'EXTRACT')
transform_path = os.path.join(script_dir, 'TRANSFORM')
os.makedirs(transform_path, exist_ok=True)

# -----------------------
# 2. Cargar CSVs existentes (si existen)
# -----------------------
csv_general_path = os.path.join(transform_path, 'pib_general.csv')
csv_servicios_path = os.path.join(transform_path, 'pib_servicios.csv')

df_general = pd.read_csv(csv_general_path) if os.path.exists(csv_general_path) else pd.DataFrame()
df_servicios = pd.read_csv(csv_servicios_path) if os.path.exists(csv_servicios_path) else pd.DataFrame()

# Obtener referencias ya existentes
ref_general_existentes = set(df_general['Referencia']) if 'Referencia' in df_general.columns else set()
ref_servicios_existentes = set(df_servicios['Referencia']) if 'Referencia' in df_servicios.columns else set()

# -----------------------
# 3. Inicializar nuevas filas
# -----------------------
tabla1_nuevas = []
tabla2_nuevas = []

# -----------------------
# 4. Explorar EXTRACT
# -----------------------
for root, dirs, files in os.walk(base_path):
    if 'pib_data.json' in files:
        ruta_json = os.path.join(root, 'pib_data.json')
        fecha = os.path.basename(root)  # Fecha de carpeta

        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Procesar tabla_1
            nuevas_filas_1 = []
            for fila in data.get("tabla_1", []):
                referencia = fila.get("Referencia")
                if referencia not in ref_general_existentes:
                    fila['fecha'] = fecha
                    nuevas_filas_1.append(fila)
                else:
                    print(f"⏩ Referencia {referencia} ya existe en tabla_1. Saltando.")

            # Procesar tabla_2
            fila2 = data.get("tabla_2", {})
            referencia2 = fila2.get("Referencia")
            if referencia2 and referencia2 not in ref_servicios_existentes:
                fila2['fecha'] = fecha
                tabla2_nuevas.append(fila2)
            else:
                print(f"⏩ Referencia {referencia2} ya existe en tabla_2. Saltando.")

            tabla1_nuevas.extend(nuevas_filas_1)

        except Exception as e:
            print(f"❌ Error procesando {ruta_json}: {e}")

# -----------------------
# 5. Guardar CSVs
# -----------------------
if tabla1_nuevas:
    df_nuevas_1 = pd.DataFrame(tabla1_nuevas)
    df_resultado_1 = pd.concat([df_general, df_nuevas_1], ignore_index=True)
    df_resultado_1.to_csv(csv_general_path, index=False)
    print("✅ Actualizado: pib_general.csv")

if tabla2_nuevas:
    df_nuevas_2 = pd.DataFrame(tabla2_nuevas)
    df_resultado_2 = pd.concat([df_servicios, df_nuevas_2], ignore_index=True)
    df_resultado_2.to_csv(csv_servicios_path, index=False)
    print("✅ Actualizado: pib_servicios.csv")

if not tabla1_nuevas and not tabla2_nuevas:
    print("🔁 No se detectaron nuevas referencias. Nada fue agregado.")