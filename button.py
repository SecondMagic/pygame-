import pygame.font
import random
from pygame.sprite import Sprite
class Button():
	def __init__(self,msg):
		self.text_color = (255,255,255)
		self.button_color = (0,0,0)
		self.font = pygame.font.SysFont(None,48)
		self.width,self.height = 200,50
		
		self.rect = pygame.Rect(0,0,self.width,self.height)
		self.rect.center = pygame.display.get_surface().get_rect().center
		
		self.prep_msg(msg)
	def prep_msg(self,msg):
		self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
		
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center
	def draw(self):
		pygame.display.get_surface().fill(self.button_color,self.rect)
		pygame.display.get_surface().blit(self.msg_image,self.msg_image_rect)

class Brick(Sprite):
	def __init__(self):
		super().__init__()
		
		file_num=random.randint(2,4)
		if file_num == 2:
			self.image = pygame.image.load('d:1/game2/image/2.jpg')
		elif file_num == 3:
			self.image = pygame.image.load('d:1/game2/image/3.jpg')
		elif file_num == 4:
			self.image = pygame.image.load('d:1/game2/image/4.jpg')
		self.rect = self.image.get_rect()
	def change_position(self,left,top):
		self.rect.left = left
		self.rect.top = top
	def draw_brick(self):
		pygame.display.get_surface().blit(self.image,self.rect)
		
class Bat():
	def __init__(self):
		self.image = pygame.image.load('d:1/game2/image/11.jpg')
		self.rect = self.image.get_rect()
		self.dir_left = 0
		self.dir_right = 0
		
		self.rect.centerx = pygame.display.get_surface().get_rect().centerx
		self.rect.top = int(pygame.display.get_surface().get_rect().height / 6 * 5)
	def draw_bat(self):
		pygame.display.get_surface().blit(self.image,self.rect)
	def update_position(self,setting):
		if self.rect.left - setting.bat_speed*self.dir_left >= 0:
			self.rect.centerx -= setting.bat_speed*self.dir_left
		if self.rect.right + setting.bat_speed*self.dir_right <= setting.screen_width:
			self.rect.centerx += setting.bat_speed*self.dir_right
	def reset(self):
		self.dir_left = 0
		self.dir_right = 0
		self.rect.centerx = pygame.display.get_surface().get_rect().centerx
		self.rect.top = int(pygame.display.get_surface().get_rect().height / 6 * 5)
class Ball(Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('d:1/game2/image/25.jpg')
		self.rect = self.image.get_rect()
		self.dir_x = random.randrange(-1,3,2)
		self.dir_y = -1
		self.stats = 0 # 0 时才判断与板的碰撞
		
		self.rect.centerx = random.randint(pygame.display.get_surface().get_rect().centerx-200,pygame.display.get_surface().get_rect().centerx+200)
		self.rect.top = int(pygame.display.get_surface().get_rect().height / 6 * 5 - self.rect.height)
	def reset(self):
		self.dir_x = random.randrange(-1,3,2)
		self.dir_y = -1
		self.stats = 0
		
		self.rect.centerx = random.randint(pygame.display.get_surface().get_rect().centerx-200,pygame.display.get_surface().get_rect().centerx+200)
		self.rect.top = int(pygame.display.get_surface().get_rect().height / 6 * 5 - self.rect.height)
	def update_position(self,setting):
		if self.rect.left + setting.ball_speed*self.dir_x < 0:
			self.dir_x *= -1
			self.stats = 0
		elif  self.rect.right + setting.ball_speed*self.dir_x > setting.screen_width:
			self.dir_x *= -1
			self.stats = 0
		self.rect.centerx += setting.ball_speed*self.dir_x
		if self.rect.top + setting.ball_speed*self.dir_y < 0:
			self.dir_y *= -1
			self.stats = 0
		elif self.rect.bottom + setting.ball_speed*self.dir_y > setting.screen_height:
			setting.game_stats = False
			self.dir_y *= 0
			self.dir_x *= 0
			setting.max_score = setting.score
			setting.score = 0
		self.rect.top += setting.ball_speed*self.dir_y
	def draw_ball(self):
		pygame.display.get_surface().blit(self.image,self.rect)
		
class Info():
	def __init__(self,x,y):
		self.text_color = (0,0,0)
		self.bg_color = (255,255,255)
		self.font = pygame.font.SysFont(None,30)
		self.fontx = x
		self.fonty = y
		
	def get_info(self,text):
		self.image = self.font.render(text,True,self.text_color)
		self.rect = self.image.get_rect()
		
		self.rect.centerx = pygame.display.get_surface().get_rect().width - self.fontx
		self.rect.top =	pygame.display.get_surface().get_rect().height - self.fonty
	def draw_info(self):
		pygame.display.get_surface().blit(self.image,self.rect)
		
class Reward(Sprite):
	def __init__(self,centerx,top):
		super().__init__()
		self.down_speed = random.randint(1,3)
		if self.down_speed == 1 :
			self.image = pygame.image.load('d:1/game2/image/30.jpg')
		elif self.down_speed == 2 :
			self.image = pygame.image.load('d:1/game2/image/31.jpg')
		elif self.down_speed == 3 :
			self.image = pygame.image.load('d:1/game2/image/32.jpg')
		self.rect = self.image.get_rect()
		
		self.rect.centerx = centerx
		self.rect.top = top
	def update(self):
		self.rect.top += self.down_speed
	def draw_reward(self):
		pygame.display.get_surface().blit(self.image,self.rect)
	def check(self):
		if self.rect.bottom >= pygame.display.get_surface().get_rect().height:
			return True
		else :
			return False

class Buff(Sprite):
	def __init__(self,reward,setting):
		super().__init__()
		self.type = reward.down_speed
		if self.type == 1:
			self.limit_time = setting.reward_type1_limit_time
		elif self.type == 2:
			self.limit_time = setting.reward_type2_limit_time
		elif self.type == 3:
			self.limit_time = setting.reward_type3_limit_time
	def update(self):
		self.limit_time -= 1
	def check_time(self):
		if self.limit_time <= 0:
			return True
		else :
			return False
	def change_other(self,setting,balls):
		if self.type == 1:	#球加速
			setting.ball_speed -= setting.ball_speed_change
		elif self.type == 2: #板子加速
			setting.bat_speed -= setting.bat_speed_change
		elif self.type == 3: #球数量增加
			i = len(balls)
			k = 1
			for sball in balls:
				if k == i :
					balls.remove(sball)
				k += 1