import game
import time
from elements import element_dict
from table import draw_grid, draw_periodic_table, element_positions
from constants import *
import os
import random

script_dir = os.path.dirname(__file__)
sound_folder = os.path.join(script_dir, 'sounds')

pygame.mixer.init()

def draw_button_with_hover(window, text, font, rect, hover_color, normal_color):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)

    button_color = hover_color if is_hovered else normal_color
    pygame.draw.rect(window, button_color, rect)
    pygame.draw.rect(window, (0, 0, 0), rect, 3)

    button_text = font.render(text, True, (255, 255, 255))
    text_rect = button_text.get_rect(center=rect.center)
    window.blit(button_text, text_rect)

    return is_hovered

def display_menu(window):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill((64, 64, 64))

    title_surface = title_font.render("Periodic Table Game", True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))

    random_option_rect = pygame.Rect((WINDOW_WIDTH // 2) - 200, WINDOW_HEIGHT // 2, 400, 70)
    increasing_option_rect = pygame.Rect((WINDOW_WIDTH // 2) - 200, (WINDOW_HEIGHT // 2) + 200, 400, 70)

    while True:
        window.blit(overlay, (0, 0))
        window.blit(title_surface, title_rect)

        if draw_button_with_hover(window, "Random Order", option_font, random_option_rect, (255, 0, 0), (128, 128, 128)):
            if pygame.mouse.get_pressed()[0]:  # left mouse button
                play_sound('bloop')
                return 'random'

        if draw_button_with_hover(window, "Increasing Order", option_font, increasing_option_rect, (255, 0, 0), (128, 128, 128)):
            if pygame.mouse.get_pressed()[0]:
                play_sound('bloop')
                return 'increasing'

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def completion(window, start_time, mistakes_made, hints_used, pause_time):
    draw_grid(window, CELL_SIZE)
    draw_periodic_table(window, CELL_SIZE, font_letter, font_number)

    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((64, 64, 64, 200))
    window.blit(overlay, (0, 0))

    final_time_text = get_elapsed_time(start_time, pause_time)

    final_time_surface = title_font.render(final_time_text, True, (0, 0, 0), (255, 255, 255))
    final_time_rect = final_time_surface.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) - 100))

    text_lines = [
        f'Mistakes made: {mistakes_made}',
        f'Hints used: {hints_used}',
    ]
    info_surface = [option_font.render(line, True, (0, 0, 0), (255, 255, 255)) for line in text_lines]
    info_rect = [surface.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) + i * 40)) for i, surface in enumerate(info_surface)]

    play_again_rect = pygame.Rect((WINDOW_WIDTH // 2) - 200, (WINDOW_HEIGHT // 2) + 320, 400, 70)

    box_rect = pygame.Rect((WINDOW_WIDTH // 2) - 250, (WINDOW_HEIGHT // 2) - 250, 500, 400)
    pygame.draw.rect(window, (255, 255, 255), box_rect)
    pygame.draw.rect(window, (0, 0, 0), box_rect, 4)

    while True:
        window.blit(final_time_surface, final_time_rect)
        for surface, rect in zip(info_surface, info_rect):
            window.blit(surface, rect)
        is_hovered = draw_button_with_hover(window, "Play Again", option_font, play_again_rect, (255, 0, 0), (128, 128, 128))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if is_hovered and play_again_rect.collidepoint(mouse_pos):
                    play_sound('bloop')
                    pygame.display.flip()
                    time.sleep(0.05)
                    game.main()

def pause(window, static_elapsed_time):
    window.fill((64, 64, 64))

    final_time_surface = title_font.render(static_elapsed_time, True, (0, 0, 0), (255, 255, 255))
    final_time_rect = final_time_surface.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) - 100))

    box_rect = pygame.Rect((WINDOW_WIDTH // 2) - 250, (WINDOW_HEIGHT // 2) - 250, 500, 400)
    pygame.draw.rect(window, (255, 255, 255), box_rect)
    pygame.draw.rect(window, (0, 0, 0), box_rect, 4)

    pause_text_surface = option_font.render("Paused", True, (0, 0, 0), (255, 255, 255))
    pause_text_rect = pause_text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(pause_text_surface, pause_text_rect)

    window.blit(final_time_surface, final_time_rect)

def interpolate_color(color_from, color_to, progress):
    r = int(color_from[0] + (color_to[0] - color_from[0]) * progress)
    g = int(color_from[1] + (color_to[1] - color_from[1]) * progress)
    b = int(color_from[2] + (color_to[2] - color_from[2]) * progress)
    return r, g, b

def generate_overlay_cells():
    cells = []
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            for atomic_number, (r, c) in element_positions.items():
                if row == r and col == c:
                    cells.append((row, col, atomic_number))
                    break
    return cells

def draw_overlay_cells(surface, cell_dim, overlay_cells_list, highlighted_cell_item, pulse_color_value):
    for row, col, atomic_number in overlay_cells_list:
        x = col * cell_dim
        y = row * cell_dim
        cell_rect = pygame.Rect(x, y, cell_dim, cell_dim)

        if (row, col, atomic_number) == highlighted_cell_item:
            pygame.draw.rect(surface, pulse_color_value, cell_rect)
        else:
            pygame.draw.rect(surface, (255, 255, 255), cell_rect)

        pygame.draw.rect(surface, (0, 0, 0), cell_rect, 1)

        num_surface = font_number.render(str(atomic_number), True, (0, 0, 0))
        num_rect = num_surface.get_rect(topleft=(col * cell_dim + 5, row * cell_dim + 5))
        surface.blit(num_surface, num_rect)

def draw_button(surface, rect, text, font, is_pressed, is_hovered):
    button_color = (190, 190, 190) if not is_hovered else (210, 210, 210)
    shadow_color = (120, 120, 120)
    highlight_color = (255, 255, 255)

    pygame.draw.rect(surface, button_color, rect)
    if is_pressed:
        pygame.draw.line(surface, shadow_color, (rect.left, rect.top), (rect.right, rect.top), 3)
        pygame.draw.line(surface, shadow_color, (rect.left, rect.top), (rect.left, rect.bottom), 3)

        pygame.draw.line(surface, highlight_color, (rect.left, rect.bottom - 1), (rect.right, rect.bottom - 1), 3)
        pygame.draw.line(surface, highlight_color, (rect.right - 1, rect.top), (rect.right - 1, rect.bottom), 3)
    else:
        pygame.draw.line(surface, highlight_color, (rect.left, rect.top), (rect.right, rect.top), 3)
        pygame.draw.line(surface, highlight_color, (rect.left, rect.top), (rect.left, rect.bottom), 3)

        pygame.draw.line(surface, shadow_color, (rect.left, rect.bottom - 1), (rect.right, rect.bottom - 1), 3)
        pygame.draw.line(surface, shadow_color, (rect.right - 1, rect.top), (rect.right - 1, rect.bottom), 3)

    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def update_hint(hint_step, highlighted_cell):
    answer = element_dict[highlighted_cell[2]].name.lower()
    if hint_step < len(answer):
        hint_step += 1
        revealed_chars = answer[:hint_step]
        remaining_chars = '_' * (len(answer) - hint_step)
        # spaces between each character and underscore
        formatted_hint = ' '.join(revealed_chars + remaining_chars)
        current_hint = 'HINT: ' + formatted_hint
        return current_hint, hint_step
    return "", hint_step

def draw_stats_box(surface, statsbox_rect, elements_found, mistakes_made, hints_used):
    text_lines = [
        f'Elements found: {elements_found} / 118',
        f'Mistakes made: {mistakes_made}',
        f'Hints used: {hints_used}',
    ]

    text_surfaces = [font_text.render(line, True, (255, 255, 255)) for line in text_lines]
    text_rects = [text_surface.get_rect(center=(statsbox_rect.centerx,
                                                statsbox_rect.centery + i * text_surface.get_height()
                                                * 2 - text_surface.get_height() * 2))
                  for i, text_surface in enumerate(text_surfaces)]
    [surface.blit(text_surface, text_rect) for text_surface, text_rect in zip(text_surfaces, text_rects)]

def draw_timer(surface, font, timer, rect):
    time_surface = font.render(timer, True, (255, 255, 255))
    surface.blit(time_surface, rect)

def get_elapsed_time(start_time, paused_time):
    elapsed_time = pygame.time.get_ticks() - start_time - paused_time
    seconds = elapsed_time // 1000
    minutes = seconds // 60
    seconds %= 60
    return f'{minutes:02}:{seconds:02}'

def play_sound(sound_type):
    sound_files = os.listdir(sound_folder)
    sound_type_files = [file for file in sound_files if sound_type in file]
    if sound_type_files:
        random_sound = random.choice(sound_type_files)

        picked_sound = pygame.mixer.Sound(os.path.join(sound_folder, random_sound))
        picked_sound.play()

def maintain_aspect_ratio(new_width, new_height, aspect_ratio):
    if new_width / new_height > aspect_ratio:
        return int(new_height * aspect_ratio), new_height
    else:
        return new_width, int(new_width / aspect_ratio)
