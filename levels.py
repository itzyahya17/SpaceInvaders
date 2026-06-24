import random
from settings import WIDTH
from ships import Enemy

def make_enemy(x_pos, y_pos, target_y, horizontal_speed, shoot_chance, health):
	new_enemy = Enemy(x_pos, y_pos, target_y=target_y, h_speed=horizontal_speed, shoot_chance=shoot_chance)
	new_enemy.health = health
	new_enemy.score_value = health  # 10hp=10pts, 20hp=20pts, 30hp=30pts
	new_enemy._update_phase()
	return new_enemy

# 1 row (blue)
def spawn_level_1(enemies):
	positions = [100, 260, 430, 600, 770, 940]
	for x_pos in positions:
		enemies.append(make_enemy(x_pos, -120, target_y=100, horizontal_speed=0.5, shoot_chance=100, health=10))

# 2 row (red, blue)
def spawn_level_2(enemies):
	front_row = [150, 370, 590, 810, 1030]
	back_row  = [260, 480, 700, 920]
	for x_pos in front_row:
		enemies.append(make_enemy(x_pos, -120, target_y=90, horizontal_speed=0.8, shoot_chance=110, health=20))
	for x_pos in back_row:
		enemies.append(make_enemy(x_pos, -300, target_y=200, horizontal_speed=0.8, shoot_chance=110, health=10))

# V Formation
def spawn_level_3(enemies):
	center_x = WIDTH // 2
	formation = [
		(center_x,        -80,  90,  30),
		(center_x - 190,  -170, 150, 20),
		(center_x + 190,  -170, 150, 20),
		(center_x - 370,  -270, 220, 10),
		(center_x + 370,  -270, 220, 10),
		(center_x - 550,  -370, 300, 30),
		(center_x + 550,  -370, 300, 30),
	]
	for x_pos, start_y, target_y, health in formation:
		enemies.append(make_enemy(x_pos, start_y, target_y=target_y, horizontal_speed=1.0, shoot_chance=90, health=health))

# 3 columns, faster
def spawn_level_4(enemies):
	column_positions = [180, WIDTH // 2, WIDTH - 180]
	column_healths   = [30, 20, 10]
	row_targets      = [90, 200, 310]
	for col_index, col_x in enumerate(column_positions):
		for row_index in range(3):
			enemies.append(make_enemy(col_x, -120 - row_index * 190, target_y=row_targets[row_index], horizontal_speed=1.3, shoot_chance=70, health=column_healths[col_index]))

# two rows + v shape (faster, higher fire probability)
def spawn_level_5(enemies):
	front_row_positions = [120, 340, 560, 780, 1000]
	front_row_healths   = [30, 20, 10, 20, 30]
	for x_pos, health in zip(front_row_positions, front_row_healths):
		enemies.append(make_enemy(x_pos, -120, target_y=80, horizontal_speed=1.6, shoot_chance=55, health=health))

	back_row_positions = [230, 450, 670, 890]
	for x_pos in back_row_positions:
		enemies.append(make_enemy(x_pos, -300, target_y=200, horizontal_speed=1.6, shoot_chance=55, health=20))

	center_x = WIDTH // 2
	v_formation = [
		(center_x,        -520, 320),
		(center_x - 210,  -640, 320),
		(center_x + 210,  -640, 320),
		(center_x - 420,  -760, 320),
		(center_x + 420,  -760, 320),
	]
	for x_pos, start_y, target_y in v_formation:
		enemies.append(make_enemy(x_pos, start_y, target_y=target_y, horizontal_speed=1.8, shoot_chance=50, health=10))

LEVEL_SPAWNERS = {
	1: spawn_level_1,
	2: spawn_level_2,
	3: spawn_level_3,
	4: spawn_level_4,
	5: spawn_level_5
}

LEVEL_INFO = {
	1: ["Level 1 - First Wave",    "Blue ships only  -  10 pts each"],
	2: ["Level 2 - Double Rows",   "Red + Blue mix  -  20 or 10 pts"],
	3: ["Level 3 - V Formation",   "All 3 colors  -  10 to 30 pts"],
	4: ["Level 4 - The Columns",   "Three columns  -  faster enemies"],
	5: ["Level 5 - Final Assault", "Everything at once  -  good luck"],
}

MAX_LEVEL = 5