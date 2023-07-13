# @Time:            2023/7/11 19:25
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            setting
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com


import sys
import pygame
from game.settings import *
from game.level import Level


class Game:
    def __init__(self):
        """
        初始化游戏
        """
        # 初始化
        pygame.init()
        # 创建窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # 设置窗口名
        pygame.display.set_caption('星露谷物语 嘀嘀嘀嘀嘀嘀配')
        # 获取时钟
        self.clock = pygame.time.Clock()
        # 创建关卡
        self.level = Level()

    def run(self):
        """
        游戏主程序
        :return:
        """
        while True:
            for event in pygame.event.get():
                # 监听是否关闭游戏
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 时间增量
            dt = self.clock.tick() / 1000
            self.level.run(dt)
            # 更新播放器
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
