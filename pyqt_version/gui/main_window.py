from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSplitter,
    QWidget,
    QDesktopWidget,
)
from PyQt5.QtGui import QPalette, QColor

PRI_COLOR = "#00ADB5"
SEC_COLOR = "#393E46"
BKG_COLOR = "#222831"
TXT_COLOR = "#EEEEEE"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spotipy")
        self.showMaximized()

        self.screen = QDesktopWidget().screenGeometry()

        self.setAutoFillBackground(True)  # Enable background color customization
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(BKG_COLOR))
        self.setPalette(palette)

        mainDiv = self.initMainDiv()
        songDiv = self.initSongDiv()

        mainDivWidth = int(self.screen.width() * 0.75)
        songDivWidth = int(self.screen.width() * 0.25)

        # Create a splitter
        splitter = QSplitter()

        # Add main and song divs to the splitter
        splitter.addWidget(mainDiv)
        splitter.addWidget(songDiv)

        splitter.setSizes([mainDivWidth, songDivWidth])

        self.setCentralWidget(splitter)

    def initMainDiv(self):
        div = QWidget()
        layout = QVBoxLayout()

        # Playlist section
        playlist_label = QLabel("Your Playlist")
        playlist_label.setStyleSheet("font-size: 20px; padding: 5px")
        layout.addWidget(playlist_label)

        # Here you can add a list widget or other UI elements for managing the playlist
        # For example: playlist_list = QListWidget()

        # Add the playlist_list to the layout

        div.setLayout(layout)

        return div

    def initSongDiv(self):
        div = QWidget()
        layout = QVBoxLayout()

        # Header Label
        header_label = QLabel("Welcome to Spotipy")
        header_label.setStyleSheet(
            f"font-size: 24px; font-weight: bold; padding: 10px; color: {TXT_COLOR}"
        )
        layout.addWidget(header_label)

        # Buttons and controls
        control_layout = QHBoxLayout()

        play_button = QPushButton("Play")
        pause_button = QPushButton("Pause")
        skip_button = QPushButton("Skip")
        volume_up_button = QPushButton("Volume Up")
        volume_down_button = QPushButton("Volume Down")

        control_layout.addWidget(play_button)
        control_layout.addWidget(pause_button)
        control_layout.addWidget(skip_button)
        control_layout.addWidget(volume_down_button)
        control_layout.addWidget(volume_up_button)

        layout.addLayout(control_layout)
        div.setLayout(layout)

        return div

    def play_music(self):
        # Add your music playback logic here
        pass
