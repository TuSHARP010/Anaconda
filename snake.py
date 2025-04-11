import pygame
import random
import time
import sys
from search_algorithms import *

# Parse command-line arguments
if len(sys.argv) != 3:
    print("Usage: python snake.py <level> <search_algorithm>")
    sys.exit(1)

level = sys.argv[1].lower()
search_algorithm = sys.argv[2].lower()

# Validate level
LEVELS = {"level0": 0, "level1": 5, "level2": 10, "level3": 15}
if level not in LEVELS:
    print("Invalid level! Choose from: level0, level1, level2, level3")
    sys.exit(1)

# Validate search algorithm
ALGORITHMS = {"bfs": bfs, "dfs": dfs, "ucs": ucs, "ids": ids, "a*": astar, "random": random_move, "greedy_bfs": greedy_bfs}
if search_algorithm not in ALGORITHMS:
    print("Invalid search algorithm! Choose from: bfs, dfs, ucs, ids, a*, random, greedy_bfs")
    sys.exit(1)

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 20
WHITE, BLACK, GREEN, RED, GRAY = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0), (128, 128, 128)
FONT = pygame.font.Font(None, 36)

# Grid settings
ROWS, COLS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# AI Snake starting position
snake_pos = [ROWS // 2, COLS // 2]

# Food position
food_pos = [random.randint(0, ROWS - 1), random.randint(0, COLS - 1)]

# Timer settings
TIME_LIMIT = 30
start_time = time.time()

# Setup Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"AI Snake Game ({search_algorithm.upper()} - {level.upper()})")

clock = pygame.time.Clock()

# Score
score = 0  

# Generate obstacles based on level
obstacles = set()
OBSTACLE_COUNT = (ROWS * COLS * LEVELS[level]) // 100  # % of total grid size
while len(obstacles) < OBSTACLE_COUNT:
    obstacle = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    if obstacle != tuple(snake_pos) and obstacle != tuple(food_pos):
        obstacles.add(obstacle)

# Game Over function
def game_over():
    print("Score: ", score)
    pygame.quit()
    sys.exit()

running = True
path = []
time_printed = False  # Move this outside the game loop

while running:
    screen.fill(BLACK)

    # Timer logic
    elapsed_time = time.time() - start_time
    time_left = max(0, TIME_LIMIT - int(elapsed_time))

    # If time runs out, end game
    if time_left == 0:
        running = False
        game_over()

    # Find path if no current path
    if not path and time_left > 0:
        ai_start_time = time.perf_counter()
        path = ALGORITHMS[search_algorithm](tuple(snake_pos), tuple(food_pos), obstacles, ROWS, COLS)
        
        if not path:  # If no path is found, retry up to 5 times
         for retry in range(5):
            path = ALGORITHMS[search_algorithm](tuple(snake_pos), tuple(food_pos), obstacles, ROWS, COLS)
            if path:
                break  # Stop retrying once a valid path is found

        ai_end_time = time.perf_counter()

        if path:
            print(f"Algorithm: {search_algorithm}, Time taken: {ai_end_time - ai_start_time:.6f} seconds, Path length: {len(path)}")

        else:
            print(f"Warning: No path found from {snake_pos} to {food_pos}, stopping AI.")
            running = False  # Stop AI if no valid path exists after multiple retries    

    # Move AI Snake
    if path:
        move = path.pop(0)  # Take next move from path
        new_pos = [snake_pos[0] + move[0], snake_pos[1] + move[1]]

        # Validate move before applying
        if 0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS and tuple(new_pos) not in obstacles:
            snake_pos[:] = new_pos  # Apply valid move
        else:
            running = False  # Stop game if invalid move
            game_over()

    # Check if AI reaches food (Increase Score, Relocate Food)
    if snake_pos == food_pos:
     score += 1  

    # Ensure food is placed in a valid, empty position
     while True:
        new_food_pos = [random.randint(0, ROWS - 1), random.randint(0, COLS - 1)]
        if tuple(new_food_pos) not in obstacles and tuple(new_food_pos) != tuple(snake_pos):
            food_pos = new_food_pos
            break  # Only break if food is placed correctly

     path = []  # Reset path so the algorithm recalculates a new one
     time_printed = False  # Allow new path search to be timed

    # Draw Snake
    pygame.draw.rect(screen, GREEN, (snake_pos[1] * CELL_SIZE, snake_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw Food
    pygame.draw.rect(screen, RED, (food_pos[1] * CELL_SIZE, food_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw Obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, (obs[1] * CELL_SIZE, obs[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Display Timer
    timer_text = FONT.render(f"Time Left: {time_left}s", True, WHITE)
    screen.blit(timer_text, (20, 20))

    # Display Score
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 50))

    pygame.display.update()
    clock.tick(5)  # Control AI speed

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            game_over()

pygame.quit()

print("Score: ", score)
