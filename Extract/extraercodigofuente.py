import requests  # Para hacer solicitudes HTTP

# Configurar cabeceras (User-Agent) para simular un navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

# URL del sitio que deseas extraer
url = "https://es.tradingeconomics.com/peru/gdp-from-services"

# Hacer la solicitud HTTP con el user-agent definido
response = requests.get(url, headers=headers)

# Verificar si la respuesta fue exitosa (código 200 OK)
if response.status_code == 200:
    # Crear carpeta si no existe (opcional, pero recomendable)
    import os
    os.makedirs("EXTRACT", exist_ok=True)

    # Guardar el HTML en un archivo local
    with open("EXTRACT/tradingeconomics.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("✅ HTML guardado exitosamente.")
else:
    # Mostrar mensaje de error si no se pudo acceder
    print(f"❌ Error {response.status_code} al intentar acceder a la página.")
