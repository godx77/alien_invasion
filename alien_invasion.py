# -*- coding:utf-8 -*-

from random import gammavariate
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    '''运行游戏的主函数'''

    # 初始化pygame
    pygame.init()

    #添加一个设置对象
    ai_settings = Settings()
    stats = GameStats(ai_settings)

    # 绘制基础屏幕
    screen = pygame.display.set_mode((ai_settings.screen_width,
        ai_settings.screen_height))
    pygame.display.set_caption('Heda Invasion')
     
    
    #------ 游戏元素 ------

    # 创建一个记分板
    scoreboard = Scoreboard(ai_settings, screen, stats) 
    # 创建一个按钮
    play_button = Button(ai_settings, screen, "Fuck Heda")
    # 创建一个飞船对象
    ship = Ship(ai_settings, screen)
    # 创建子弹
    bullets = Group()   # 子弹编组，以便能管理所有发出去的子弹
    # 外星人
    aliens = Group()     # 外星人编组
    gf.creat_fleet(ai_settings, screen, ship, aliens)

    # 游戏运行主循环
    while True:
        gf.check_events(ai_settings, screen, stats, scoreboard, ship, play_button, aliens, bullets)

        # 飞船用完时游戏结束
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, scoreboard, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, scoreboard, ship, bullets, aliens, play_button)
        
run_game()