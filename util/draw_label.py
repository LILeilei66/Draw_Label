from matplotlib import image as mpimg
import matplotlib.pyplot as plt
import cv2
from numpy import zeros as npzeros
from numpy import array as nparray
from queue import Queue

import cv2

def connect_pts(pt1, pt2):
    """
    判断 pt1, pt2 是否相连, 若否, 插入点使其相连.
    注意: 由于 cv2 的坐标为(col, row), 与 array <-> img 的标识方法不同, 因此在本函数中只以 col, row 表示, 不以 x, y 表示.
    前开后闭.
    经确认上右下左四向无问题.
    :param pt1: list 上一个点 [col, row]
    :param pt2: list 新的点   [col, row]
    :return: line_list
    """
    line_list = []
    col1, row1 = pt1
    col2, row2 = pt2
    if abs(col1 - col2) > 1 or abs(row1 - row2) > 1:
        if row1 == row2:
            if col1 < col2:
                for col in range(col1+1, col2+1):
                    line_list.append([col, row1])
            elif col2 < col1:
                for col in range(col1-1, col2-1, -1):
                    line_list.append([col, row1])
        else:
            if row1 < row2:
                for row in range(row1+1, row2+1):
                    col = int((col2 - col1) / (row2 - row1) * (row - row1) + col1)
                    line_list.append([col, row])
            elif row2 < row1:
                for row in range(row1-1, row2-1, -1):
                    col = int((col2 - col1) / (row2 - row1) * (row - row1) + col1)
                    line_list.append([col, row])
    else:
        line_list.append(pt2)
    return line_list

def add_dict(dict, list):
    """
    将新的点 list 加入到之前的点 dict 中.
    :param dict: {'row': [col, ...], ...}
    :param list: [[col, row], ...]
    :return: dict, flag_closed: bool, 闭合与否.
    """
    assert len(list) > 0
    for pt in list:
        col, row = pt
        if row in dict.keys():
            if col in dict[row]: # 如果已经交叉闭合, 则结束记录返回,
                flag_closed = True
                return dict, flag_closed
            dict[row].append(col)
        else:
            dict[row] = [col]
        flag_closed = False
    return dict, flag_closed

def draw_event(event, x, y, flags, param):
    """
    创建鼠标事件, 进行圈画.
    :param event:   CV2 内置的鼠标事件
    :param x:       鼠标位置.column 位置
    :param y:       鼠标位置.row 位置
    :param flags:   CV2 内置的鼠标FLAG, 判断是否左键为按下情况.
    :param param:   传入的额外参数, [图片, 边界点dict, 第一个点, 上一个点, 图形是否闭合]
    :return: param
    """
    img = param[0]
    edge_dict = param[1]
    first_pt = param[2]
    last_pt = param[3]
    if event == cv2.EVENT_LBUTTONDOWN:
        print('start', x, y)
        edge_dict[y] = [x]
        param[2] = [x, y]
        param[3] = [x, y]

    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON: # 按住鼠标进行拖动
        print(first_pt, last_pt)
        list = connect_pts(pt1=last_pt, pt2=[x, y]) # 将当前点与上一个点相连
        edge_dict, param[4] = add_dict(edge_dict, list)
        print('Move : (%d, %d)' % (x, y))
        cv2.line(img, tuple(last_pt), (x,y), (0, 0, 255), 1)
        param[3] = [x, y]


    elif event == cv2.EVENT_LBUTTONUP:
        """
        检查图像是否闭合, 若已经闭合, 返回.
        若尚未闭合, 链接当前点与第一个点.
        """
        if param[4] is False:
            extra_line_list = connect_pts([x,y], first_pt)
            edge_dict, param[4] = add_dict(edge_dict, extra_line_list)
            cv2.line(img, (x,y), tuple(first_pt), (0, 0, 255), 1)
        print('END: (%d, %d)' % (x, y))

class DrawLabel():
    """
    使用此 class 进行单幅图像圈画.
    """
    def __init__(self):
        # 变成dict以后就可以直接fill了:
        # 在同一个index里面, 先填满，然后空，再填满.
        self.edge_dict = {}
        self.first_pt = []
        self.last_pt =[]
        self.flag_closed = False

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
        cv2.setMouseCallback('draw label', draw_event, [self.img_edged, self.edge_dict,
            self.first_pt, self.last_pt, self.flag_closed])
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
        对于每一个index对应的value进行sort, 继而进行填空.
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
    # TODO: 点的数量不对.
    drawlabel = DrawLabel()
    fp = 'E:\gif\恶性\恶性\\0000041760管亚军1.gif'
    drawlabel.read_gif(fp)
    drawlabel.draw_edge()
    plt.subplot(1,2,1), plt.imshow(drawlabel.img_origin)
    plt.subplot(1,2,2), plt.imshow(drawlabel.img_edged)
    plt.show()
    # pt1 = [0,0]
    # pt2 = [2,2]
    # pt3 = [2,0]
    # pt4 = [0,2]
    # print(connect_pts(pt1,pt2))
    # print(connect_pts(pt1, pt3))
    # print(connect_pts(pt1, pt4))