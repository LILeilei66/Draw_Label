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
    if abs(row1 - row2) > 1:
        """
        X|O|O
        O|O|O
        O|X|O 
        """
        if row1 < row2:
            for row in range(row1 + 1, row2 + 1): # 此线初始点即上一条线终点, 因此已经在dict中, 无需再添加.
                col = int((col2 - col1) / (row2 - row1) * (row - row1) + col1)
                line_list.append([col, row])
        elif row2 < row1:
            for row in range(row1 - 1, row2 - 1, -1):
                col = int((col2 - col1) / (row2 - row1) * (row - row1) + col1)
                line_list.append([col, row])
        assert len(line_list) == abs(pt1[1] - pt2[1])

    elif row1 == row2: # 填成直线.
        if col1 < col2:
            for col in range(col1+1, col2+1):
                line_list.append([col, row1])
        elif col2 < col1:
            for col in range(col1-1, col2-1, -1):
                line_list.append([col, row1])
        assert len(line_list) == abs(pt2[0] - pt1[0])

    else:
        line_list.append(pt2)
        assert len(line_list) == 1

    return line_list

def add_dict(dict, list, cnt=None, ):
    """
    将新的点 list 加入到之前的点 dict 中.
    :param dict: {'row': [col, ...], ...}
    :param list: [[col, row], ...]
    :return: dict, flag_closed: bool, 闭合与否.
    """

    try:
        assert  len(list) > 0
    except AssertionError:
        print(cnt)
        flag_closed = False
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

"""
def draw_event(event, x, y, flags, param):
    '''
    创建鼠标事件, 进行圈画.
    :param event:   CV2 内置的鼠标事件
    :param x:       鼠标位置.column 位置
    :param y:       鼠标位置.row 位置
    :param flags:   CV2 内置的鼠标FLAG, 判断是否左键为按下情况.
    :param param:   传入的额外参数, [图片, 边界点dict, 第一个点, 上一个点, 图形是否闭合]
    :return: param
    [self.img_edged, self.edge_dict, self.first_pt, self.last_pt, self.flag_closed]
    '''
    img = param.img_edged
    edge_dict = param.edge_dict
    first_pt = param.first_pt
    last_pt = param.last_pt
    flag_closed = param.flag_closed
    if event == cv2.EVENT_LBUTTONDOWN:
        print('start', x, y)
        edge_dict[y] = [x]
        param.first_pt = [x, y]
        param.last_pt = [x, y]

    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON: # 按住鼠标进行拖动
        if flag_closed is False:
            list = connect_pts(pt1=last_pt, pt2=[x, y]) # 将当前点与上一个点相连
            param.edge_dict, param.flag_closed = add_dict(edge_dict, list)
            print('Move : (%d, %d)' % (x, y))
            cv2.line(img, tuple(last_pt), (x,y), (0, 0, 255), 1)
            param.last_pt = [x, y]

    elif event == cv2.EVENT_LBUTTONUP:
        '''
        检查图像是否闭合, 若已经闭合, 返回.
        若尚未闭合, 链接当前点与第一个点.
        '''
        print(flag_closed)
        if flag_closed is False:
            extra_line_list = connect_pts([x,y], first_pt)
            param.edge_dict, param.flag_closed = add_dict(edge_dict, extra_line_list)
            cv2.line(img, (x,y), tuple(first_pt), (0, 0, 255), 1)
        print(param.flag_closed)
        print(param.edge_dict)
"""

def draw_event(event, x, y, flags, param):
    """
    怀疑如果操作太多, 有时长的影响.
    :param event:
    :param x:   col
    :param y:   row
    :param flags:
    :param param: [img, edge_list]
    :return:
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(param.edge_list) == 0:
            param.edge_list = [[x, y]] # [col, row]
        else:
            param.edge_list.append([x, y])
    elif flags == cv2.EVENT_FLAG_LBUTTON and event == cv2.EVENT_MOUSEMOVE:
        param.edge_list.append([x, y])
    elif flags == cv2.EVENT_LBUTTONUP:
        print('button up: ', x, y)
        param.edge_list.append([x, y])
        cv2.line(param.img_edged, tuple(param.edge_list[-1]), tuple(param.edge_list[0]), (0, 0,
        255),3)

    if len(param.edge_list) > 1:
        cv2.line(param.img_edged, tuple(param.edge_list[-2]), tuple(param.edge_list[-1]), (0, 0,
        255),3)


class DrawLabel():
    """
    使用此 class 进行单幅图像圈画.
    整体思路:
    =========
    1. draw: 在draw的时候存入edge_list, 并画线.
    2. 连线: 将 list 的点通过 connect 进行扩展.
    3. 存 dict: 将扩展后的点存入 dictionary.
    3. 闭合判断: 判断图像是否闭合, 若非则收尾相连.
    4. 交叉判断: 判断交叉并进行修剪.# TODO: 如果自己用的话，只要每次都不要交叉就好了.
    """
    def __init__(self):
        # 变成dict以后就可以直接fill了:
        # 在同一个index里面, 先填满，然后空，再填满.
        self.edge_dict = {}
        self.edge_list = []
        self.flag_closed = False

    def read_gif(self, fp):
        self.img_origin = mpimg.imread(fp)
        self.img_edged = self.img_origin.copy()
        height, width = self.img_origin.shape[:2]
        self.img_label = npzeros((height, width))

    def draw_edge(self):
        """
        通过 cv2 的鼠标事件, 画出边界.
        :return:
        """
        cv2.namedWindow('draw label')
        cv2.setMouseCallback('draw label', draw_event, self)
        while(1):
            # draw: 在draw的时候存入edge_list, 并画线.
            cv2.imshow('draw label', self.img_edged)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        assert abs(self.img_edged - self.img_origin).sum() != 0

    def save_edge(self):
        """
        1. 连线: 将 list 的点通过 connect 进行扩展.
        2. 存 dict: 将扩展后的点存入 dictionary.
        将 row 作为 edge_dict 的 index.
        :return:
        """
        self.edge_dict = {self.edge_list[0][1]: [self.edge_list[0][0]]}
        for i, point in enumerate(self.edge_list[1:]): # 将本点与前一个点比较
            expanded_list = connect_pts(self.edge_list[i], point)
            self.edge_dict, self.flag_closed = add_dict(self.edge_dict, expanded_list, i)
            if self.flag_closed is True:
                break

        # 3. 闭合判断: 判断图像是否闭合, 若非则收尾相连.
        if self.flag_closed is False:
            expanded_list = connect_pts(self.edge_list[-1], self.edge_list[0])
            self.edge_dict, self.flag_closed = add_dict(self.edge_dict, expanded_list)
            cv2.line(self.img_edged, tuple(self.edge_list[-1]), tuple(self.edge_list[0]), (0, 0,
        255),3)
            cv2.imshow('draw label', self.img_edged)

        # 4. 对于dict里面的每个index的值进行sort
        for key in self.edge_dict.keys():
            self.edge_dict[key] = sorted(self.edge_dict[key])

    def cut(self):
        """
        如果交叉, 进行修剪.
        :return:
        """
        pass

    def fill_label(self, flag):
        """
        填充画出的边界作为 label.
        使用 queue 来完成遍历填充.
        对于每一个index对应的value进行sort, 继而进行填空.
        :param flag: 良恶性, 良性为2, 恶性为1.
        :return:
        """
        assert self.flag_closed is True
        for row in self.edge_dict.keys():
            to_fill = True
            if len(self.edge_dict[row]) == 1: # 在上下出现一个角
                self.img_label[row, self.edge_dict[row][0]] = flag # 将此点标上
                continue
            for i in range(1, len(self.edge_dict[row])):  # 将当前点与上一个点比较.
                if to_fill is True:
                    col = self.edge_dict[row][i] # 当前点
                    last_col = self.edge_dict[row][i-1] # 上一个点
                    row = int(row)
                    self.img_label[row, last_col:col] = flag
                    if col - last_col > 1:  # 两点之间有距离需要填充
                        to_fill = False

                else:
                    to_fill = True
        assert self.img_label.sum() != 0
        # print('draw label')




if __name__ == '__main__':
    drawlabel = DrawLabel()
    fp = 'E:\gif\恶性\恶性\\0000041760管亚军1.gif'
    drawlabel.read_gif(fp)
    drawlabel.draw_edge()
    drawlabel.save_edge()
    drawlabel.fill_label(255)
    plt.subplot(1,3,1), plt.imshow(drawlabel.img_origin)
    plt.subplot(1,3,2), plt.imshow(drawlabel.img_edged)
    plt.subplot(1,3,3), plt.imshow(drawlabel.img_label)
    plt.show()
    for i in drawlabel.edge_dict.keys():
        if drawlabel.img_label[i,:].sum() == 0:
            print(i)
    # pt1 = [0,0]
    # pt2 = [2,2]
    # pt3 = [2,0]
    # pt4 = [0,2]
    # print(connect_pts(pt1,pt2))
    # print(connect_pts(pt1, pt3))
    # print(connect_pts(pt1, pt4))


