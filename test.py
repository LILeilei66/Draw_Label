import unittest
from util.draw_label import connect_pts, add_dict
from util.draw_label import draw_event
import cv2
from numpy import zeros as npzeros

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
        edge_dict = {0: [0]}
        first_pt = [0,0]
        last_pt = [0,0]
        flag_closed = False
        param = [img, edge_dict, first_pt, last_pt, flag_closed]
        draw_event(event, x, y, flags, param)
        self.assertEqual(len(edge_dict), 3)

    def test_04_draw_event2(self):
        # 测试闭合探测
        event = cv2.EVENT_MOUSEMOVE
        x = 0
        y = 1
        flags = cv2.EVENT_FLAG_LBUTTON
        img = npzeros((10, 10))
        edge_dict = {0: [1, 2], 1: [1, 2]} #dict: {'row': [col, ...], ...}
        first_pt = [1, 1]
        last_pt = [2, 1] # list: [[col, row], ...]
        flag_closed = False
        param = [img, edge_dict, first_pt, last_pt, flag_closed]
        draw_event(event, x, y, flags, param)
        self.assertEqual(len(edge_dict[1]), 2)
        self.assertTrue(param[4])

    def test_05_draw_event3(self):
        # 非闭合自动补齐
        event = cv2.EVENT_LBUTTONUP
        x = 2
        y = 2
        flags = None
        img = npzeros((10, 10))
        edge_dict = {0: [0, 1, 2], 1: [2], 2: [2]} #dict: {'row': [col, ...], ...}
        first_pt = [0, 0]
        last_pt = [2, 2] # list: [[col, row], ...]
        flag_closed = False
        param = [img, edge_dict, first_pt, last_pt, flag_closed]
        draw_event(event, x, y, flags, param)
        self.assertEqual(len(edge_dict[1]), 2)
        self.assertTrue(param[4])


if __name__ == '__main__':
    unittest.main()
    # tests = Tests()
    # tests.test_05_draw_event3()