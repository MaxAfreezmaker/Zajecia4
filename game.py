# To create & start using python venv:
#       python -m venv venv
#       source venv/bin/activate
from tkinter import filedialog

# Intall specific modules with pip:
# f.e.:   pip install pygame

# Requirements
# 1. Make simulation real time
# 2. Add pause / resume logic
# 3. Add save / load logic

# High-level logic
# 1. Create and init the simulation grid (Connect with tick)
# 2. Start the simulation with a tick interval of <n> seconds
# 3. At each tick:
#   3.1. Update the grid - loop over each element of the board
#   3.2. Render new generation

# General approach
# 1. Plan & write down the general workflow
#  1.1. Define Input&Output 
#  1.2. Consider adding validation
# 2. Separate the main algorithms / actors in the code. Try to abstract as much common code as possible
# 3. Define communication between the objects
# 4. List the patterns you could apply
# 5. Build PoCs (Proof of concepts). Try to separate implementation of specific steps. Prepare smaller modules
#    and combine them into a complete application
# 6. Refine if needed

# Deadline - 15th of December 2023
# Mail with: 
# 1. short screen recording demonstrating the new features
# 2. Linked code
# 3. Short description of the changes. Which design patterns you used and how you applied them. 

import pygame
import numpy as np
import pickle
from datetime import datetime
from tkinter import Tk, filedialog
# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1620, 780
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
# Button dimensions
button_width, button_height = 200, 50
button_x, button_y = (width - button_width) // 2, height - button_height - 10

button_width_pause, button_height_pause = 200, 50
button_x_pause, button_y_pause = (width - button_width_pause) // 2, height - button_height_pause - 10

button_width_save, button_height_save = 200, 50
button_x_save, button_y_save = (width - button_width_save // 2, height - button_height_save - 10)

button_width_load, button_height_load = 200, 50
button_x_load, button_y_load = (width - button_width_load // 2, height - button_height_load - 10)

button_spacing = 10

# Calculate buttons
total_button_width = button_width + button_width_pause + button_width_save + button_width_load + 2 * button_spacing

# Calculate the stating position
start_x = (width - total_button_width) // 2

# Setting position for all buttons
button_x = start_x
button_x_pause = button_x + button_width + button_spacing
button_x_save = button_x_pause + button_width_pause + button_spacing
button_x_load = button_x_save + button_width_save + button_spacing
# Pause maker
pause = False

# Save file
def save_game_state():
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f'saved_game_state_{current_datetime}.pickle'
    with open(file_path, 'wb') as file:
        pickle.dump(game_state, file)

# Load File
def load_game_state():
    file_path = filedialog.askopenfilename(defaultextension=".pickle", filetypes=[("Pickle files", "*.pickle")])
    if file_path:
        global game_state
        with open(file_path, 'rb') as file:
            game_state = pickle.load(file)

# Button settings
def draw_button():
    pygame.draw.rect(screen, green, (button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Next Generation", True, black)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

def draw_button_pause():
    pygame.draw.rect(screen, red, (button_x_pause, button_y_pause, button_width_pause, button_height_pause))
    font = pygame.font.Font(None, 36)
    if pause:
        text = font.render("Resume", True, black)
        text_rect = text.get_rect(
            center=(button_x_pause + button_width_pause // 2, button_y_pause + button_height_pause // 2))
        screen.blit(text, text_rect)
    else:
        text = font.render("Pause", True, black)
        text_rect = text.get_rect(
            center=(button_x_pause + button_width_pause // 2, button_y_pause + button_height_pause // 2))
        screen.blit(text, text_rect)

def draw_button_save():
    pygame.draw.rect(screen, blue, (button_x_save, button_y_save, button_width_save, button_height_save))
    font = pygame.font.Font(None, 36)
    text = font.render("Save", True, black)
    text_rect = text.get_rect(center=(button_x_save + button_width_save // 2, button_y_save + button_height_save // 2))
    screen.blit(text, text_rect)
def draw_button_load():
    pygame.draw.rect(screen, blue, (button_x_load, button_y_load, button_width_load, button_height_load))
    font = pygame.font.Font(None, 36)
    text = font.render("Load", True, black)
    text_rect = text.get_rect(center=(button_x_load + button_width_load // 2, button_y_load + button_height_load // 2))
    screen.blit(text, text_rect)

def draw_grid():
    for y in range(0, height, cell_height):
        for x in range(0, width, cell_width):
            cell = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, gray, cell, 1)

def next_generation():
    global game_state
    new_state = np.copy(game_state)

    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = game_state[(x - 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y + 1) % n_cells_y]

            if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1

    game_state = new_state

def draw_cells():
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            if game_state[x, y] == 1:
                pygame.draw.rect(screen, black, cell)

# Clock initiate
clock = pygame.time.Clock()
generation_interval = 1000
last_generation_time = pygame.time.get_ticks()

# Update Timer
GENERATION_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(GENERATION_EVENT, generation_interval)

# App Run
running = True
while running:
    screen.fill(white)
    draw_grid()
    draw_cells()
    draw_button()
    draw_button_pause()
    draw_button_save()
    draw_button_load()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # Pause button

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_x_pause <= event.pos[0] <= button_x_pause + button_width_pause and button_y_pause <= event.pos[
                1] <= button_y_pause + button_height_pause:
                pause = not pause
                last_generation_time = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONDOWN:

                # Adding new generation manually
            if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[
                1] <= button_y + button_height:
                next_generation()

                # Saving Game
            elif button_x_save <= event.pos[0] <= button_x_save + button_width_save and button_y_save <= event.pos[
                1] <= button_y_save + button_height_save:
                save_game_state()

                # Loading saved game
            elif button_x_load <= event.pos[0] <= button_x_load + button_width_load and button_y_load <= event.pos[
                    1] <= button_y_load + button_height_load:
                load_game_state()
                print("Game state loaded!")

        if event.type == GENERATION_EVENT and not pause:
            next_generation()
            last_generation_time = pygame.time.get_ticks()


    pygame.display.flip()
    clock.tick(20)
pygame.quit()

