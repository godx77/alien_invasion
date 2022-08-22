#  -*- coding:utf-8 -*-
import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    '''记分板'''
    def __init__(self, ai_settings, screen, stats):
        # initial attributes
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # score board display settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 37)

        self.prep_score()   # you should display the initial score (0)
        self.prep_highest_score()
        self.prep_level()
        self.prep_ships()

        return
    
    def prep_score(self):
        '''render score text to get the corresponding img'''
        rounded_score = int(round(self.stats.score, -1))    # -1表示圆为最近的10的整倍数
        score_str = "{:,}".format(rounded_score)            # 逗号表示添加千分位符
        self.score_img = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # get the score_img rect and put it in the proper position
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top   = 20
        
        return

    def prep_highest_score(self):
        '''render highest score text'''
        rounded_highest_score = int(round(self.stats.highest_score, -1))
        highest_score_str = "Highest: {:,}".format(rounded_highest_score)
        self.highest_score_img = self.font.render(highest_score_str, True, self.text_color, self.ai_settings.bg_color)

        self.highest_score_rect = self.highest_score_img.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx
        self.highest_score_rect.top = 20

        return

    def prep_level(self):
        self.level_img = self.font.render("level: " + str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_img.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top   = self.score_rect.bottom + 10

        return

    def prep_ships(self):
        '''show how mant ships left by image'''
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = ship_number * (ship.rect.width)
            ship.rect.y = 10
            self.ships.add(ship)
            
        return
        
    def show_score(self):
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.highest_score_img, self.highest_score_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.ships.draw(self.screen)   # draw all ship sprites
        return

