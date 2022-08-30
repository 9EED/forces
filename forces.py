from math import *
from random import *
from pyray import *
import numpy as np


width = 800
height = 600
cameraX = 0
cameraY = 0
cameraZ = 1
scroll = 0.1
playing = True
walls = True
wallsX = 2000
wallsY = 2000
cellSize = 5

def circle( x, y, r, color):
    draw_circle( int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), r*cameraZ+1, color)
def circle_line( x, y, r, color):
    draw_circle_lines( int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), r*cameraZ+1, color)
def line( x1, y1, x2, y2, color):
    draw_line( int((x1+cameraX)*cameraZ + width/2), int((y1+cameraY)*cameraZ + height/2), int(( x2+cameraX)*cameraZ + width/2), int((y2+cameraY)*cameraZ + height/2), color)
def text( text, x, y, size, color):
    draw_text( text, int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), int(size*cameraZ+1), color)
def rectangle_lines( x, y, w, h, color):
    draw_rectangle_lines( int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), int(w*cameraZ), int(h*cameraZ), color)
types = {
    "red": {
        "relations": {
            "red": random()*0.04-0.02,
            "green": random()*0.04-0.02,
            "blue": random()*0.04-0.02,
            "white": random()*0.04-0.02,
        },
        "color": Color( 200, 30, 30, 255)
    },
    "green": {
        "relations": {
            "red": random()*0.04-0.02,
            "green": random()*0.04-0.02,
            "blue": random()*0.04-0.02,
            "white": random()*0.04-0.02,
        },
        "color": Color( 50, 200, 50, 255)
    },
    "blue": {
        "relations": {
            "red": random()*0.04-0.02,
            "green": random()*0.04-0.02,
            "blue": random()*0.04-0.02,
            "white": random()*0.04-0.02,
        },
        "color": Color( 50, 50, 200, 255)
    },
    "white": {
        "relations": {
            "red": random()*0.04-0.02,
            "green": random()*0.04-0.02,
            "blue": random()*0.04-0.02,
            "white": random()*0.04-0.02,
        },
        "color": Color( 200, 200, 200, 255)
    },
}

class Dot():
    def __init__(self, pos, type):
        self.pos = pos
        self.vel = np.array([0, 0])
        self.type = type
    def update(self, walls, wallsX, wallsY):
        if walls:
            if self.pos[0] > wallsX or self.pos[0] < -wallsX :
                self.pos -= 20 * (self.pos[0]-wallsX) / abs(self.pos[0]-wallsX)
                self.vel[0] *= -1
            if self.pos[1] > wallsY or self.pos[1] < -wallsY :
                self.pos -= 20 * (self.pos[1]-wallsY) / abs(self.pos[1]-wallsY)
                self.vel[1] *= -1
        self.pos += self.vel
    def render(self):
        circle(self.pos[0], self.pos[1], cellSize, types[self.type]["color"])

dots = []
for i in range(60):
    dots.append(Dot(
        np.array([
            random()*wallsX*2-wallsX,
            random()*wallsY*2-wallsY
        ]),
        choice(list(types.keys()))
    ))


init_window( width, height, "forces")
set_target_fps(60)
while not window_should_close():

    #pausing
    if is_key_pressed(KEY_SPACE):
        playing = not playing
    #camera controls
    if is_mouse_button_pressed(MOUSE_BUTTON_LEFT): #starting pos to calculate mouses veleocity
        mouse_start_x = get_mouse_x()
        mouse_start_y = get_mouse_y()
    if is_mouse_button_down(MOUSE_BUTTON_LEFT): 
        mouse_velocity_x = get_mouse_x() - mouse_start_x
        mouse_velocity_y = get_mouse_y() - mouse_start_y
        mouse_start_x = get_mouse_x()
        mouse_start_y = get_mouse_y()
        cameraX += mouse_velocity_x * 0.8 / cameraZ
        cameraY += mouse_velocity_y * 0.8 / cameraZ
    if get_mouse_wheel_move() > 0: # zoom in
        if cameraZ < 10000:
            cameraZ *= 1 + scroll
    if get_mouse_wheel_move() < 0: # zoom out
        if cameraZ > 0.0001:
            cameraZ *= 1 - scroll
    
    #simulation
    if playing:
        for dot in dots:
            dot.update( walls, wallsX, wallsY)
            for dot2 in dots:
                d = sqrt( (dot.pos[0]-dot2.pos[0])**2 + (dot.pos[1]-dot2.pos[1])**2 )
                if d > cellSize:
                    G = types[dot.type]["relations"][dot2.type]
                    force = G / (d**2)
                    vector = dot.pos - dot2.pos
                    vector = vector / np.linalg.norm(vector)
                    vector = vector * G
                    dot.vel = dot.vel + vector

    #rendering
    begin_drawing()
    clear_background(Color( 20, 20, 27, 255))

    for dot in dots:
        dot.render()

    if walls:
        rectangle_lines( -wallsX, -wallsY, wallsX*2, wallsY*2, WHITE)
    if not playing:
        draw_rectangle( width-20, 20, 5, 20, WHITE)
        draw_rectangle( width-31, 20, 5, 20, WHITE)
    draw_fps( 10, 10)
    end_drawing()

close_window()