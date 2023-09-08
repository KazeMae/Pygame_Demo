# @Time:            2023/7/11 20:04
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            actor
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from game.settings import *
from actor.timer import Timer
from scene.support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop, toggle_bag):
        super().__init__(group)

        # 导入动画
        self.animations = {str: []}
        self.import_assets()
        # 设置动画状态, 默认为闲置向下
        self.status = 'down_idle'
        # 动画数组索引
        self.frame_index = 0
        # 移动动画速度
        self.frame_move_speed = 4

        # 一般设置
        # 设置精灵为获取的动画列表, self.animations的容器类似于 C++ 的 map<string, vector<image> >
        self.image = self.animations[self.status][self.frame_index]
        # 设置显示位置, 位置为从外面传入的 pos
        self.rect = self.image.get_rect(center=pos)
        # 设置玩家画面在第几层
        self.z = LAYERS['main']

        # 玩家碰撞箱, 复制 rect 然后缩小
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprites = collision_sprites

        # 移动属性
        self.direction = pygame.math.Vector2()
        # 玩家位置, 并设置初始位置
        self.pos = pygame.math.Vector2(self.rect.center)
        # 玩家速度
        self.speed = 200

        # 玩家工具列表
        self.tools = ['hoe', 'axe', 'water']
        # 玩家工具索引
        self.tool_index = 0
        # 玩家工具
        self.selected_tool = self.tools[self.tool_index]

        # 种子列表
        self.seeds = ['corn', 'tomato']
        # 种子索引
        self.seed_index = 0
        # 玩家手上的种子
        self.selected_seed = self.seeds[self.seed_index]
        # 疾跑
        self.speeds = ['speed', 'unspeed']
        self.speed_index = 1
        self.selected_speed = self.speeds[self.speed_index]

        # 库存
        self.item_inventory = {
            'wood': 0,
            'apple': 0,
            'corn': 0,
            'tomato': 0,
        }
        self.seed_inventory = {
            'corn': 5,
            'tomato': 5
        }
        self.money = 200

        # 互动
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.toggle_shop = toggle_shop
        self.toggle_bag = toggle_bag

        # 泥土
        self.soil_layer = soil_layer

        # 计时器
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200),
            'bag': Timer(500),
        }

        # 声音
        self.watering_sound = pygame.mixer.Sound('../resource/audio/water.mp3')
        self.watering_sound.set_volume(0.2)

    def use_tool(self):
        """
        使用工具时
        :return:
        """
        # print('use tool')
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)

        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if hasattr(tree, 'damage') and tree.rect.collidepoint(self.target_pos):
                    tree.damage()

        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
            self.watering_sound.play()

    def use_seed(self):
        """
        使用种子时
        :return:
        """
        # 判断玩家是否有种子
        if self.seed_inventory[self.selected_seed] > 0:
            self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
            self.seed_inventory[self.selected_seed] -= 1

    def get_target_pos(self):
        """
        获取工具作用位置
        :return:
        """
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def import_assets(self):
        """
        导入资源
        :return:
        """
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],  # 角色行走动画
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],  # 角色限制动画
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],  # 锄头动画
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],  # 斧头动画
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}  # 水动画

        for animation in self.animations.keys():
            full_path = '../resource/graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        """
        更新动画帧
        :param dt: 时间增量
        :return:
        """
        self.frame_index += self.frame_move_speed * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        """
        读入玩家操作并回馈
        :return:
        """
        keys = pygame.key.get_pressed()
        # 如果玩家在使用工具和睡觉时, 则不允许移动
        if not self.timers['tool use'].active and not self.sleep:
            # 方向移动 竖直
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            # 方向移动 水平
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # 玩家疾跑
            if keys[pygame.K_LSHIFT]:
                self.speed = 400
                self.frame_move_speed = 8
                self.speed_index = 0
                self.selected_speed = self.speeds[self.speed_index]
            else:
                self.speed = 200
                self.frame_move_speed = 4
                self.speed_index = 1
                self.selected_speed = self.speeds[self.speed_index]

            # 使用工具按键
            if keys[pygame.K_SPACE]:
                # 使用一个计时器
                self.timers['tool use'].activate()
                # 如果玩家使用工具, 则使玩家停下
                self.direction = pygame.math.Vector2()
                # 使动画从头播放
                self.frame_index = 0

            # 切换工具, 并且切换工具没按下时候
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                # 激活切换工具计时器
                self.timers['tool switch'].activate()
                # 更新工具索引
                self.tool_index = ((self.tool_index + 1) % len(self.tools))
                # print(self.tool_index)
                # 更新工具状态
                self.selected_tool = self.tools[self.tool_index]

            # 使用种子按键
            if keys[pygame.K_LCTRL]:
                # 使用一个计时器
                self.timers['seed use'].activate()
                # 如果玩家使用种子, 则使玩家停下
                self.direction = pygame.math.Vector2()
                # 使动画从头播放
                self.frame_index = 0

            # 切换种子, 并且切换种子没按下时候
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                # 激活切换种子计时器
                self.timers['seed switch'].activate()
                # 更新种子索引
                self.seed_index = ((self.seed_index + 1) % len(self.seeds))
                # print(self.tool_index)
                # 更新种子状态
                self.selected_seed = self.seeds[self.seed_index]

            # 睡觉和商人
            if keys[pygame.K_RETURN]:
                # 检测玩家是否与 interaction 精灵碰撞, 返回碰撞了哪些 Bad or Trader
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                # 列表不为空
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Trader':
                        self.toggle_shop()

                    else:
                        self.status = 'left_idle'
                        self.sleep = True

            if keys[pygame.K_TAB] and not self.timers['bag'].active:
                self.timers['bag'].activate()
                self.toggle_bag()

    def get_status(self):
        """
        如果角色没有移动, 则将状态更新为对应方向的闲置状态
        :return:
        """
        # 如果移动距离为0, 则更新为闲置状态
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # 如果使用工具, 更新状态为 '状态_工具'
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timer(self):
        # 遍历所有计时器, 全部更新
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        """
        实现碰撞无法移动效果
        :param direction: 水平和竖直
        :return:
        """
        for sprite in self.collision_sprites.sprites():
            # 判断 sprite 所属的类是否有 hitbox 属性
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):

                    # 水平方向
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # 向右移动
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # 向左移动
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    # 竖直方向
                    if direction == 'vertical':
                        if self.direction.y > 0:  # 向下移动
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # 向上移动
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        """
        移动玩家位置
        :param dt: 时间增量
        :return:
        """
        # 向量归一化, 使两个向量相加为 1, 实现斜向移动, 零向量不可使用, 判断向量的模是否大于0
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # 计算并改变玩家移动后的位置 竖直
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

        # 计算并改变玩家移动后的位置 水平
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # print(self.rect.centerx, self.rect.centery)

    def update(self, dt):
        """
        更新玩家
        :param dt:
        :return:
        """
        # 获取玩家操作
        self.input()
        # 更新玩家状态是否为闲置
        self.get_status()
        # 更新计时器
        self.update_timer()
        # 获取工具作用位置
        self.get_target_pos()

        # 改变玩家位置
        self.move(dt)
        # 更新动画
        self.animate(dt)
