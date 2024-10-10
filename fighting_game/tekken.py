import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Fighting Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define player properties
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 100
player1_pos = [100, SCREEN_HEIGHT - PLAYER_HEIGHT]
player2_pos = [SCREEN_WIDTH - 150, SCREEN_HEIGHT - PLAYER_HEIGHT]

player1_health = 100
player2_health = 100

move_speed = 5
attack_range = 60

# Health bar dimensions
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20

# Main game loop
clock = pygame.time.Clock()

def draw_health_bars():
    # Draw health bars for both players
    pygame.draw.rect(screen, RED, (50, 50, player1_health * 2, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH - 250, 50, player2_health * 2, HEALTH_BAR_HEIGHT))

def handle_movement(keys):
    global player1_pos, player2_pos

    # Player 1 movement (A and D)
    if keys[pygame.K_a] and player1_pos[0] > 0:
        player1_pos[0] -= move_speed
    if keys[pygame.K_d] and player1_pos[0] + PLAYER_WIDTH < player2_pos[0]:
        player1_pos[0] += move_speed

    # Player 2 movement (Left and Right arrows)
    if keys[pygame.K_LEFT] and player2_pos[0] > player1_pos[0] + PLAYER_WIDTH:
        player2_pos[0] -= move_speed
    if keys[pygame.K_RIGHT] and player2_pos[0] + PLAYER_WIDTH < SCREEN_WIDTH:
        player2_pos[0] += move_speed

def handle_attacks(keys):
    global player1_health, player2_health

    # Player 1 attack (W key)
    if keys[pygame.K_w] and abs(player1_pos[0] - player2_pos[0]) < attack_range:
        player2_health -= 10
        if player2_health < 0:
            player2_health = 0

    # Player 2 attack (Up arrow key)
    if keys[pygame.K_UP] and abs(player1_pos[0] - player2_pos[0]) < attack_range:
        player1_health -= 10
        if player1_health < 0:
            player1_health = 0

def draw_players():
    # Draw Player 1 (red rectangle)
    pygame.draw.rect(screen, RED, (*player1_pos, PLAYER_WIDTH, PLAYER_HEIGHT))
    # Draw Player 2 (blue rectangle)
    pygame.draw.rect(screen, BLUE, (*player2_pos, PLAYER_WIDTH, PLAYER_HEIGHT))

def check_win():
    if player1_health <= 0:
        return "Player 2 Wins!"
    elif player2_health <= 0:
        return "Player 1 Wins!"
    return None

def reset_game():
    global player1_health, player2_health, player1_pos, player2_pos
    player1_health = 100
    player2_health = 100
    player1_pos = [100, SCREEN_HEIGHT - PLAYER_HEIGHT]
    player2_pos = [SCREEN_WIDTH - 150, SCREEN_HEIGHT - PLAYER_HEIGHT]

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Check for events (e.g., quit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Handle player movement
    handle_movement(keys)

    # Handle player attacks
    handle_attacks(keys)

    # Draw health bars and players
    draw_health_bars()
    draw_players()

    # Check win condition
    win_message = check_win()
    if win_message:
        font = pygame.font.Font(None, 74)
        win_text = font.render(win_message, True, GREEN)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        reset_game()

    # Update display
    pygame.display.update()

    # Cap frame rate
    clock.tick(60)
