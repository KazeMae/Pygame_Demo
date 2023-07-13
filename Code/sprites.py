# @Time:            2023/7/13 1:26
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            sprites.py
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com

import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    """
    加载地板, 房子, 栅栏的贴图
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


class Water(Generic):
    """
    加载水的贴图
    继承自Generic类
    能够继承父类的属性和方法
    """
    def __init__(self, pos, frames, groups):
        # 动画设置
        self.frames = frames
        self.frame_index = 0

        # 调用父类的构造函数来进行初始化
        super().__init__(
            pos=pos,
            surface=self.frames[self.frame_index],
            groups=groups,
            z=LAYERS['water'])

    def animate(self, dt):
        """
        加载水动画
        :param dt:
        :return:
        """
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)


class WildFlower(Generic):
    """
    加载花的贴图
    继承自Generic类
    能够继承父类的属性和方法
    """
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)

class Tree(Generic):
    """
    加载树的贴图
    继承自Generic类
    能够继承父类的属性和方法
    """
    def __init__(self, pos, surface, groups, name):
        super().__init__(pos, surface, groups)