import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
DONUT_COLOR = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Donut")

# Define donut parameters
R1 = 1
R2 = 2
K2 = 5
K1 = WIDTH / 4

A = 0
B = 0

def plot(x, y, color=DONUT_COLOR):
    screen.set_at((int(x), int(y)), color)

def render_frame(A, B):
    zbuffer = [[0] * WIDTH for _ in range(HEIGHT)]
    output = [[' '] * WIDTH for _ in range(HEIGHT)]

    cos_A = math.cos(A)
    sin_A = math.sin(A)
    cos_B = math.cos(B)
    sin_B = math.sin(B)

    for theta in range(0, 628, 10):
        costheta = math.cos(theta / 100)
        sintheta = math.sin(theta / 100)

        for phi in range(0, 628, 1):
            cosphi = math.cos(phi / 100)
            sinphi = math.sin(phi / 100)

            x = R2 + R1 * costheta
            y = R1 * sintheta

            x1 = x * (cos_B * cosphi + sin_A * sin_B * sinphi) - y * cos_A * sin_B
            y1 = x * (sin_B * cosphi - sin_A * cos_B * sinphi) + y * cos_A * cos_B
            z1 = K2 + x * cos_A * sinphi + y * sin_A
            ooz = 1 / z1

            xp = int(WIDTH / 2 + K1 * ooz * x1)
            yp = int(HEIGHT / 2 - K1 * ooz * y1)
            if 0 <= xp < WIDTH and 0 <= yp < HEIGHT:
                if ooz > zbuffer[yp][xp]:
                    zbuffer[yp][xp] = ooz
                    luminance_index = costheta * cosphi * sin_B - cos_A * costheta * sinphi - sin_A * sintheta + cos_B * (cos_A * sintheta - costheta * sinphi * sin_A)
                    if luminance_index > 0:
                        luminance = luminance_index * 8
                        output[yp][xp] = ".,-~:;=!*#$@"[int(luminance)]

    for i in range(HEIGHT):
        for j in range(WIDTH):
            plot(j, i, (0, 0, 0) if output[i][j] == ' ' else DONUT_COLOR)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BACKGROUND_COLOR)

    render_frame(A, B)
    pygame.display.flip()

    A += 0.04
    B += 0.02 
