# @Time:            2023/8/23 2:15
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            transition
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from settings import *

class Transition:
    def __init__(self, reset, player):

        # 设置
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player

        # 覆盖图层
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # 白色
        self.color = 255
        # 变暗速度
        self.speed = -1

    def play(self):
        # 不断变暗
        self.color += self.speed
        if self.color == 0:
            self.speed *= -1
            self.reset()
        if self.color > 255:
            self.color = 255
            self.player.sleep = False
            self.speed = -1
        # 填充整个图像
        self.image.fill((self.color, self.color, self.color))
        # 图像放置位置
        self.display_surface.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
