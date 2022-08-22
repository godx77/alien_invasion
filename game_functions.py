# -*- coding:utf-8 -*-

import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(ai_settings, event, screen, stats, scoreboard, ship, aliens, bullets):
    if event.key   == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:    # 这里用elif是因为event监控两个不同的事件
        ship.moving_left = True  
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_RETURN and not stats.game_active:  # 按回车也可以开始或重置游戏
        start_game(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)
    elif event.key == pygame.K_SPACE:   # 开火
        fire_bullet(ai_settings, screen, ship, bullets)
    
    return

def fire_bullet(ai_settings, screen, ship, bullets):
    '''玩家按下空格键时开火'''
    # 添加一颗新子弹并加入子弹编组
    if len(bullets) < ai_settings.bullet_allowed:   # 还允许发射子弹
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

    return

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    
    return

def check_events(ai_settings, screen, stats, scoreboard, ship, play_button, aliens, bullets):
    '''侦听用户事件并响应'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 移动命令
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(ai_settings, event, screen, stats, scoreboard, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()   # 获取光标位置
            check_play_button(ai_settings, screen, stats, scoreboard, ship,  play_button, mouse_x, mouse_y, aliens, bullets)
                
    return

def check_play_button(ai_settings, screen, stats, scoreboard, ship,  play_button, mouse_x, mouse_y, aliens, bullets):
    '''检测玩家是否点击了Play按钮并给出响应，注意游戏开始和需要重置游戏时都需要点击Play'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:    # 必须要是游戏处于非激活状态时点击才重置或开始游戏，不然在游戏过程中点击也会重置
       start_game(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)

    return

def start_game(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    '''用于对玩家开始或重新开始游戏时的响应函数'''
    # 重置统计信息
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)     # 只要游戏应该开始了，那么光标就应该是不可见的
    stats.reset_stats()                 # 重置大部分属性，比如飞船数量
    stats.game_active = True

    scoreboard.prep_score()             # 每次游戏开始时都应该刷新分数，否则只能在第一颗子弹击中后才刷新显示
    scoreboard.prep_highest_score()
    scoreboard.prep_level()
    scoreboard.prep_ships()

    # 清空外星人和子弹
    aliens.empty()
    bullets.empty()
    # 创建外星人和将飞船居中
    creat_fleet(ai_settings, screen, ship,  aliens)
    ship.center_ship()

    return


# ------- Bullet ------- #

def update_bullets(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    '''更新所有子弹实时位置，并且删除已经消失的子弹'''
    bullets.update()  
        # 原来是在Bullet类中定义了update_bullet()方法，然后遍历对每一个精灵调用
        # 为编组中的所有子弹都执行这一操作，也可以将Bullet类的update_bullet()方法改为
        # update()，这样就可以用bullets.update()对编组中的每个精灵调用update来更新位置
        # 这样就不用循环了
        # 注意，并不是指定任意方法编组都会对其中的精灵进行该函数的操作，只有update()可以
        # 相当于在Bullet中对Grup的update方法进行了override(重写)
    for bullet in bullets.copy():   # bullets是无序的，更像是集合，不应该直接对原编组进行改动     
        if bullet.rect.bottom <= 0:  
            # 删除到达顶部的子弹
            bullets.remove(bullet)
    
    check_aliens_bullets_collisions(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)

    return

def check_aliens_bullets_collisions(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    # 检测是否有子弹和外星人发生了碰撞，一经发现，二者都删除掉(True)
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # add 50 score when bullet shot on an alien
    if collision:
        for aliens in collision.values():   # 碰撞字典中子弹为key，被射到的外星人为value列表，因为一颗（大）子弹可能击中多个外星人
            stats.score += 50 * len(aliens)
            scoreboard.prep_score()
        check_highest_score(stats, scoreboard)
    
    # 如若aliens被消灭完了，就清空屏幕上的子弹并且重新生成一群外星人
    if (0 == len(aliens)):
        ai_settings.increase_speed()
        bullets.empty()
        stats.level += 1    # 消灭一群外星人等级加一
        scoreboard.prep_level()
        creat_fleet(ai_settings, screen, ship, aliens)

    return

def check_highest_score(stats, scoreboard):
    if stats.score > stats.highest_score:
        stats.highest_score = stats.score
        scoreboard.prep_highest_score()

    return

# ------- Bullet ------- #

# ------- Alien ------- #

def get_number_aliens_x(ai_settings, alien_width):
    '''获取每行可容纳的外星人数量'''
    available_space_x = ai_settings.screen_width - 2 * alien_width    # 横向可用空间
    number_aliens_x =  int(available_space_x / (2 * alien_width))     # 横向可摆放外星人数量 
                                                                      # 考虑间距，每个外星人占两个外星人的位置
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''获取纵向可以容纳的外星人行数'''
    available_space_y = (ai_settings.screen_height - 
        3 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height ))

    return number_rows

def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''创建单个外星人'''
    alien   = Alien(ai_settings, screen)
    alien_width  = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number      # x值随外星人编号递增 
    alien.y = alien_height + 2 * alien_height * row_number      # y值随外星人行号递增 
    alien.rect.x = alien.x  # 赋予准确值，再进行取整
    alien.rect.y = alien.y
    aliens.add(alien)       # 将该外星人加入编组

    return


def creat_fleet(ai_settings, screen, ship, aliens):
    '''创建一群外星人'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)    
    number_rows     = get_number_rows(ai_settings, 
        ship.rect.height, alien.rect.height)

    # 创建一群外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings, screen, aliens, alien_number, row_number)

    return

def update_aliens(ai_settings, stats, screen, scoreboard, ship, aliens, bullets):
    '''更新 所有 外星人的位置'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # 检测外星人是否碰到了飞船
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, scoreboard, ship, aliens, bullets)

    # 检测是否有外星人撞到了屏幕底部并作出响应
    check_aliens_bottom(ai_settings, stats, screen, scoreboard, ship, aliens, bullets)

    return
    

def check_fleet_edges(ai_settings, aliens):
    '''检查外星人群中是否有个体触及边缘并采取行动'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
    return

def change_fleet_direction(ai_settings, aliens):
    '''外星人下移指定距离并改变左右移动方向'''
    for alien in aliens.sprites():
        alien.y += alien.ai_settings.fleet_drop_speed
        alien.rect.y = alien.y
        # alien.individual_direction *= -1
    ai_settings.fleet_direction *= -1       # 改变左右移动方向
    # alien.individual_direction *= -1
    # 此处犯的错误：
    # 书上是如上述语句这样写的，但是因为我为每个外星人定义了属性fleet_direction
    # 而且外星人对象在创建时就被赋予了这样的一个移动方向属性，也即 ai_settings.fleet_direction
    # 已经赋值给了alien.fleet_direction，当我在for循环外部整体更改了ai_settings.fleet_direction时，
    # 每个外星人的移动方向并没有被重新赋值
    # 注意，fleet_direction本身就是一群外星人的属性，因而也不应该作为单个外星人的属性来编程，因而不推
    # 荐采用这种方式，除非每个外星人都可能有自己独特的移动方向

    return

def ship_hit(ai_settings, stats, screen, scoreboard, ship, aliens, bullets):
    '''响应外星人撞到了飞船这一事件'''
    if stats.ship_left > 0:
        stats.ship_left -= 1
        scoreboard.prep_ships()
        # 清空子弹和外星人
        bullets.empty()
        aliens.empty()

        # 又创建一群外星人并将飞船居中
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    
        # 程序暂停1秒
        sleep(0.5)
    else:
        stats.game_active = False
        # 立马让光标可见
        pygame.mouse.set_visible(True)

    return

def check_aliens_bottom(ai_settings, stats, screen, scoreboard, ship, aliens, bullets):
    '''检查是否有外星人撞到了屏幕下方'''
    screen_rect = screen.get_rect()
    
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 就像外星人撞到飞船一样处理
            ship_hit(ai_settings,stats, screen, scoreboard, ship, aliens, bullets)
            break

    return
# ------- Alien ------- #





def update_screen(ai_settings, screen, stats, scoreboard, ship, bullets, aliens, play_button):
    '''更新屏幕'''
    # 每次都重新绘制屏幕以设置背景颜色
    screen.fill(ai_settings.bg_color)
    # 绘制记分板
    scoreboard.show_score()
    # 绘制飞船，必须在背景填充后，确保飞船出现在背景前面
    ship.blit_ship()
    # 在飞船后绘制子弹
    for bullet in bullets.sprites():    # 返回精灵列表
        bullet.draw_bullet()
    # 绘制编组中每个外星人，且保证在绘制子弹之后，这样外星人就在最上层
    for alien in aliens.sprites():
        alien.blit_alien() 

    # 在游戏未激活时显示按钮
    if not stats.game_active:
        play_button.draw_button()

    # 不断更新屏幕(前面的操作并不会真的使要显示的东西显示出来，而是这一步统一更新显示)
    pygame.display.flip()
    
    return