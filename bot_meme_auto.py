import os
import time
import random
import requests
from datetime import datetime
import json

# ===========================================
# ⚙️ CONFIGURACIÓN DEL BOT
# ===========================================

# Lista de páginas con sus tokens de acceso
PAGINAS = [
    {"id": "218002698753443", "token": "EAAG...TOKEN1"},
    {"id": "109770060936390", "token": "EAAG...TOKEN2"},
    {"id": "193608728242239", "token": "EAAG...TOKEN3"}
]

# Carpeta donde están tus memes (ajustada para tu VM)
CARPETA_MEMES = r"/home/jonatanpc23/bot_memes/memes"

# Tiempo entre publicaciones (en segundos)
INTERVALO = 60 * 60 * 2  # Cada 2 horas

# Archivo donde se guarda el registro de memes ya publicados
ARCHIVO_LOG = "memes_publicados.json"

# ===========================================
# 🧩 FUNCIONES
# ===========================================

def cargar_memes_publicados():
    """Carga la lista de memes ya publicados desde el archivo JSON."""
    if not os.path.exists(ARCHIVO_LOG):
        return []
    with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_memes_publicados(lista):
    """Guarda la lista de memes publicados."""
    with open(ARCHIVO_LOG, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

def seleccionar_meme(memes_publicados):
    """Selecciona un meme que no haya sido publicado aún."""
    archivos = [f for f in os.listdir(CARPETA_MEMES) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    disponibles = [m for m in archivos if m not in memes_publicados]

    if not disponibles:
        print("⚠️ No hay nuevos memes disponibles. Agrega más imágenes a la carpeta.")
        return None

    return random.choice(disponibles)

def publicar_meme(pagina_id, access_token, meme):
    """Sube el meme a una página de Facebook."""
    ruta = os.path.join(CARPETA_MEMES, meme)
    mensaje = random.choice([
        "😂 Ríete un rato 😆"
        "🤣 No puedo con esto 🤣"
        "😅 Clásico pero cierto"
        "🙈 Todos hemos estado ahí..."
        "💀 Humor 100% garantizado"
        "🔥 Nivel de risa: máximo"
        "🤪 Pura joya del internet"
        "🧠 Risa inteligente (más o menos 😅)"
        "📸 El meme del momento"
        "🤣 A esto le llamo arte moderno"
        "💥 Literalmente yo"
        "😎 Esto merece un Oscar"
        "😂 Si te ríes, pierdes"
        "👀 ¿Te pasó igual?
        "⚡ Lo mejor que verás hoy
        "🧃 Pura vitamina M (de meme)"
        "💫 El algoritmo hizo lo suyo"
        "😂 Ni el Excel lo entiende"
        "😵 Esto me representa"
        "🔥 Nivel dios de humor"
    ])

    url = f"https://graph.facebook.com/{pagina_id}/photos"
    with open(ruta, "rb") as imagen:
        archivos_post = {'source': imagen}
        data = {'caption': mensaje, 'access_token': access_token}
        response = requests.post(url, files=archivos_post, data=data)

    if response.status_code == 200:
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Publicado en {pagina_id}: {meme}")
        return True
    else:
        print(f"❌ Error en {pagina_id}: {response.text}")
        return False

# ===========================================
# 🚀 BUCLE PRINCIPAL
# ===========================================

def main():
    memes_publicados = cargar_memes_publicados()

    while True:
        meme = seleccionar_meme(memes_publicados)
        if meme:
            for pagina in PAGINAS:
                ok = publicar_meme(pagina["id"], pagina["token"], meme)
                if ok and meme not in memes_publicados:
                    memes_publicados.append(meme)
                    guardar_memes_publicados(memes_publicados)

        print(f"⏳ Esperando {INTERVALO/3600:.1f} horas antes del siguiente post...\n")
        time.sleep(INTERVALO)

if __name__ == "__main__":
    main()
