import pygame
class Setting():
	def __init__(self):
		self.screen_color = (230,230,230)
		self.screen_width = 860
		self.screen_height = 540
		self.background_image = pygame.image.load('d:1/game2/image/40.jpg')
		#游戏是否开始
		self.game_stats = False
		self.game_stop = False
		
		self.bat_speed = 6 #板子初始化时的速度
		self.bat_speed_change = 2 #板子速度改变时的加速度
		self.bat_speed_max = 12 #板子的最大速度
		
		self.ball_speed = 2 #球初始化时的速度
		self.ball_speed_change = 1 #球速度改变时的加速度
		self.ball_speed_max = 4 #球的最大速度
		
		self.score = 0
		self.max_score = 0
		self.total_score = 0
		
		self.reward_num = 3
		self.reward_display = 5 #奖励出现概率 %
		self.reward_type1_limit_time = 1000
		self.reward_type2_limit_time = 2000
		self.reward_type3_limit_time = 2000