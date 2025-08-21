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
model.fragmentShader = RainbowShader  
model.translation[0] = -10
model.translation[1] = 3
model.translation[2] = -40
model.rotation[1] = 0
model.rotation[0] = 90
model.rotation[2] = 0
model.scale = [(i*0.05) for i in model.scale]
rend.models.append(model)

model2 = Model("rose.obj")
model2.LoadTexture("rose.bmp")
model2.vertexShader = vertexShader
model2.fragmentShader = romanticShader
model2.translation[0] = -10
model2.translation[1] = -15
model2.translation[2] = -30
model2.rotation[1] = 100
model2.rotation[0] = -90
model2.rotation[2] = -80
model2.scale = [0.2, 0.2, 0.2]
rend.models.append(model2)

model4 = Model("Penguin.obj")
model4.LoadTexture("Penguin.bmp")
model4.vertexShader = vertexShader
model4.fragmentShader = oceanShader
model4.translation[1] = -2
model4.translation[2] = -10
model4.scale = [(i*2) for i in model4.scale]
rend.models.append(model4)

model3 = Model("bird.obj")
model3.LoadTexture("bird.bmp")
model3.vertexShader = vertexShader
model3.fragmentShader = fireShader
model3.translation[0] = 10
model3.translation[1] = -8
model3.translation[2] = -30
model3.rotation[1] = 0
model3.rotation[0] = -90
model3.rotation[2] = 0
model3.scale = [(i*0.5) for i in model3.scale]
rend.models.append(model3)

#model4 = Model("wheel.obj")
#model4.LoadTexture("wheel.bmp")
#model4.vertexShader = vertexShader
#model4.fragmentShader = gouradShader
#model4.translation[0] = 0
#model4.translation[1] = 0
#model4.translation[2] = 0
#model4.rotation[1] = 0
#model4.rotation[0] = 0
#model4.rotation[2] = 0
#model4.scale = [(i*1) for i in model4.scale]
#rend.models.append(model4)









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