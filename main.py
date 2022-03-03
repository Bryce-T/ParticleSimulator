"""
Particle Simulator game by Bryce Taylor
- Coded in 2020
- Created using Pygame API
- Inspired by popular games such as Powder Game and Powder Toy

"""

import random
import pygame as pg

WIDTH = 400
HEIGHT = 625

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Particle Simulator')

pg.font.init()

clock = pg.time.Clock()


# Text and buttons

def draw_text(string, color, center_x, center_y):
    font = pg.font.Font('freesansbold.ttf', 18)
    text = font.render(string, True, color)
    text_rect = text.get_rect()
    text_rect.center = (center_x, center_y)
    screen.blit(text, text_rect)


class Button:
    def __init__(self, x, y, width, height, color, text, text_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color

    def draw(self):
        pg.draw.rect(screen, self.color,
                     (self.x, self.y, self.width, self.height))
        draw_text(self.text, self.text_color, self.x +
                  (self.width / 2), self.y + (self.height / 2))


powder_button = Button(5, 405, 90, 30, (175, 175, 175),
                       "Powder", (150, 125, 100))
water_button = Button(5, 440, 90, 30, (175, 175, 175),
                      "Water", (0, 100, 255))
gas_button = Button(5, 475, 90, 30, (175, 175, 175), "Gas", (200, 100, 100))
fire_button = Button(5, 510, 90, 30, (175, 175, 175), "Fire", (255, 50, 0))
stone_button = Button(5, 545, 90, 30, (175, 175, 175),
                      "Stone", (80, 80, 80))
lava_button = Button(5, 580, 90, 30, (175, 175, 175), "Lava", (255, 90, 0))

cloud_button = Button(105, 405, 90, 30, (175, 175, 175),
                      "Cloud", (255, 255, 255))
ice_button = Button(105, 440, 90, 30, (175, 175, 175), "Ice", (150, 150, 180))
salt_button = Button(105, 475, 90, 30, (175, 175, 175),
                     "Salt", (240, 240, 240))
plant_button = Button(105, 510, 90, 30, (175, 175, 175),
                      "Plant", (0, 255, 75))
vine_button = Button(105, 545, 90, 30, (175, 175, 175),
                     "Vine", (0, 125, 35))
oil_button = Button(105, 580, 90, 30, (175, 175, 175),
                    "Oil", (100, 30, 50))

acid_button = Button(205, 405, 90, 30, (175, 175, 175),
                     "Acid", (200, 255, 0))
eraser_button = Button(205, 475, 90, 30, (175, 175, 175), "Eraser", BLACK)
pen_size_button = Button(205, 510, 90, 30, (175, 175, 175), "Pen Size", BLACK)
stop_button = Button(205, 545, 90, 30, (175, 175, 175), "Start/Stop", BLACK)
clear_button = Button(205, 580, 90, 30, (175, 175, 175), "Clear", BLACK)

buttons = [powder_button, water_button, stone_button, clear_button, gas_button, fire_button, acid_button, eraser_button,
           lava_button, cloud_button, stop_button, pen_size_button, ice_button, salt_button, plant_button, vine_button, oil_button]


# Classes for particles

class Particle:
    def __init__(self, type):
        self.particle_type = type
        self.color = (255, 0, 0)
        self.x_dir = (0, 0)
        self.y_dir = (0, 0)
        self.hot = False
        self.cool = False
        self.flammable = False
        self.disappearing = False
        self.rains = False
        self.acidic = False

        if self.particle_type == "Powder":
            self.color = (175, 150, 125)
            self.x_dir = (0, 0)
            self.y_dir = (1, 1)
            self.flammable = True
        elif self.particle_type == "Water":
            self.color = (0, 100, 255)
            self.x_dir = (-1, 0, 0, 1)
            self.y_dir = (1, 1)
            self.cool = True
        elif self.particle_type == "Gas":
            self.color = (200, 100, 100)
            self.x_dir = (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
            self.y_dir = (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
            self.flammable = True
        elif self.particle_type == "Stone":
            self.color = (100, 100, 100)
            self.x_dir = (0, 0)
            self.y_dir = (0, 0)
        elif self.particle_type == "Fire":
            self.color = (255, 50, 0)
            self.x_dir = (-1, 0, 1)
            self.y_dir = (-1, -1, -1, -1, -1, 0, 0, 1, 1, 1)
            self.hot = True
            self.disappearing = True
        elif self.particle_type == "Lava":
            self.color = (255, 90, 0)
            self.x_dir = (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
            self.y_dir = (1, 0, 0)
            self.hot = True
        elif self.particle_type == "Steam":
            self.color = (200, 200, 200)
            self.x_dir = (-1, 0, 0, 0, 1)
            self.y_dir = (-1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 1)
            self.disappearing = True
        elif self.particle_type == "Cloud":
            self.color = (230, 230, 230)
            self.x_dir = (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
            self.y_dir = (-1, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            self.flammable = True
            self.rains = True
        elif self.particle_type == "Ice":
            self.color = (200, 200, 255)
            self.x_dir = (0, 0)
            self.y_dir = (0, 0)
            self.cool = True
        elif self.particle_type == "Salt":
            self.color = (240, 240, 240)
            self.x_dir = (0, 0)
            self.y_dir = (1, 1)
        elif self.particle_type == "Saltwater":
            self.color = (150, 150, 255)
            self.x_dir = (-1, 0, 0, 1)
            self.y_dir = (1, 1)
            self.cool = True
        elif self.particle_type == "Plant":
            self.color = (0, 255, 75)
            self.x_dir = (0, 0)
            self.y_dir = (0, 0)
            self.flammable = True
        elif self.particle_type == "Vine":
            self.color = (0, 125, 35)
            self.x_dir = (0, 0)
            self.y_dir = (0, 0)
            self.flammable = True
        elif self.particle_type == "Oil":
            self.color = (100, 30, 50)
            self.x_dir = (-1, 0, 0, 1)
            self.y_dir = (1, 1)
            self.flammable = True
        elif self.particle_type == "Acid":
            self.color = (200, 255, 0)
            self.x_dir = (-1, 0, 0, 1)
            self.y_dir = (1, 1)
            self.acidic = True

    def calculate_movement(self):
        return random.choice(self.x_dir), random.choice(self.y_dir)


# Grid generation

grid = [[None for i in range(0, 100)] for j in range(0, 100)]

particles = 0

mouse_down = False
selected_type = "Powder"
stopped = False
pen_size = 1

while True:

    mouse_pos = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        elif event.type == pg.MOUSEBUTTONDOWN:

            mouse_down = True

            for button in buttons:
                if button.x <= mouse_pos[0] <= button.x + button.width and button.y <= mouse_pos[1] <= button.y + button.height:
                    if button.text == "Clear":
                        grid = [[None for i in range(0, 100)]
                                for j in range(0, 100)]
                        particles = 0
                    elif button.text == "Start/Stop":
                        if stopped == True:
                            stopped = False
                        else:
                            stopped = True
                    elif button.text == "Pen Size":
                        if pen_size == 3:
                            pen_size = 1
                        else:
                            pen_size += 1
                    else:
                        selected_type = button.text

        elif event.type == pg.MOUSEBUTTONUP:

            mouse_down = False

    if mouse_down and mouse_pos[1] < 400:
        if pen_size == 1:
            i, j = mouse_pos[0] // 4, mouse_pos[1] // 4

            if grid[i][j] and selected_type == "Eraser":
                grid[i][j] = None
                particles -= 1
            elif not grid[i][j] and selected_type != "Eraser":
                grid[i][j] = Particle(selected_type)
                particles += 1

        elif pen_size == 2:
            i, j = mouse_pos[0] // 4, mouse_pos[1] // 4
            squares = ((i, j + 1), (i + 1, j),
                       (i, j), (i - 1, j), (i, j - 1))
            for position in squares:
                if 0 <= position[0] <= 99 and 0 <= position[1] <= 99 and grid[position[0]][position[1]] and selected_type == "Eraser":
                    grid[position[0]][position[1]] = None
                    particles -= 1
                elif 0 <= position[0] <= 99 and 0 <= position[1] <= 99 and not grid[position[0]][position[1]] and selected_type != "Eraser":
                    grid[position[0]][position[1]] = Particle(selected_type)
                    particles += 1

        elif pen_size == 3:
            i, j = mouse_pos[0] // 4, mouse_pos[1] // 4
            squares = ((i + 1, j + 1), (i, j + 1), (i - 1, j + 1), (i + 1, j),
                       (i, j), (i - 1, j), (i + 1, j - 1), (i, j - 1), (i - 1, j - 1))
            for position in squares:
                if 0 <= position[0] <= 99 and 0 <= position[1] <= 99 and grid[position[0]][position[1]] and selected_type == "Eraser":
                    grid[position[0]][position[1]] = None
                    particles -= 1
                elif 0 <= position[0] <= 99 and 0 <= position[1] <= 99 and not grid[position[0]][position[1]] and selected_type != "Eraser":
                    grid[position[0]][position[1]] = Particle(selected_type)
                    particles += 1

    pg.draw.rect(screen, BLACK, (0, 0, 400, 400))
    pg.draw.rect(screen, WHITE, (0, 400, 400, 225))

    for i in range(0, 100):
        for j in range(0, 100):
            if grid[i][j]:
                pg.draw.rect(screen, grid[i][j].color, (i * 4, j * 4, 4, 4))

    for button in buttons:
        button.draw()

    draw_text("Selected:", BLACK, 350, 410)
    draw_text(selected_type, BLACK, 350, 430)

    draw_text("Particles:", BLACK, 350, 460)
    draw_text(str(particles), BLACK, 350, 480)

    draw_text("Pen Size:", BLACK, 350, 510)
    draw_text(str(pen_size), BLACK, 350, 530)

    pg.display.update()

    # Updates particles

    if not stopped:

        cubes = []
        for i in range(99, -1, -1):
            for j in range(99, -1, -1):
                if grid[i][j]:
                    cubes.append((i, j))

        for i, j in cubes:

            if grid[i][j].disappearing and random.randint(1, 20) == 1:
                grid[i][j] = None
                particles -= 1
                continue

            if grid[i][j].particle_type == "Plant" and random.randint(1, 200) == 1 and j > 0 and not grid[i][j - 1]:
                grid[i][j - 1] = Particle("Plant")
                particles += 1
                continue

            if grid[i][j].particle_type == "Vine" and random.randint(1, 200) == 1 and j < 99 and not grid[i][j + 1]:
                grid[i][j + 1] = Particle("Vine")
                particles += 1
                continue

            if j == 0 and grid[i][j].rains:
                grid[i][j] = Particle("Water")
                continue

            move_x, move_y = grid[i][j].calculate_movement()

            if (i == 0 and move_x < 0) or (i == 99 and move_x > 0):
                move_x = 0
            if (j == 0 and move_y < 0) or (j == 99 and move_y > 0):
                move_y = 0

            at_location = grid[i + move_x][j + move_y]

            if not at_location:
                grid[i + move_x][j + move_y] = grid[i][j]
                grid[i][j] = at_location

            elif at_location.flammable and grid[i][j].hot:
                grid[i + move_x][j + move_y] = Particle("Fire")

            elif at_location.hot and grid[i][j].flammable:
                if grid[i][j].rains:
                    grid[i][j] = Particle("Water")
                else:
                    grid[i][j] = Particle("Fire")

            elif at_location.particle_type not in ("Water", "Acid") and grid[i][j].acidic:
                grid[i + move_x][j + move_y] = grid[i][j]
                grid[i][j] = None
                particles -= 1

            elif (at_location.particle_type == "Water" and grid[i][j].acidic) or (grid[i][j].particle_type == "Water" and at_location.acidic):
                grid[i + move_x][j + move_y].disappearing = True
                grid[i][j].disappearing = True

            elif (at_location.hot and grid[i][j].cool) or (at_location.cool and grid[i][j].hot):
                grid[i][j] = None
                particles -= 1
                grid[i + move_x][j + move_y] = Particle("Steam")

            elif at_location.particle_type == "Ice" and grid[i][j].particle_type == "Water":
                grid[i][j] = Particle("Ice")

            elif (at_location.particle_type == "Water" and grid[i][j].particle_type == "Salt") or (at_location.particle_type == "Salt" and grid[i][j].particle_type == "Water"):
                grid[i][j] = Particle("Saltwater")
                grid[i + move_x][j + move_y] = Particle("Saltwater")

            elif at_location.particle_type == "Water" and grid[i][j].particle_type == "Saltwater":
                grid[i][j] = Particle("Water")
                grid[i + move_x][j + move_y] = Particle("Saltwater")

            elif at_location.particle_type == "Saltwater" and grid[i][j].particle_type == "Water":
                grid[i][j] = Particle("Saltwater")
                grid[i + move_x][j + move_y] = Particle("Water")

            elif move_y != 0:
                move_y = 0
                at_location = grid[i + move_x][j + move_y]
                if not at_location:
                    grid[i + move_x][j + move_y] = grid[i][j]
                    grid[i][j] = at_location

    clock.tick(120)
