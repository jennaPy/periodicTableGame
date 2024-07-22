import pygame

pygame.font.init()
font_letter = pygame.font.Font(None, 30)
font_number = pygame.font.Font(None, 22)
font_text = pygame.font.Font(None, 32)
title_font = pygame.font.Font(None, 150)
option_font = pygame.font.Font(None, 56)

CELL_SIZE = 65
GRID_WIDTH, GRID_HEIGHT = 20, 15
WINDOW_WIDTH, WINDOW_HEIGHT = CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT
