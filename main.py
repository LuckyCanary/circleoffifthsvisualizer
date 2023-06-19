import pygame
from pygame.locals import *
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

LARGE_RADIUS = 250
SMALL_RADIUS = 100

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

key_centers = {
    "C": {"notes": ["C", "D", "E", "F", "G", "A", "B"], "chords": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
          "accidentals": 0, "relative": "Am"},
    "G": {"notes": ["G", "A", "B", "C", "D", "E", "F#"], "chords": ["G", "Am", "Bm", "C", "D", "Em", "F#dim"],
          "accidentals": 1, "relative": "Em"},
    "D": {"notes": ["D", "E", "F#", "G", "A", "B", "C#"], "chords": ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"],
          "accidentals": 2, "relative": "Bm"},
    "A": {"notes": ["A", "B", "C#", "D", "E", "F#", "G#"], "chords": ["A", "Bm", "C#m", "D", "E", "F#m", "G#dim"],
          "accidentals": 3, "relative": "F#m"},
    "E": {"notes": ["E", "F#", "G#", "A", "B", "C#", "D#"], "chords": ["E", "F#m", "G#m", "A", "B", "C#m", "D#dim"],
          "accidentals": 4, "relative": "C#m"},
    "B": {"notes": ["B", "C#", "D#", "E", "F#", "G#", "A#"], "chords": ["B", "C#m", "D#m", "E", "F#", "G#m", "A#dim"],
          "accidentals": 5, "relative": "G#m"},
    "F#": {"notes": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
           "chords": ["F#", "G#m", "A#m", "B", "C#", "D#m", "E#dim"],
           "accidentals": 6, "relative": "D#m"},
    "C#": {"notes": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
           "chords": ["C#", "D#m", "E#m", "F#", "G#", "A#m", "B#dim"],
           "accidentals": 7, "relative": "A#m"},
    "Ab": {"notes": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"], "chords": ["Ab", "Bbm", "Cm", "Db", "Eb", "Fm", "Gdim"],
           "accidentals": 4, "relative": "Fm"},
    "Eb": {"notes": ["Eb", "F", "G", "Ab", "Bb", "C", "D"], "chords": ["Eb", "Fm", "Gm", "Ab", "Bb", "Cm", "Ddim"],
           "accidentals": 3, "relative": "Cm"},
    "Bb": {"notes": ["Bb", "C", "D", "Eb", "F", "G", "A"], "chords": ["Bb", "Cm", "Dm", "Eb", "F", "Gm", "Adim"],
           "accidentals": 2, "relative": "Gm"},
    "F": {"notes": ["F", "G", "A", "Bb", "C", "D", "E"], "chords": ["F", "Gm", "Am", "Bb", "C", "Dm", "Edim"],
          "accidentals": 1, "relative": "Dm"},
}
minor_key_centers = {
    "Am": {"notes": ["A", "B", "C", "D", "E", "F", "G"], "chords": ["Am", "Bdim", "C", "Dm", "Em", "F", "G"],
           "accidentals": 0, "relative": "C"},
    "Em": {"notes": ["E", "F#", "G", "A", "B", "C", "D"], "chords": ["Em", "F#dim", "G", "Am", "Bm", "C", "D"],
           "accidentals": 1, "relative": "G"},
    "Bm": {"notes": ["B", "C#", "D", "E", "F#", "G", "A"], "chords": ["Bm", "C#dim", "D", "Em", "F#m", "G", "A"],
           "accidentals": 2, "relative": "D"},
    "F#m": {"notes": ["F#", "G#", "A", "B", "C#", "D", "E"], "chords": ["F#m", "G#dim", "A", "Bm", "C#m", "D", "E"],
            "accidentals": 3, "relative": "A"},
    "C#m": {"notes": ["C#", "D#", "E", "F#", "G#", "A", "B"], "chords": ["C#m", "D#dim", "E", "F#m", "G#m", "A", "B"],
            "accidentals": 4, "relative": "E"},
    "G#m": {"notes": ["G#", "A#", "B", "C#", "D#", "E", "F#"], "chords": ["G#m", "A#dim", "B", "C#m", "D#m", "E", "F#"],
            "accidentals": 5, "relative": "B"},
    "D#m": {"notes": ["D#", "E#", "F#", "G#", "A#", "B", "C#"], "chords": ["D#m", "E#dim", "F#", "G#m", "A#m", "B", "C#"],
            "accidentals": 6, "relative": "F#"},
    "A#m": {"notes": ["A#", "B#", "C#", "D#", "E#", "F#", "G#"], "chords": ["A#m", "B#dim", "C#", "D#m", "E#m", "F#", "G#"],
            "accidentals": 7, "relative": "C#"},
    "Fm": {"notes": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"], "chords": ["Fm", "Gdim", "Ab", "Bbm", "Cm", "Db", "Eb"],
           "accidentals": 4, "relative": "Ab"},
    "Cm": {"notes": ["C", "D", "Eb", "F", "G", "Ab", "Bb"], "chords": ["Cm", "Ddim", "Eb", "Fm", "Gm", "Ab", "Bb"],
           "accidentals": 3, "relative": "Eb"},
    "Gm": {"notes": ["G", "A", "Bb", "C", "D", "Eb", "F"], "chords": ["Gm", "Adim", "Bb", "Cm", "Dm", "Eb", "F"],
           "accidentals": 2, "relative": "Bb"},
    "Dm": {"notes": ["D", "E", "F", "G", "A", "Bb", "C"], "chords": ["Dm", "Edim", "F", "Gm", "Am", "Bb", "C"],
           "accidentals": 1, "relative": "F"},
}

selected_key = None

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle of Fifths")


def draw_circle():
    pygame.draw.circle(window, GRAY, (CENTER_X, CENTER_Y), 300, 2)

    pygame.draw.circle(window, GRAY, (CENTER_X, CENTER_Y), LARGE_RADIUS)
    pygame.draw.circle(window, GRAY, (CENTER_X, CENTER_Y), SMALL_RADIUS)


def draw_relative_minor_buttons():
    angle_increment = 2 * math.pi / len(key_centers)
    starting_angle = -math.pi / 2
    for key, value in key_centers.items():
        angle = starting_angle + list(key_centers.keys()).index(key) * angle_increment
        x = int(CENTER_X + SMALL_RADIUS * math.cos(angle))
        y = int(CENTER_Y + SMALL_RADIUS * math.sin(angle))
        pygame.draw.circle(window, WHITE, (x, y), 20)
        font = pygame.font.Font(None, 20)
        text = font.render(value["relative"], True, (0, 0, 0))  # Display relative minor key letter
        text_rect = text.get_rect(center=(x, y))
        window.blit(text, text_rect)


def check_relative_minor_click():
    global selected_key
    if event.type == MOUSEBUTTONDOWN:
        for key, value in key_centers.items():
            angle_increment = 2 * math.pi / len(key_centers)
            starting_angle = -math.pi / 2
            angle = starting_angle + list(key_centers.keys()).index(key) * angle_increment
            x = int(CENTER_X + SMALL_RADIUS * math.cos(angle))
            y = int(CENTER_Y + SMALL_RADIUS * math.sin(angle))
            if math.sqrt((event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2) <= 20:
                selected_key = key


def draw_key_centers():
    angle_increment = 2 * math.pi / len(key_centers)  # Adjusted angle increment
    starting_angle = -math.pi / 2  # Start angle at 12 o'clock position
    for i, key in enumerate(key_centers.keys()):
        angle = starting_angle + i * angle_increment
        x = int(CENTER_X + 250 * math.cos(angle))
        y = int(CENTER_Y + 250 * math.sin(angle))
        pygame.draw.circle(window, WHITE, (x, y), 20)
        pygame.draw.circle(window, GRAY, (x, y), 20, 2)
        font = pygame.font.Font(None, 32)  # Increased font size
        text = font.render(key, True, BLACK)
        text_rect = text.get_rect(center=(x, y))
        window.blit(text, text_rect)
        first_letter = font.render(key[0], True, BLACK)
        letter_rect = first_letter.get_rect(center=(x, y))  # Center the letter within the circle
        if len(key) > 1:
            letter_rect.move_ip(-(letter_rect.width // 2), 0)  # Adjust the position for keys with two characters
        window.blit(first_letter, letter_rect)


def draw_selected_key_info():
    if selected_key:
        info = key_centers[selected_key]
        # Display key information (notes, chords, accidentals, relative) on the screen
        font = pygame.font.Font(None, 30)
        text_surface = font.render(f"Key: {selected_key}", True, WHITE)
        window.blit(text_surface, (20, 20))

        notes_text = "Notes: " + ", ".join(info["notes"])
        notes_surface = font.render(notes_text, True, WHITE)
        window.blit(notes_surface, (20, 60))

        chords_text = "Chords: " + ", ".join(info["chords"])
        chords_surface = font.render(chords_text, True, WHITE)
        window.blit(chords_surface, (20, 100))

        acc_text = f"Accidentals: {info['accidentals']}"
        acc_surface = font.render(acc_text, True, WHITE)
        window.blit(acc_surface, (20, 140))

        rel_text = f"Relative: {info['relative']}"
        rel_surface = font.render(rel_text, True, WHITE)
        window.blit(rel_surface, (20, 180))


def check_click():
    global selected_key
    if event.type == MOUSEBUTTONDOWN:
        for key, value in key_centers.items():
            angle_increment = 2 * math.pi / len(key_centers)  # Adjusted angle increment
            starting_angle = -math.pi / 2  # Start angle at 12 o'clock position
            angle = starting_angle + list(key_centers.keys()).index(key) * angle_increment
            x = int(CENTER_X + 250 * math.cos(angle))
            y = int(CENTER_Y + 250 * math.sin(angle))
            if math.sqrt((event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2) <= 20:
                selected_key = key


running = True

while running:
    window.fill((0, 0, 0))
    draw_circle()
    draw_key_centers()
    draw_relative_minor_buttons()
    draw_selected_key_info()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        check_click()
        check_relative_minor_click()

pygame.quit()
