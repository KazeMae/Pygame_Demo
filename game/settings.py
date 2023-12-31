# @Time:            2023/7/11 19:25
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            setting
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com

from pygame.math import Vector2

# 屏幕和区块大小
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

# 工具, 种子, 疾跑小图标位置
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5),
    'speed': (50, SCREEN_HEIGHT - 70)
}

# 玩家工具作用位置的偏移量
PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50, 40),
    'right': Vector2(50, 40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50)
}

# 图层顺序
LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10
}

# 小树和大树的苹果位置
APPLE_POS = {
    'Small': [(18, 17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    'Large': [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)]
}

# 植物生长速度
GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7
}

# 商店收购价格
SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 10,
    'tomato': 20
}

# 商店出售价格
PURCHASE_PRICES = {
    'corn': 4,
    'tomato': 5
}

# 中英转换
EN_TO_CN = {
    'wood': '木头',
    'apple': '苹果',
    'corn': '玉米',
    'tomato': '番茄'
}
