import pygame
import random
import sys

# --- Configuración general ---
ANCHO = 600
ALTO = 600
TAM_CELDA = 20
COLUMNAS = ANCHO // TAM_CELDA
FILAS = ALTO // TAM_CELDA
FPS = 12

# --- Colores (R, G, B) ---
NEGRO = (15, 15, 25)
VERDE = (50, 200, 80)
VERDE_OSCURO = (35, 150, 60)
ROJO = (220, 60, 60)
BLANCO = (240, 240, 240)
GRIS = (40, 40, 55)

# --- Direcciones ---
ARRIBA = (0, -1)
ABAJO = (0, 1)
IZQUIERDA = (-1, 0)
DERECHA = (1, 0)


def nueva_comida(serpiente):
    """Genera una posición de comida que no esté sobre la serpiente."""
    while True:
        pos = (random.randint(0, COLUMNAS - 1), random.randint(0, FILAS - 1))
        if pos not in serpiente:
            return pos


def dibujar_celda(pantalla, pos, color):
    rect = pygame.Rect(
        pos[0] * TAM_CELDA, pos[1] * TAM_CELDA, TAM_CELDA, TAM_CELDA
    )
    pygame.draw.rect(pantalla, color, rect)
    pygame.draw.rect(pantalla, NEGRO, rect, 1)


def dibujar_cuadricula(pantalla):
    for x in range(0, ANCHO, TAM_CELDA):
        pygame.draw.line(pantalla, GRIS, (x, 0), (x, ALTO))
    for y in range(0, ALTO, TAM_CELDA):
        pygame.draw.line(pantalla, GRIS, (0, y), (ANCHO, y))


def mostrar_texto(pantalla, texto, tam, color, centro_y):
    fuente = pygame.font.SysFont("consolas", tam, bold=True)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(ANCHO // 2, centro_y))
    pantalla.blit(superficie, rect)


def pantalla_game_over(pantalla, puntaje):
    """Muestra la pantalla de fin de juego. Devuelve True si se reinicia."""
    while True:
        pantalla.fill(NEGRO)
        mostrar_texto(pantalla, "GAME OVER", 60, ROJO, ALTO // 2 - 60)
        mostrar_texto(pantalla, f"Puntaje: {puntaje}", 36, BLANCO, ALTO // 2)
        mostrar_texto(
            pantalla, "ENTER = jugar de nuevo   ESC = salir",
            24, BLANCO, ALTO // 2 + 60
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
    # Estado inicial de la serpiente (centro del tablero)
    inicio = (COLUMNAS // 2, FILAS // 2)
    serpiente = [inicio, (inicio[0] - 1, inicio[1]), (inicio[0] - 2, inicio[1])]
    direccion = DERECHA
    siguiente_direccion = DERECHA
    comida = nueva_comida(serpiente)
    puntaje = 0

    while True:
        # --- Entrada del usuario ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_UP, pygame.K_w) and direccion != ABAJO:
                    siguiente_direccion = ARRIBA
                elif evento.key in (pygame.K_DOWN, pygame.K_s) and direccion != ARRIBA:
                    siguiente_direccion = ABAJO
                elif evento.key in (pygame.K_LEFT, pygame.K_a) and direccion != DERECHA:
                    siguiente_direccion = IZQUIERDA
                elif evento.key in (pygame.K_RIGHT, pygame.K_d) and direccion != IZQUIERDA:
                    siguiente_direccion = DERECHA

        direccion = siguiente_direccion

        # --- Mover la serpiente ---
        cabeza = serpiente[0]
        nueva_cabeza = (cabeza[0] + direccion[0], cabeza[1] + direccion[1])

        # Colisión con paredes
        if (
            nueva_cabeza[0] < 0 or nueva_cabeza[0] >= COLUMNAS
            or nueva_cabeza[1] < 0 or nueva_cabeza[1] >= FILAS
        ):
            return puntaje

        # Colisión consigo misma
        if nueva_cabeza in serpiente:
            return puntaje

        serpiente.insert(0, nueva_cabeza)

        # ¿Comió?
        if nueva_cabeza == comida:
            puntaje += 1
            comida = nueva_comida(serpiente)
        else:
            serpiente.pop()  # avanza sin crecer

        # --- Dibujar todo ---
        pantalla.fill(NEGRO)
        dibujar_cuadricula(pantalla)
        dibujar_celda(pantalla, comida, ROJO)
        for i, segmento in enumerate(serpiente):
            color = VERDE if i == 0 else VERDE_OSCURO
            dibujar_celda(pantalla, segmento, color)

        mostrar_texto(pantalla, f"Puntaje: {puntaje}", 24, BLANCO, 18)
        pygame.display.flip()

        reloj.tick(FPS)


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Snake - Pygame")
    reloj = pygame.time.Clock()

    while True:
        puntaje = jugar(pantalla, reloj)
        pantalla_game_over(pantalla, puntaje)


if __name__ == "__main__":
    main()
