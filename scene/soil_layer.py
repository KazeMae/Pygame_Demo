# @Time:            2023/8/23 2:38
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            soil
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from pytmx.util_pygame import load_pygame
from game.settings import *
from scene.soil_tile import SoilTile
from scene.support import *


class SoilLayer:
    def __init__(self, all_sprites):
        # 精灵组
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # 图形
        self.soil_surface = pygame.image.load('../resource/graphics/soil/o.png')
        self.soil_surfaces = import_folder_dict('../resource/graphics/soil/')

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