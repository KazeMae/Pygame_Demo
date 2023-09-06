# @Time:            2023/8/26 16:29
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            sky
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from game.settings import *


class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.light_color = [255, 255, 255]
        self.night_color = [38, 101, 189]
        self.light = True

    def reset(self):
        self.start_color = self.light_color
        self.light = True

    def display(self, dt):
        if self.start_color[0] >= 39:
            for index, value in enumerate(self.night_color):
                if self.start_color[index] > value:
                    self.start_color[index] -= 2 * dt
                else:
                    self.start_color[index] = value
        else:
            for index, value in enumerate(self.light_color):
                if self.start_color[index] < value:
                    self.start_color[index] += 2 * dt
                else:
                    self.start_color[index] = value

        # if self.light and self.start_color[0] <= 39:
        #     self.light = False
        #     self.start_color = self.night_color
        #
        # if not self.light and self.start_color[0] >= 254:
        #     self.light = True
        #     self.start_color = self.light_color

        self.full_surface.fill(self.start_color)
        self.display_surface.blit(self.full_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
