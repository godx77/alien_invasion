# -*- coding:utf-8 -*-

class Settings():
    '''外星人入侵游戏中的所有设置的类'''
    def __init__(self):
        '''初始化所有设置'''

        # static settings
        # 屏幕设置
        self.screen_width   = 1000
        self.screen_height  = 800
        self.bg_color       = (230, 230, 230)

        # 飞船设置
        self.ship_speed_factor = 2             # 速度因子
        self.ship_limit        = 3             # 飞船个数限制

        # 子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width        = 3
        self.bullet_height       = 15
        self.bullet_color        = (60,60,60)
        self.bullet_allowed      = 7         # 允许存在的子弹数

        # 外星人设置
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed   = 70  # 下移速度


        # difficulty control factors
        self.speedup_scale = 1.1    # in which extent we wanna enhance game speed
        self.alien_points_scale = 1.5

        self.initialize_dynamic_settings()

        return

    def initialize_dynamic_settings(self):
        '''initialize dynamic settings changing during the game process'''
        self.ship_speed_factor   = 2             
        self.bullet_speed_factor = 3
        self.alien_speed_factor  = 0.5

        self.fleet_direction     = 1    # 1 represents moving right，-1 moving left

        self.alien_points        = 50   # the least scores you'll get when you shot an alien

        return

    def increase_speed(self):

        self.ship_speed_factor   *= self.speedup_scale            
        self.bullet_speed_factor *= self.speedup_scale     
        self.alien_speed_factor  *= self.speedup_scale     

        self.alien_points = int(self.alien_points * self.alien_points_scale)
        
        return

