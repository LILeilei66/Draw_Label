import unittest
from util.draw_label import connect_pts, add_dict
from util.draw_label import draw_event, DrawLabel
import cv2
from numpy import zeros as npzeros

class object():
    pass

class Tests(unittest.TestCase):
    def test_01_connect_pts(self):
        pt1 = [0, 0]
        pt2 = [0, 2]
        pt3 = [2, 2]
        pt4 = [2, 0]
        self.assertEqual(len(connect_pts(pt1, pt2)), 2)
        self.assertEqual(len(connect_pts(pt2, pt3)), 2)
        self.assertEqual(len(connect_pts(pt3, pt4)), 2)
        self.assertEqual(len(connect_pts(pt4, pt1)), 2)

    def test_02_add_dict(self):
        dict = {1: [2], 0: [1]}
        list = [[2,2],[1,1]]
        dict, _ = add_dict(dict, list)
        self.assertEqual(len(dict.keys()), 3)
        self.assertEqual(len(dict[0]), 1)
        self.assertEqual(len(dict[1]), 2)
        self.assertEqual(len(dict[2]), 1)

    def test_03_draw_event(self):
        # 测试通过draw_event添加点
        event = cv2.EVENT_MOUSEMOVE
        x = 1
        y = 2
        flags = cv2.EVENT_FLAG_LBUTTON
        img = npzeros((10, 10))
        edge_list = [[0,0]]
        param = object()
        setattr(param, 'img_edged', img)
        setattr(param, 'edge_list', edge_list)
        draw_event(event, x, y, flags, param)
        self.assertEqual(len(edge_list), 2)

    def test_04_save_edge(self):
        # 测试闭合探测
        drawlabel = DrawLabel()
        drawlabel.img_origin = npzeros((5,5))
        drawlabel.edge_list = [[0,1], [0, 2], [1, 2], [1, 1]]
        drawlabel.img_edged = drawlabel.img_origin.copy()
        drawlabel.save_edge()
        self.assertTrue(drawlabel.flag_closed)
        rows_list = sorted(drawlabel.edge_dict.keys())
        assert len(rows_list) == (rows_list[-1] - rows_list[0] + 1)  # 确认所有点均已补齐.

    def test_05_save_edge2(self):
        # 非闭合自动补齐
        drawlabel = DrawLabel()
        drawlabel.img_origin = npzeros((5,5))
        drawlabel.edge_list = [[0,1], [0, 3], [3,3]]
        drawlabel.img_edged = drawlabel.img_origin.copy()
        drawlabel.save_edge()
        self.assertTrue(drawlabel.flag_closed)
        rows_list = sorted(drawlabel.edge_dict.keys())
        assert len(rows_list) == (rows_list[-1] - rows_list[0] + 1)  # 确认所有点均已补齐.

    def test_06_fill_label(self):
        # 圈出部分填充
        import numpy as np
        drawlabel = DrawLabel()
        drawlabel.img_origin = npzeros((6, 6))
        drawlabel.img_edged = drawlabel.img_origin.copy()
        drawlabel.img_label = npzeros((6, 6))
        edge_dict = { 0: list(np.arange(5)),
                      1: [0, 4],
                      2: [0, 4],
                      3: [0, 4],
                      4: list(np.arange(5))}
        drawlabel.edge_dict = edge_dict
        drawlabel.flag_closed = True
        drawlabel.fill_label(255)
        self.assertEqual(drawlabel.img_label.sum(), 255 * 5 * 4)



if __name__ == '__main__':
    unittest.main()
    # tests = Tests()
    # tests.test_04_save_edge()