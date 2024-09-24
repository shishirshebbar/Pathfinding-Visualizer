import pygame
import sys
from tkinter import messagebox,Tk

window_width = 500
window_height = 500

window = pygame.display.set_mode((window_width,window_height))

columns_no  = 25
rows_no = 25

box_width  = window_width//columns_no
box_height = window_height//rows_no
grid=[]

class Box:
    def __init__(self,x,y):
        self.x=  x
        self.y = y
    def draw(self,window,color):
        pygame.draw.rect(window,color,(self.x*box_width,self.y*box_height,box_width-2,box_height-2))
for x in range(columns_no):
    arr = []
    for y in range(rows_no):
        arr.append(Box(x,y))
    grid.append(arr)

def main():
    while True:
        for event in pygame.event.get():
            #closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill((128,128,128))
        for x in range(columns_no):
            for y in range(rows_no):
                box= grid[x][y]
                box.draw(window,(20,20,20))
        pygame.display.flip()

main()