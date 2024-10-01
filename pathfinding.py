from tkinter import messagebox, Tk
import pygame
import sys

width = 500
height = 500

window = pygame.display.set_mode((width, height))

columns = 25
rows = 25

box_w = width // columns
box_h = height // rows

grid = []
queue = []
path = []


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_w,self.y * box_h, box_w-2, box_h-2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


pygame.font.init()
font = pygame.font.SysFont("Calibri", 20)



for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)


for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()




def main():
    begin_search = False
    set_target_box = False
    searching = True
    target_box = None
    set_start_box = False

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left mouse button click
                if event.button == 1: 
                    x, y = pygame.mouse.get_pos()
                    i = x // box_w
                    j = y // box_h
                    if not set_start_box and not grid[i][j].wall:
                        start_box = grid[i][j]
                        start_box.start = True
                        start_box.visited = True
                        queue.append(start_box)
                        set_start_box = True

            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw the Wall
                if event.buttons[0]:
                    i = x // box_w
                    j = y // box_h
                    grid[i][j].wall = True
                # Set the Target
                if event.buttons[2] and not set_target_box:
                    i = x // box_w
                    j = y // box_h
                    target_box = grid[i][j]
                    target_box.target = True
                    set_target_box = True
            # Start the Algorithm
            if event.type == pygame.KEYDOWN and set_target_box:
                begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution found", "There is no solution present")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))

                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))

                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (10, 10, 10))
                if box.target:
                    box.draw(window, (200, 200, 0))

                
            instructions = [
                "Instructions:",
                "1. Left click to start",
                "2. Left click and hold to draw walls",
                "3. Right click to set target",
                "4. Press SPACE to start"
            ]
            for i, instruction in enumerate(instructions):
                text_surface = font.render(instruction, True, (200, 200, 200))
                window.blit(text_surface, (0, height - (len(instructions) - i) * 20 - 10))

        pygame.display.flip()


main()