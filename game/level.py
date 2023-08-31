# @Time:            2023/7/11 19:41
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            level
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com

import pygame
from random import randint
from pytmx.util_pygame import load_pygame
from game.settings import *
from game.transition import Transition
from actor.player import Player
from actor.overlay import Overlay
from actor.camera_group import CameraGroup
from actor.shopmenu import ShopMenu
from scene.generic import Generic
from scene.tree import Tree
from scene.water import Water
from scene.wild_flower import WildFlower
from scene.support import import_folder
from scene.interaction import Interaction
from scene.soil_layer import SoilLayer
from scene.rain import Rain
from scene.particle import Particle
from scene.sky import Sky
from scene.bag import Bag


class Level:
    def __init__(self):
        # 获取屏幕
        self.display_surface = pygame.display.get_surface()

        # 创建精灵组[所有显示精灵, 碰撞精灵, 树精灵, 互动精灵]
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        # 土壤
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)

        self.setup()

        # 建立叠加层
        self.overlay = Overlay(self.player)
        # 过渡
        self.transition = Transition(self.reset, self.player)

        # 天空
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) < 3  # 概率30%
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        # 商店
        self.menu = ShopMenu(self.player, self.toggle_shop)
        # 商店状态
        self.shop_active = False

        # 背包
        self.bag = Bag(self.player, self.toggle_bag)
        self.bag_active = False

        # 拾取声音和音量
        self.success_sound = pygame.mixer.Sound('../resource/audio/success.wav')
        self.success_sound.set_volume(0.3)
        self.music = pygame.mixer.Sound('../resource/audio/music.mp3')
        self.music.set_volume(0.3)
        self.music.play(loops=-1)

    def setup(self):
        # 获取地图tmx文件
        tmx_data = load_pygame('../resource/data/map.tmx')

        # 房子地板, 和地毯, 注意绘制顺序
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
            Generic((x * TILE_SIZE, y * TILE_SIZE), surface, [self.all_sprites, self.collision_sprites])

        # 水
        water_frames = import_folder('../resource/graphics/water')
        for x, y, surface in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # 树
        for objec in tmx_data.get_layer_by_name('Trees'):
            Tree(
                pos=(objec.x, objec.y),
                surface=objec.image,
                groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                name=objec.name,
                player_add=self.player_add
            )

        # 野花
        for objec in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((objec.x, objec.y), objec.image, [self.all_sprites, self.collision_sprites])

        # 空气墙
        for x, y, surface in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # 玩家
        for objec in tmx_data.get_layer_by_name('Player'):
            if objec.name == 'Start':
                self.player = Player(
                    pos=(objec.x, objec.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites,
                    interaction=self.interaction_sprites,
                    soil_layer=self.soil_layer,
                    toggle_shop=self.toggle_shop,
                    toggle_bag=self.toggle_bag
                )

            if objec.name == 'Bed':
                Interaction((objec.x, objec.y), (objec.width, objec.height), self.interaction_sprites, 'Bed')

            if objec.name == 'Trader':
                Interaction((objec.x, objec.y), (objec.width, objec.height), self.interaction_sprites, 'Trader')

        # 载入地图地板
        Generic(
            pos=(0, 0),
            surface=pygame.image.load('../resource/graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground']
        )

    def player_add(self, item):
        """
        玩家物品增加
        :param item:物品种类
        :return:
        """
        self.player.item_inventory[item] += 1
        self.success_sound.play()

    def toggle_shop(self):
        # 标记商店开启或关闭
        self.shop_active = not self.shop_active

    def toggle_bag(self):
        # 标记商店开启或关闭
        self.bag_active = not self.bag_active

    def reset(self):
        """
        每日更新
        :return:
        """
        # 植物
        self.soil_layer.update_plants()

        # 土地浇水重置
        self.soil_layer.remove_water()
        # 随机降雨
        self.raining = randint(0, 10) < 3  # 概率30%
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.watet_all()
        # 苹果
        # 遍历所有树
        for tree in self.tree_sprites.sprites():
            # 遍历树上的苹果
            if len(tree.apple_sprites.sprites()) > 0:
                for apple in tree.apple_sprites.sprites():
                    apple.kill()
                tree.create_fruit()

        # 时间
        self.sky.start_color = [255, 255, 255]
        self.sky.light = True

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, LAYERS['main'])
                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

    def run(self, dt):
        # 填充屏幕
        self.display_surface.fill('blue')
        # 以玩家为中心绘制精灵
        self.all_sprites.custom_draw(self.player)

        # 根据是否打开商店来绘制精灵
        if self.shop_active:
            self.menu.update()
        else:
            # 更新精灵
            self.all_sprites.update(dt)
            # 收获植物
            self.plant_collision()

        # 绘制背包
        if self.bag_active and not self.shop_active:
            self.bag.update()

        # 绘制叠加层
        self.overlay.display()
        # 下雨
        if self.raining and not self.shop_active:
            self.rain.updata()
        # 时间流逝
        self.sky.display(dt)

        # 判断是否睡觉
        if self.player.sleep:
            self.transition.play()
