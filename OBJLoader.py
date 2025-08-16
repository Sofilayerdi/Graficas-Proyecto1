import numpy as np

class OBJ:
    def __init__(self, filename):
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []  
        self.load(filename)
        
    def load(self, filename):
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex = list(map(float, line.strip().split()[1:4]))
                    self.vertices.append(vertex)
                elif line.startswith('vn '):
                    normal = list(map(float, line.strip().split()[1:4]))
                    self.normals.append(normal)
                elif line.startswith('vt '):
                    vts = list(map(float, line.strip().split()[1:3]))
                    self.texcoords.append(vts)
                elif line.startswith('f '):
                    face_vertices = line.strip().split()[1:]
                    if len(face_vertices) == 3:
                        face = []
                        for v in face_vertices:
                            parts = v.split('/')
                            vertex_index = int(parts[0]) if parts[0] else 1
                            texcoord_index = int(parts[1]) if len(parts) > 1 and parts[1] else 1
                            normal_index = int(parts[2]) if len(parts) > 2 and parts[2] else 1
                            face.append((vertex_index, texcoord_index, normal_index))
                        self.faces.append(face)
                    elif len(face_vertices) > 3:
                        # Triangulación para polígonos
                        for i in range(1, len(face_vertices)-1):
                            face = []
                            for j in [0, i, i+1]:
                                parts = face_vertices[j].split('/')
                                vertex_index = int(parts[0]) if parts[0] else 1
                                texcoord_index = int(parts[1]) if len(parts) > 1 and parts[1] else 1
                                normal_index = int(parts[2]) if len(parts) > 2 and parts[2] else 1
                                face.append((vertex_index, texcoord_index, normal_index))
                            self.faces.append(face)