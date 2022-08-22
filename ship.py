# -*- coding:utf-8 -*-

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''飞船类，用以管理飞船的所有属性和行为'''
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载图片并获取图片以及屏幕外接矩形
        self.image = pygame.image.load(r'alien_invasion\images\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 飞船移动标志
        self.moving_right  = False
        self.moving_left   = False

        # 移动速度
        # self.step = self.ai_settings.ship_speed_factor  
        # 注意当在游戏中途修改设置时，由于飞船已经创建，所以已经
        # 创建的飞船并不能同步设置，而需要一个个改
        # 正确的做法可以是：
        #     当飞船的属性需要整体性控制时，可以将其放到设置中
        #     当飞船的属性需要一个个控制时，应当将其放到类声明中
        # 因此这里其实是不必要声明该属性的

        # 确定放置飞船的初始位置
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom  = self.screen_rect.bottom
        self.ship_center = float(self.rect.centerx)     # 注意rect.centerx只能存储整数值

        return

    def blit_ship(self):
        '''在相应位置绘制出飞船(图片)'''
        self.screen.blit(self.image, self.rect)

        return

    def center_ship(self):
        '''飞船居中'''
        self.ship_center = self.screen_rect.centerx

        return

    def update(self):
        '''飞船的移动'''
        step = self.ai_settings.ship_speed_factor      # 移动速度，也即单步步长
        if self.moving_right:
            # if self.rect.right + self.step > right:  # 检查是否靠近边缘，再动就超出边界了
            if self.rect.right > self.screen_rect.right:# 超过一点点也没关系，总不会超出去很多的
                pass                                   # 别再超过了就行了
            else:
                self.ship_center += step
        if self.moving_left:
            if self.rect.left < self.screen_rect.left:
                pass
            else:
                self.ship_center -= step
        self.rect.centerx = self.ship_center    # 这时候再将float型centerx赋给rect
                                                # 只影响最多半个像素

        return
