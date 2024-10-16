from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFrame
from PyQt5.QtGui import QPixmap, QPolygon, QPainter, QColor, QIcon, QPen
from PyQt5.QtCore import QPoint, Qt, QSize
from PyQt5.QtMultimedia import QSound
import sys

class LandingPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('League of Legends - Home')

        self.label = QLabel(self)
        self.pixmap = QPixmap('landing_page.jpg')
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())

        self.button = QPushButton('MATCH HISTORY', self)
        self.button.setGeometry(385, 84, 150, 30)

        self.button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #aba98f;
                font-family: 'Arial', sans-serif;
                font-weight: 900;
                font-size: 13px;
                border: 2px solid rgba(0, 0, 0, 0);
            }
            QPushButton:hover {
                color: #D4AF37;
            }
        """)

        self.click_sound = QSound("click.wav")
        self.button.clicked.connect(self.on_button_click)
        self.setFixedSize(self.pixmap.width(), self.pixmap.height())

    def on_button_click(self):
        self.click_sound.play()
        self.open_match_history()

    def open_match_history(self):
        self.match_history_page = MatchHistoryPage()
        self.match_history_page.show()
        self.close()


class MatchHistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('League of Legends - Match History')

        # image for background
        self.label = QLabel(self)
        self.pixmap = QPixmap('match_history_default.jpg')
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())

        # Home Button
        self.home_button = QPushButton('HOME', self)
        self.home_button.setGeometry(200, 25, 100, 30)
        self.home_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #aba98f;
                font-family: 'Arial', sans-serif;
                font-weight: 900;
                font-size: 14px;
                border: 2px solid rgba(0, 0, 0, 0);
            }
            QPushButton:hover {
                color: #D4AF37;
            }
        """)

        self.click_sound = QSound("click.wav")
        self.home_button.clicked.connect(self.on_home_click)

        self.collapsed = False
        self.create_collapsible_widget()
        self.create_rectangles()  # draw rectangles

        self.setFixedSize(self.pixmap.width(), self.pixmap.height())

    # sidebar to toggle friends list
    def create_collapsible_widget(self):
        # sidebar settings
        sidebar_width = 225
        sidebar_height = self.height() + 110

        sidebar_x = self.width() + 415
        sidebar_y = 80

        # sidebar 1 start
        self.sidebar1 = QLabel(self)  # display image
        self.sidebar1.setGeometry(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
        
        # load image for sidebar 1
        pixmap = QPixmap('friends_list.jpg')
        self.sidebar1.setPixmap(pixmap)
        self.sidebar1.setScaledContents(True) 
        self.sidebar1.show()  # shown at start

        # sidebar 2 start
        self.sidebar2 = QFrame(self)
        self.sidebar2.setGeometry(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
        self.sidebar2.setStyleSheet("background-color: #1e1e1e;")
        self.sidebar2.hide()  # hidden at start

        # initial settings for triangle
        triangle_width, triangle_height = 30, 30
        self.triangle_x_initial = sidebar_x - triangle_width + 1 
        self.triangle_y_initial = sidebar_y + (sidebar_height // 2) - (triangle_height // 2)

        self.triangle_button = QPushButton(self)
        self.triangle_button.setGeometry(self.triangle_x_initial, self.triangle_y_initial, triangle_width, triangle_height)
        self.triangle_button.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.triangle_button.setIcon(self.create_triangle_icon(Qt.RightArrow))
        self.triangle_button.setIconSize(QSize(triangle_width, triangle_height))

        # link to the sidebar
        self.triangle_button.clicked.connect(self.toggle_sidebar)
        self.triangle_button.show()  # visible at start

    # triangle toggle button
    def create_triangle_icon(self, direction):
        size = QSize(35, 35)  
        polygon = QPolygon()

        if direction == Qt.LeftArrow:
            polygon = QPolygon([
                QPoint(0, size.height() // 2),
                QPoint(size.width(), 0),
                QPoint(size.width(), size.height())
            ])
        elif direction == Qt.RightArrow:
            polygon = QPolygon([
                QPoint(size.width(), size.height() // 2),
                QPoint(0, 0),
                QPoint(0, size.height())
            ])

        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)

        # color triangle
        painter = QPainter(pixmap)
        pen = QPen(QColor("#D4AF37"))  # gold outline
        pen.setWidth(4)  # thicker line
        painter.setPen(pen) 
        painter.setBrush(Qt.NoBrush)  # transparent
        painter.drawPolygon(polygon)
        painter.end()

        return QIcon(pixmap)

    def toggle_sidebar(self):
        triangle_width, triangle_height = 30, 30

        if self.collapsed:
            # show sidebar1 and hide sidebar2
            self.sidebar1.show()
            self.sidebar2.hide()

            self.triangle_button.setIcon(self.create_triangle_icon(Qt.RightArrow))
            self.triangle_button.setGeometry(self.triangle_x_initial, self.triangle_y_initial, triangle_width, triangle_height)
        else:
            # show sidebar2 and hide sidebar1
            self.sidebar1.hide()
            self.sidebar2.show()

            # triangle location
            triangle_x = self.width() - triangle_width
            triangle_y = self.triangle_y_initial

            self.triangle_button.setIcon(self.create_triangle_icon(Qt.LeftArrow))
            self.triangle_button.setGeometry(triangle_x, triangle_y, triangle_width, triangle_height)

        self.collapsed = not self.collapsed
    
    # placeholder rectangles
    def create_rectangles(self):
        # red rect
        self.rect1 = QFrame(self)
        self.rect1.setGeometry(0, 120, 600, 599)  
        self.rect1.setStyleSheet("border: 2px solid red;")

        # blue rect
        self.rect2 = QFrame(self)
        self.rect2.setGeometry(600, 120, 425, 300)  
        self.rect2.setStyleSheet("border: 2px solid blue;")

        # green rect
        self.rect3 = QFrame(self)
        self.rect3.setGeometry(600, 420, 425, 300)  
        self.rect3.setStyleSheet("border: 2px solid green;")

        # show at start
        self.rect1.show()
        self.rect2.show()
        self.rect3.show()

    def on_home_click(self):
        self.click_sound.play()
        self.go_to_home()

    def go_to_home(self):
        self.landing_page = LandingPage()
        self.landing_page.show()
        self.close()


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    landing_page = LandingPage()
    landing_page.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
