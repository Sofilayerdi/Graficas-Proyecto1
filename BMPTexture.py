import struct

class BMPTexture(object):
    def __init__(self, filename):
        with open(filename, "rb") as image:
            image.seek(10)
            data_offset = struct.unpack('<I', image.read(4))[0]

            image.seek(18)
            self.width = struct.unpack('<I', image.read(4))[0]
            self.height = struct.unpack('<I', image.read(4))[0]

            image.seek(data_offset)
            self.pixels = []

            # Calcular padding
            bytes_per_row = ((self.width * 3 + 3) // 4) * 4
            padding = bytes_per_row - (self.width * 3)

            for y in range(self.height):
                pixelRow = []
                for x in range(self.width):
                    b = struct.unpack('B', image.read(1))[0] / 255.0
                    g = struct.unpack('B', image.read(1))[0] / 255.0
                    r = struct.unpack('B', image.read(1))[0] / 255.0
                    pixelRow.append([r, g, b])
                
                if padding > 0:
                    image.read(padding)
                    
                self.pixels.append(pixelRow)
            
            self.pixels.reverse()

    def getColor(self, u, v):
        u = max(0.0, min(0.999, u))
        v = max(0.0, min(0.999, v))
        
        x_exact = u * (self.width - 1)
        y_exact = v * (self.height - 1)
        
        x0 = int(x_exact)
        y0 = int(y_exact)
        x1 = min(x0 + 1, self.width - 1)
        y1 = min(y0 + 1, self.height - 1)
        
        fx = x_exact - x0
        fy = y_exact - y0
        
        c00 = self.pixels[y0][x0]  # Top-left
        c10 = self.pixels[y0][x1]  # Top-right
        c01 = self.pixels[y1][x0]  # Bottom-left
        c11 = self.pixels[y1][x1]  # Bottom-right
        
        # Interpolación bilinear
        # Primero interpolar horizontalmente
        c0 = [c00[i] * (1 - fx) + c10[i] * fx for i in range(3)]
        c1 = [c01[i] * (1 - fx) + c11[i] * fx for i in range(3)]
        
        # Luego interpolar verticalmente
        final_color = [c0[i] * (1 - fy) + c1[i] * fy for i in range(3)]
        
        return final_color