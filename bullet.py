# -*- coding:utf-8 -*-

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''表示子弹并对其进行管理的类'''
    def __init__(self, ai_settings, screen, ship):
        '''在飞船的位置创建一颗子弹'''
        super().__init__()
        
        self.ai_settings = ai_settings
        self.screen = screen

        # 创建一个表示子弹的矩形(初始位置在左上角，后续调整)
        self.rect = pygame.Rect(0,0, 
            ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top    # 子弹从飞机顶部射出

        self.y = float(self.rect.y)      # y就是子弹rect的top
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
    
        return

    def update(self):
        '''确定单个子弹的实时位置'''
        self.y -= self.speed_factor
        self.rect.y = self.y

        return

    def draw_bullet(self):
        '''绘出子弹'''
        pygame.draw.rect(self.screen, self.color, self.rect)

        return