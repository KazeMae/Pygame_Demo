# @Time:            2023/7/13 19:54
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            water
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
from game.settings import *
from scene.generic import Generic


class Water(Generic):
    """
    加载水的贴图
    继承自Generic类
    能够继承父类的属性和方法
    """

    def __init__(self, pos, frames, groups):
        # 动画设置
        self.frames = frames
        self.frame_index = 0

        # 调用父类的构造函数来进行初始化
        super().__init__(
            pos=pos,
            surface=self.frames[self.frame_index],
            groups=groups,
            z=LAYERS['water'])

    def animate(self, dt):
        """
        加载水动画
        :param dt:
        :return:
        """
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
