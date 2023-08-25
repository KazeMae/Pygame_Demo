# @Time:            2023/8/24 10:09
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            drop
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from random import randint
from scene.generic import Generic


class RainDrop(Generic):
    def __init__(self, surface, pos, moving, groups, z):
        super().__init__(pos, surface, groups, z)
        # 设置
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # 移动
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            # 向左2单位，向下4单位
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        # 移动
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # 计时器
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
