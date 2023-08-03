# @Time:            2023/7/12 13:52
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            overlay
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
from turtle import speed

import pygame
from game.settings import *


class Overlay:
    """
    玩家界面的叠加层
    """

    def __init__(self, player):
        # 基本设置
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # 导入
        overlay_path = '../resource/graphics/overlay/'
        # 加载玩家工具和种子图标的图像
        self.tools_surface = {
            tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools
        }
        self.seeds_surface = {
            seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds
        }
        self.speed_surface = {
            speed: pygame.image.load(f'{overlay_path}{speed}.png').convert_alpha() for speed in player.speeds
        }

    def display(self):
        # 播放工具: 获取图片, 获取位置, 绘制图片于 self.display_surface
        tool_surface = self.tools_surface[self.player.selected_tool]
        tool_rect = tool_surface.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surface, tool_rect)
        # 播放种子: 同上
        seed_surface = self.seeds_surface[self.player.selected_seed]
        seed_rect = seed_surface.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surface, seed_rect)
        # 播放疾跑动画
        speed_surface = self.speed_surface[self.player.selected_speed]
        speed_rect = seed_surface.get_rect(midbottom=OVERLAY_POSITIONS['speed'])
        self.display_surface.blit(speed_surface, speed_rect)
