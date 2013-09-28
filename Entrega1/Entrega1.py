import pygame
import random
import time
from pygame.locals import *
#Mi entrega 1 corresponde a un poco de experimentacion que hice con el codigo de un tutorial para mover un objeto en la pantalla
#mezclado con la posibilidad de disparar en la direccion en que el cuadrado esta viendo (la ultima direccion a la que apunto)
#Ademas incluye paredes las cuales no pueden ser atravesada. Incluye un enemigo que ataca de forma periodica (use modulo time)


black = (0,0,0)
white = (255,255,255)
green = (0,255,0)      

#Clase correspondiente a balas
class Bullet(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    direccion = 0
    def __init__(self):
        # Call the parent's constructor

        pygame.sprite.Sprite.__init__(self)
         
        # Set height, width
        self.image = pygame.Surface([6, 6])
        self.image.fill((black))
 
        #Entregar coordenadas del objeto (el rect indica donde esta!)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        direccion = 0
         
    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x=x
        self.change_y=y
         
    # Find a new position for the player
    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

 #El jugador
class Player(pygame.sprite.Sprite):
 
    
    change_x=0
    change_y=0
     

    def __init__(self,x,y):
        # Constructor del padre (clase sprite)
        pygame.sprite.Sprite.__init__(self)
         
        #Dimensiones del personaje y su color
        self.image = pygame.Surface([20, 20])
        self.image.fill((green))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
     
    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
         
    # Nueva posicion de personaje (evita colision con paredes
    def update(self,walls):

        ##Solo se edita la posicion del personaje si es falso que hay una colision con un objeto wall
        #if not pygame.sprite.spritecollide(self,walls,False):
        #     self.rect.x += self.change_x
        #     self.rect.y += self.change_y
        #Eso asi no funciono porque se queda atascado utilizare la manera en que lo hacen en el tutorial
        #guardar la posicion actual en una variable auxiliar, y mover la persona a una nueva posicion
        #si esta es una colision volver a la vieja
        old_x = self.rect.x
     
        self.rect.x = self.change_x + old_x
     
        if pygame.sprite.spritecollide(self,walls,False):
            self.rect.x = old_x

        old_y = self.rect.y
     
        self.rect.y = self.change_y + old_y
        if pygame.sprite.spritecollide(self,walls,False):
            self.rect.y = old_y

#Clase de paredes
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(black)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
       
#Clase de enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
         
        #Dimensiones del personaje y su color
        self.image = pygame.Surface([30, 30])
        self.image.fill((green))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        pygame.time.set_timer(USEREVENT,500)
        #Timer para disparos
       

    def shoot (self,bullets):
        newbullet = Bullet()
        newbullet.rect.x= self.rect.x
        newbullet.rect.y= self.rect.y
        newbullet.direccion = 2
        bullets.add(newbullet)

#Comienza el uso de pygame (recien aca se pueden instanciar sprites!)

pygame.init()
 
# Crear pantalla de tamaño dado

screen = pygame.display.set_mode([500, 500])
 
# Display

pygame.display.set_caption('Entrega1')
 
# Creacion de los objetos del programa

player = Player( 250,250 )
movingsprites = pygame.sprite.Group()
movingsprites.add(player)
bullet_list = pygame.sprite.Group()
walls = pygame.sprite.Group()
enemybullets = pygame.sprite.Group()
unicoenemigo = Enemy(30,50)
enemigos = pygame.sprite.Group()
enemigos.add(unicoenemigo)
#Crear mundo

wall1 = Wall(0,0,20,500)
wall2 = Wall(480,0,20,500)
wall3 = Wall(20,0,460,20)
wall4 = Wall(20,480,460,20)
wall5 = Wall(20,100,230,20)
wall6 = Wall(20,200,230,20)
walls.add(wall1)
walls.add(wall2)
walls.add(wall3)
walls.add(wall4)
walls.add(wall5)
walls.add(wall6)

clock = pygame.time.Clock()
done = False
direccionbala = 0 #Left = 1, RIGHT = 2, UP = 3, Down = 4

while done == False:
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
 
        # Set the speed based on the key pressed
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                player.changespeed(-3,0)
                direccionbala = 1
            if event.key == pygame.K_RIGHT:
                player.changespeed(3,0)
                direccionbala = 2
            if event.key == pygame.K_UP:
                player.changespeed(0,-3)
                direccionbala = 3
            if event.key == pygame.K_DOWN:
                player.changespeed(0,3)
                direccionbala = 4
            if event.key == pygame.K_SPACE:
                bullet = Bullet()
                bullet.rect.x = player.rect.x
                bullet.rect.y = player.rect.y
                bullet.direccion = direccionbala
                movingsprites.add(bullet)
                bullet_list.add(bullet)
                 
        # Reset speed when key goes up      
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3,0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-3,0)
            if event.key == pygame.K_UP:
                player.changespeed(0,3)
            if event.key == pygame.K_DOWN:
                player.changespeed(0,-3)
        if event.type == pygame.USEREVENT:      
            unicoenemigo.shoot(enemybullets)
            

    # This actually moves the player block based on the current speed
    player.update(walls)
    #Direccion de las balas
    for bullet in bullet_list:
        if(bullet.direccion==1):
            bullet.changespeed(-7,0)
        if(bullet.direccion==2):
            bullet.changespeed(7,0)
        if(bullet.direccion==3):
            bullet.changespeed(0,-7)
        if(bullet.direccion==4):
            bullet.changespeed(0,7)
        bullet.update()
        if(bullet.rect.x>500 or bullet.rect.x<0 or bullet.rect.y>500 or bullet.rect.y<0):
            bullet.remove

    for bullet in enemybullets:
        bullet.changespeed(7,0)
        bullet.update()
    # -- Draw everything
    # Clear screen
    screen.fill(white)
     
    # Draw sprites
    movingsprites.draw(screen)
    walls.draw(screen)
    enemigos.draw(screen)
    enemybullets.draw(screen)
    #tile_list.draw(screen)
    # Flip screen
    pygame.display.flip()
     
    # Pause
    
    clock.tick(40)
                 
pygame.quit()