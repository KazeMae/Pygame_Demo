# @Time:            2023/8/27 23:10
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            menu
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from game.settings import *
from actor.timer import Timer


class ShopMenu:
    def __init__(self, player, toggle_menu):
        # 设置
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../resource/font/DinkieBitmap-9pxDemo.ttf', 30)

        # 页面设置
        self.width = 400
        self.space = 10
        self.padding = 8

        # 条目数量
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        # 出售与购买的边界
        self.sell_border = len(self.player.item_inventory) - 1

        self.text_surfaces = []
        self.total_height = 0

        self.setup()
        # 选择
        self.index = 0
        self.timer = Timer(200)

    def display_money(self):
        text_surface = self.font.render('钱 ' + f'{self.player.money}', False, 'Black')
        text_rect = text_surface.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10, 10), 0, 6)
        self.display_surface.blit(text_surface, text_rect)

    def setup(self):
        for item in self.options:
            cn_item = EN_TO_CN[item]
            text_surface = self.font.render(cn_item, False, 'Black')
            self.text_surfaces.append(text_surface)
            self.total_height += text_surface.get_height() + (self.padding * 2)

        self.total_height += len(self.text_surfaces)
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            # 更新商店状态
            self.toggle_menu()

        if keys[pygame.K_UP] and not self.timer.active:
            self.index = (self.index - 1 + 6) % 6
            self.timer.activate()

        if keys[pygame.K_DOWN] and not self.timer.active:
            self.index = (self.index + 1) % 6
            self.timer.activate()

        if keys[pygame.K_SPACE] and not self.timer.active:
            self.timer.activate()
            # 获取物品信息
            current_item = self.options[self.index]
            # 卖出
            if self.index <= self.sell_border:
                if self.player.item_inventory[current_item] > 0:
                    self.player.item_inventory[current_item] -= 1
                    self.player.money += SALE_PRICES[current_item]
            # 购买
            else:
                if self.player.money >= PURCHASE_PRICES[current_item]:
                    self.player.seed_inventory[current_item] += 1
                    self.player.money -= PURCHASE_PRICES[current_item]

    def show_entry(self, text_surface, amount, top, selected):
        # 背景
        background_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surface.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', background_rect, 0, 4)
        # 文本
        text_rect = text_surface.get_rect(midleft=(self.main_rect.left + 20, background_rect.centery))
        self.display_surface.blit(text_surface, text_rect)
        # 金额
        amount_surface = self.font.render('库存' + str(amount), False, 'Black')
        amount_rect = amount_surface.get_rect(midright=(self.main_rect.right - 20, background_rect.centery))
        self.display_surface.blit(amount_surface, amount_rect)

        # 选择
        if selected:
            pygame.draw.rect(self.display_surface, 'black', background_rect, 4, 4)
            # 渲染出售和收购的字体
            if self.index <= self.sell_border:
                self.sell_text = self.font.render('收购' + f'${SALE_PRICES[self.options[self.index]]}', False, 'Black')
                pos_rect = self.sell_text.get_rect(midleft=(self.main_rect.left + 150, background_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else:
                self.buy_text = self.font.render('出售' + f'${PURCHASE_PRICES[self.options[self.index]]}', False, 'Black')
                pos_rect = self.buy_text.get_rect(midleft=(self.main_rect.left + 150, background_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()
        self.display_money()

        for text_index, text_surface in enumerate(self.text_surfaces):
            top = self.main_rect.top + text_index * (text_surface.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surface, amount, top, self.index == text_index)
