# @Time:            2023/8/23 1:48
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            interaction
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from scene.generic import Generic
from game.settings import *


class Interaction(pygame.sprite.Sprite):
    """
    交互对象
    """
    def __init__(self, pos, size, groups, name):
        surface = pygame.Surface(size)
        # 调用父类的构造函数来进行初始化
        super().__init__(groups)
        # 获取精灵的图像
        self.image = surface
        # 传入的位置信息创建精灵的矩形区域
        self.rect = self.image.get_rect(topleft=pos)
        # 精灵所在的图层
        self.z = LAYERS['main']
        # 碰撞箱, y轴缩小 75% 实现玩家可以站在物体后面的效果
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
        self.name = name
