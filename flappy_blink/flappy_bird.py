import pygame
import sys
import random
import time

# --- Game Config ---
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Blink 🐦")
font = pygame.font.SysFont("Arial", 36)

# --- Game State ---
bird_y = HEIGHT // 2
bird_velocity = 0
pipe_x = WIDTH
pipe_height = random.randint(100, HEIGHT - PIPE_GAP - 100)
score = 0
game_over = False

# --- Main Game Loop ---
running = True
while running:
    clock.tick(FPS)
    screen.fill((135, 206, 235))  # Sky blue background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Jump (will be replaced with blink later)
        if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = JUMP_STRENGTH

        # Restart after game over
        if game_over and event.type == pygame.KEYDOWN:
            bird_y = HEIGHT // 2
            bird_velocity = 0
            pipe_x = WIDTH
            pipe_height = random.randint(100, HEIGHT - PIPE_GAP - 100)
            score = 0
            game_over = False

    if not game_over:
        # Bird physics
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Bird rect
        bird_rect = pygame.Rect(WIDTH // 4 - 20, int(bird_y) - 20, 40, 40)
        pygame.draw.ellipse(screen, (255, 255, 0), bird_rect)

        # Pipe logic
        pipe_x -= PIPE_SPEED
        if pipe_x + PIPE_WIDTH < 0:
            pipe_x = WIDTH
            pipe_height = random.randint(100, HEIGHT - PIPE_GAP - 100)
            score += 1  # Increase score when bird passes a pipe

        top_pipe = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
        bottom_pipe = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP)

        pygame.draw.rect(screen, (34, 139, 34), top_pipe)
        pygame.draw.rect(screen, (34, 139, 34), bottom_pipe)

        # Check for collision
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe) or bird_y >= HEIGHT:
            game_over = True

        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (20, 20))
    
    else:
        # Game over screen
        game_over_text = font.render("Game Over", True, (200, 0, 0))
        score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
        restart_text = font.render("Press any key to restart", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
        screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
