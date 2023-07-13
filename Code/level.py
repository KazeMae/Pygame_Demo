# @Time:            2023/7/11 19:41
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            level
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com

import pygame
from settings import *
from player import Player
from overlay import Overlay
from camera_group import CameraGroup
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import import_folder

class Level:
    def __init__(self):
        # 获取屏幕
        self.display_surface = pygame.display.get_surface()

        # 创建精灵组
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # 建立玩家和地图
        self.setup()
        #
        self.overlay = Overlay(self.player)

    def setup(self):
        # 获取地图tmx文件
        tmx_data = load_pygame('../data/map.tmx')

        # 房子地板, 地板和地毯, 注意绘制顺序
        for layer in ['HouseFloor', 'HouseFurnitureBottom', ]:
            for x, y, surface in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, LAYERS['house bottom'])

        # 房子墙, 桌椅等家具
        for x, y, surface in tmx_data.get_layer_by_name('HouseWalls').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, LAYERS['main'])
        for x, y, surface in tmx_data.get_layer_by_name('HouseFurnitureTop').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, LAYERS['main'])

        # 栅栏
        for x, y, surface in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surface,  [self.all_sprites, self.collision_sprites])

        # 水
        water_frames = import_folder('../graphics/water')
        for x, y, surface in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # 树
        for objec in tmx_data.get_layer_by_name('Trees'):
            Tree((objec.x, objec.y), objec.image, [self.all_sprites, self.collision_sprites], objec.name)

        # 野花
        for objec in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((objec.x, objec.y), objec.image, [self.all_sprites, self.collision_sprites])

        # 空气墙
        for x, y, surface in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # 载入玩家
        for objec in tmx_data.get_layer_by_name('Player'):
            if objec.name == 'Start':
                self.player = Player((objec.x, objec.y), self.all_sprites, self.collision_sprites)
        # 载入地图地板
        Generic(
            pos=(0, 0),
            surface=pygame.image.load('../graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground'],
        )

    def run(self, dt):
        # 填充屏幕
        self.display_surface.fill('blue')
        # 绘制精灵于屏幕
        # self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.player)
        # 更新精灵
        self.all_sprites.update(dt)
        # 绘制叠加层
        self.overlay.display()