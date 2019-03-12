from matplotlib import image as mpimg
import matplotlib.pyplot as plt
import cv2
from numpy import zeros as npzeros
from numpy import array as nparray
from queue import Queue

def draw_event(event, x, y, flags, param):
    """
    创建鼠标事件, 进行圈画.
    :param event:   CV2 内置的鼠标事件
    :param x:       鼠标位置.column 位置
    :param y:       鼠标位置.row 位置
    :param flags:   CV2 内置的鼠标FLAG, 判断是否左键为按下情况.
    :param param:   传入的额外参数, [图片, 边界点]
    :return: param
    """
    img = param[0]
    edge_dict = param[1]
    # todo: 如何把线填满.
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        if y in edge_dict.keys(): # 若此 row 存在于 edge_dict 的 index 中, 则在值后append x.
            edge_dict[y].append(x)
        else:                     # 若此 row 不存在, 则创建 list 存储 x.
            edge_dict[y] = [x]
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:

        edge_dict.append([x, y])
        print('Move : (%d, %d)' % (x, y))
        print(edge_dict.__len__())
        print(edge_dict[-2])
        cv2.line(img, tuple(edge_dict[-2]), tuple(edge_dict[-1]), (0, 0, 255),1)
    elif event == cv2.EVENT_LBUTTONUP:
        print('END: (%d, %d)' % (x, y))

class DrawLabel():
    """
    使用此 class 进行单幅图像圈画.
    """
    def __init__(self):
        # TODO: 把 edge_list 换成 edge_dict 如何.
        # 变成dict以后就可以直接fill了:
        # 在同一个index里面, 先填满，然后空，再填满.
        self.edge_dict = {}

    def read_gif(self, fp):
        self.img_origin = mpimg.imread(fp)
        self.img_edged = self.img_origin.copy()

    def draw_edge(self):
        """
        通过 cv2 的鼠标事件, 画出边界.
        将 row 作为 edge_dict 的 index.
        :return:
        """
        cv2.namedWindow('draw label')
        cv2.setMouseCallback('draw label', draw_event, [self.img_edged, self.edge_dict])
        while(1):
            cv2.imshow('draw label', self.img_edged)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        assert abs(self.img_edged - self.img_origin).sum() != 0
        print(len(self.edge_dict))

    def fill_label(self, flag):
        """
        填充画出的边界作为 label.
        使用 queue 来完成遍历填充.
        :param flag: 良恶性, 良性为2, 恶性为1.
        :return:
        """
        height, width = self.img_origin.shape
        self.label = npzeros((height, width))
        edge_array = nparray(self.edge_dict)
        start_pt = edge_array.mean(0)
        curr_pt = start_pt[:]
        label_queue = Queue()
        while not label_queue.empty():
            pass


        pass
        # print('draw label')




if __name__ == '__main__':
    drawlabel = DrawLabel()
    fp = 'E:\gif\恶性\恶性\\0000041760管亚军1.gif'
    drawlabel.read_gif(fp)
    drawlabel.draw_edge()
    plt.subplot(1,2,1), plt.imshow(drawlabel.img_origin)
    plt.subplot(1,2,2), plt.imshow(drawlabel.img_edged)
    plt.show()
