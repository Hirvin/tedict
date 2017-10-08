
import sys

from functools import partial

from PyQt5.QtCore import QEvent, QUrl, Qt

from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,

                             QWidget, QPushButton, QSlider,

                             QVBoxLayout, QLabel)

from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

from PyQt5.QtMultimediaWidgets import QVideoWidget



app = QApplication(sys.argv)

w = QWidget()
