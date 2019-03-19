# -*- coding: utf-8 -*-
import os
from numpy import ndarray
from matplotlib import image as mpimg

class Visualizer():
    """
    此 class 用来存储所有图像, 图像内容共有如下  X   个:
    1. img_origin
    2. img_label    '.png'

    Draw_Label-master
    |
    |__ dataset (saveroot = 'Draw_Label-master//dataset')
    |   |__ 恶性 ( name = '恶性')
    |   |   |__ img_origin  (sub_dir_origin = 'img_origin')
    |   |   |__ img_label   (sub_dir_label = 'img_label)
    |   |__ 良性
    |   |   |__ img_origin
    |   |   |__ img_label
    """
    def __init__(self, root, name, subdir_label='img_label'):
        self.img_label_path = os.path.join(root, name, subdir_label)

    def save_img(self, fn, img_label):
        assert isinstance(img_label, ndarray)

        # 1. save img_label to self.img_label_path
        self.save_fp = os.path.join(self.img_label_path, fn + '.png')
        mpimg.imsave(fname=self.save_fp, arr=img_label)
        assert os.path.isfile(self.save_fp)
