import pygame
from elements import elements

colors = {
    "Nonmetal": "#FFFF99",
    "Alkali Metal": "#DAE9F8",
    "Alkaline Earth Metal": "#CEC7F9",
    "Transition Metal": "#F2CEEF",
    "Post-Transition Metal": "#C1F0C8",
    "Metalloid": "#83E28E",
    "Halogen": "#98D5FA",
    "Noble Gas": "#F7C7AC",
    "Lanthanide": "#E8E8E8",
    "Actinide": "#D0D0D0",
    "Empty Cell": "#404040"
}

group_start_positions = {
    1: (1, 1), 2: (2, 2),
    3: (4, 3), 4: (4, 4), 5: (4, 5), 6: (4, 6), 7: (4, 7), 8: (4, 8), 9: (4, 9), 10: (4, 10), 11: (4, 11), 12: (4, 12),
    13: (2, 13), 14: (2, 14), 15: (2, 15), 16: (2, 16), 17: (2, 17), 18: (1, 18)
}

element_positions = {}

# Initialise positions
for group_number, start_position in group_start_positions.items():
    group_elements = [element for element in elements if element.group_number == group_number]
    group_elements.sort(key=lambda x: x.atomic_number)

    current_row, current_col = start_position

    for element in group_elements:
        element_positions[element.atomic_number] = (current_row, current_col)
        current_row += 1

lanthanides = [element for element in elements if 57 <= element.atomic_number <= 71]
actinides = [element for element in elements if 89 <= element.atomic_number <= 103]

lanthanides_start = (9, 4)
actinides_start = (10, 4)

for element in lanthanides:
    element_positions[element.atomic_number] = lanthanides_start
    lanthanides_start = (lanthanides_start[0], lanthanides_start[1] + 1)

for element in actinides:
    element_positions[element.atomic_number] = actinides_start
    actinides_start = (actinides_start[0], actinides_start[1] + 1)

def draw_grid(window, cell_size):
    for x in range(0, window.get_width(), cell_size):
        pygame.draw.line(window, (0, 0, 0), (x, 0), (x, window.get_height()))
    for y in range(0, window.get_height(), cell_size):
        pygame.draw.line(window, (0, 0, 0), (0, y), (window.get_width(), y))

def draw_periodic_table(window, cell_size, letter, number):
    for row in range(15):
        for col in range(20):
            group_name = "Empty Cell"
            element = None
            atomic_number = None
            for atomic_number, (r, c) in element_positions.items():
                if row == r and col == c:
                    element = elements[atomic_number - 1]
                    group_name = element.group_name
                    break
            if group_name == "Empty Cell":
                if (row, col) == (6, 3):
                    color = colors["Lanthanide"]
                elif (row, col) == (7, 3):
                    color = colors["Actinide"]
                else:
                    color = colors["Empty Cell"]
            else:
                color = colors[group_name]
            pygame.draw.rect(window, color, (col * cell_size, row * cell_size, cell_size, cell_size))

            if group_name != "Empty Cell":
                text_surface = letter.render(element.symbol, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=((col + 0.5) * cell_size, (row + 0.5) * cell_size))
                window.blit(text_surface, text_rect)

                text_surface = number.render(str(atomic_number), True, (0, 0, 0))
                text_rect = text_surface.get_rect(topleft=(col * cell_size + 5, row * cell_size + 5))
                window.blit(text_surface, text_rect)

                text_surface = number.render(str(round(element.molar_mass)), True, (0, 0, 0))
                text_rect = text_surface.get_rect(bottomleft=(col * cell_size + 5, (row + 1) * cell_size - 5))
                window.blit(text_surface, text_rect)
            if color != "#404040":
                pygame.draw.rect(window, (0, 0, 0), (col * cell_size, row * cell_size, cell_size, cell_size), 1)
