# @Time:            2023/7/13 19:57
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            tree
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
from scene.generic import Generic


class Tree(Generic):
    """
    加载树的贴图
    继承自Generic类
    能够继承父类的属性和方法
    """

    def __init__(self, pos, surface, groups, name):
        super().__init__(pos, surface, groups)
