import numpy as np
import random
import math

def vertexShader(vertex, normal, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"] 
    projectionMatrix = kwargs["projectionMatrix"] 
    viewportMatrix = kwargs["viewportMatrix"]

    normal = kwargs.get("normal", [0, 0, 1])  

    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]
    
    nt = [normal[0],
          normal[1],
          normal[2],
          0]

    vt = (viewportMatrix * projectionMatrix * viewMatrix * modelMatrix) @ vt
    vt = vt.tolist()[0]

    nt = modelMatrix @ nt
    nt = nt.tolist()[0]

    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3]]
    
    nt = [nt[0],
          nt[1],
          nt[2]]

    nt = nt / np.linalg.norm(nt)

    return vt, nt

def fragmentShader(**kwargs):
    r, g , b = kwargs["pixelColor"]
    return [r, g, b]

def flatShader(**kwargs):
    A, B, C = kwargs["verts"]
    r, g , b = kwargs["pixelColor"]
    dirLight = kwargs["dirLight"]
    

    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]

    normal = [(nA[0]+nB[0]+nC[0])/3,
              (nA[1]+nB[1]+nC[1])/3,
              (nA[2]+nB[2]+nC[2])/3]
    
    #intensity = normal DOT -dirLight
    intensity = np.dot(normal, -np.array(dirLight))
    intensity = max(0, intensity)

    r *= intensity
    g *= intensity
    b *= intensity

    return [r, g, b]

def gouradShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    r, g , b = kwargs["pixelColor"]
    dirLight = kwargs["dirLight"]
    textureList = kwargs.get("textureList")

    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]

    tA = [A[6], A[7]]
    tB = [B[6], B[7]]
    tC = [C[6], C[7]]

    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
    
    UVs = [u*tA[0] + v*tB[0] + w*tC[0],
           u*tA[1] + v*tB[1] + w*tC[1]]
    
    if textureList is not None:
        if len(textureList) > 0:
            texColor = textureList[0].getColor(UVs[0], UVs[1])

            r *= texColor[0]
            g *= texColor[1]
            b *= texColor[2]

    
    #intensity = normal DOT -dirLight
    intensity = np.dot(normal, -np.array(dirLight))
    intensity = max(0, intensity)

    r *= intensity
    g *= intensity
    b *= intensity

    return [r, g, b]


def RainbowShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    pos = (u * 0.3 + v * 0.6 + w * 0.1)
    
    if pos < 0.166:
        r, g, b = 1.0, 0.0, 0.0    # Rojo
    elif pos < 0.333:
        r, g, b = 1.0, 0.5, 0.0    # Naranja
    elif pos < 0.5:
        r, g, b = 1.0, 1.0, 0.0    # Amarillo
    elif pos < 0.666:
        r, g, b = 0.0, 1.0, 0.0    # Verde
    elif pos < 0.833:
        r, g, b = 0.0, 0.0, 1.0    # Azul
    else:
        r, g, b = 0.5, 0.0, 0.5    # Violeta
    
    return [r, g, b]

def oceanShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    # Coordenadas de textura simuladas
    tx = u * 10
    ty = v * 10
    
    # Patrón de onda
    wave1 = math.sin(tx * 2 + ty) * 0.5
    wave2 = math.sin(tx * 1.5 - ty * 2) * 0.3
    wave = wave1 + wave2
    
    # Color base azul con variación
    base_blue = 0.6 + wave * 0.2
    r = 0.1
    g = 0.3 + wave * 0.1
    b = min(1.0, base_blue)
    
    # Highlight basado en normales
    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
    highlight = max(0, np.dot(normal, [0, 1, 0])) ** 2
    r += highlight * 0.5
    g += highlight * 0.3
    b += highlight * 0.1
    
    return [r, g, b]

def discoShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    center_u = 1/3
    center_v = 1/3
    center_w = 1/3
    
    dist = math.sqrt((u-center_u)**2 + (v-center_v)**2 + (w-center_w)**2)
    
    rings = math.sin(dist * 50)  
    
    r = abs(math.sin(dist * 20))  #
    g = (rings + 1) / 2          
    b = 1 - dist                 
    
    return [r, g, b]

def fireShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    # Base de las llamas (zona más caliente)
    flame_base = 1.0 - v  # Más intenso en la parte inferior
    
    # Patrón de llamas con ruido fractal
    noise1 = math.sin(u * 10.0 + v * 20.0) * 0.5
    noise2 = math.sin(u * 7.0 - v * 15.0) * 0.3
    noise3 = math.sin(u * 15.0 + v * 25.0) * 0.2
    combined_noise = (noise1 + noise2 + noise3) * v
    
    # Forma de las llamas
    flame_shape = flame_base * (1.0 + combined_noise)
    
    # Gradiente de color (de amarillo a rojo)
    r = min(1.0, flame_shape * 1.2)  # Componente roja
    g = flame_shape * 0.6             # Componente verde
    b = flame_shape * 0.1             # Componente azul
    
    # Zona más caliente (núcleo de la llama)
    hot_core = max(0.0, flame_shape - 0.7) * 2.0
    r += hot_core * 0.5
    g += hot_core * 0.3
    
    # Efecto de chispas aleatorias
    if random.random() > 0.98:
        r, g, b = 1.0, 1.0, 0.8  # Destellos blancos
    
    return [r, g, b]

def neonShader(**kwargs):
    """Shader de neón con bordes brillantes y colores vibrantes"""
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    # Calcular normal interpolada
    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
    # Fresnel effect (bordes más brillantes)
    view_dir = [0, 0, 1]  # Vista hacia adelante
    fresnel = 1.0 - abs(np.dot(normal, view_dir))
    fresnel = fresnel ** 2
    
    # Colores neón cíclicos
    time_sim = (u + v + w) * 5
    r = (math.sin(time_sim) + 1) * 0.5
    g = (math.sin(time_sim + 2.094) + 1) * 0.5  # 120° desfasado
    b = (math.sin(time_sim + 4.188) + 1) * 0.5  # 240° desfasado
    
    # Intensificar con efecto fresnel
    intensity = 0.3 + fresnel * 0.7
    r *= intensity
    g *= intensity
    b *= intensity
    
    return [min(1.0, r), min(1.0, g), min(1.0, b)]

def crystalShader(**kwargs):
    """Shader de cristal con reflejos y transparencia simulada"""
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    # Calcular normal
    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
    # Facetas del cristal
    facet_u = math.floor(u * 8) / 8.0
    facet_v = math.floor(v * 8) / 8.0
    facet_pattern = (facet_u + facet_v) * 2.0
    
    # Color base azul cristalino
    base_r = 0.7 + math.sin(facet_pattern) * 0.2
    base_g = 0.8 + math.cos(facet_pattern * 1.3) * 0.1
    base_b = 0.9 + math.sin(facet_pattern * 0.7) * 0.1
    
    # Reflejos especulares
    light_dir = [0.5, 0.7, 1.0]  # Dirección de luz
    reflection = max(0, np.dot(normal, light_dir)) ** 3
    
    # Añadir brillo especular
    r = base_r + reflection * 0.5
    g = base_g + reflection * 0.4
    b = base_b + reflection * 0.3
    
    return [min(1.0, r), min(1.0, g), min(1.0, b)]

def woodShader(**kwargs):
    """Shader de madera con vetas y anillos"""
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    # Coordenadas para crear anillos de madera
    center_x = 0.5
    center_y = 0.5
    
    # Distancia desde el centro (para anillos)
    dist = math.sqrt((u - center_x)**2 + (v - center_y)**2)
    
    # Anillos de crecimiento
    rings = math.sin(dist * 30) * 0.5 + 0.5
    
    # Vetas de madera
    grain = math.sin(u * 40 + v * 10) * 0.3 + 0.7
    
    # Nudos ocasionales
    knot_dist = math.sqrt((u - 0.3)**2 + (v - 0.7)**2)
    knot = 1.0 - max(0, min(1, (0.1 - knot_dist) * 10))
    
    # Color base de madera
    wood_base = rings * grain * knot
    r = wood_base * 0.6 + 0.3    # Tono marrón
    g = wood_base * 0.4 + 0.2    # Menos verde
    b = wood_base * 0.2 + 0.1    # Menos azul
    
    return [min(1.0, r), min(1.0, g), min(1.0, b)]

def galaxyShader(**kwargs):
    """Shader de galaxia con estrellas y nebulosas"""
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    
    # Base oscura del espacio
    space_base = 0.1
    
    # Nebulosa con múltiples capas
    nebula1 = (math.sin(u * 5) + 1) * 0.5
    nebula2 = (math.sin(v * 3 + u * 2) + 1) * 0.5
    nebula3 = (math.sin(w * 4 - u * 1.5) + 1) * 0.5
    
    nebula_intensity = (nebula1 + nebula2 + nebula3) / 3.0
    
    # Colores de nebulosa
    r = space_base + nebula_intensity * 0.6  # Rosa/rojo
    g = space_base + nebula_intensity * 0.3  # Menos verde
    b = space_base + nebula_intensity * 0.8  # Azul/violeta
    
    # Estrellas aleatorias (puntos brillantes)
    star_chance = random.random()
    if star_chance > 0.97:  # 3% de probabilidad
        brightness = random.random()
        r += brightness * 0.5
        g += brightness * 0.5
        b += brightness * 0.5
    
    # Espiral galáctica
    angle = math.atan2(v - 0.5, u - 0.5)
    spiral_dist = math.sqrt((u - 0.5)**2 + (v - 0.5)**2)
    spiral = math.sin(angle * 3 - spiral_dist * 10) * 0.3 + 0.7
    
    r *= spiral
    g *= spiral
    b *= spiral
    
    return [max(0, min(1.0, r)), max(0, min(1.0, g)), max(0, min(1.0, b))]