# -*- coding:utf-8 -*-

class GameStats():
    '''记录游戏统计信息的类'''
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        # 先将游戏状态改为非活动状态, 需要通过单机play按钮来启动
        self.game_active = False
        
        self.highest_score = 0      

        self.reset_stats()

        return

    def reset_stats(self):
        '''一旦要重新开始游戏很多属性就必须得靠重新创建实例才行
        而我们肯定是一开始就创建且仅创建一个统计信息的实例，
        后续重新开始游戏时再一个个去设置属性就很麻烦，所以弄一个一键重设的方法'''
        self.ship_left = self.ai_settings.ship_limit
        self.score     = 0
        self.level     = 1

        return
