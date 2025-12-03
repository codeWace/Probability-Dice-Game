import pygame
import random
import os

# --- Settings ---
SCREEN_WIDTH = 800  # Bigger window
SCREEN_HEIGHT = 450
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Probability Dice Game")
clock = pygame.time.Clock()

# --- Font ---
FONT = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)

# --- Load Dice Animation Frames ---
dice_folder = "assets/dice/roll_frames"  # 24 frames of rolling dice
dice_frames = []
for file in sorted(os.listdir(dice_folder)):
    if file.endswith(".png"):
        img = pygame.image.load(os.path.join(dice_folder, file)).convert_alpha()
        img = pygame.transform.scale(img, (128,128))  # Bigger dice
        dice_frames.append(img)

# --- Game Variables ---
score = 0
current_question_index = 0
current_roll = None
roll_anim_index = 0
rolling = False
message = ""

questions = [
    {"question": "Probability of rolling a 4?", "answer": [4]},
    {"question": "Probability of rolling an even number?", "answer": [2,4,6]},
    {"question": "Probability of rolling >3?", "answer": [4,5,6]},
    {"question": "Probability of rolling a 1 or 2?", "answer": [1,2]},
    {"question": "Probability of rolling less than 5?", "answer": [1,2,3,4]},
    {"question": "Probability of rolling a 3?", "answer": [3]},
    {"question": "Probability of rolling an odd number?", "answer": [1,3,5]},
    {"question": "Probability of rolling a number divisible by 3?", "answer": [3,6]},
    {"question": "Probability of rolling 5 or 6?", "answer": [5,6]},
    {"question": "Probability of rolling exactly 2 dice to sum 7?", "answer": ["sum7"]}  # optional multi-dice
]

# --- Functions ---
def roll_dice():
    return random.randint(1,6)

def check_answer(roll, correct_values):
    if "sum7" in correct_values:  # placeholder for future multi-dice
        return True
    return roll in correct_values

def draw_background():
    screen.fill((30, 30, 30))
    for x in range(0, SCREEN_WIDTH, 64):
        pygame.draw.line(screen, (50,50,50), (x,0), (x,SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, 64):
        pygame.draw.line(screen, (50,50,50), (0,y), (SCREEN_WIDTH,y))

def game_over_screen():
    global score, current_question_index, rolling, message
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Restart game
                score = 0
                current_question_index = 0
                rolling = False
                message = ""
                return

        draw_background()
        over_surf = FONT.render(f"GAME OVER! Final Score: {score}", True, (255, 215, 0))
        restart_surf = FONT.render("Press R to Restart", True, (0,255,255))
        screen.blit(over_surf, (SCREEN_WIDTH//2 - over_surf.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(restart_surf, (SCREEN_WIDTH//2 - restart_surf.get_width()//2, SCREEN_HEIGHT//2 + 20))
        pygame.display.update()
        clock.tick(FPS)

# --- Main Game Loop ---
running = True
while running:
    dt = clock.tick(FPS)/1000
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not rolling:
                rolling = True
                roll_anim_index = 0

    # --- Animate Dice Roll ---
    if rolling:
        screen.blit(dice_frames[int(roll_anim_index)], (SCREEN_WIDTH//2 - 64, SCREEN_HEIGHT//2 - 64))
        roll_anim_index += 0.6
        if roll_anim_index >= len(dice_frames):
            rolling = False
            current_roll = roll_dice()
            if check_answer(current_roll, questions[current_question_index]["answer"]):
                message = "Correct!"
                score += 1
            else:
                message = f"Wrong! Rolled {current_roll}"
            current_question_index += 1
            if current_question_index >= len(questions):
                game_over_screen()
    else:
        if current_roll:
            dice_img = dice_frames[-1]  # show last frame after rolling
            screen.blit(dice_img, (SCREEN_WIDTH//2 - 64, SCREEN_HEIGHT//2 - 64))

    # --- Draw Question ---
    if current_question_index < len(questions):
        q_surf = FONT.render(questions[current_question_index]["question"], True, (255,255,255))
        screen.blit(q_surf, (20, 30))

    # --- Draw Score ---
    score_surf = FONT.render(f"Score: {score}", True, (0,255,0))
    screen.blit(score_surf, (SCREEN_WIDTH - 150, 90))

    # --- Draw Message ---
    if message:
        msg_surf = FONT.render(message, True, (255, 200, 0))
        screen.blit(msg_surf, (SCREEN_WIDTH//2 - msg_surf.get_width()//2, SCREEN_HEIGHT - 50))

    pygame.display.update()
