# Daniela Villamar 19086
# Graficas por computadora
# Julio 2023

import struct
from collections import namedtuple #Utilizando la librería nametuple para facilitar la lectura del código.

from matplotlib.ft2font import GLYPH_NAMES

V2 = namedtuple('Point2', ['x', 'y'])

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b): # Creamos un color
    
    return bytes([int(b * 255),
                  int(g * 255),
                  int(r * 255)])

class Renderer(object):
    def __init__(self, w, h): 
        self.width = w
        self.height = h
        self.clearColor = color(0,0,0) # Color predeterminado
        self.currColor = color(1,1,1)

        self.glViewport(0, 0, self.width, self.height) #Viewport del tamaño de la pantalla
        self.glClear()


    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height


    def glClearColor (self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor (self, r, g, b):
        self.currColor = color(r,g,b) 

    def glClearViewport (self, clr=None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x,y,clr)

    # Array de pixeles
    def glClear(self):
        '''
            Para determinar el color del fondo hay que borrar todos los que están en la pantalla.
        '''
        # Array de pixeles
        self.pixels = [[self.clearColor for y in range(self.height)]
                        for x in range (self.width)] # Array de ancho x altura

    def glPoint (self, x, y, clr = None):
        '''
            Función para trazar un punto en la pantalla con coordenadas
        '''
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor # Falta validar que x y y no supere el tamaño para eviar inconvenientes

    def glPoint_vp(self, ndcX, ndcY, clr = None):
        '''
            Función para trazar un punto en la pantalla con coordenadas "normalizadas"
        '''
        if ndcX < -1 or ndcX > 1 or ndcY < -1 or ndcY > 1:
            return

        x = (ndcX + 1) * (self.vpWidth / 2) + self.vpX
        y = (ndcY + 1) * (self.vpHeight / 2) + self.vpY

        x = int(x)
        y = int(y)

        self.glPoint(x, y, clr)

    def glLine(self, v0, v1, clr=None):
        '''
            Bresenham line algorithm.
            Chivo: y = m * x + b
        '''
        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)

        # Si el punto 0 es igual al punto 1, solo se tiene que dibujar un punto
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0,clr)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx # Si es true es que la línea está muy inclinada. Entonces se tiene que recorrerlo de forma vertical.

        if steep:
            # Para recorrer de forma vertical
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            # Significa ue el punto inicial está del lado derecho. Dibujamos de L a R
            # Cambiamos para dibujar de R a L
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        # Para pintarlo hay que buscar el punto central de cada pixel. 
        offset = 0
        limit = 0.5 # Representa el punto central del pixel
        m = dy / dx
        y = y0

        for x in range (x0, x1 + 1):
            # Si está muy inclinado, dibujo de forma vertical
            if steep:
                # Vertical
                self.glPoint(y, x, clr)
            else:
                # Dibujado de forma horizontal.
                self.glPoint(x, y, clr)

            offset += m
            
            # Revizar si el pixel llegó a la mitad del pixel. Si no llegó pinto el de abajo.
            if offset >= limit:
                if y0 < y1:
                    # De abajo para arriba. La pendiente es positiva.
                    y += 1
                else:
                    # La pendiente es negativa. De arriba para abajo.
                    y -= 1

                limit += 1


    def glEvenOdd (self, x, y, poligono):
        '''
            Algoritmo tomado de Even-odd rule/Wikipedia
        '''
        num = len(poligono)
        pos = num - 1
        c = False
        for i in range(num):
            # Ver si el punto es una esquina?
            if (x == poligono[i][0]) and (y == poligono[i][1]):
                return True
            if ((poligono[i][1] > y) != (poligono[pos][1] > y)):
                slope = (x-poligono[i][0])*(poligono[pos][1]-poligono[i][1])-(poligono[pos][0]-poligono[i][0])*(y-poligono[i][1])
                # Ver si el punto es un borde?
                if slope == 0:
                    return True
                if (slope < 0) != (poligono[pos][1] < poligono[i][1]):
                    c = not c
            pos = i
        return c

    def glFillPoli (self, poligono, clr=None):
        '''
            Utilizando el algoritmo de Even-odd pintar el polígono
        '''
        for y in range(self.height):
            for x in range(self.width):
                if self.glEvenOdd(x, y, poligono):
                    self.glPoint(x, y, clr)
            

    # Función para crear el bitmap/frame buffer y ver resultado final
    def glFinish (self, filename):
       
        with open(filename, "wb") as file:

            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
        
            file.write(dword( 14 + 40 + (self.width * self.height * 3))) 
            file.write(dword(0))
            file.write(dword(14 + 40))

            file.write(dword(40))
            file.write(dword(self.width)) 
            file.write(dword(self.height))
            file.write(word(1)) 
            file.write(word(24)) 
            file.write(dword(0)) 
            file.write(dword(self.width * self.height * 3)) # Image size

            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
