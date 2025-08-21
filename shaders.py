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
    #intensity = np.dot(normal, -np.array(dirLight))
    #intensity = max(0, intensity)

    #r *= intensity
    #g *= intensity
    #b *= intensity

    return [r, g, b]

def gouradShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    r, g, b = kwargs["pixelColor"]
    dirLight = kwargs["dirLight"]
    textureList = kwargs.get("textureList")

    # Verificar que tenemos suficiente información en los vértices
    if len(A) < 8 or len(B) < 8 or len(C) < 8:
        print("Warning: Vértices sin suficiente información")
        return [r, g, b]

    nA = [A[3], A[4], A[5]]
    nB = [B[3], B[4], B[5]]
    nC = [C[3], C[4], C[5]]

    tA = [A[6], A[7]]
    tB = [B[6], B[7]]
    tC = [C[6], C[7]]

    # Interpolación de normales
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
    # Normalizar la normal
    normal_length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
    if normal_length > 0:
        normal = [n/normal_length for n in normal]
    
    # Interpolación de UVs
    UVs = [u*tA[0] + v*tB[0] + w*tC[0],
           u*tA[1] + v*tB[1] + w*tC[1]]
    
    # Aplicar textura
    if textureList and len(textureList) > 0:
        try:
            # Asegurar que UVs están en rango válido
            u_clamped = max(0.0, min(0.999, UVs[0]))
            v_clamped = max(0.0, min(0.999, UVs[1]))
            
            texColor = textureList[0].getColor(u_clamped, v_clamped)
            if texColor and len(texColor) >= 3:
                r = texColor[0]
                g = texColor[1] 
                b = texColor[2]
        except Exception as e:
            print(f"Error accessing texture: {e}")

    return [max(0, min(1, r)), max(0, min(1, g)), max(0, min(1, b))]



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
    
    flame_base = 1.0 - v  
    
    noise1 = math.sin(u * 10.0 + v * 20.0) * 0.5
    noise2 = math.sin(u * 7.0 - v * 15.0) * 0.3
    noise3 = math.sin(u * 15.0 + v * 25.0) * 0.2
    combined_noise = (noise1 + noise2 + noise3) * v
    
    flame_shape = flame_base * (1.0 + combined_noise)
    
    r = min(1.0, flame_shape * 1.2)  
    g = flame_shape * 0.6             
    b = flame_shape * 0.1             
    
    hot_core = max(0.0, flame_shape - 0.7) * 2.0
    r += hot_core * 0.5
    g += hot_core * 0.3
    
    if random.random() > 0.98:
        r, g, b = 1.0, 1.0, 0.8  
    
    return [r, g, b]


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

    """Rosa con aspecto cristalino y reflejos"""
    import math
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs.get("textureList")
    dirLight = kwargs["dirLight"]
    
    # Color base cristalino
    r, g, b = 0.9, 0.95, 1.0
    
    # Aplicar textura con efecto cristal
    if textureList and len(textureList) > 0 and len(A) >= 8:
        tA = [A[6], A[7]]
        tB = [B[6], B[7]]
        tC = [C[6], C[7]]
        
        u_tex = u*tA[0] + v*tB[0] + w*tC[0]
        v_tex = u*tA[1] + v*tB[1] + w*tC[1]
        
        u_tex = max(0.0, min(0.999, u_tex))
        v_tex = max(0.0, min(0.999, v_tex))
        
        try:
            texColor = textureList[0].getColor(u_tex, v_tex)
            if texColor:
                # Mezclar con tinte azul cristalino
                r = texColor[0] * 0.8 + 0.2
                g = texColor[1] * 0.9 + 0.1  
                b = texColor[2] * 1.2
        except:
            pass
    
    # Efectos de cristal - facetas
    facet_u = math.floor(u_tex * 12) / 12.0
    facet_v = math.floor(v_tex * 12) / 12.0
    facet_pattern = math.sin(facet_u * 20) * math.cos(facet_v * 20)
    
    # Añadir reflexiones especulares intensas
    if len(A) >= 6:
        nA = [A[3], A[4], A[5]]
        nB = [B[3], B[4], B[5]]
        nC = [C[3], C[4], C[5]]
        
        normal = [u*nA[0] + v*nB[0] + w*nC[0],
                  u*nA[1] + v*nB[1] + w*nC[1],
                  u*nA[2] + v*nB[2] + w*nC[2]]
        
        length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
        if length > 0:
            normal = [n/length for n in normal]
        
        # Reflexión especular muy intensa
        reflection = max(0, sum(n * l for n, l in zip(normal, dirLight))) ** 8
        
        r += reflection * 0.5 + facet_pattern * 0.2
        g += reflection * 0.4 + facet_pattern * 0.2
        b += reflection * 0.3 + facet_pattern * 0.3
    
    return [min(1.0, r), min(1.0, g), min(1.0, b)]

def romanticShader(**kwargs):
    import math
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    textureList = kwargs.get("textureList")
    
    r, g, b = 1.0, 1.0, 1.0
    
    if textureList and len(textureList) > 0 and len(A) >= 8:
        tA = [A[6], A[7]]
        tB = [B[6], B[7]]
        tC = [C[6], C[7]]
        
        u_tex = u*tA[0] + v*tB[0] + w*tC[0]
        v_tex = u*tA[1] + v*tB[1] + w*tC[1]
        
        u_tex = max(0.0, min(0.999, u_tex))
        v_tex = max(0.0, min(0.999, v_tex))
        
        try:
            texColor = textureList[0].getColor(u_tex, v_tex)
            if texColor:
                r, g, b = texColor[0], texColor[1], texColor[2]
        except:
            pass
    
    effect = math.sin(u_tex * 10) * math.cos(v_tex * 8) * 0.3
    
    r += effect * 0.3  
    g += effect * 0.1  
    b += effect * 0.5  
    
    brillo = max(0, 1.0 - (u + v + w - 0.33) * 3) * 0.4
    r += brillo
    g += brillo * 0.7
    b += brillo
    
    return [min(1.0, r), min(1.0, g), min(1.0, b)]