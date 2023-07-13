# @Time:            2023/7/13 19:56
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            wild_flower
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
from scene.generic import Generic


class WildFlower(Generic):
    """
    加载花的贴图
    继承自Generic类
    能够继承父类的属性和方法
    """
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

