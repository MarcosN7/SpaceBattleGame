import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load background music
pygame.mixer.music.load("backgroundneon.mp3") 

# Load laser sound effect
laser_sound = pygame.mixer.Sound("laser.mp3") 


# Set up the game window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Invaders")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Menu variables
menu_active = True
player_name = ""
scoreboard = []

# Background
background_image = pygame.image.load("background.jpg")  # Replace with your space background image
background_image = pygame.transform.scale(background_image, (window_width, window_height))
background_y = -window_height
background_speed = 2

# Player spaceship
player_width, player_height = 64, 64
player_image = pygame.image.load("spaceship.png")  # Replace with your spaceship image
player_image = pygame.transform.scale(player_image, (player_width, player_height))
player_x = window_width // 2 - player_width // 2
player_y = window_height - player_height - 10
player_speed = 8

#laser
last_bullet_time = pygame.time.get_ticks()


#Meteors
meteor_width, meteor_height = 50, 50
meteor_image = pygame.image.load("meteor.png")  
meteor_image = pygame.transform.scale(meteor_image, (meteor_width, meteor_height))
meteor_x = []
meteor_y = []
meteor_speed = []
max_meteors_per_level = 10  # Adjust the maximum number of meteors per level as desired
num_meteors = 6  # Adjust the number of meteors as desired
for i in range(num_meteors):
    meteor_x.append(random.randint(0, window_width - meteor_width))
    meteor_y.append(random.randint(-300, -meteor_height))
    meteor_speed.append(random.randint(1, 3))


# Enemy aliens
enemy_width, enemy_height = 48, 48
enemy_image = pygame.image.load("enemy.png") 
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
enemy_x = []
enemy_y = []
enemy_speed = []
num_enemies = 6
for i in range(num_enemies):
    enemy_x.append(random.randint(0, window_width - enemy_width))
    enemy_y.append(random.randint(50, 200))
    enemy_speed.append(2)

# Explosion Animation
explosion_image = pygame.image.load("explosion.gif")
explosion_image = pygame.transform.scale(explosion_image, (enemy_width, enemy_height))
explosion_duration = 3.5  # Duration of explosion animation in seconds
explosion_x = 0
explosion_y = 0
explosion_active = False

# Bullets
bullet_width, bullet_height = 8, 24
bullet_image = pygame.Surface((bullet_width, bullet_height))
bullet_image.fill(white)
bullet_x = 0
bullet_y = player_y
bullet_speed = 10
bullet_state = "ready"  # "ready" - ready to be fired, "fired" - bullet is moving

# Game variables
score = 0
level = 1

# Play background music
pygame.mixer.music.play(-1)  # "-1" indicates infinite loop

# Set background music volume
pygame.mixer.music.set_volume(0.5)  # Adjust the volume level (0.0 to 1.0)

#laser sound
pygame.mixer.init()
laser_sound = pygame.mixer.Sound("laser.mp3") 

# Menu variables
menu_active = True
player_name = ""
scoreboard = []

# Menu loop
while menu_active:
    # Handle menu events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and player_name != "":
                menu_active = False
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                player_name += event.unicode

    # Draw the menu
    window.fill(black)
    font = pygame.font.Font(None, 36)
    title_text = font.render("Space Invaders", True, white)
    name_text = font.render("Enter Your Name:", True, white)
    player_text = font.render(player_name, True, white)
    prompt_text = font.render("Press Enter to Start", True, white)
    window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 200))
    window.blit(name_text, (window_width // 2 - name_text.get_width() // 2, 300))
    window.blit(player_text, (window_width // 2 - player_text.get_width() // 2, 350))
    window.blit(prompt_text, (window_width // 2 - prompt_text.get_width() // 2, 450))
    pygame.display.update()


# Game loop
running = True
clock = pygame.time.Clock()
def player_movement(direction):
    global player_x
    if direction == "left":
        player_x -= player_speed
    elif direction == "right":
        player_x += player_speed


def fire_bullet():
    global bullet_state, bullet_x, bullet_y, last_bullet_time
    current_time = pygame.time.get_ticks()
    if current_time - last_bullet_time >= 100:  # Adjust the delay between shots (in milliseconds)
        bullet_state = "fired"
        bullet_x = player_x + player_width // 2 - bullet_width // 2
        bullet_y = player_y
        last_bullet_time = current_time
        laser_sound.play()  # Play the laser sound effect


def draw_player():
    window.blit(player_image, (player_x, player_y))

def draw_enemy(x, y):
    window.blit(enemy_image, (x, y))

def draw_bullet(x, y):
    pygame.draw.rect(window, white, (x, y, bullet_width, bullet_height))


def collision_detection(enemy_x, enemy_y, bullet_x, bullet_y):
    if bullet_y < enemy_y + enemy_height and bullet_y + bullet_height > enemy_y:
        if bullet_x < enemy_x + enemy_width and bullet_x + bullet_width > enemy_x:
            return True
    return False


def start_explosion(x, y):
    global explosion_x, explosion_y, explosion_active
    explosion_x = x - (enemy_width // 2)
    explosion_y = y - (enemy_height // 2)
    explosion_active = True

def draw_explosion():
    if explosion_active:
        window.blit(explosion_image, (explosion_x, explosion_y))

def draw_meteor(x, y):
    window.blit(meteor_image, (x, y))

def check_collision_meteor(player_x, player_y, meteor_x, meteor_y):
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    meteor_rect = pygame.Rect(meteor_x, meteor_y, meteor_width, meteor_height)
    return player_rect.colliderect(meteor_rect)

def update_meteors():
    global running, num_meteors, level
    for i in range(num_meteors):
        meteor_y[i] += meteor_speed[i]
        if meteor_y[i] > window_height:
            meteor_x[i] = random.randint(0, window_width - meteor_width)
            meteor_y[i] = random.randint(-600, -meteor_height)
            meteor_speed[i] = random.uniform(1, 3)

        if check_collision_meteor(player_x, player_y, meteor_x[i], meteor_y[i]):
            game_over()
            running = False

    # Increase level and add more meteors
    if level < 10 and score >= level * 100:
        level += 1
        num_meteors = min(max_meteors_per_level, num_meteors + 1)
        for i in range(num_meteors - 6):  # Adjust the starting number of meteors accordingly
            meteor_x.append(random.randint(0, window_width - meteor_width))
            meteor_y.append(random.randint(-600, -meteor_height))
            meteor_speed.append(random.uniform(1, 3))


def draw_meteors():
    for i in range(num_meteors):
        draw_meteor(meteor_x[i], meteor_y[i])


def game_over():
    global running
    font = pygame.font.Font(None, 64)
    text = font.render("Game Over", True, white)
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)
    running = False

def draw_score_level():
    font = pygame.font.Font(None, 24)
    score_text = font.render("Score: " + str(score), True, white)
    level_text = font.render("Level: " + str(level), True, white)
    window.blit(score_text, (10, 10))
    window.blit(level_text, (window_width - level_text.get_width() - 10, 10))

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_movement("left")
            elif event.key == pygame.K_RIGHT:
                player_movement("right")
            elif event.key == pygame.K_SPACE and bullet_state == "ready":
                fire_bullet()


    # Update player position
    if player_x < 0:
        player_x = 0
    elif player_x > window_width - player_width:
        player_x = window_width - player_width

    # Update enemy positions and check collisions
    for i in range(num_enemies):
        # Game over condition
        if enemy_y[i] > player_y:
            game_over()
            break

        enemy_x[i] += enemy_speed[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= window_width - enemy_width:
            enemy_speed[i] *= -1
            enemy_y[i] += 20

        if collision_detection(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            score += 10
            start_explosion(enemy_x[i], enemy_y[i])
            enemy_x[i] = random.randint(0, window_width - enemy_width)
            enemy_y[i] = random.randint(50, 200)
            bullet_state = "ready"

    # Update bullet position
    if bullet_state == "fired":
        bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_state = "ready"

    # Update meteor positions and check collisions
    update_meteors()

    # Update background position
    background_y += background_speed
    if background_y >= 0:
        background_y = -window_height

    # Draw background
    window.blit(background_image, (0, background_y))
    window.blit(background_image, (0, background_y + window_height))

    # Draw game objects
    draw_player()
    for i in range(num_enemies):
        draw_enemy(enemy_x[i], enemy_y[i])
    if bullet_state == "fired":
        draw_bullet(bullet_x, bullet_y)
    draw_explosion()
    draw_meteors()

    # Draw score and level
    draw_score_level()

    # Update the display
    pygame.display.update()

    # Increase level
    if score >= level * 100:
        level += 1
        enemy_speed.append(random.choice([-2, 2]))
        enemy_x.append(random.randint(0, window_width - enemy_width))
        enemy_y.append(random.randint(50, 200))
        num_enemies += 1

    # Set the frame rate
    clock.tick(60)
    
# Stop background music
pygame.mixer.music.stop()

# Quit the mixer module
pygame.mixer.quit()

# Quit the game
pygame.quit()
