# @Time:            2023/7/13 19:53
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            generic
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from game.settings import *


class Generic(pygame.sprite.Sprite):
    """
    通用精灵类
    继承pygame.sprite.Sprite类
    """
    def __init__(self, pos, surface, groups, z=LAYERS['main']):
        """
        初始化
        :param pos: 精灵的初始位置，即左上角的坐标
        :param surface: 用于表示精灵图像的表面对象
        :param groups: 精灵组
        :param z: 精灵所在的图层
        """
        # 调用父类的构造函数来进行初始化
        super().__init__(groups)
        # 获取精灵的图像
        self.image = surface
        # 传入的位置信息创建精灵的矩形区域
        self.rect = self.image.get_rect(topleft=pos)
        # 精灵所在的图层
        self.z = z
        # 碰撞箱, y轴缩小 75% 实现玩家可以站在物体后面的效果
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
