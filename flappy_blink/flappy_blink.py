import pygame
import sys
import random
import math
import cv2
import mediapipe as mp
import threading
import time
import os

# --- High Score Load ---
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read())
        except ValueError:
            high_score = 0

# --- Game State ---
game_state = "start"  # "start", "playing", "game_over"
should_flap = False

# --- Blink Detection Thread ---
def blink_detection_thread():
    global should_flap, game_state
    
    webcam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    EAR_THRESHOLD = 0.20
    CONSEC_FRAMES = 2
    blink_counter = 0

    eye_landmarks = {
        "left_corner": 133,
        "right_corner": 246,
        "top_outer": 159,
        "bottom_outer": 145,
        "top_inner": 160,
        "bottom_inner": 144
    }

    def euclidean(p1, p2):
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def get_ear(landmarks):
        eye = {k: landmarks[v] for k, v in eye_landmarks.items()}
        vert1 = euclidean(eye["top_outer"], eye["bottom_outer"])
        vert2 = euclidean(eye["top_inner"], eye["bottom_inner"])
        horiz = euclidean(eye["left_corner"], eye["right_corner"])
        return (vert1 + vert2) / (2.0 * horiz)

    while True:
        success, frame = webcam.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0].landmark
            ear = get_ear(landmarks)
            if ear < EAR_THRESHOLD:
                blink_counter += 1
            else:
                blink_counter = 0

            # Only allow blinking to trigger flapping when in 'playing' state
            # This avoids accidental jumps on menus or during reset
            if blink_counter >= CONSEC_FRAMES and game_state == "playing":
                should_flap = True
                blink_counter = 0

        time.sleep(0.01)

# --- Game Config ---
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 60
PIPE_GAP_BASE = 220  # Base gap size
PIPE_GAP = PIPE_GAP_BASE  # This will be adjusted dynamically
PIPE_SPEED = 3

# --- Init Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Blink \U0001F425")
font_large = pygame.font.SysFont("Arial", 36)
font_small = pygame.font.SysFont("Arial", 18)

# --- Game Variables ---
bird_y = HEIGHT // 2
bird_velocity = 0
pipe_x = WIDTH
# Subtracting 100 from both sides prevents pipes from appearing too close to the screen edges,
# which would make the gap unplayable or invisible.
pipe_height = random.randint(100, HEIGHT - PIPE_GAP - 100)
score = 0

# --- Start Blink Thread ---
threading.Thread(target=blink_detection_thread, daemon=True).start()

# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "start" and event.type == pygame.KEYDOWN:
            game_state = "playing"
        elif game_state == "game_over" and event.type == pygame.KEYDOWN:
            if score > high_score:
                high_score = score
                with open("highscore.txt", "w") as f:
                    f.write(str(high_score))
            bird_y = HEIGHT // 2
            bird_velocity = 0
            pipe_x = WIDTH
            PIPE_GAP = PIPE_GAP_BASE  # Reset to base gap
            pipe_height = random.randint(100, HEIGHT - PIPE_GAP - 100)
            score = 0
            game_state = "start"

    if game_state == "start":
        screen.fill((135, 206, 235))  # Sky blue background
        title = font_large.render("Flappy Blink", True, (0, 0, 0))
        prompt = font_small.render("Press any key to start", True, (50, 50, 50))
        texts = [title, prompt]
        spacing = 10
        total_height = sum(t.get_height() for t in texts) + spacing
        start_y = (HEIGHT - total_height) // 2
        for i, t in enumerate(texts):
            rect = t.get_rect(center=(WIDTH // 2, start_y + i * (t.get_height() + spacing)))
            screen.blit(t, rect)
        pygame.display.flip()
        continue

    clock.tick(FPS)
    screen.fill((135, 206, 235))  # Sky blue background

    if game_state == "playing":
        if should_flap:
            bird_velocity = JUMP_STRENGTH
            should_flap = False

        bird_velocity += GRAVITY
        bird_y += bird_velocity

        bird_rect = pygame.Rect(WIDTH // 4 - 20, int(bird_y) - 20, 40, 40)
        pygame.draw.ellipse(screen, (255, 255, 0), bird_rect)

        pipe_x -= PIPE_SPEED
        if pipe_x + PIPE_WIDTH < 0:
            pipe_x = WIDTH
            # Increase difficulty gradually by reducing the pipe gap as score increases
            # Ensures a minimum gap of 120px for playability
            PIPE_GAP = max(120, PIPE_GAP_BASE - score * 2)
            pipe_height = random.randint(100, HEIGHT - PIPE_GAP - 100)
            score += 1

        top_pipe = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
        bottom_pipe = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP)

        pygame.draw.rect(screen, (34, 139, 34), top_pipe)
        pygame.draw.rect(screen, (34, 139, 34), bottom_pipe)

        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe) or bird_y >= HEIGHT:
            game_state = "game_over"

        score_text = font_small.render(f"Score: {score}", True, (0, 0, 0))
        high_score_text = font_small.render(f"High Score: {high_score}", True, (0, 0, 0))
        screen.blit(score_text, (20, 20))
        screen.blit(high_score_text, (20, 40))

    elif game_state == "game_over":
        game_over_text = font_large.render("Game Over", True, (200, 0, 0))
        score_text = font_small.render(f"Final Score: {score}", True, (0, 0, 0))
        high_score_text = font_small.render(f"High Score: {high_score}", True, (0, 0, 0))
        restart_text = font_small.render("Press any key to restart", True, (0, 0, 0))

        texts = [game_over_text, score_text, high_score_text, restart_text]
        spacing = 20
        total_height = sum(t.get_height() for t in texts) + spacing * (len(texts) - 1)
        start_y = (HEIGHT - total_height) // 2
        for i, t in enumerate(texts):
            rect = t.get_rect(center=(WIDTH // 2, start_y + i * (t.get_height() + spacing)))
            screen.blit(t, rect)

    fps = int(clock.get_fps())
    fps_text = font_small.render(f"FPS: {fps}", True, (0, 0, 0))
    fps_rect = fps_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(fps_text, fps_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()