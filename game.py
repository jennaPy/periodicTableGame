from random import choice
from gamefunctions import *
from constants import *

def main():
    pygame.init()
    # Set up the window
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Periodic Table")

    game_mode = display_menu(WINDOW)

    elements_found = 0
    mistakes_made = 0
    hints_used = 0

    textbox_rect = pygame.Rect(7 * CELL_SIZE, 12.5 * CELL_SIZE, 6 * CELL_SIZE, CELL_SIZE)

    statsbox_rect = pygame.Rect(14.5 * CELL_SIZE, 11.5 * CELL_SIZE, 5 * CELL_SIZE, 3 * CELL_SIZE)

    hint_rect = pygame.Rect(1.5 * CELL_SIZE, 12.5 * CELL_SIZE, 3 * CELL_SIZE, CELL_SIZE)

    exit_rect = pygame.Rect(0.25 * CELL_SIZE, 0.25 * CELL_SIZE, 0.5 * CELL_SIZE, 0.5 * CELL_SIZE)

    timer_rect = pygame.Rect(0, 0, 100, 50)
    timer_rect.midtop = (WINDOW_WIDTH // 2, 20)

    pulse_speed = 4
    pulse_value = 0
    pulse_direction = 1

    fade_counter = 0
    fade_time = 180

    border_color = (0, 0, 0)

    current_hint = ""
    hint_step = 0

    start_time = pygame.time.get_ticks()
    pause_start_time = 0
    total_paused_time = 0

    overlay_cells = generate_overlay_cells()

    highlighted_cell = None

    if game_mode == 'random':
        if overlay_cells:
            highlighted_cell = choice(overlay_cells)
    elif game_mode == 'increasing':
        if overlay_cells:
            overlay_cells.sort(key=lambda x: x[2])  # Sort by atomic number
            highlighted_cell = overlay_cells[0]

    text_input = ''

    # Main loop
    running = True
    clock = pygame.time.Clock()
    hint_button_pressed = False
    exit_button_pressed = False
    hint_button_hovered = False
    exit_button_hovered = False
    paused = False
    static_elapsed_time = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        pause_start_time = pygame.time.get_ticks()
                        static_elapsed_time = get_elapsed_time(start_time, total_paused_time)  # Store static elapsed time
                    else:
                        total_paused_time += pygame.time.get_ticks() - pause_start_time
                elif not paused:
                    if event.key == pygame.K_RETURN and text_input != '':
                        if overlay_cells:
                            answer = element_dict[highlighted_cell[2]].name.lower()
                            if text_input.strip().lower() == answer:
                                overlay_cells.remove(highlighted_cell)
                                if overlay_cells:
                                    if game_mode == 'random':
                                        highlighted_cell = choice(overlay_cells)
                                    elif game_mode == 'increasing':
                                        highlighted_cell = overlay_cells[0]
                                else:
                                    highlighted_cell = None
                                elements_found += 1
                                play_sound('correct')
                                border_color = (0, 255, 0)  # correct answer
                                current_hint = ""
                                hint_step = 0
                                if elements_found == 118:
                                    completion(WINDOW, start_time, mistakes_made, hints_used, total_paused_time)
                            else:
                                mistakes_made += 1
                                play_sound('wrong')
                                border_color = (255, 0, 0)  # incorrect answer
                            fade_counter = fade_time
                        text_input = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        char = event.unicode.lower()
                        if char.isalpha():
                            if len(text_input) < 18:
                                text_input += char

            if not paused:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if hint_rect.collidepoint(event.pos) and hint_step < len(element_dict[highlighted_cell[2]].name):
                        hint_button_pressed = True
                        play_sound('button_click')
                    if exit_rect.collidepoint(event.pos):
                        exit_button_pressed = True
                        play_sound('button_click')

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if hint_button_pressed or exit_button_pressed:
                        if hint_rect.collidepoint(event.pos) and hint_step < len(element_dict[highlighted_cell[2]].name):
                            hint_button_pressed = False
                            current_hint, hint_step = update_hint(hint_step, highlighted_cell)
                            hints_used += 1
                        if exit_rect.collidepoint(event.pos):
                            exit_button_pressed = False
                            play_sound('bloop')
                            pygame.display.flip()
                            time.sleep(0.2)
                            game.main()

                if event.type == pygame.MOUSEMOTION:
                    hint_button_hovered = hint_rect.collidepoint(event.pos)
                    exit_button_hovered = exit_rect.collidepoint(event.pos)
                    if not hint_button_hovered:
                        if hint_button_pressed:
                            hint_button_pressed = False

                    if not exit_button_hovered:
                        if exit_button_pressed:
                            exit_button_pressed = False

        if not paused:
            pulse_value += pulse_direction * pulse_speed
            if pulse_value >= 255 or pulse_value <= 0:
                pulse_direction *= -1
                pulse_value = max(0, min(255, pulse_value))

            pulse_color = interpolate_color((255, 0, 0), (255, 255, 255), pulse_value / 255)

            if fade_counter > 0:
                fade_counter -= 1
                if fade_counter == 0:
                    border_color = (0, 0, 0)
                else:
                    fade_progress = 1 - (fade_counter / fade_time)
                    fade_color = interpolate_color(border_color, (0, 0, 0), fade_progress)  # Fade to black
                    border_color = fade_color

            WINDOW.fill((255, 255, 255))

            draw_grid(WINDOW, CELL_SIZE)

            # Draw periodic table
            draw_periodic_table(WINDOW, CELL_SIZE, font_letter, font_number)

            # Draw overlay cells
            if highlighted_cell:
                draw_overlay_cells(WINDOW, CELL_SIZE, overlay_cells, highlighted_cell, pulse_color)

            # Draw buttons
            draw_button(WINDOW, hint_rect, "Hint", font_text, hint_button_pressed, hint_button_hovered)
            draw_button(WINDOW, exit_rect, "<", font_text, exit_button_pressed, exit_button_hovered)

            # Draw text box
            pygame.draw.rect(WINDOW, (255, 255, 255), textbox_rect)
            pygame.draw.rect(WINDOW, border_color, textbox_rect, 4)
            text_surface = font_text.render(text_input, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=textbox_rect.center)
            WINDOW.blit(text_surface, text_rect)

            # Draw hint text
            hint_surface = font_text.render(current_hint, True, (0, 0, 0))
            hint_rect_text = hint_surface.get_rect(
                center=(textbox_rect.centerx, textbox_rect.bottom + 40))
            WINDOW.blit(hint_surface, hint_rect_text)

            # Draw stats box
            draw_stats_box(WINDOW, statsbox_rect, elements_found, mistakes_made, hints_used)

            # Draw timer
            elapsed_time = get_elapsed_time(start_time, total_paused_time)
            timer_surface = font_text.render(elapsed_time, True, (0, 0, 0))
            timer_rect_rendered = timer_surface.get_rect(center=timer_rect.center)
            WINDOW.blit(timer_surface, timer_rect_rendered)

            pygame.display.update()

        else:
            pause(WINDOW, static_elapsed_time)
            pygame.display.update()

        clock.tick(60)

    pygame.quit()
