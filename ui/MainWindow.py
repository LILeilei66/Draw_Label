from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWidgets import QFileDialog

import sys


class UiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_btn = QPushButton('开始绘图')
        self.src_btn = QPushButton('gif来源')
        self.dst_btn = QPushButton('存储位置')

        self.info_src = QLabel('图像来源位置：')
        self.info_dst = QLabel('图像存储位置：')
        self.src_txt = QLabel('')
        self.dst_txt = QLabel('')

        btn_box = QVBoxLayout()
        btn_box.addWidget(self.start_btn)
        btn_box.addWidget(self.src_btn)
        btn_box.addWidget(self.dst_btn)

        label_box = QVBoxLayout()
        label_box.addWidget(self.info_src)
        label_box.addWidget(self.src_txt)
        label_box.addWidget(self.info_dst)
        label_box.addWidget(self.dst_txt)

        main_layout = QVBoxLayout()
        main_layout.addLayout(btn_box)
        main_layout.addLayout(label_box)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.create_connection()

    def create_connection(self):
        self.src_btn.clicked.connect(self.get_src_dir)
        self.dst_btn.clicked.connect(self.get_dst_dir)

    def get_src_dir(self):
        self.src_dir = QFileDialog.getExistingDirectory()
        print(self.src_dir)
        self.src_txt.setText(self.src_dir)

    def get_dst_dir(self):
        self.dst_dir = QFileDialog.getExistingDirectory()
        print(self.dst_dir)
        self.dst_txt.setText(self.dst_dir)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = UiMainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
