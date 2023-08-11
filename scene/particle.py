# @Time:            2023/8/12 0:54
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            particle
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from scene.generic import Generic
from game.settings import *


class Particle(Generic):
    """
    实现破环树木和采集苹果时候的闪烁
    """
    def __init__(self, pos, surface, groups, z, duration=200):
        """
        初始化方法
        :param pos: 精灵的初始位置，即左上角的坐标
        :param surface: 用于表示精灵图像的表面对象
        :param groups: 精灵组
        :param z: 精灵所在的图层
        """
        super().__init__(pos, surface, groups)
        # 获取开始时间
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # 白色表面
        mask_surface = pygame.mask.from_surface(self.image)
        new_surface = mask_surface.to_surface()
        new_surface.set_colorkey((0, 0, 0))
        self.image = new_surface

    def update(self, dt):
        """
        精灵要很快自我毁灭，创建内部计时器
        :param dt:
        :return:
        """
        # 获取当前时间
        current_time = pygame.time.get_ticks()
        # 如果存在时间超过设定值则就销毁
        if current_time - self.start_time > self.duration:
            self.kill()
