# Daniela Villamar 19086
# Graficas por computadora
# Julio 2023

from structure import Renderer, color, V2
import random

width = 960
height = 540

rend = Renderer(width, height) 

def drawPoli(poligono, clr=None):
    for i in range(len(poligono)):
        rend.glLine(poligono[i],
                    poligono[ (i+1) % len(poligono)],
                    clr)


poli = [V2(165, 380), V2(185, 360), V2(180, 330), 
        V2(207, 345), V2(233, 330), V2(230, 360),
        V2(250, 380), V2(220, 385), V2(205, 410), 
        V2(193, 383)]

poli2 = [V2(321, 335), V2(288, 286), V2(339, 251), V2(374, 302)]

poli3 = [V2(377, 249), V2(411, 197), V2(436, 249)]

poli4 = [V2(413, 177), V2(448, 159), V2(502, 88),
         V2(553, 53), V2(535, 36), V2(676, 37),
         V2(660, 52), V2(750, 145), V2(761, 179),
         V2(672, 192), V2(659, 214), V2(615, 214),
         V2(632, 230), V2(580, 230), V2(597, 215),
         V2(552, 214), V2(517, 144), V2(466, 180)]

poli5 = [V2(682, 175), V2(708, 120), V2(735, 148), V2(739, 170)]

# Dibujo/estructura de polígonos
drawPoli(poli, color(1,0,0))
drawPoli(poli2, color(0,1,0))
drawPoli(poli3, color(0,0,1))
drawPoli(poli4, color(1,1,1))
drawPoli(poli5, color(1,1,1))

# Pintado de polígonos
rend.glFillPoli(poli, color(1,0,0))
rend.glFillPoli(poli2, color(0,1,0))
rend.glFillPoli(poli3, color(0,0,1))
rend.glFillPoli(poli4, color(1,1,1))
rend.glFillPoli(poli5, color(0,0,0))

rend.glFinish('output.bmp')


