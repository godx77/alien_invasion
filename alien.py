# -*- coding:utf-8 -*-

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''描述外星人的类'''
    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # 加载外星人图片
        self.image = pygame.image.load(r'alien_invasion\images\alien.bmp')
        self.rect  = self.image.get_rect()


        # 外星人暂时放在左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


        return

    def blit_alien(self):
        '''在指定位置绘制外星人'''
        self.screen.blit(self.image, self.rect)

        return

    def check_edges(self):
        '''检查单个外星人是否触及边缘，是则返回True'''
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        '''更新单个外星人的位置， 左右移动'''
        self.x += (self.ai_settings.alien_speed_factor * 
            self.ai_settings.fleet_direction)
        self.rect.x = self.x

        return

    
    
