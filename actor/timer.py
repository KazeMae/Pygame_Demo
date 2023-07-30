# @Time:            2023/7/12 10:08
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            timer
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com

import pygame


class Timer:
    def __init__(self, duration, func=None):
        """
        计时器初始化
        :param duration: 持续时间
        :param func: 函数
        """

        self.duration = duration
        self.func = func
        # 开始时间
        self.start_time = 0
        # 活动状态
        self.active = False

    def activate(self):
        """
        激活计时器
        :return:
        """
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        """
        停用计时器
        :return:
        """
        self.active = False
        self.start_time = 0

    def update(self):
        """
        更新
        :return:
        """
        # 获取当前时间
        current_time = pygame.time.get_ticks()
        # 如果执行的时间大于设定的持续时间, 则停止计时器
        if current_time - self.start_time >= self.duration:
            # 停止时执行函数
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()
