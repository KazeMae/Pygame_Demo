# @Time:            2023/8/26 5:52
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            plant
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from game.settings import *
from scene.support import import_folder
class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered):
        super().__init__(groups)
        self.plant_type = plant_type
        self.frames = import_folder(f'../resource/graphics/fruit/{plant_type}')
        self.soil = soil
        self.check_watered = check_watered

        # 植物生长的时间
        self.age = 0
        # 植物成熟的时间
        self.max_age = len(self.frames) - 1
        # 生长速度
        self.grow_speed = GROW_SPEED[plant_type]
        # 是否可以收割
        self.harvestable = False

        # 精灵设置
        self.image = self.frames[self.age]
        self.y_offset = -16 if plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom=soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['ground plant']

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed
            # 如果植物成长值大于 1 则玩家不能踩在上面
            if int(self.age) > 0:
                self.z = LAYERS['main']
                self.hitbox = self.rect.copy().inflate(-26, -self.rect.height * 0.4)

            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True

            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))