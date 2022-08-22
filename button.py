 # -*- coding:utf-8 -*-

import pygame.font

class Button():
    '''按钮类'''
    def __init__(self, ai_settings, screen, msg):
        # 基本属性
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # 按钮尺寸
        self.width, self.height =  200, 50
        self.button_color = (128, 128, 214)
        self.text_color   = (255, 255, 255)
        self.text_font    = pygame.font.SysFont(None, 48)   # None表示默认字体，48为字体大小

        # 按钮自身的矩形位置
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 由于按钮只创建一次，所以可以把渲染Play文本的函数调用放在构造函数中
        self.prep_msg(msg)

        return

    def prep_msg(self, msg):
        '''将文本渲染为图像'''
        self.msg_img = self.text_font .render(msg, True, self.text_color, self.button_color)
        # 待渲染文本，是否开启抗锯齿，文本颜色，文本图像背景色(此处用按钮颜色代替，否则为透明) 

        # 获取文本图像的矩形并使其在按钮上居中
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

        return
    
    def draw_button(self):
        '''画出按钮和文本，且文本在上'''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_img, self.msg_img_rect)

        return