from util.draw_label import DrawLabel
from util.visualizer import Visualizer
import os

if __name__ == '__main__':
    save_root = './/dataset'
    name_list = ['恶性', '良性']
    subdir_origin = 'img_origin'
    for name in name_list:
        print(name)
        img_origin_path = os.path.join(save_root, name, subdir_origin)
        fn_list = os.listdir(img_origin_path)
        visualizer = Visualizer(root=save_root, name=name, subdir_label='img_label')
        f_save_path = visualizer.img_label_path

        # 确认一下读取了所有的 gif 文件.
        if name == '恶性':
            assert len(fn_list) == 1464
            flag = 2
        elif name == '良性':
            assert len(fn_list) == 2826
            flag = 1
        else:
            raise IndexError

        # TODO: while len(f_save_list) == fn_list, do ...
        while len(os.listdir(f_save_path)) < len(fn_list):
            f_save_list = os.listdir(f_save_path)

            for fn in fn_list:
                # 对于每一个 gif 文件做处理.
                # 1. 圈label
                # 2. 存label

                f_name = fn.split('.')[-2] # e.g., '0000041760管亚军1'
                save_f = f_name + '.png'
                if save_f in f_save_list:
                    continue
                print(f_name)
                read_fp = os.path.join(img_origin_path, fn)

                # 1. 圈label
                drawlabel = DrawLabel()
                drawlabel.read_gif(read_fp)
                drawlabel.draw_edge()
                drawlabel.save_edge()
                drawlabel.fill_label(flag=flag)
                # 2. 存label
                visualizer.save_img(fn=f_name, img_label=drawlabel.img_label)
