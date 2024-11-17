from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFrame, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QPolygon, QPainter, QColor, QIcon, QPen
from PyQt5.QtCore import QPoint, Qt, QSize
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import pandas as pd
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QUrl  # Corrected import for QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest





class TitlePage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('League of Legends - Title')

        # Set background image
        self.label = QLabel(self)
        self.pixmap = QPixmap('title_page.jpg')  # Make sure this file is accessible
        if not self.pixmap.isNull():  # Check if the image loaded successfully
            self.label.setPixmap(self.pixmap)
            self.setFixedSize(self.pixmap.width(), self.pixmap.height())
        else:
            print("Error: title_page.jpg not found or could not be loaded.")
            self.setFixedSize(800, 600)  # Default size if image fails

        # Create the clickable box
        self.clickable_box = QFrame(self)
        self.clickable_box.setGeometry(160, 660, 75, 75)  # x, y, w, h
        self.clickable_box.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0);
                border: 3px solid #D4AF37;  /* Gold border */
            }
            QFrame:hover {
                border: 3px solid #FFD700;  /* Brighter gold on hover */
            }
        """)

        # Load click sound
        self.click_sound = QSound("click.wav")  

        # Username text box
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("USERNAME")  
        self.username_input.setGeometry(55, 230, 290, 50)  # Position and size
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #D4AF37;
                border-radius: 5px;
                font-size: 14px;
                color: #aba98f;
                background-color: rgba(0, 0, 0, 0);
            }
            QLineEdit:focus {
                border: 2px solid #FFD700;  /* Highlight border on focus */
            }
        """)

        # Password text box
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("PASSWORD")  
        self.password_input.setGeometry(55, 300, 290, 50)  # Position and size
        self.password_input.setEchoMode(QLineEdit.Password)  # Mask password input
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #D4AF37;
                border-radius: 5px;
                font-size: 14px;
                color: #aba98f;
                background-color: rgba(0, 0, 0, 0);
            }
            QLineEdit:focus {
                border: 2px solid #FFD700;  /* Highlight border on focus */
            }
        """)
        
    # Initialize and load the YouTube video in the background
        self.preloaded_video_widget = QWebEngineView(self)
        self.preloaded_video_widget.setUrl(QUrl("https://www.youtube.com/embed/S1navXaTarQ?controls=0&rel=0"))
        self.preloaded_video_widget.hide()  # Keep it hidden on the TitlePage

    def mousePressEvent(self, event):
        # Check if the click was inside the box
        if self.clickable_box.geometry().contains(event.pos()):
            self.click_sound.play()
            self.check_credentials()

    def keyPressEvent(self, event):
        # Check if the "Enter" or "Return" key was pressed
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.check_credentials()
            
    def check_credentials(self):
        # Get text from username and password fields
        username = self.username_input.text()
        password = self.password_input.text()

        # Validate credentials soflyah
        if username == '' and password == '':
            self.open_landing_page()
        else:
            self.show_error_message()

    def show_error_message(self):
        # Display an error message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Login Failed")
        msg.setText("Incorrect username or password.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def open_landing_page(self):
        self.landing_page = LandingPage(preloaded_video_widget=self.preloaded_video_widget)
        self.landing_page.show()
        self.close()


class LandingPage(QWidget):
    def __init__(self, preloaded_video_widget):
        super().__init__()

        self.setWindowTitle('League of Legends - Home')

        self.label = QLabel(self)
        self.pixmap = QPixmap('landing_page.jpg')
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())

        self.button = QPushButton('MATCH HISTORY', self)
        self.button.setGeometry(385, 84, 150, 30)
        
        # Save the preloaded video widget
        self.preloaded_video_widget = preloaded_video_widget

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
        # Pass the preloaded video widget to MatchHistoryPage
        self.match_history_page = MatchHistoryPage(self.preloaded_video_widget)
        self.match_history_page.show()
        self.close()

class MatchHistoryPage(QWidget):
    def __init__(self, preloaded_video_widget):
        super().__init__()
        self.setWindowTitle('League of Legends - Match History')

        # Background image
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
        self.create_rectangles(preloaded_video_widget)  # draw rectangles with the preloaded video widget

        self.setFixedSize(self.pixmap.width(), self.pixmap.height())

    # Sidebar to toggle friends list
    def create_collapsible_widget(self):
        # Sidebar settings
        sidebar_width = 225
        sidebar_height = self.height() + 110

        sidebar_x = self.width() + 415
        sidebar_y = 80

        # Sidebar 1 start
        self.sidebar1 = QLabel(self)
        self.sidebar1.setGeometry(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
        
        # Load image for sidebar 1
        pixmap = QPixmap('friends_list.jpg')
        self.sidebar1.setPixmap(pixmap)
        self.sidebar1.setScaledContents(True)
        self.sidebar1.show()  # Shown at start

        # Sidebar 2 start
        self.sidebar2 = QFrame(self)
        self.sidebar2.setGeometry(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
        self.sidebar2.setStyleSheet("background-color: #1e1e1e;")
        self.sidebar2.hide()  # Hidden at start

        # Initial settings for triangle
        triangle_width, triangle_height = 30, 30
        self.triangle_x_initial = sidebar_x - triangle_width + 1 
        self.triangle_y_initial = sidebar_y + (sidebar_height // 2) - (triangle_height // 2)

        self.triangle_button = QPushButton(self)
        self.triangle_button.setGeometry(self.triangle_x_initial, self.triangle_y_initial, triangle_width, triangle_height)
        self.triangle_button.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.triangle_button.setIcon(self.create_triangle_icon(Qt.RightArrow))
        self.triangle_button.setIconSize(QSize(triangle_width, triangle_height))

        # Link to the sidebar
        self.triangle_button.clicked.connect(self.toggle_sidebar)
        self.triangle_button.show()  # Visible at start

    # Triangle toggle button
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

        # Color triangle
        painter = QPainter(pixmap)
        pen = QPen(QColor("#D4AF37"))  # Gold outline
        pen.setWidth(4)  # Thicker line
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)  # Transparent
        painter.drawPolygon(polygon)
        painter.end()

        return QIcon(pixmap)

    def toggle_sidebar(self):
        triangle_width, triangle_height = 30, 30

        if self.collapsed:
            # Show sidebar1 and hide sidebar2
            self.sidebar1.show()
            self.sidebar2.hide()

            self.triangle_button.setIcon(self.create_triangle_icon(Qt.RightArrow))
            self.triangle_button.setGeometry(self.triangle_x_initial, self.triangle_y_initial, triangle_width, triangle_height)
        else:
            # Show sidebar2 and hide sidebar1
            self.sidebar1.hide()
            self.sidebar2.show()

            # Triangle location
            triangle_x = self.width() - triangle_width
            triangle_y = self.triangle_y_initial

            self.triangle_button.setIcon(self.create_triangle_icon(Qt.LeftArrow))
            self.triangle_button.setGeometry(triangle_x, triangle_y, triangle_width, triangle_height)

        self.collapsed = not self.collapsed
    
    # Create rectangles with the preloaded video widget
    def create_rectangles(self, preloaded_video_widget):
        # Red rectangle
        self.rect1 = QFrame(self)
        self.rect1.setGeometry(0, 120, 600, 599)
        self.rect1.setStyleSheet("border: 2px solid red;")
        self.create_data_panels()  


        # Blue rectangle replaced with top_champs image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(600, 120, 425, 300)
        pixmap = QPixmap("top_champs.jpg")  # Load the image
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Scale the image to fit the label size

        # Load sound files
        self.sett_sound = QSound("sett.wav")
        self.lee_sin_sound = QSound("lee_sin.wav")
        self.yasuo_sound = QSound("yasuo.wav")

        # Three transparent buttons with hover effect inside the 'blue_box'
        self.button1 = QPushButton("", self)
        self.button1.setGeometry(622, 200, 120, 200)  # Adjust position and size
        self.button1.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);  /* Transparent */
                border: none;
            }
            QPushButton:hover {
                border: 2px solid black;  /* Black border on hover */
                border-radius: 5px;
            }
        """)
        # Play Sett sound and load Sett video
        self.button1.clicked.connect(lambda: [self.sett_sound.play(), self.load_video("https://www.youtube.com/embed/TzyCcImymXU?controls=0&rel=0")])

        self.button2 = QPushButton("", self)
        self.button2.setGeometry(745, 165, 130, 245)  # Adjust position and size
        self.button2.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);  /* Transparent */
                border: none;
            }
            QPushButton:hover {
                border: 2px solid black;  /* Black border on hover */
                border-radius: 5px;
            }
        """)
        # Play Lee Sin sound and load Lee Sin video
        self.button2.clicked.connect(lambda: [self.lee_sin_sound.play(), self.load_video("https://www.youtube.com/embed/S1navXaTarQ?controls=0&rel=0")])

        self.button3 = QPushButton("", self)
        self.button3.setGeometry(880, 200, 120, 200)  # Adjust position and size
        self.button3.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);  /* Transparent */
                border: none;
            }
            QPushButton:hover {
                border: 2px solid black;  /* Black border on hover */
                border-radius: 5px;
            }
        """)
        # Play Yasuo sound and load Yasuo video
        self.button3.clicked.connect(lambda: [self.yasuo_sound.play(), self.load_video("https://www.youtube.com/embed/F-NWK4ZVDYQ?controls=0&rel=0")])

        # Green rectangle with preloaded YouTube video
        self.video_widget = preloaded_video_widget
        self.video_widget.setParent(self)
        self.video_widget.setGeometry(600, 420, 425, 300)
        self.video_widget.setStyleSheet("border: 2px solid green;")
        self.video_widget.show()  # Show the preloaded video widget in the green rectangle

        # Show all components
        self.rect1.show()
        self.image_label.show()
        self.video_widget.show()
        self.button1.show()
        self.button2.show()
        self.button3.show()
        self.data_panel.show()
        self.create_data_panels()  





    # Method to load video in the green rectangle
    def load_video(self, url):
        self.video_widget.setUrl(QUrl(url))

    def on_home_click(self):
        self.click_sound.play()
        self.go_to_home()

    def go_to_home(self):
        self.landing_page = LandingPage(self.video_widget)  # Pass preloaded_video_widget here
        self.landing_page.show()
        self.close()

    def create_data_panels(self):
        # Path to the CSV file
        file_path = 'match_hist.csv'

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Create a frame for the data panel inside the red rectangle
        self.data_panel = QFrame(self)
        self.data_panel.setGeometry(20, 140, 560, 550)  # Adjust based on the red rectangle's position and size
        self.data_panel.setStyleSheet("""
            background-color: rgb(10, 20, 40); 
            border-radius: 10px; 
            border: 2px solid #444; 
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        """)

        # Add a vertical layout for content
        layout = QVBoxLayout(self.data_panel)
        layout.setSpacing(15)  # More spacing between items
        layout.setContentsMargins(15, 15, 15, 15)  # Comfortable margins

        # Initialize the network manager
        self.network_manager = QNetworkAccessManager(self)

        # Add content from the DataFrame
        for index, row in df.iterrows():
            # Get the image URL directly from the image_url column
            image_url = row['image_url']

            # Create a card-style widget for the item
            widget = QWidget(self.data_panel)
            widget.setStyleSheet("""
                background-color: rgb(20, 30, 60);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
                padding: 12px;
            """)

            # Create a horizontal layout inside the widget
            h_layout = QHBoxLayout(widget)
            h_layout.setSpacing(12)  # Spacing between icon and text
            h_layout.setContentsMargins(10, 10, 10, 10)

            # Create a QLabel for the champion icon
            icon_label = QLabel(widget)
            icon_label.setFixedSize(90, 90)  # Adjusted size for modern feel
            icon_label.setStyleSheet("""
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            """)

            # Set a placeholder image while the image is being loaded
            placeholder_pixmap = QPixmap(90, 90)
            placeholder_pixmap.fill(Qt.gray)
            icon_label.setPixmap(placeholder_pixmap)

            # Create a vertical layout for the text
            text_layout = QVBoxLayout()
            text_layout.setSpacing(5)
            text_layout.setContentsMargins(0, 0, 0, 0)

            # Create a QLabel for the champion's data (e.g. kills, deaths, assists)
            text_label = QLabel(f"{row['win']}", widget)
            text_label.setStyleSheet("""
                color: #D4AF37;
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
                text-align: left;
            """)
            text_layout.addWidget(text_label)

            # Create additional labels for other stats
            additional_stats = QLabel(f"""
                Gold: {row['gold_earned']} | Minions: {row['total_minions_killed']}
                Damage Dealt: {row['total_damage_dealt_champions']} | Damage Taken: {row['total_damage_taken']}
                CC Time: {row['total_time_crowd_controlled']}s | Vision Score: {row['vision_score']}
                Wards Placed: {row['wards_placed']}
            """, widget)
            additional_stats.setStyleSheet("""
                color: #B0B0B0;
                font-size: 12px;
                font-family: 'Segoe UI', sans-serif;
                text-align: left;
            """)
            text_layout.addWidget(additional_stats)

            # Add icon and stats to the horizontal layout
            h_layout.addWidget(icon_label)
            h_layout.addLayout(text_layout)

            # Add the widget to the panel layout
            layout.addWidget(widget)

            # Request the image from the URL (use the image_url column here)
            self.download_image(image_url, icon_label)

        # Show the data panel
        self.data_panel.show()

    def download_image(self, url, icon_label):
        # Create a request to download the image
        request = QNetworkRequest(QUrl(url))
        reply = self.network_manager.get(request)
        
        # Connect the finished signal to handle image download
        reply.finished.connect(lambda: self.on_image_downloaded(reply, icon_label))

    def on_image_downloaded(self, reply, icon_label):
        # If there are no errors in downloading
        if reply.error() == 0:
            image_data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            # Scale the pixmap to fit the icon's size (while maintaining aspect ratio)
            scaled_pixmap = pixmap.scaled(icon_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)

            # Center the image within the icon
            icon_label.setAlignment(Qt.AlignCenter)
        else:
            print(f"Error downloading image: {reply.errorString()}")




 







def main():
    app = QApplication(sys.argv)
    title_page = TitlePage()
    title_page.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
