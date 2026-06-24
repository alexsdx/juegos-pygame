# 🎮 Juegos en Pygame

Colección de dos juegos clásicos reimplementados en **Python** con la librería **[Pygame](https://www.pygame.org/)**: el mítico **Snake** 🐍 y el legendario **Pong** 🏓.

Ambos son juegos completos y autocontenidos en un solo archivo cada uno, ideales para aprender los fundamentos de la programación de videojuegos: bucle principal, manejo de eventos, detección de colisiones, dibujado y control de fotogramas por segundo.

---

## 📦 Contenido del repositorio

| Archivo | Descripción |
|---------|-------------|
| `snake.py` | Juego de la serpiente clásico. |
| `pong.py` | Juego de Pong (Jugador vs CPU). |
| `README.md` | Este archivo. |
| `.gitignore` | Exclusiones de archivos temporales de Python. |

---

## 🔧 Requisitos e instalación

1. Tener **Python 3.8 o superior** instalado.
2. Instalar la librería Pygame:

   ```bash
   pip install pygame
   ```

---

## 🐍 Snake (`snake.py`)

El objetivo es comer la mayor cantidad de comida posible para hacer crecer la serpiente, sin chocar contra las paredes ni contra tu propio cuerpo.

### ▶️ Cómo jugar

```bash
python snake.py
```

### 🎮 Controles

| Tecla | Acción |
|-------|--------|
| **Flechas** o **W A S D** | Mover la serpiente |
| **ENTER** | Reiniciar tras perder |
| **ESC** | Salir |

### ✨ Características

- La serpiente crece cada vez que come.
- La comida aparece en posiciones aleatorias, nunca sobre la serpiente.
- Detección de colisiones con las paredes y con el propio cuerpo.
- No se permiten giros de 180° (no puedes invertir la dirección de golpe).
- Contador de puntaje y pantalla de *Game Over* con opción de reiniciar.

### ⚙️ Personalización

En la sección de configuración al inicio del archivo puedes ajustar:

- `FPS` → velocidad del juego (mayor = más difícil).
- `ANCHO`, `ALTO`, `TAM_CELDA` → tamaño del tablero y de las celdas.
- Los colores definidos como constantes.

---

## 🏓 Pong (`pong.py`)

Un Pong clásico donde controlas la paleta izquierda y te enfrentas a una CPU. El primero en llegar a 5 puntos gana.

### ▶️ Cómo jugar

```bash
python pong.py
```

### 🎮 Controles

| Tecla | Acción |
|-------|--------|
| **Flechas ↑ ↓** o **W / S** | Mover tu paleta |
| **ENTER** | Jugar de nuevo tras una partida |
| **ESC** | Salir |

### ✨ Características

- Modo **Jugador vs CPU** con una IA que sigue la pelota.
- Rebotes con ángulo variable según el punto de la paleta donde golpea la pelota.
- Marcador en pantalla y fin de partida al llegar a 5 puntos.
- Pantalla de victoria con opción de reiniciar.

### ⚙️ Personalización

En la sección de configuración al inicio del archivo puedes ajustar:

- `PUNTAJE_GANADOR` → puntos necesarios para ganar.
- `IA_VEL` → dificultad de la CPU (mayor = más difícil).
- `PALETA_VEL`, `PALETA_ALTO`, `PELOTA_VEL_BASE` → velocidad y tamaño de las paletas y la pelota.

---

## 📜 Licencia

Proyecto de uso libre con fines educativos. ¡Siéntete libre de modificarlo y experimentar!
