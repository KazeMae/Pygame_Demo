# @Time:            2023/7/11 20:04
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            player
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com


import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # 导入动画
        self.animations = {str: []}
        self.import_assets()
        # 设置动画状态, 默认为闲置向下
        self.status = 'down_idle'
        # 动画数组索引
        self.frame_index = 0

        # 一般设置
        # 设置精灵为获取的动画列表, self.animations的容器类似于C++的map<string, vector<image> >
        self.image = self.animations[self.status][self.frame_index]
        # 设置显示位置, 位置为从外面传入的 pos
        self.rect = self.image.get_rect(center=pos)

        # 移动属性
        self.direction = pygame.math.Vector2()
        # 玩家位置, 并设置初始位置
        self.pos = pygame.math.Vector2(self.rect.center)
        # 玩家速度
        self.speed = 200

    def import_assets(self):
        """
        导入资源
        :return:
        """
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],  # 角色行走动画
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],  # 角色限制动画
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],  # 锄头动画
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],  # 斧头动画
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}  # 水动画

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        # 监听用户操作
        keys = pygame.key.get_pressed()
        # 方向移动 竖直
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
        # 方向移动 水平
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

    def get_status(self):
        """
        如果角色没有移动, 则将状态更新为对应方向的闲置状态
        :return:
        """
        # 如果移动距离为0, 则更新为闲置状态
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        # TODO：如果使用工具

    def move(self, dt):
        # 向量归一化, 使两个向量相加为 1, 实现斜向移动, 零向量不可使用, 判断向量的模是否大于0
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # 计算玩家移动后的位置 竖直
        self.pos.y += self.direction.y * self.speed * dt
        # 改变玩家位置 竖直
        self.rect.centery = self.pos.y

        # 计算玩家移动后的位置 水平
        self.pos.x += self.direction.x * self.speed * dt
        # 改变玩家位置 水平
        self.rect.centerx = self.pos.x

    def update(self, dt):
        # 获取玩家操作
        self.input()
        # 更新玩家状态是否为闲置
        self.get_status()
        # 改变玩家位置
        self.move(dt)
        # 更新动画
        self.animate(dt)
