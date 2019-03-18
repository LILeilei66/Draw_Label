from .ui.MainWindow import UiMainWindow
from .util.draw_label import DrawLabel
from PyQt5.QtWidgets import QApplication
import sys

class MainWindow(UiMainWindow):
    def __init__(self):
        super().__init__()
        self.start_btn.click.connect(self.start_main_func)

    def start_main_func(self):
        draw_label = DrawLabel()
        draw_label.draw_edge()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())