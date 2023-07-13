# @Time:            2023/7/13 1:14
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            camera_group
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com

import pygame
from player import Player
from settings import *


class CameraGroup(pygame.sprite.Group):
    """
    摄像机类:
    自定义的精灵绘制逻辑，
    使得玩家精灵居中显示在屏幕上，
    同时实现了按图层顺序绘制精灵的功能。
    """

    def __init__(self):
        super().__init__()
        # 获取屏幕
        self.display_surface = pygame.display.get_surface()
        # 设置偏移量
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        """
        自定义绘制 精灵
        :return:
        """
        # 根据玩家精灵的位置计算出偏移量, 让玩家精灵居中显示在屏幕上
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        # 遍历所有图层
        for layer in LAYERS.values():
            # 遍历所有精灵, 排序实现越远离中心的精灵越晚绘制
            for sprite in sorted(self.sprites(), key=lambda
                    sprite: sprite.rect.centery):
                # 如果精灵所在图层为当前所在图层, 则绘制精灵
                if sprite.z == layer:
                    """
                    计算偏移量, 通过偏移量绘制精灵位置
                    用于创建精灵在屏幕上绘制位置的副本, 实现只改变视觉上的位置的效果
                    """
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
