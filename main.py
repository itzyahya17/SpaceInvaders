import pygame
import random
import os
pygame.font.init()
pygame.mixer.init()

from settings import WIDTH, HEIGHT, WIN, BACKGROUND as BG, BASE_DIR
from ships import Player, Enemy, collide
from levels import LEVEL_SPAWNERS, LEVEL_INFO, MAX_LEVEL

shoot_sound     = pygame.mixer.Sound(os.path.join(BASE_DIR, "sounds", "shoot.ogg"))
explosion_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "sounds", "explosion.ogg"))
hit_sound       = pygame.mixer.Sound(os.path.join(BASE_DIR, "sounds", "hit.ogg"))
level_up_sound  = pygame.mixer.Sound(os.path.join(BASE_DIR, "sounds", "level_up.ogg"))
game_over_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "sounds", "game_over.ogg"))

shoot_sound.set_volume(0.4)
explosion_sound.set_volume(0.6)
hit_sound.set_volume(0.7)
level_up_sound.set_volume(0.8)
game_over_sound.set_volume(0.8)

HIGHSCORE_FILE = os.path.join(BASE_DIR, "highscore.txt")

def load_high_score():
	if os.path.exists(HIGHSCORE_FILE):
		with open(HIGHSCORE_FILE, "r") as f:
			try:
				return int(f.read())
			except:
				return 0
	return 0

def save_high_score(score):
	with open(HIGHSCORE_FILE, "w") as f:
		f.write(str(score))

def draw_scrolling_bg(background_y, speed=1): #background animation trick
	WIN.blit(BG, (0, background_y))
	WIN.blit(BG, (0, background_y - HEIGHT))
	background_y += speed
	if background_y >= HEIGHT:
		background_y = 0
	return background_y

def draw_screen(title, subtitle, prompt, color1=(0, 255, 0), color2=(255, 255, 0)):
	title_font  = pygame.font.SysFont("comicsans", 70, bold=True)
	sub_font    = pygame.font.SysFont("comicsans", 40)
	prompt_font = pygame.font.SysFont("comicsans", 35)
	WIN.blit(BG, (0, 0))
	title_surface  = title_font.render(title,    1, color1)
	sub_surface    = sub_font.render(subtitle,   1, color2)
	prompt_surface = prompt_font.render(prompt,  1, (255, 255, 255))
	WIN.blit(title_surface,  (WIDTH // 2 - title_surface.get_width()  // 2, HEIGHT // 2 - 110))
	WIN.blit(sub_surface,    (WIDTH // 2 - sub_surface.get_width()    // 2, HEIGHT // 2 - 20))
	WIN.blit(prompt_surface, (WIDTH // 2 - prompt_surface.get_width() // 2, HEIGHT // 2 + 60))
	pygame.display.update()

def level_intro_screen(level):
	clock = pygame.time.Clock()
	title_text, info_text = LEVEL_INFO[level]
	while True:
		draw_screen(title_text, info_text, "Press Enter to Start", (0, 255, 0), (255, 255, 0))
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return

def level_complete_screen(level):
	clock = pygame.time.Clock()
	level_up_sound.play()
	while True:
		draw_screen(
			f"Level {level} Complete!",
			f"Press Enter for Level {level + 1}",
			"Get ready...",
			(0, 255, 0), (255, 255, 255)
		)
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return

def game_over_screen(score):
	clock      = pygame.time.Clock()
	high_score = load_high_score()
	new_record = score > high_score
	if new_record:
		save_high_score(score)
		high_score = score

	title_font  = pygame.font.SysFont("comicsans", 70, bold=True)
	score_font  = pygame.font.SysFont("comicsans", 45)
	record_font = pygame.font.SysFont("comicsans", 36, bold=True)
	prompt_font = pygame.font.SysFont("comicsans", 32)
	background_y = 0

	while True:
		background_y = draw_scrolling_bg(background_y)

		title_surface  = title_font.render("You Lost!", 1, (255, 0, 0))
		score_surface  = score_font.render(f"Your Score:  {score}", 1, (255, 255, 0))
		high_score_surface  = score_font.render(f"High Score:  {high_score}", 1, (0, 255, 255))
		prompt_surface = prompt_font.render("ENTER - Play Again     M - Main Menu", 1, (255, 255, 255))

		WIN.blit(title_surface,      (WIDTH // 2 - title_surface.get_width()      // 2, HEIGHT // 2 - 215))
		WIN.blit(score_surface,      (WIDTH // 2 - score_surface.get_width()      // 2, HEIGHT // 2 - 70))
		WIN.blit(high_score_surface, (WIDTH // 2 - high_score_surface.get_width() // 2, HEIGHT // 2 - 10))

		if new_record:
			record_surface = record_font.render("New High Score!", 1, (255, 215, 0)) # gold colour
			WIN.blit(record_surface, (WIDTH // 2 - record_surface.get_width() // 2, HEIGHT // 2 + 55))

		WIN.blit(prompt_surface, (WIDTH // 2 - prompt_surface.get_width() // 2, HEIGHT // 2 + 110))

		pygame.display.update()
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return "play"
				if event.key == pygame.K_m:
					return "menu"

def you_won_screen(score):
	clock      = pygame.time.Clock()
	high_score = load_high_score()
	new_record = score > high_score
	if new_record:
		save_high_score(score)
		high_score = score

	level_up_sound.play()

	title_font  = pygame.font.SysFont("comicsans", 80, bold=True)
	label_font  = pygame.font.SysFont("comicsans", 38)
	value_font  = pygame.font.SysFont("comicsans", 38, bold=True)
	prompt_font = pygame.font.SysFont("comicsans", 30)
	background_y = 0

	y_title  = HEIGHT // 2 - 220
	y_line1  = HEIGHT // 2 - 110
	y_score  = HEIGHT // 2 - 110
	y_best   = HEIGHT // 2 - 55
	y_line2  = HEIGHT // 2 - 0
	y_record = HEIGHT // 2 + 20
	y_prompt = HEIGHT // 2 + 90

	while True:
		background_y = draw_scrolling_bg(background_y)

		title_surface = title_font.render("You Won!", 1, (255, 215, 0))
		WIN.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, y_title))

		pygame.draw.line(WIN, (255, 255, 255), (WIDTH // 2 - 200, y_line1), (WIDTH // 2 + 200, y_line1), 2)

		score_label_surface = label_font.render("Score", 1, (180, 180, 180))
		score_value_surface = value_font.render(str(score), 1, (255, 255, 255))
		WIN.blit(score_label_surface, (WIDTH // 2 - 180, y_score))
		WIN.blit(score_value_surface, (WIDTH // 2 + 180 - score_value_surface.get_width(), y_score))

		best_label_surface = label_font.render("Best", 1, (180, 180, 180))
		best_value_surface = value_font.render(str(high_score), 1, (0, 220, 255))
		WIN.blit(best_label_surface, (WIDTH // 2 - 180, y_best))
		WIN.blit(best_value_surface, (WIDTH // 2 + 180 - best_value_surface.get_width(), y_best))

		pygame.draw.line(WIN, (255, 255, 255), (WIDTH // 2 - 200, y_line2), (WIDTH // 2 + 200, y_line2), 2)

		if new_record:
			record_surface = label_font.render("New Record!", 1, (255, 215, 0))
			WIN.blit(record_surface, (WIDTH // 2 - record_surface.get_width() // 2, y_record))

		prompt_surface = prompt_font.render("ENTER  -  Play Again          M  -  Main Menu", 1, (200, 200, 200))
		WIN.blit(prompt_surface, (WIDTH // 2 - prompt_surface.get_width() // 2, y_prompt))

		pygame.display.update()
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return "play"
				if event.key == pygame.K_m:
					return "menu"

def main():
	FPS              = 90
	level            = 1
	score            = 0
	background_y     = 0
	laser_velocity   = 10
	player_velocity  = 9
	enemies          = []
	lost             = False
	game_over_frame_count = 0
	game_over_played = False
	paused           = False

	LEVEL_HP = {1: 100, 2: 120, 3: 150, 4: 180, 5: 220}

	main_font       = pygame.font.SysFont("comicsans", 50)
	high_score_font = pygame.font.SysFont("comicsans", 28)

	player = Player(600, HEIGHT - 150, health=LEVEL_HP[1])
	clock  = pygame.time.Clock()

	level_intro_screen(level)
	LEVEL_SPAWNERS[level](enemies)

	def redraw_window():
		nonlocal background_y
		bg_speed = 1 + (level - 1) * 0.3
		new_background_y = draw_scrolling_bg(background_y, bg_speed)
		return new_background_y

	while True:
		clock.tick(FPS)

		if not paused:
			background_y = redraw_window()

			enemies_label   = main_font.render(f"Enemies: {len(enemies)}", 1, (255, 0, 0))
			level_label     = main_font.render(f"Level: {level}",          1, (0, 255, 0))
			score_label     = main_font.render(f"Score: {score}",          1, (255, 255, 0))
			high_score_label = high_score_font.render(f"High Score: {load_high_score()}", 1, (180, 180, 180))

			WIN.blit(enemies_label,   (10, 10))
			WIN.blit(level_label,     (WIDTH - level_label.get_width() - 10, 10))
			WIN.blit(score_label,     (WIDTH // 2 - score_label.get_width() // 2, 10))
			WIN.blit(high_score_label,(10, HEIGHT - 45))

			for enemy in enemies:
				enemy.draw(WIN)
			player.draw(WIN)

			pygame.display.update()

		if player.health <= 0:
			player.health = 0
			lost = True
			game_over_frame_count += 1
			if not game_over_played:
				game_over_sound.play()
				game_over_played = True

		if game_over_frame_count > 5:
			return game_over_screen(score)

		if len(enemies) == 0 and not lost:
			if level >= MAX_LEVEL:
				return you_won_screen(score)
			else:
				level_complete_screen(level)
				level += 1
				new_level_health      = LEVEL_HP.get(level, 220)
				player.health         = new_level_health
				player.max_health     = new_level_health
				enemies.clear()
				player.lasers.clear()
				level_intro_screen(level)
				LEVEL_SPAWNERS[level](enemies)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE and not lost:
					paused = not paused
				if paused:
					if event.key == pygame.K_RETURN:
						paused = False
					if event.key == pygame.K_m:
						return "menu"

		if paused:
			pause_font   = pygame.font.SysFont("comicsans", 60, bold=True)
			options_font = pygame.font.SysFont("comicsans", 38)
			pause_label  = pause_font.render("PAUSED",          1, (255, 255, 0))
			resume_label = options_font.render("ENTER  -  Resume",  1, (255, 255, 255))
			menu_label   = options_font.render("M  -  Main Menu",   1, (255, 255, 255))

			overlay = pygame.Surface((500, 220), pygame.SRCALPHA)
			overlay.fill((0, 0, 0, 180))
			WIN.blit(overlay,       (WIDTH // 2 - 250,                         HEIGHT // 2 - 110))
			WIN.blit(pause_label,   (WIDTH // 2 - pause_label.get_width()  // 2, HEIGHT // 2 - 90))
			WIN.blit(resume_label,  (WIDTH // 2 - resume_label.get_width() // 2, HEIGHT // 2 - 10))
			WIN.blit(menu_label,    (WIDTH // 2 - menu_label.get_width()   // 2, HEIGHT // 2 + 50))
			pygame.display.update()
			clock.tick(60)
			continue

		pressed_keys = pygame.key.get_pressed()
		if not lost:
			player.moving_left  = False
			player.moving_right = False
			if pressed_keys[pygame.K_LEFT]  and player.x - player_velocity > 24:
				player.x -= player_velocity
				player.moving_left = True
			if pressed_keys[pygame.K_RIGHT] and player.x + player_velocity + player.get_width() < WIDTH - 24:
				player.x += player_velocity
				player.moving_right = True
			if pressed_keys[pygame.K_UP]   and player.y - player_velocity > 0:
				player.y -= player_velocity
			if pressed_keys[pygame.K_DOWN] and player.y + player_velocity + player.get_height() + 70 < HEIGHT:
				player.y += player_velocity
			if pressed_keys[pygame.K_SPACE]:
				if player.shoot():
					shoot_sound.play()
			player.move()

		for enemy in enemies[:]:
			enemy.move()
			enemy.move_lasers(laser_velocity, player)

			if enemy.settled and enemy.shoot_chance > 0:
				if random.randrange(0, enemy.shoot_chance) == 1:
					enemy.shoot()

			if enemy.dying and enemy.hit_timer <= 0:
				enemies.remove(enemy)
				explosion_sound.play()
				continue

			if collide(enemy, player):
				player.health -= 20
				player.hit_timer = 12
				hit_sound.play()
				enemies.remove(enemy)

		score += player.collect_score()
		player.move_lasers(-laser_velocity, enemies)

		if player.was_hit:
			hit_sound.play()
			player.was_hit = False

def main_menu():
	title_font  = pygame.font.SysFont("comicsans", 42, bold=True)
	game_font   = pygame.font.SysFont("comicsans", 80, bold=True)
	prompt_font = pygame.font.SysFont("comicsans", 45)
	credit_font = pygame.font.SysFont("comicsans", 28)
	background_y = 0

	from settings import ENEMY_SHIP_GREEN, ENEMY_SHIP_RED, ENEMY_SHIP_BLUE, PLAYER_SHIP_ORANGE
	menu_enemies = [
		{"img": ENEMY_SHIP_GREEN, "x": 100,  "y": 80,  "speed": 1.2, "dir": 1},
		{"img": ENEMY_SHIP_RED,   "x": 400,  "y": 160, "speed": 0.9, "dir": -1},
		{"img": ENEMY_SHIP_BLUE,  "x": 800,  "y": 60,  "speed": 1.5, "dir": 1},
		{"img": ENEMY_SHIP_GREEN, "x": 1000, "y": 200, "speed": 1.0, "dir": -1},
		{"img": ENEMY_SHIP_RED,   "x": 600,  "y": 130, "speed": 0.7, "dir": 1},
	]
	player_demo = {"x": WIDTH // 2, "y": HEIGHT - 120, "dir": 1, "speed": 0.8}

	while True:
		background_y = draw_scrolling_bg(background_y)

		for menu_enemy in menu_enemies:
			menu_enemy["x"] += menu_enemy["speed"] * menu_enemy["dir"]
			if menu_enemy["x"] > WIDTH + 50:
				menu_enemy["x"] = -50
			elif menu_enemy["x"] < -50:
				menu_enemy["x"] = WIDTH + 50
			WIN.blit(menu_enemy["img"], (menu_enemy["x"], menu_enemy["y"]))

		player_demo["x"] += player_demo["speed"] * player_demo["dir"]
		if player_demo["x"] > WIDTH - 80:
			player_demo["dir"] = -1
		elif player_demo["x"] < 80:
			player_demo["dir"] = 1
		WIN.blit(PLAYER_SHIP_ORANGE, (player_demo["x"], player_demo["y"]))

		lab_label    = title_font.render("AoICT Lab Project",            1, (0, 200, 120))
		game_label   = game_font.render("Space Invader",                 1, (0, 255, 255))
		prompt_label = prompt_font.render("Press Enter to Start...",     1, (255, 255, 255))
		reset_label  = credit_font.render("Press R to Reset High Score", 1, (255, 0, 0))
		name_label   = credit_font.render("Made by: Muhammad Yahya",     1, (255, 215, 0))
		class_label  = credit_font.render("BCS 1-B",                     1, (255, 215, 0))
		high_score_label = credit_font.render(f"High Score: {load_high_score()}", 1, (180, 180, 180))

		WIN.blit(lab_label,       (WIDTH // 2 - lab_label.get_width()       // 2, HEIGHT // 2 - 220))
		WIN.blit(game_label,      (WIDTH // 2 - game_label.get_width()      // 2, HEIGHT // 2 - 130))
		WIN.blit(prompt_label,    (WIDTH // 2 - prompt_label.get_width()    // 2, HEIGHT // 2 + 20))
		WIN.blit(reset_label,     (WIDTH // 2 - reset_label.get_width()     // 2, HEIGHT // 2 + 80))
		WIN.blit(name_label,      (WIDTH - name_label.get_width()  - 20,          HEIGHT - 85))
		WIN.blit(class_label,     (WIDTH - class_label.get_width() - 20,          HEIGHT - 55))
		WIN.blit(high_score_label,(20, HEIGHT - 55))

		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					result = main()
					if result == "menu":
						continue
				if event.key == pygame.K_r:
					save_high_score(0)

main_menu()