# @Time:            2023/7/11 19:41
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            level
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com

import pygame
from settings import *
from player import Player


class Level:
    def __init__(self):
        # 获取屏幕
        self.display_surface = pygame.display.get_surface()

        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        self.player = Player((640, 360), self.all_sprites)

    def run(self, dt):
        # 填充屏幕
        self.display_surface.fill('blue')
        # 绘制精灵于屏幕
        self.all_sprites.draw(self.display_surface)
        # 更新精灵
        self.all_sprites.update(dt)
