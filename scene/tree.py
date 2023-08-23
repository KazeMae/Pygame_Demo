# @Time:            2023/7/13 19:57
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            tree
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame.image
from random import randint, choice
from game.settings import *
from actor.timer import Timer
from scene.generic import Generic
from scene.particle import Particle


class Tree(Generic):
    """
    加载树的贴图
    继承自Generic类
    能够继承父类的属性和方法
    """

    def __init__(self, pos, surface, groups, name, player_add):
        super().__init__(pos, surface, groups)

        # 树的属性
        self.health = 5
        self.alive = True
        # 被砍掉的树的图片
        stump_path = f'../resource/graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self. stump_surface = pygame.image.load(stump_path).convert_alpha()
        # 砍树所需时间(树健康值-1的时间）
        self.invul_timer = Timer(200)

        # 苹果图片
        self.apple_surface = pygame.image.load('../resource/graphics/fruit/apple.png')
        # 苹果位置
        self.apple_pos = APPLE_POS[name]
        # 苹果精灵
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

    def damage(self):
        # 砍树时候
        self.health -= 1

        # 拿走苹果
        if len(self.apple_sprites.sprites()) > 0:
            # 去掉苹果精灵
            random_apple = choice(self.apple_sprites.sprites())
            # 播放摘苹果动画
            Particle(
                pos=random_apple.rect.topleft,
                surface=random_apple.image,
                groups=self.groups()[0],
                z=LAYERS['fruit']
            )
            self.player_add('apple')
            random_apple.kill()

    def check_death(self):
        """
        判断树是否被砍
        :return:
        """
        # print(self.health)
        if self.health <= 0:
            Particle(
                pos=self.rect.topleft,
                surface=self.image,
                groups=self.groups()[0],
                z=LAYERS['fruit'],
                duration=300
            )
            self.image = self.stump_surface
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, self.rect.height * 0.1 )
            self.alive = False
            self.player_add('wood')

    def update(self, dt):
        if self.alive:
            self.check_death()

    def create_fruit(self):
        for pos in self.apple_pos:
            # 随机生成苹果
            if randint(0, 10) < 2:
                # 将苹果从相对树的坐标转换到相对整个地图的坐标
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(
                    pos=(x, y),
                    surface=self.apple_surface,
                    groups=[self.apple_sprites, self.groups()[0]],
                    z=LAYERS['fruit']
                )
