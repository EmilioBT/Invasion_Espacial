import pygame
import random
import math
from pygame import mixer

# Inicializar a pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("nave-espacial.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Espacio.png")

# Texto Final
fuente_final = pygame.font.Font('freesansbold.ttf', 32)

# Musica
mixer.music.load('fondo.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Player
playerImg = pygame.image.load("nave.png")
player_X = 368
player_Y = 500
player_X_Cambio = 0

# Asteroides
asteroideImg = []
enemigo_X = []
enemigo_Y = []
enemigo_X_Cambio = []
enemigo_Y_Cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    asteroideImg.append(pygame.image.load("asteroide.png"))
    enemigo_X.append(random.randint(0,736))
    enemigo_Y.append(random.randint(50,200))
    enemigo_X_Cambio.append(0.3)
    enemigo_Y_Cambio.append(50)

# Bala
balas = []
balaImg = pygame.image.load("bala.png")
bala_X = 0
bala_Y = 500
bala_Y_Cambio = 0.3
bala_visible = False

# Puntuacion
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# Funcion puntuacion
def mostrar_puntuacion(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255,255,255))
    pantalla.blit(texto, (x, y))

# Funcion del jugador
def player(x, y):
    pantalla.blit(playerImg, (x, y))

# Funcion del asteroide
def asteroide(x, y, ene):
    pantalla.blit(asteroideImg[ene], (x, y))

# Funcion disparo balas
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(balaImg, (x + 16, y + 10))

# Funcion colisiones
def colision_objetos (x1, x2, y1, y2):
    distancia = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distancia < 27:
        return True
    else:
        return False

# Funcion Game Over
def game_over ():
    texto_game_over = fuente_final.render('GAME OVER', True, (255, 255, 255))
    pantalla.blit(texto_game_over, (60, 200))

# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # Imagen Fondo
    pantalla.blit(fondo, (0,0))

    # Iterar eventos
    for evento in pygame.event.get():

        # Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Presion teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                player_X_Cambio = -0.3
            if evento.key == pygame.K_RIGHT:
                player_X_Cambio = 0.3
            if evento.key == pygame.K_SPACE:
                sonido_disparo = mixer.Sound('disparo.mp3')
                sonido_disparo.play()
                nueva_bala = {
                    "x": player_X,
                    "y": player_Y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)
                if not bala_visible:
                    bala_X = player_X
                    disparar_bala(bala_X, bala_Y)

        # Soltar teclas
        if evento.type ==pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                player_X_Cambio = 0

    # Modificar posicion del jugador
    player_X += player_X_Cambio

    # Delimitar pantalla del jugador
    if player_X <= 0:
        player_X = 0
    if player_X >=736:
        player_X = 736

    # Modificar posicion del enemigo
    for e in range(cantidad_enemigos):
        # Game over
        if enemigo_Y[e] > 490:
            for k in range(cantidad_enemigos):
                enemigo_Y[k] = 1000
            game_over()
            break
        enemigo_X[e] += enemigo_X_Cambio[e]
        # Delimitar pantalla del enemigo
        if enemigo_X[e] <= 0:
            enemigo_X_Cambio[e] = 0.3
            enemigo_Y[e] += enemigo_Y_Cambio[e]
        if enemigo_X[e] >= 736:
            enemigo_X_Cambio[e] = -0.3
            enemigo_Y[e] += enemigo_Y_Cambio[e]
        # Colision
        """colision = colision_objetos(enemigo_X[e], bala_X, enemigo_Y[e], bala_Y)
        if colision:
            bala_Y = 500
            bala_visible = False
            puntaje += 1
            enemigo_X[e] = random.randint(0, 736)
            enemigo_Y[e] = random.randint(50, 200)
        asteroide(enemigo_X[e], enemigo_Y[e], e)"""
        for bala in balas:
            colision_bala_enemigo = colision_objetos( enemigo_X[e], bala["x"], enemigo_Y[e], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("disparo.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_X[e] = random.randint(0, 736)
                enemigo_Y[e] = random.randint(20, 200)
                break

        asteroide(enemigo_X[e], enemigo_Y[e], e)


    # Movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(balaImg, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)
    """if bala_Y <= -64:
        bala_Y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_X, bala_Y)
        bala_Y -= bala_Y_Cambio"""



    player(player_X, player_Y)

    # Mostrar puntuacion
    mostrar_puntuacion(texto_x, texto_y)

    # Actualizar pantalla
    pygame.display.update()