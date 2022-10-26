import pygame, sys

from pygame.locals import *
# importamos pygame

clock = pygame.time.Clock() # iniciamos nuestro reloj
 
pygame.init() # inicializamos pygame
pygame.display.set_caption('Pick em All') # Nombre de la ventana

WINDOW_SIZE = (1200,700) # Tamaño de la ventana
movimiento_fondo=0
px=20
py=200
ancho=40
velocidad=10
salto=False
cuentasalto=10
cuentapasos=0
izquierda=False
derecha=False
verdadero_scroll=[0,0]
W,H=1200,700
screen = pygame.display.set_mode((W,H)) 

display = pygame.Surface((300, 200))

fondo=pygame.image.load("FOREST1.png").convert()
display.blit(fondo,(0,0))

player_image = pygame.image.load('ArthurCaminar1.png').convert()
player_image.set_colorkey((0, 0, 0))
tierra_image = pygame.image.load('dirt1.png')
tierra_pasto_image = pygame.image.load('1.png')
tierra_1_image= pygame.image.load("3.png")
picos_image=pygame.image.load("picos.png")
TILE_SIZE = 16

quieto = pygame.image.load("Arthur_Caminar1.png")

movdere = [pygame.image.load("Arthur_Caminar1.png"),
pygame.image.load("Arthur_Caminar2.png"),
pygame.image.load("Arthur_Caminar3.png"),
pygame.image.load("Arthur_Caminar4.png")]

salto = [pygame.image.load("ArthurSalto1.png"),
pygame.image.load("ArthurSalto2.png"),
pygame.image.load("ArthurSalto3.png"),
pygame.image.load("ArthurSalto4.png"),
pygame.image.load("ArthurSalto5.png")]

movizqui = [pygame.image.load("ArthurCaminarizq1.png"),
pygame.image.load("ArthurCaminarizq2.png"),
pygame.image.load("ArthurCaminarizq3.png"),
pygame.image.load("ArthurCaminarizq4.png")]


def cargar_mapa(camino):
    f=open(camino +".txt","r")
    dato=f.read()
    f.close()
    dato=dato.split("\n")
    mapa_juego1=[]
    for fila in dato:
        mapa_juego1.append(list(fila))
    return mapa_juego1

mapa_juego1=cargar_mapa("mapa1")

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(150, 150, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

while True: # Bucle del juego
    verdadero_scroll[0] +=(player_rect.x-verdadero_scroll[0]-150)/5
    verdadero_scroll[1]+=(player_rect.y-verdadero_scroll[1]-100)/5
    scroll=verdadero_scroll.copy()
    scroll[0]=int(scroll[0])
    scroll[1]=int(scroll[1])

    x_relativa = movimiento_fondo % fondo.get_rect().width
    display.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
    if x_relativa < W:
      display.blit(fondo, (x_relativa, 0))
    movimiento_fondo-=.1
    tile_rects = []
    y = 0
    for fila in mapa_juego1:
        x = 0
        for tile in fila:
            if tile == '1':
                display.blit(tierra_pasto_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '2':
                display.blit(tierra_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '3':
                display.blit(tierra_1_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile=="4":
                display.blit(picos_image, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_image, (player_rect.x  -scroll[0], player_rect.y -scroll[1]))

    for event in pygame.event.get():
        if event.type==QUIT:
         pygame.quit()
         sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 4:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # actualizamos nuestra pantalla
    clock.tick(60) # Ponemos el juego a 60 fps
