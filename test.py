<<<<<<< HEAD
import unittest
from util.draw_label import connect_pts, add_dict

class Tests(unittest.TestCase):
    def test_01_connect_pts(self):
        pt1 = [0, 0]
        pt2 = [2, 2]
        pt3 = [2, 0]
        pt4 = [0, 2]
        self.assertEqual(len(connect_pts(pt1, pt2)), 2)
        self.assertEqual(len(connect_pts(pt1, pt3)), 2)
        self.assertEqual(len(connect_pts(pt1, pt4)), 2)

    def test_02_add_dict(self):
        dict = {1: [2], 0: [1]}
        list = [[2,2],[1,1]]
        dict = add_dict(dict, list)
        self.assertEqual(len(dict.keys()), 3)
        self.assertEqual(len(dict[0]), 1)
        self.assertEqual(len(dict[1]), 2)
        self.assertEqual(len(dict[2]), 1)

if __name__ == '__main__':
=======
import unittest
from util.draw_label import connect_pts, add_dict

class Tests(unittest.TestCase):
    def test_01_connect_pts(self):
        pt1 = [0, 0]
        pt2 = [2, 2]
        pt3 = [2, 0]
        pt4 = [0, 2]
        self.assertEqual(len(connect_pts(pt1, pt2)), 2)
        self.assertEqual(len(connect_pts(pt1, pt3)), 2)
        self.assertEqual(len(connect_pts(pt1, pt4)), 2)

    def test_02_add_dict(self):
        dict = {1: [2], 0: [1]}
        list = [[2,2],[1,1]]
        dict = add_dict(dict, list)
        self.assertEqual(len(dict.keys()), 3)
        self.assertEqual(len(dict[0]), 1)
        self.assertEqual(len(dict[1]), 2)
        self.assertEqual(len(dict[2]), 1)

if __name__ == '__main__':
>>>>>>> d442b7d3103652f635b174b76ec685cc1002a646
    unittest.main()