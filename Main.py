import pygame import requests import threading import time

================= CONFIG =================

COHERE_API_KEY = "TU_API_KEY_COHERE" ELEVEN_API_KEY = "TU_API_KEY_ELEVENLABS" VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # voz por defecto

=========================================

pygame.init() screen = pygame.display.set_mode((800, 600)) pygame.display.set_caption("VRM IA") font = pygame.font.SysFont(None, 30)

clock = pygame.time.Clock()

estado_actual = "neutral" texto_respuesta = ""

================= IA =================

def generar_texto(prompt): global texto_respuesta

headers = {
    "Authorization": f"Bearer {COHERE_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "command-r-plus",
    "message": prompt
}

res = requests.post("https://api.cohere.ai/v1/chat", json=data, headers=headers)
texto_respuesta = res.json().get("text", "")

hablar(texto_respuesta)

def hablar(texto): url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "xi-api-key": ELEVEN_API_KEY,
    "Content-Type": "application/json"
}

data = {
    "text": texto,
    "model_id": "eleven_multilingual_v2"
}

response = requests.post(url, json=data, headers=headers)

with open("voz.mp3", "wb") as f:
    f.write(response.content)

pygame.mixer.init()
pygame.mixer.music.load("voz.mp3")
pygame.mixer.music.play()

================= UI =================

def dibujar_boton(texto, x, y): rect = pygame.Rect(x, y, 150, 50) pygame.draw.rect(screen, (70, 70, 200), rect) txt = font.render(texto, True, (255,255,255)) screen.blit(txt, (x+10, y+15)) return rect

================= LOOP =================

running = True while running: screen.fill((20, 20, 30))

btn_feliz = dibujar_boton("Feliz", 50, 500)
btn_triste = dibujar_boton("Triste", 250, 500)
btn_enfadado = dibujar_boton("Enfadado", 450, 500)

# Simulación visual simple
if estado_actual == "feliz":
    pygame.draw.circle(screen, (255,255,0), (400,200), 50)
elif estado_actual == "triste":
    pygame.draw.circle(screen, (100,100,255), (400,200), 50)
elif estado_actual == "enfadado":
    pygame.draw.circle(screen, (255,50,50), (400,200), 50)

# Texto IA
txt_surface = font.render(texto_respuesta[:60], True, (255,255,255))
screen.blit(txt_surface, (50, 50))

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        if btn_feliz.collidepoint(event.pos):
            estado_actual = "feliz"
            threading.Thread(target=generar_texto, args=("Responde feliz",)).start()

        if btn_triste.collidepoint(event.pos):
            estado_actual = "triste"
            threading.Thread(target=generar_texto, args=("Responde triste",)).start()

        if btn_enfadado.collidepoint(event.pos):
            estado_actual = "enfadado"
            threading.Thread(target=generar_texto, args=("Responde enfadado",)).start()

pygame.display.flip()
clock.tick(60)

pygame.quit()
