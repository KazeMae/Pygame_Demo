# @Time:            2023/8/24 9:37
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            sky
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from game.settings import *
from random import randint, choice
from scene.support import import_folder
from scene.rain_drop import RainDrop


class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('../resource/graphics/rain/drops/')
        self.rain_floor = import_folder('../resource/graphics/rain/floor/')
        self.floor_w, self.floor_h = pygame.image.load('../resource/graphics/world/ground.png').get_size()

    def create_floor(self):
        """
        创建雨滴
        :return:
        """
        RainDrop(
            surface=choice(self.rain_floor),
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=False,
            groups=self.all_sprites,
            z=LAYERS['rain floor']
        )

    def create_drops(self):
        """
        创建雨丝
        :return:
        """
        RainDrop(
            surface=choice(self.rain_drops),
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=True,
            groups=self.all_sprites,
            z=LAYERS['rain drops']
        )

    def updata(self):
        self.create_floor()
        self.create_drops()
