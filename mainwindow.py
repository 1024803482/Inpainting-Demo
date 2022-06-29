import numpy as np
import imageio
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import cv2
import PIL


class PaintingMainWindow(QWidget):
    def __init__(self):
        super(PaintingMainWindow, self).__init__()
        # 直接采用绝对布局
        # 设置空间尺寸
        window_width = 1100
        window_height = 800
        self.setFixedSize(window_width, window_height)
        self.windowCenter()

        # 初始化状态栏 statusBar
        self.statusBar = QStatusBar(self)
        self.statusBar.setFixedSize(200, 20)
        self.statusBar.move(0, window_height-20)
        self.statusBar.setStyleSheet('QStatusBar{color:rgb(20, 20, 20,);}')
        self.statusBar.showMessage("图像修复测试窗口", 3000)

        # 设置窗口标题
        self.setWindowTitle("图像修复测试")
        # 设置窗口Icon
        self.setWindowIcon(QIcon(QPixmap("./Icons/pulse.svg")))
        # 设置背景颜色
        self.setStyleSheet('QWidget{background-color:rgb(224, 224, 224);}')

        # 显示图片窗口设置
        show_width = window_width // 2 - 30
        show_height = show_width
        self.show_width = show_width
        self.show_height = show_height

        # 设置输入图像窗口 (需要绘图) raw_label
        self.raw_label = QLabel(self)
        self.raw_label.setFixedSize(show_width, show_height)
        self.raw_label.move(20, 60)
        self.raw_label.setAlignment(Qt.AlignCenter)
        canvas = QPixmap(show_width, show_height)
        canvas.fill(QColor(175, 175, 175))
        self.raw_label.setPixmap(canvas)
        # self.raw_label.setStyleSheet('QLabel{background-color:rgb(175, 175, 175);}')
        # 设置输入图像标题 raw_title
        self.raw_title = QLabel(self)
        self.raw_title.setFixedSize(show_width, 30)
        self.raw_title.move(20, 30)
        self.raw_title.setStyleSheet("QLabel{font-size:16px; font-weight:bold; font-family:Arial;"
                                     "color:rgb(30, 30, 30,); background-color:rgb(150, 150, 150);}")
        self.raw_title.setText("图像输入")
        self.raw_title.setAlignment(Qt.AlignCenter)

        # 设置输出图像窗口 result_label
        self.result_label = QLabel(self)
        self.result_label.setFixedSize(show_width, show_height)
        self.result_label.move(window_width-20-show_width, 60)
        self.result_label.setAlignment(Qt.AlignCenter)
        canvas = QPixmap(show_width, show_height)
        canvas.fill(QColor(175, 175, 175))
        self.result_label.setPixmap(canvas)
        # self.result_label.setStyleSheet('QLabel{background-color:rgb(175, 175, 175);}')
        # 输出图像标题设置 result_title
        self.result_title = QLabel(self)
        self.result_title.setFixedSize(show_width, 30)
        self.result_title.move(window_width-20-show_width, 30)
        self.result_title.setStyleSheet("QLabel{font-size:16px; font-weight:bold; font-family:Arial;"
                                        "color:rgb(30, 30, 30,); background-color:rgb(150, 150, 150);}")
        self.result_title.setText("修复结果")
        self.result_title.setAlignment(Qt.AlignCenter)

        # 设置状态显示窗口 state_label
        state_height = 100
        state_width = show_width
        self.state_label = QLabel(self)
        self.state_label.setFixedSize(state_width, state_height)
        self.state_label.setAlignment(Qt.AlignLeft)
        self.state_label.setStyleSheet("QLabel{font-size:15px; font-family:Arial;"
                                       "color:rgb(10, 10, 10,);background-color:rgb(200, 200, 200);}")
        self.state_label.move(20, window_height - state_height - state_height // 2)
        self.state_label.setWordWrap(True)
        # 状态窗口初始文字设置
        self.state_label.setText("图像修复测试窗口")
        # 状态窗口标题设置 state_title
        self.state_title = QLabel(self)
        self.state_title.setFixedSize(state_width, 30)
        self.state_title.move(20, window_height - state_height - state_height // 2 - 30)
        self.state_title.setStyleSheet("QLabel{font-size:16px; font-weight:bold; font-family:Arial;"
                                       "color:rgb(50, 50, 50,); background-color:rgb(175, 175, 175);}")
        self.state_title.setText("状态窗口")
        self.state_title.setAlignment(Qt.AlignCenter)

        # 按钮设置
        button_height = 50
        button_width = 100
        # 打开文件按钮 open_file_label
        self.open_file_label = QPushButton(self)
        self.open_file_label.setFixedSize(button_width, button_height)
        self.open_file_label.setStyleSheet("QPushButton{font-size:15px; font-family:Arial; font-weight:bold;"
                                           "color:rgb(50, 50, 50,); background-color:rgb(175, 175, 175, 100)}")
        self.open_file_label.setText("打开文件")
        self.open_file_label.move(window_width - show_width - 20 + 24, 100 + show_height + 25)
        self.open_file_label.clicked.connect(self.getFileName)

        # 图像修复按钮 inpaint_label
        self.inpaint_label = QPushButton(self)
        self.inpaint_label.setFixedSize(button_width, button_height)
        self.inpaint_label.setStyleSheet("QPushButton{font-size:15px; font-family:Arial; font-weight:bold;"
                                         "color:rgb(50, 50, 50,); background-color:rgb(175, 175, 175, 100)}")
        self.inpaint_label.setText("图像修复")
        self.inpaint_label.move(window_width - show_width - 20 + button_width + 48, 100 + show_height + 25)
        self.inpaint_label.clicked.connect(self.imageInpainting)

        # 保存图像 imsave_label
        self.imsave_label = QPushButton(self)
        self.imsave_label.setFixedSize(button_width, button_height)
        self.imsave_label.setStyleSheet("QPushButton{font-size:15px; font-family:Arial; font-weight:bold;"
                                        "color:rgb(50, 50, 50,); background-color:rgb(175, 175, 175, 100)}")
        self.imsave_label.setText("保存图像")
        self.imsave_label.clicked.connect(self.saveImage)
        self.imsave_label.move(window_width - show_width - 20 + 2 * button_width + 72, 100 + show_height + 25)

        # 保存图像 exit_label
        self.exit_label = QPushButton(self)
        self.exit_label.setFixedSize(button_width, button_height)
        self.exit_label.setStyleSheet("QPushButton{font-size:15px; font-family:Arial; font-weight:bold;"
                                      "color:rgb(50, 50, 50,); background-color:rgb(175, 175, 175, 100)}")
        self.exit_label.setText("退出程序")
        self.exit_label.move(window_width - show_width - 20 + 3 * button_width + 96, 100 + show_height + 25)
        self.exit_label.clicked.connect(QApplication.instance().quit)

        """ 相关参数设置 """
        self.raw_image = None
        self.result_image = None
        self.mask = None
        self.result_image = None
        self.lastPoint = QPoint()
        self.endPoint = QPoint()
        self.org_name = None

    def windowCenter(self):
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        w = (screen.width() - window.width()) // 2
        h = (screen.height() - window.height()) // 2 - 50
        self.move(w, h)

    def getFileName(self):  # 读取文件
        image_path, file_type = QFileDialog.getOpenFileName(self, "图像文件读取", "./", "*.JPG;;*.PNG")
        if image_path == '':
            self.state_label.setText("打开文件失败")
            self.statusBar.showMessage("打开文件失败", 3000)
            pass
        else:
            self.org_name = image_path.split('/')[-1]
            self.raw_image = imageio.imread(image_path)
            size = self.raw_image.shape
            h, w = size[0], size[1]
            if max([h, w]) > self.show_width - 20:
                ratio_h = 1.0 * (self.show_width - 20) / h
                ratio_w = 1.0 * (self.show_width - 20) / w
                ratio = min([ratio_h, ratio_w])
                h = int(ratio * h)
                w = int(ratio * w)
                self.raw_image = cv2.resize(self.raw_image, (w, h))
            self.raw_image[self.raw_image==255] = 254
            bg = 175 * np.ones((self.show_height, self.show_width, 3), dtype=np.uint8)
            top = self.show_height//2 - h//2
            down = top + h
            left = self.show_width//2 - w//2
            right = left + w
            bg[top:down, left:right] = self.raw_image
            imageio.imwrite("temp.png", bg)
            self.raw_label.setPixmap(QPixmap(QImage("./temp.png")))
            # self.raw_label.setPixmap(QPixmap(QImage(bg, self.show_width, self.show_height, self.show_width*3,
            #                                         QImage.Format.Format_RGB888)))
            canvas = QPixmap(self.show_width, self.show_height)
            canvas.fill(QColor(175, 175, 175))
            self.result_label.setPixmap(canvas)
            self.state_label.setText("成功打开文件：{}\n滑动鼠标生成掩码".format(image_path))
            self.statusBar.showMessage("成功打开文件", 3000)

    def imageInpainting(self):
        if self.raw_image is None:
            self.state_label.setText("需要加载超声图像")
            self.statusBar.showMessage("图像修复失败", 3000)
            pass
        else:
            image = self.raw_label.pixmap().toImage()
            size = image.size()
            s = image.bits().asstring(size.width() * size.height() * image.depth() // 8)  # format 0xffRRGGBB
            arr = np.frombuffer(s, dtype=np.uint8).reshape((size.height(), size.width(), image.depth() // 8))
            arr = arr[:, :, ::-1]
            image = arr[:, :, 1:4]
            size = self.raw_image.shape
            h, w = size[0], size[1]
            top = self.show_height // 2 - h // 2
            down = top + h
            left = self.show_width // 2 - w // 2
            right = left + w
            mask = image[top:down, left:right]
            if len(mask.shape) == 3:
                mask = np.mean(mask, axis=-1)
            mask = np.uint8(mask >= 252)
            self.result_image = cv2.inpaint(self.raw_image, mask, 3, cv2.INPAINT_NS)
            bg = 175 * np.ones((self.show_height, self.show_width, 3), dtype=np.uint8)
            bg[top:down, left:right] = self.result_image
            imageio.imwrite("temp.png", bg)
            self.result_label.setPixmap(QPixmap(QImage("./temp.png")))
            self.state_label.setText("图像修复完成")
            self.statusBar.showMessage("修复完成", 3000)

    def saveImage(self):
        if self.org_name is not None:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Image", self.org_name, "All Files (*)",)
        else:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Image", './image.png', "All Files (*)", )
        if self.result_image is None:
            self.state_label.setText("未读入图像")
            self.statusBar.showMessage("保存失败", 3000)
            pass
        elif filename == "":
            self.state_label.setText("修复图像未保存")
            self.statusBar.showMessage("保存失败", 3000)
            pass
        else:
            imageio.imwrite(filename, self.result_image)
            self.state_label.setText("修复图像保存成功：{}".format(filename))
            self.statusBar.showMessage("保存成功", 3000)

    def paintEvent(self, event):
        pp = QPainter(self.raw_label.pixmap())
        pp.setPen(QPen(Qt.white, 6, Qt.DashLine))
        # 根据鼠标指针前后两个位置绘制直线
        pp.drawLine(self.lastPoint, self.endPoint)
        # 让前一个坐标值等于后一个坐标值，
        # 这样就能实现画出连续的线
        self.lastPoint = self.endPoint
        painter = QPainter(self)
        painter.drawPixmap(20, 60, self.raw_label.pixmap())

    def mousePressEvent(self, event):
        # 鼠标左键按下
        if event.button() == Qt.LeftButton:
            self.lastPoint = QPoint(event.pos().x()-20, event.pos().y()-60)
            self.endPoint = self.lastPoint

    def mouseMoveEvent(self, event):
        # 鼠标左键按下的同时移动鼠标
        if event.buttons() and Qt.LeftButton:
            self.endPoint = QPoint(event.pos().x()-20, event.pos().y()-60)
            # 进行重新绘制
            self.update()
            self.statusBar.showMessage("制作掩码ing", 3000)

    def mouseReleaseEvent(self, event):
        # 鼠标左键释放
        if event.button() == Qt.LeftButton:
            self.endPoint = QPoint(event.pos().x()-20, event.pos().y()-60)
            # 进行重新绘制
            self.update()


def main():
    app = QApplication(sys.argv)
    window = PaintingMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
