import pygame
import random
from settings import (HEIGHT, WIDTH, ENEMY_SHIP_GREEN, ENEMY_SHIP_RED, ENEMY_SHIP_BLUE, LASER_GREEN, LASER_RED, LASER_BLUE, LASER_ORANGE, PLAYER_SHIP_ORANGE)

def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

class Laser:
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self, window):
		window.blit(self.img, (self.x, self.y))

	def move(self, velocity):
		self.y += velocity

	def off_screen(self, screen_height):
		return not(self.y <= screen_height and self.y >= 0)

	def collision(self, obj):
		return collide(self, obj)

class Ship:
	COOLDOWN = 20

	def __init__(self, x, y, health=100):
		self.x = x
		self.y = y
		self.health = health
		self.ship_img = None
		self.laser_img = None
		self.lasers = []
		self.cool_down_counter = 0
		self.hit_timer = 0

	def draw_hit_effect(self, window):
		if self.hit_timer > 0: # 12 frames tak count
			flash_surface = self.ship_img.copy()
			flash_surface.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
			window.blit(flash_surface, (self.x, self.y))

	def draw(self, window):
		window.blit(self.ship_img, (self.x, self.y))
		self.draw_hit_effect(window)
		for laser in self.lasers:
			laser.draw(window)

	def move_lasers(self, velocity, obj):
		self.cooldown()
		for laser in self.lasers[:]:
			laser.move(velocity)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			elif laser.collision(obj):
				if self.health > 20:
					obj.health -= 20
				elif self.health > 10:
					obj.health -= 15
				else:
					obj.health -= 10
				obj.hit_timer = 12
				if hasattr(obj, 'was_hit'):
					obj.was_hit = True
				self.lasers.remove(laser)

	def cooldown(self):
		if self.cool_down_counter >= self.COOLDOWN:
			self.cool_down_counter = 0
		elif self.cool_down_counter > 0:
			self.cool_down_counter += 1 # counts till 20 frames

	def shoot(self):
		if self.cool_down_counter == 0:
			laser_x_position = self.x + self.ship_img.get_width() // 2 - self.laser_img.get_width() // 2
			laser = Laser(laser_x_position, self.y, self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter = 1
			return True
		return False

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()


class Player(Ship):
	MAX_TILT   = 10
	TILT_SPEED = 10
	TILT_DECAY = 10

	def __init__(self, x, y, health=100):
		super().__init__(x, y, health)
		self.ship_img     = PLAYER_SHIP_ORANGE
		self.laser_img    = LASER_RED
		self.mask         = pygame.mask.from_surface(self.ship_img)
		self.max_health   = health
		self.score_earned = 0
		self.was_hit      = False
		self.tilt         = 0
		self.moving_left  = False
		self.moving_right = False

	def move(self):
		if self.hit_timer > 0:
			self.hit_timer -= 1

		if self.moving_right:
			self.tilt = min(self.tilt + self.TILT_SPEED, self.MAX_TILT)
		elif self.moving_left:
			self.tilt = max(self.tilt - self.TILT_SPEED, -self.MAX_TILT)
		else:
			if self.tilt > 0:
				self.tilt = max(0, self.tilt - self.TILT_DECAY)
			elif self.tilt < 0:
				self.tilt = min(0, self.tilt + self.TILT_DECAY)

	def collect_score(self):
		points_earned = self.score_earned
		self.score_earned = 0
		return points_earned

	def check_hit_enemy_laser(self, player_laser, enemy_list):
		for enemy in enemy_list:
			for enemy_laser in enemy.lasers[:]:
				if player_laser.collision(enemy_laser):
					enemy.lasers.remove(enemy_laser)
					return True
		return False

	def check_hit_enemy_ship(self, player_laser, enemy_list):
		for enemy in enemy_list:
			if player_laser.collision(enemy):
				enemy.health -= 10
				enemy.hit_timer = 4
				enemy._update_phase()
				if enemy.health <= 0:
					enemy.dying = True
					self.score_earned += enemy.score_value
				return True
		return False

	def move_lasers(self, velocity, enemy_list):
		self.cooldown()
		for laser in self.lasers[:]:
			laser.move(velocity)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			else:
				if self.check_hit_enemy_laser(laser, enemy_list):
					if laser in self.lasers:
						self.lasers.remove(laser)
					continue
				if self.check_hit_enemy_ship(laser, enemy_list):
					if laser in self.lasers:
						self.lasers.remove(laser)

	def healthbar(self, window):
		bar_width  = 150
		bar_height = 22
		bar_x      = self.x + self.ship_img.get_width() // 2 - bar_width // 2
		bar_y      = self.y + self.ship_img.get_height() + 10

		pygame.draw.rect(window, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=15)

		current_health  = max(0, self.health)
		green_fill_width = int(bar_width * (current_health / self.max_health))
		right_radius    = 15 if green_fill_width == bar_width else 0
		if green_fill_width > 0:
			pygame.draw.rect(window, (0, 255, 0), (bar_x, bar_y, green_fill_width, bar_height),
				border_top_left_radius=15, border_bottom_left_radius=15,
				border_top_right_radius=right_radius, border_bottom_right_radius=right_radius)

		health_percentage = int((current_health / self.max_health) * 100)
		health_font       = pygame.font.SysFont("comicsans", 18, bold=True)
		health_label      = health_font.render(str(health_percentage) + "%", 1, (255, 255, 255))
		window.blit(health_label, (bar_x + bar_width // 2 - health_label.get_width() // 2, bar_y + bar_height // 2 - health_label.get_height() // 2))

	def draw(self, window):
		tilted_ship_image = pygame.transform.rotate(self.ship_img, -self.tilt)

		original_center_x = self.x + self.ship_img.get_width()  // 2
		original_center_y = self.y + self.ship_img.get_height() // 2
		draw_x            = original_center_x - tilted_ship_image.get_width()  // 2
		draw_y            = original_center_y - tilted_ship_image.get_height() // 2

		window.blit(tilted_ship_image, (draw_x, draw_y))

		if self.hit_timer > 0:
			flash_surface = tilted_ship_image.copy()
			flash_surface.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
			window.blit(flash_surface, (draw_x, draw_y))

		for laser in self.lasers:
			laser.draw(window)

		self.healthbar(window)


class Enemy(Ship):
	def __init__(self, x, y, target_y, h_speed, shoot_chance):
		super().__init__(x, y, health=30)
		self.target_y          = target_y
		self.horizontal_speed  = h_speed
		self.horizontal_dir    = random.choice([-1, 1])
		self.dying             = False
		self.score_value       = self.health
		self.cool_down_counter = random.randint(1, 60)
		self.shoot_chance      = shoot_chance
		self.settled           = False
		self._update_phase()

	def _update_phase(self):
		if self.health > 20:
			self.ship_img  = ENEMY_SHIP_GREEN
			self.laser_img = LASER_GREEN
		elif self.health > 10:
			self.ship_img  = ENEMY_SHIP_RED
			self.laser_img = LASER_ORANGE
		else:
			self.ship_img  = ENEMY_SHIP_BLUE
			self.laser_img = LASER_BLUE
		self.mask = pygame.mask.from_surface(self.ship_img)

	def move(self):
		if self.hit_timer > 0:
			self.hit_timer -= 1

		if not self.settled:
			if self.y < self.target_y:
				self.y += 3
			else:
				self.settled = True
			return

		self.x += self.horizontal_speed * self.horizontal_dir
		if self.x <= 24:
			self.x = 24
			self.horizontal_dir = 1
		elif self.x >= WIDTH - self.get_width() - 24:
			self.x = WIDTH - self.get_width() - 24
			self.horizontal_dir = -1

	def shoot(self):
		if self.settled and self.cool_down_counter == 0:
			laser_x_position = self.x + self.ship_img.get_width() // 2 - self.laser_img.get_width() // 2
			laser = Laser(
				laser_x_position,
				self.y + self.ship_img.get_height(),
				self.laser_img
			)
			self.lasers.append(laser)
			self.cool_down_counter = 1
			return True
		return False