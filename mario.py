import pygame, sys
from pygame.locals import*


pygame.init()
W,H = 1440, 580
pantalla = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pick Em All")

imgscreen = pygame.image.load("CITY.png").convert()
pantalla.blit(imgscreen,(0,0))

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

x = 0
px = 50
py = 400
ancho = 40
velocidad = 10

# Control de FPS
reloj = pygame.time.Clock()

# Variables salto
salto = False
# Contador de salto
cuentaSalto = 10

# Variables dirección
izquierda = False
derecha = False

# Pasos
cuentaPasos = 0

# Movimiento
def recarga_pantalla():
	# Variables globales
	global cuentaPasos
	global x

	# Fondo en movimiento
	x_relativa = x % imgscreen.get_rect().width
	pantalla.blit(imgscreen, (x_relativa - imgscreen.get_rect().width, 0))
	if x_relativa < W:
		pantalla.blit(imgscreen, (x_relativa, 0))
	x -= 5
	# Contador de pasos
	if cuentaPasos + 1 >= 4:
		cuentaPasos = 0
	# Movimiento a la izquierda
	if izquierda:
		pantalla.blit(movizqui[cuentaPasos // 1], (int(px), int(py)))
		cuentaPasos += 1

		# Movimiento a la derecha
	elif derecha:
		pantalla.blit(movdere[cuentaPasos // 1], (int(px), int(py)))
		cuentaPasos += 1

	elif salto + 1 >= 5:
		pantalla.blit(salto[cuentaPasos // 1], (int(px), int(py)))
		cuentaPasos += 1

	else:
		pantalla.blit(quieto,(int(px), int(py)))

ejecuta = True

# Bucle de acciones y controles
while ejecuta:
	# FPS
	reloj.tick(24)

	# Bucle del juego
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			ejecuta = False

	# Opción tecla pulsada
	keys = pygame.key.get_pressed()

	# Tecla A - Moviemiento a la izquierda
	if keys[pygame.K_a] and px > velocidad:
		px -= velocidad
		izquierda = True
		derecha = False

	# Tecla D - Moviemiento a la derecha
	elif keys[pygame.K_d] and px < 900 - velocidad - ancho:
		px += velocidad
		izquierda = False
		derecha = True

	# Personaje quieto
	else:
		izquierda = False
		derecha = False
		cuentaPasos = 0

	# Tecla W - Moviemiento hacia arriba
	if keys[pygame.K_w] and py > 100:
		py -= velocidad

	# Tecla S - Moviemiento hacia abajo
	if keys[pygame.K_s] and py < 300:
		py += velocidad
	# Tecla SPACE - Salto
	if not salto:
		if keys[pygame.K_SPACE]:
			salto = True
			izquierda = False
			derecha = False
			cuentaPasos = 0
	else:
		if cuentaSalto >= -10:
			py -= (cuentaSalto * abs(cuentaSalto)) * 0.5
			cuentaSalto -= 1
		else:
			cuentaSalto = 10
			salto = False

	# Actualización de la ventana
	pygame.display.update()
	#Llamada a la función de actualización de la ventana
	recarga_pantalla()

# Salida del juego
pygame.quit()