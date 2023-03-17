import pygame
import sys
import re
import math
# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 16

# Load the boat image
boat_image = pygame.image.load('boat.png')
waypoints = [("N200.10", "E100.20"), ("N123.10", "E20.20"), ("W200.10", "E180.20"),
             ("N0.10", "E250.20"), ("W100.10", "E200.20"), ("N180.10", "E150.20")]


def process_input(input_str):
    pattern = r'([NS])(\d+\.\d+)\s+([WE])(\d+\.\d+)'
    match = re.match(pattern, input_str)

    if not match:
        print("Invalid input format. Example: N30.30 W50.10")
        return 0, 0

    direction1, degrees1, direction2, degrees2 = match.groups()
    degrees1, degrees2 = float(degrees1), float(degrees2)

    x_pos = SCREEN_WIDTH // 2
    y_pos = SCREEN_HEIGHT // 2

    if direction1 == "N":
        y_pos -= degrees1
    elif direction1 == "S":
        y_pos += degrees1

    if direction2 == "W":
        x_pos -= degrees2
    elif direction2 == "E":
        x_pos += degrees2

    return x_pos, y_pos


def draw_axes(screen):
    # Draw horizontal axis and coordinate labels
    for x in range(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2 + 1, 10):
        if x != 0:
            pygame.draw.line(screen, BLACK, (x + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 5),
                             (x + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 5))



    # Draw vertical axis and coordinate labels
    for y in range(-SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2 + 1, 10):
        if y != 0:
            pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2 - 5, y + SCREEN_HEIGHT // 2),
                             (SCREEN_WIDTH // 2 + 5, y + SCREEN_HEIGHT // 2))



    # Draw coordinates on left-hand side of screen
    font = pygame.font.Font(None, 18)
    for y in range(-SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2 + 1, 40):
        if y != 0:
            label = font.render(str(-y), True, BLACK)
            label_rect = label.get_rect(center=(20, y + SCREEN_HEIGHT // 2))
            screen.blit(label, label_rect)

    # Draw coordinates at bottom of screen
    font = pygame.font.Font(None, 18)
    for x in range(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2 + 1, 40):
        if x != 0:
            label = font.render(str(x), True, BLACK)
            label_rect = label.get_rect(center=(x + SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
            screen.blit(label, label_rect)


def plot_waypoints(screen, waypoints):
        # Load the marker image
        marker_img = pygame.image.load('marker1.png')

        # Loop through the waypoints and plot a marker for each one
        for lat, lon in waypoints:


            #Convert the latitude and longitude to pixel coordinates on the screen
            # Convert latitude and longitude to x and y coordinates

            x = (float(lon[1:]) - 180) * (800 / 360)  # assumes a screen width of 800 pixels
            y = (90 - float(lat[1:])) * (600 / 180)  # assumes a screen height of 600 pixels

            # Create a Rect object for the marker image
            marker_rect = marker_img.get_rect(center=(x, y))
            # Draw the marker on the screen
            screen.blit(marker_img,marker_rect)

        return

# Set up the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boat Navigation")

# Load font
font = pygame.font.Font(None, FONT_SIZE)

# Initial boat position
boat_x = SCREEN_WIDTH // 2 - 15
boat_y = SCREEN_HEIGHT // 2 - 15

axis_color = (200, 200, 200)
# Set up the clock
clock = pygame.time.Clock()
FPS = 60

# Main loop
running = True
while running:
    font = pygame.font.SysFont('Arial', 20)
    screen.fill(WHITE)
    draw_axes(screen)
    plot_waypoints(screen, waypoints)

    # Draw coordinates
    font = pygame.font.SysFont('Arial', 16)
    x_label = font.render(f"X: {boat_x - SCREEN_WIDTH//2 +15}", True, BLACK)
    y_label = font.render(f"Y: {boat_y - SCREEN_HEIGHT//2+15 }", True, BLACK)
    screen.blit(x_label, (750, 10))
    screen.blit(y_label, (750, 30))
    pygame.draw.line(screen, axis_color, (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)
    pygame.draw.line(screen, axis_color, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)
    screen.blit(boat_image, (boat_x, boat_y))


    # Update display and limit frame rate
    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                input_str = input("Enter direction and coordinates (e.g., N30.30 W50.10): ")
                x_pos, y_pos = process_input(input_str)

                # Ensure the boat stays within the window
                boat_x = max(min(x_pos, SCREEN_WIDTH - boat_image.get_width()), 0)
                boat_y = max(min(y_pos, SCREEN_HEIGHT - boat_image.get_height()), 0)





pygame.quit()
sys.exit()
