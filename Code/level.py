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
from overlay import Overlay
from camera_group import CameraGroup
from sprites import Generic


class Level:
    def __init__(self):
        # 获取屏幕
        self.display_surface = pygame.display.get_surface()

        # 创建精灵组
        self.all_sprites = CameraGroup()
        # 建立玩家和地图
        self.setup()
        #
        self.overlay = Overlay(self.player)

    def setup(self):
        # 载入玩家
        self.player = Player((640, 360), self.all_sprites)
        # 载入地图
        Generic(
            pos=(0, 0),
            surface=pygame.image.load('../graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground'],
        )

    def run(self, dt):
        # 填充屏幕
        self.display_surface.fill('blue')
        # 绘制精灵于屏幕
        # self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.player)
        # 更新精灵
        self.all_sprites.update(dt)
        # 绘制叠加层
        self.overlay.display()
