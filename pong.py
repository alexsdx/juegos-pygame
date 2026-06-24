import pygame
import random
import sys

# --- Configuración general ---
ANCHO = 800
ALTO = 600
FPS = 60

# --- Paletas ---
PALETA_ANCHO = 14
PALETA_ALTO = 100
PALETA_VEL = 6          # velocidad del jugador
PALETA_MARGEN = 30      # separación respecto al borde

# --- Pelota ---
PELOTA_TAM = 16
PELOTA_VEL_BASE = 5

# --- IA (jugador derecho) ---
IA_VEL = 5              # velocidad máxima de la CPU

# --- Puntaje para ganar ---
PUNTAJE_GANADOR = 5

# --- Colores (R, G, B) ---
NEGRO = (15, 15, 25)
BLANCO = (240, 240, 240)
GRIS = (90, 90, 110)
VERDE = (80, 220, 120)


def reiniciar_pelota():
    """Coloca la pelota al centro con dirección aleatoria."""
    x = ANCHO // 2 - PELOTA_TAM // 2
    y = ALTO // 2 - PELOTA_TAM // 2
    dir_x = random.choice((-1, 1))
    dir_y = random.choice((-1, 1))
    vel_x = PELOTA_VEL_BASE * dir_x
    vel_y = PELOTA_VEL_BASE * dir_y * random.uniform(0.5, 1.0)
    return pygame.Rect(x, y, PELOTA_TAM, PELOTA_TAM), vel_x, vel_y


def mostrar_texto(pantalla, texto, tam, color, x, y, centrado=True):
    fuente = pygame.font.SysFont("consolas", tam, bold=True)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect()
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    pantalla.blit(superficie, rect)


def dibujar_red(pantalla):
    """Dibuja la línea punteada central."""
    for y in range(0, ALTO, 30):
        pygame.draw.rect(pantalla, GRIS, (ANCHO // 2 - 2, y, 4, 18))


def pantalla_fin(pantalla, ganador):
    """Pantalla de fin de partida. Devuelve True si se reinicia."""
    while True:
        pantalla.fill(NEGRO)
        mostrar_texto(pantalla, f"¡Gana {ganador}!", 60, VERDE, ANCHO // 2, ALTO // 2 - 60)
        mostrar_texto(
            pantalla, "ENTER = jugar de nuevo   ESC = salir",
            24, BLANCO, ANCHO // 2, ALTO // 2 + 20
        )
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def jugar(pantalla, reloj):
    # Paleta izquierda (jugador) y derecha (CPU)
    jugador = pygame.Rect(
        PALETA_MARGEN, ALTO // 2 - PALETA_ALTO // 2, PALETA_ANCHO, PALETA_ALTO
    )
    cpu = pygame.Rect(
        ANCHO - PALETA_MARGEN - PALETA_ANCHO,
        ALTO // 2 - PALETA_ALTO // 2, PALETA_ANCHO, PALETA_ALTO
    )

    pelota, vel_x, vel_y = reiniciar_pelota()
    puntos_jugador = 0
    puntos_cpu = 0

    while True:
        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # --- Movimiento del jugador (flechas o W/S) ---
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            jugador.y -= PALETA_VEL
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            jugador.y += PALETA_VEL
        jugador.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

        # --- IA simple: sigue la pelota con velocidad limitada ---
        if cpu.centery < pelota.centery - 10:
            cpu.y += IA_VEL
        elif cpu.centery > pelota.centery + 10:
            cpu.y -= IA_VEL
        cpu.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

        # --- Mover la pelota ---
        pelota.x += vel_x
        pelota.y += vel_y

        # Rebote en techo y suelo
        if pelota.top <= 0:
            pelota.top = 0
            vel_y *= -1
        elif pelota.bottom >= ALTO:
            pelota.bottom = ALTO
            vel_y *= -1

        # Rebote en las paletas
        if pelota.colliderect(jugador) and vel_x < 0:
            pelota.left = jugador.right
            vel_x *= -1
            # El ángulo depende de dónde golpea respecto al centro de la paleta
            desfase = (pelota.centery - jugador.centery) / (PALETA_ALTO / 2)
            vel_y = PELOTA_VEL_BASE * desfase
        elif pelota.colliderect(cpu) and vel_x > 0:
            pelota.right = cpu.left
            vel_x *= -1
            desfase = (pelota.centery - cpu.centery) / (PALETA_ALTO / 2)
            vel_y = PELOTA_VEL_BASE * desfase

        # --- Puntos ---
        if pelota.right < 0:
            puntos_cpu += 1
            pelota, vel_x, vel_y = reiniciar_pelota()
        elif pelota.left > ANCHO:
            puntos_jugador += 1
            pelota, vel_x, vel_y = reiniciar_pelota()

        # --- ¿Fin de partida? ---
        if puntos_jugador >= PUNTAJE_GANADOR:
            return "Jugador"
        if puntos_cpu >= PUNTAJE_GANADOR:
            return "CPU"

        # --- Dibujar ---
        pantalla.fill(NEGRO)
        dibujar_red(pantalla)
        pygame.draw.rect(pantalla, BLANCO, jugador)
        pygame.draw.rect(pantalla, BLANCO, cpu)
        pygame.draw.ellipse(pantalla, VERDE, pelota)

        mostrar_texto(pantalla, str(puntos_jugador), 50, BLANCO, ANCHO // 2 - 60, 50)
        mostrar_texto(pantalla, str(puntos_cpu), 50, BLANCO, ANCHO // 2 + 60, 50)

        pygame.display.flip()
        reloj.tick(FPS)


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pong - Pygame")
    reloj = pygame.time.Clock()

    while True:
        ganador = jugar(pantalla, reloj)
        pantalla_fin(pantalla, ganador)


if __name__ == "__main__":
    main()
