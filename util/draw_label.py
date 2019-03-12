from matplotlib import image as mpimg
import matplotlib.pyplot as plt
import cv2


def draw_event(event, x, y, flags, param):
    img = param[0]
    edge_list = param[1]
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        edge_list.append((x, y))
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        edge_list.append((x, y))
        print('Move : (%d, %d)' % (x, y))
        print(edge_list.__len__())
        img = cv2.line(img, edge_list[-2], edge_list[-1], color=(255,255,255), thickness=1)
    elif event == cv2.EVENT_LBUTTONUP:
        print('END: (%d, %d)' % (x, y))
    return edge_list

class DrawLabel():
    def __init__(self):
        self.edge_list = []
        pass

    def read_gif(self, fp):
        self.img_origin = mpimg.imread(fp)


    def draw_label(self):
        cv2.namedWindow('draw label')
        cv2.setMouseCallback('draw label', draw_event, [self.img_origin, self.edge_list])
        while(1):
            cv2.imshow('draw label', self.img_origin)
            if cv2.waitKey() & 0xFF == 27:
                break
        # print('draw label')




if __name__ == '__main__':
    drawlabel = DrawLabel()
    fp = 'E:\gif\恶性\恶性\\0000041760管亚军1.gif'
    drawlabel.read_gif(fp)
    drawlabel.draw_label()
