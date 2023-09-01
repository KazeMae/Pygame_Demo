# @Time:            2023/9/1 2:16
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            bag
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from scene.shopmenu import ShopMenu


class Bag(ShopMenu):
    def __init__(self, player, toggle_bag):
        super().__init__(player, toggle_bag)

    def show_entry(self, text_surface, amount, top, selected):
        # 背景
        background_rect = pygame.Rect(self.main_rect.left, top, self.width,
                                      text_surface.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', background_rect, 0, 4)
        # 文本
        text_rect = text_surface.get_rect(midleft=(self.main_rect.left + 20, background_rect.centery))
        self.display_surface.blit(text_surface, text_rect)
        # 金额
        amount_surface = self.font.render('库存' + str(amount), False, 'Black')
        amount_rect = amount_surface.get_rect(midright=(self.main_rect.right - 20, background_rect.centery))
        self.display_surface.blit(amount_surface, amount_rect)

    def update(self):
        self.input()
        self.display_money()

        for text_index, text_surface in enumerate(self.text_surfaces):
            top = self.main_rect.top + text_index * (text_surface.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surface, amount, top, self.index == text_index)
