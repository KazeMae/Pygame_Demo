# @Time:            2023/8/23 2:38
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            soil
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from random import choice
from pytmx.util_pygame import load_pygame
from game.settings import *
from scene.plant import Plant
from scene.soil_tile import SoilTile
from scene.support import *
from scene.water_tile import WaterTile
from scene.rain import Rain

class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):
        # 精灵组
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        # 图形
        self.soil_surfaces = import_folder_dict('../resource/graphics/soil/')
        self.water_surfaces = import_folder('../resource/graphics/soil_water')

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        """
        创建泥土格子
        :return:
        """
        ground = pygame.image.load('../resource/graphics/world/ground.png')
        # 水平区块
        horizontal_tiles = ground.get_width() // TILE_SIZE
        # 垂直区块
        vertical_tiles = ground.get_height() // TILE_SIZE
        self.grid = [[[] for col in range(horizontal_tiles)] for row in range(vertical_tiles)]
        # 标记哪些区块可以耕种
        for x, y, surface in load_pygame('../resource/data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        """
        创建可以耕种的区块
        :return:
        """
        self.hit_rects = []
        # 枚举每个区块
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        """
        开垦土地
        :param point: 被开垦土地的坐标
        :return:
        """
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    # 标记已开垦
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()
                    if self.raining:
                        self.watet_all()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')

                pos = soil_sprite.rect.topleft
                surface = choice(self.water_surfaces)
                WaterTile(pos, surface, [self.all_sprites, self.water_sprites])

    def watet_all(self):
        # 枚举每个区块
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    WaterTile((x, y), choice(self.water_surfaces), [self.all_sprites, self.water_sprites])

    def remove_water(self):
        # 销毁所有的水精灵
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        # 清理所有的耕地
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def check_watered(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.grid[y][x]
        return 'W' in cell

    def plant_seed(self, target_pos, seed):
        for soil_sprite in self.soil_sprites.sprites():
            # 检测是否包含 target_pos
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                # 标记种植
                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(seed, [self.all_sprites, self.plant_sprites, self.collision_sprites], soil_sprite, self.check_watered)

    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        # 枚举每个元素
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                # 如果被垦
                if 'X' in cell:
                    # 平滑贴图
                    t = 'X' in self.grid[index_row - 1][index_col]
                    b = 'X' in self.grid[index_row + 1][index_col]
                    r = 'X' in row[index_col + 1]
                    l = 'X' in row[index_col - 1]

                    tile_type = 'o'

                    if all((t, r, b, l)):
                        tile_type = 'x'

                    if l and not any((t, r, b)):
                        tile_type = 'r'
                    if r and not any((t, l, b)):
                        tile_type = 'l'
                    if r and l and not any((t, b)):
                        tile_type = 'lr'

                    if t and not any((r, l, b)):
                        tile_type = 'b'
                    if b and not any((r, l, t)):
                        tile_type = 't'
                    if b and t and not any((r, l)):
                        tile_type = 'tb'

                    if l and b and not any((t, r)):
                        tile_type = 'tr'
                    if r and b and not any((t, l)):
                        tile_type = 'tl'
                    if l and t and not any((b, r)):
                        tile_type = 'br'
                    if r and t and not any((b, l)):
                        tile_type = 'bl'

                    if all((t, b, r)) and not l:
                        tile_type = 'tbr'
                    if all((t, b, l)) and not r:
                        tile_type = 'tbl'
                    if all((l, r, t)) and not b:
                        tile_type = 'lrb'
                    if all((l, r, b)) and not t:
                        tile_type = 'lrt'

                    SoilTile(
                        pos=(index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surface=self.soil_surfaces[tile_type],
                        groups=[self.all_sprites, self.soil_sprites]
                    )
