import sys
import pygame
import random
from setting import Setting
from button import Button
from button import Brick
from button import Bat
from button import Ball
from button import Info
from button import Reward
from button import Buff
from pygame.sprite import Sprite
from pygame.sprite import Group
def game_run():
	setting = Setting()
	pygame.init()
	screen = pygame.display.set_mode((setting.screen_width,setting.screen_height))
	pygame.display.set_caption("Game")
	#screen.fill(setting.screen_color)
	button_start = Button('Start')
	bricks = Group()
	bat = Bat()
	ball = Ball()
	balls = Group()
	balls.add(ball)
	buffs = Group()
	info_score = Info(100,50)
	info_max_score = Info(200,50)
	info_bat_speed = Info(400,50)
	info_ball_speed = Info(600,50)
	rewards = Group()

	while True:
		screen.blit(setting.background_image,(0,0))
		event_check(setting,button_start,bricks,bat,balls,rewards,buffs)
		if setting.total_score != 0 and setting.total_score <= setting.score :
			setting.game_stats = False
			setting.max_score = setting.score
			setting.score = 0
		if setting.game_stats == False:
			button_start.draw()
		elif setting.game_stop == True:
			for brick in bricks:
				brick.draw_brick()
			for reward in rewards:
				reward.draw_reward()
			bat.draw_bat()
			for sball in balls:
				sball.draw_ball()
			button_start.draw()
			info_score.draw_info()
			info_max_score.draw_info()
			info_bat_speed.draw_info()
			info_ball_speed.draw_info()
		else :
			#板子，球，砖块，奖励位置重新计算
			for sball in balls :
				sball.update_position(setting)
			bat.update_position(setting)
			rewards.update()
			buffs.update()
			check_change(balls,bat,bricks,setting,rewards,buffs)
			info_score.get_info('scroe:'+str(setting.score))
			info_max_score.get_info('max:'+str(setting.max_score))
			info_bat_speed.get_info('bat speed:'+str(setting.bat_speed))
			info_ball_speed.get_info('ball speed:'+str(setting.ball_speed))
			
			#礼物时间计算
			for buff in buffs:
				if buff.check_time():
					buff.change_other(setting,balls)
					buffs.remove(buff)
			#板子，球，砖块，奖励绘制
			for reward in rewards:
				if reward.check() :
					rewards.remove(reward)
				else :
					reward.draw_reward()
			for brick in bricks:
				brick.draw_brick()
			bat.draw_bat()
			for sball in balls:
				sball.draw_ball()
			info_score.draw_info()
			info_max_score.draw_info()
			info_bat_speed.draw_info()
			info_ball_speed.draw_info()
		pygame.display.flip()
		
#键盘，鼠标事件
def event_check(setting,button_start,bricks,bat,balls,rewards,buffs):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				bat.dir_left=1
			elif event.key == pygame.K_d:
				bat.dir_right=1
			elif event.key == pygame.K_w:
				if (setting.bat_speed + 1) <= 10 :
					setting.bat_speed += 1
			elif event.key == pygame.K_s:
				if (setting.bat_speed - 1) >= 1 :
					setting.bat_speed = 1
			elif event.key == pygame.K_p:
				if setting.game_stats == True:
					setting.game_stop = True
			elif event.key == pygame.K_q:
				sys.exit()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				bat.dir_left=0
			elif event.key == pygame.K_d:
				bat.dir_right=0
			#elif event.key == pygame.K_w:
			#elif event.key == pygame.K_s:
			#elif event.key == pygame.K_j:
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			if button_start.rect.collidepoint(mouse_x,mouse_y) and setting.game_stats == False:
				#点击开始游戏时初始化所有组件
				setting.game_stats = True
				bricks.empty()
				rewards.empty()
				buffs.empty()
				bat.reset()
				setting.bat_speed = 6
				setting.ball_speed = 2
				setting.total_score = 0
				i = 0
				for sball in balls:
					if i == 0 :
						sball.reset()
						i = 1
					else :
						balls.remove(sball)
				
				create_brick(bricks,setting)
			if 	button_start.rect.collidepoint(mouse_x,mouse_y) and setting.game_stop == True :
				setting.game_stop = False
def create_brick(bricks,setting):
	brick = Brick()
	brick_width = brick.rect.width
	brick_height = brick.rect.height
	
	num_x=int((setting.screen_width-2*brick_width)/(brick_width+1))
	num_y=int((setting.screen_height-brick_height-setting.screen_height/2)/(brick_height+5))
	
	for y in range(num_y):
		for x in range(num_x):
			new_brick = Brick()
			new_brick.change_position(brick_width+(brick_width+1)*x,brick_height+(brick_height+5)*y)
			bricks.add(new_brick)
	setting.total_score = len(bricks)
def check_change(balls,bat,bricks,setting,rewards,buffs):
	#球与板子的碰撞检测
	for sball in balls :
		if sball.rect.colliderect(bat.rect) and sball.stats == 0:
			sball.dir_y *=-1
			sball.stats = 1
			if sball.rect.left < bat.rect.left and sball.rect.right >= bat.rect.left and sball.dir_x == 1 :
				sball.dir_x *=-1
			if sball.rect.left <= bat.rect.right and sball.rect.right > bat.rect.right and sball.dir_x == -1:
				sball.dir_x *=-1
	#球与砖块的碰撞检测
	for sball in balls :
		list_collide=pygame.sprite.spritecollide(sball,bricks,True)
		if len(list_collide) > 0:
			sball.stats = 0
			setting.score +=len(list_collide)
			sball.dir_y *=-1	
			#奖励
			for param in list_collide:
				if random.randint(1,100) <= setting.reward_display and len(rewards) < setting.reward_num: #5%概率出奖励,场上同时只能存在3个奖励
					reward = Reward(param.rect.centerx,param.rect.top)
					rewards.add(reward)
	#奖励与板子的碰撞检测
	list_reward=pygame.sprite.spritecollide(bat,rewards,True)
	for param in list_reward:
		if param.down_speed == 3 and len(balls) <3: #球数量加1
			balls.add(Ball())
			buffs.add(Buff(param,setting))
		if param.down_speed == 2 and setting.bat_speed < setting.bat_speed_max : #板子速度增加
			setting.bat_speed += setting.bat_speed_change
			buffs.add(Buff(param,setting))
		if param.down_speed == 1 and setting.ball_speed <= setting.ball_speed_max : #球速度增加
			setting.ball_speed += setting.ball_speed_change
			buffs.add(Buff(param,setting))
game_run()