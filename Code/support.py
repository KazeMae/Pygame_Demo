# @Time:            2023/7/11 21:08
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            support
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com


import pygame
# walk(path) 返回这个文件夹包含的所有文件
from os import walk


def import_folder(path):
    """
    从文件夹中获取动画数组
    :param path: 动画帧图所在位置
    :return: 动画数组
    """
    surface_list = []
    # 获取文件夹路径, 子文件夹列表, 图像文件列表
    for folder_name, sub_folder, img_files in walk(path):
        # 从图像文件列表中获取每个图像的名称
        for image in img_files:
            # 组合得到完整路径
            full_path = path + '/' + image
            # print(full_path)
            # 获取图像, 并将图像转换为适合显示的格式 ( convert_alpha() )
            image_surf = pygame.image.load(full_path).convert_alpha()
            # 放入动画列表
            surface_list.append(image_surf)

    return surface_list
