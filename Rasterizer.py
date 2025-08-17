import pygame
import random
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from shaders import *
from OBJLoader import OBJ

width = 880
height = 800

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.glLoadBackground("ventana.bmp")

model = Model("butterfly.obj")
model.LoadTexture("butterfly.bmp")
model.vertexShader = vertexShader
model.fragmentShader = flatShader
model.translation[0] = -10
model.translation[1] = 3
model.translation[2] = -30
model.scale = [(i*0.05) for i in model.scale]

#model = Model("rose.obj")
#model.LoadTexture("rose.bmp")
#model.vertexShader = vertexShader
#model.fragmentShader = flatShader
#model.translation[0] = -10
#model.translation[1] = 3
#model.translation[2] = -20
#model.scale = [(i*0.5) for i in model.scale]

#model = Model("butterfly.obj")
#model.LoadTexture("butterfly.bmp")
#model.vertexShader = vertexShader
#model.fragmentShader = flatShader
#model.translation[2] = -5
#model.scale = [(i*2) for i in model.scale]

rend.models.append(model)

rend.dirLight = [0, 0, -1]
rend.primitiveType = TRIANGLES



# Configurar transformación y shaders
#model.translation[0] = width / 2
#model.translation[1] = height / 3

#model.rotation[1] = 180

#rend.glColor(0,0,1)

#rend.glRender()

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                rend.camera.translation[0] += 0.1
            elif event.key == pygame.K_LEFT:
                rend.camera.translation[0] -= 0.1

            elif event.key == pygame.K_UP:
                rend.camera.translation[1] += 0.1
            elif event.key == pygame.K_DOWN:
                rend.camera.translation[1] -= 0.1


            elif event.key == pygame.K_q:
                rend.camera.translation[2] += 2 * deltaTime  
            elif event.key == pygame.K_e:
                rend.camera.translation[2] -= 2 * deltaTime


            elif event.key == pygame.K_a:
                rend.camera.rotation[1] -= 45 * deltaTime
            elif event.key == pygame.K_d:
                rend.camera.rotation[1] += 45 * deltaTime
            elif event.key == pygame.K_w:
                rend.camera.rotation[0] -= 45 * deltaTime
            elif event.key == pygame.K_s:
                rend.camera.rotation[0] += 45 * deltaTime
        

    

    rend.glClearBackground()
    rend.glRender()
    pygame.display.flip()


GenerateBMP("output.bmp", width, height, 3, rend.frameBuffer)
pygame.quit()