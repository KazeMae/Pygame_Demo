# @Time:            2023/9/1 2:58
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            welcome
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import sys
import pygame

from actor.timer import Timer
from game.settings import *


class Welcome:
    def __init__(self, player):
        # 设置
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.back_surface = pygame.image.load('../resource/graphics/welcome/welcome.png').convert()
        # 颜色
        self.color = 255
        # 游戏状态
        self.begin = 0
        # 字体
        self.big_font = pygame.font.Font('../resource/font/DinkieBitmap-9pxDemo.ttf', 100)
        self.mid_font = pygame.font.Font('../resource/font/DinkieBitmap-9pxDemo.ttf', 50)
        self.small_font = pygame.font.Font('../resource/font/DinkieBitmap-9pxDemo.ttf', 40)

        # 计时器
        self.timer = Timer(400)

    def input(self):
        keys = pygame.key.get_pressed()
        # 开始游戏
        if keys[pygame.K_RETURN]:
            self.begin = 1

        if keys[pygame.K_ESCAPE] and not self.timer.active:
            self.timer.activate()
            if self.begin == 1:
                self.begin = 2
            elif self.begin == 2:
                pygame.quit()
                sys.exit()

    def display(self):
        if self.begin == 0:
            # 放置背景
            self.display_surface.blit(self.back_surface, (0, 0))
            # 生成标题和标题位置, 并绘制
            title_surface = self.big_font.render('星露谷物语', False, 'White')
            title_rect = title_surface.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.display_surface.blit(title_surface, title_rect)
            # 生成提示语和提示语, 并绘制
            hint_surface = self.mid_font.render('按Enter进入游戏', False, 'White')
            hint_rect = hint_surface.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
            self.display_surface.blit(hint_surface, hint_rect)

        elif self.begin == 2:
            # 背景
            menu_rect = pygame.Rect(250, 150, 800, 400)
            pygame.draw.rect(self.display_surface, 'White', menu_rect, 0, 20)
            # 标题
            title_surface = self.mid_font.render('菜单', False, 'Black')
            title_rect = title_surface.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 130))
            self.display_surface.blit(title_surface, title_rect)
            # 选项
            hint_surface = self.small_font.render('按 Enter 继续游戏', False, 'Black')
            hint_rect = hint_surface.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))
            self.display_surface.blit(hint_surface, hint_rect)
            hint_surface = self.small_font.render('再按 Esc 退出游戏', False, 'Black')
            hint_rect = hint_surface.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))
            self.display_surface.blit(hint_surface, hint_rect)
            # 更新计时器
            self.timer.update()
