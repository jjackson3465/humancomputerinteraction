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
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QListWidget, QLabel, QCheckBox
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QListWidget
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

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

        # Validate credentials 
        if username == 'soflyah' and password == 'password':
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

            # Add images to sidebar2 (example: profile picture or achievements)
            self.add_images_to_sidebar(self.sidebar2, ["top_champs.png", "best_champs", "ban_champs"])

            # Triangle location
            triangle_x = self.width() - triangle_width
            triangle_y = self.triangle_y_initial

            self.triangle_button.setIcon(self.create_triangle_icon(Qt.LeftArrow))
            self.triangle_button.setGeometry(triangle_x, triangle_y, triangle_width, triangle_height)

        self.collapsed = not self.collapsed

    def add_images_to_sidebar(self, sidebar, image_paths):
        # Clear existing content in the sidebar
        for widget in sidebar.findChildren(QWidget):
            widget.deleteLater()

        # Remove the existing layout if it exists
        existing_layout = sidebar.layout()
        if existing_layout is not None:
            QWidget().setLayout(existing_layout)  # Break the connection to avoid memory leaks
            del existing_layout

        # Create a new layout for the sidebar
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Get the width of the sidebar
        sidebar_width = sidebar.width() - 20  # Adjust for padding

        # Add images to the sidebar
        for image_path in image_paths:
            label = QLabel(sidebar)

            # Load the image
            pixmap = QPixmap(image_path)

            if not pixmap.isNull():
                # Scale the image to the sidebar width, maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    sidebar_width,
                    pixmap.height(),  # Keep height proportional
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                label.setPixmap(scaled_pixmap)
            else:
                # If image fails to load, display placeholder text
                label.setText("Image not found")
                label.setAlignment(Qt.AlignCenter)

            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        # Set the new layout to the sidebar
        sidebar.setLayout(layout)

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
        file_path = 'match_hist.csv'
        df = pd.read_csv(file_path)

        # Create a frame for the data panel inside the red rectangle
        self.data_panel = QFrame(self)
        self.data_panel.setGeometry(20, 140, 560, 550)
        self.data_panel.setStyleSheet("""
            background-color: rgb(10, 20, 40); 
            border-radius: 12px; 
            border: 2px solid #444; 
            padding: 20px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
        """)

        # Main layout with horizontal split
        main_layout = QHBoxLayout(self.data_panel)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Create a smaller panel for stat selection
        stat_panel = QFrame(self.data_panel)
        stat_panel.setStyleSheet("""
            background-color: rgb(20, 30, 50); 
            border-radius: 12px; 
            border: 2px solid #444; 
            padding: 15px;
        """)
        stat_layout = QVBoxLayout(stat_panel)
        stat_layout.setSpacing(15)

        # Multi-select list for grouped stats
        self.stats_list_widget = QListWidget(stat_panel)
        self.stats_list_widget.addItem("K/D/A")  # Group kills, deaths, assists
        self.stats_list_widget.addItem("Items")  # Group all item stats
        self.stats_list_widget.addItem("Perks")  # Group perk stats
        self.stats_list_widget.addItem("Level")  # For champion level and basic info
        self.stats_list_widget.addItem("Gold")  # Group gold earned and minion kills
        self.stats_list_widget.addItem("Damage")  # Group total damage stats
        self.stats_list_widget.addItem("Vision")  # Vision score and wards placed
        self.stats_list_widget.setSelectionMode(QListWidget.MultiSelection)  # Enable multi-selection
        self.stats_list_widget.setStyleSheet("""
            QListWidget {
                background-color: rgba(0, 0, 0, 0.8);
                color: #aba98f;
                font-size: 15px;
                border: 2px solid #D4AF37;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #FFD700;
                color: black;
            }
        """)

        self.stats_list_widget.itemSelectionChanged.connect(self.filter_stats)  # Connect selection change
        stat_layout.addWidget(self.stats_list_widget)

        # Add the stat panel to the left side of the main layout (smaller area)
        main_layout.addWidget(stat_panel, 1)

        # Add a scroll area for the stats display (on the right, taking most of the space)
        self.scroll_area = QScrollArea(self.data_panel)
        self.scroll_area.setWidgetResizable(True)

        # Apply custom scrollbar stylesheet
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #1E1E1E;  /* Dark background for the scrollbar */
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #D4AF37;  /* Gold color for the scrollbar handle */
                border-radius: 6px;
                min-height: 20px;  /* Ensure the handle is always visible */
            }
            QScrollBar::handle:vertical:hover {
                background: #F1C40F;  /* Brighter gold on hover */
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: #1E1E1E;  /* Match background for scrollbar arrows */
                border: none;
            }
            QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
                background: #333333;  /* Slightly brighter for hover */
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;  /* Transparent background for empty space */
            }
        """)

        # Create a widget to hold the stat labels
        self.stats_widget = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.stats_widget)

        # Layout for the scrollable area
        self.stats_layout = QVBoxLayout(self.stats_widget)
        self.stats_layout.setSpacing(20)
        self.stats_widget.setLayout(self.stats_layout)

        # Display the selected stats by default
        self.display_stats(df, ["K/D/A"])  # Default stats to display
        main_layout.addWidget(self.scroll_area, 4)  # Add the scroll area to the right, taking more space

        self.data_panel.show()

    def filter_stats(self):
        selected_stats = [item.text() for item in self.stats_list_widget.selectedItems()]
        file_path = 'match_hist.csv'
        df = pd.read_csv(file_path)

        # Display the selected stats
        self.display_stats(df, selected_stats)

    def display_stats(self, df, stats):
        # Remove previous stats (if any)
        for widget in self.stats_widget.findChildren(QLabel):
            widget.deleteLater()

        # Add the selected stats to the panel
        for index, row in df.iterrows():
            # Determine win/loss color and label
            outcome = "Win" if row['win'] == "Win" else "Loss"
            outcome_color = "green" if outcome == "Win" else "red"
            
            # Champion name with the outcome (Win/Loss)
            stat_text = f"<b style='color:#C89B3C'>{row['champion']}:</b> <span style='color:{outcome_color};'>{outcome}</span><br>"

            # Handle grouped stats
            if "K/D/A" in stats:
                kda_text = f"<b style='color:#C89B3C'>K/D/A:</b> {row['kills']}/{row['deaths']}/{row['assists']}"
                stat_text += f"{kda_text}<br>"

            if "Items" in stats:
                items_text = f"<b style='color:#C89B3C'>Items:</b> {row['item0']}, {row['item1']}, {row['item2']}, {row['item3']}, {row['item4']}, {row['item5']}, {row['item6']}"
                stat_text += f"{items_text}<br>"

            if "Perks" in stats:
                perks_text = f"<b style='color:#C89B3C'>Keystone:</b> {row['perk_keystone']} <b style='color:#C89B3C'>Primary Perks:</b> {row['perk_primary_row_1']}, {row['perk_primary_row_2']}, {row['perk_primary_row_3']}, <b style='color:#C89B3C'>Secondary Perks:</b> {row['perk_secondary_row_1']}, {row['perk_secondary_row_2']}"
                stat_text += f"{perks_text}<br>"

            if "Level" in stats:
                champion_info = f"<b style='color:#C89B3C'>Level:</b> {row['champion_level']}"
                stat_text += f"{champion_info}<br>"

            if "Gold" in stats:
                gold_minions = f"<b style='color:#C89B3C'>Gold Earned:</b> {row['gold_earned']}, <b style='color:#C89B3C'>Minions Killed:</b> {row['total_minions_killed']}"
                stat_text += f"{gold_minions}<br>"

            if "Damage" in stats:
                damage_stats = f"<b style='color:#C89B3C'>Total Damage Dealt:</b> {row['total_damage_dealt_champions']}, <b style='color:#C89B3C'>Total Damage Taken:</b> {row['total_damage_taken']}"
                stat_text += f"{damage_stats}<br>"

            if "Vision" in stats:
                vision_stats = f"<b style='color:#C89B3C'>Vision Score:</b> {row['vision_score']}, <b style='color:#C89B3C'>Wards Placed:</b> {row['wards_placed']}"
                stat_text += f"{vision_stats}<br>"

            # Remove the last <br> tag to avoid trailing blank space
            stat_text = stat_text.rstrip('<br>')

            # Create a QLabel for the stat text
            label = QLabel(stat_text, self.stats_widget)
            label.setWordWrap(True)  # Enable text wrapping
            label.setStyleSheet("""
                color: #aba98f;
                font-size: 15px;
                padding: 12px;
                background-color: rgba(0, 0, 0, 0.4);
                border-radius: 8px;
                margin-bottom: 12px;
            """)
            label.setAlignment(Qt.AlignTop)  # Align text to the top of the box
            self.stats_layout.addWidget(label)

        # Ensure the layout stretches to accommodate the content properly
        self.stats_layout.addStretch()  # Add stretch at the end to ensure scroll area can expand















 







def main():
    app = QApplication(sys.argv)
    title_page = TitlePage()
    title_page.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
