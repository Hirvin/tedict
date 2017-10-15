#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from functools import partial
from PyQt5.QtCore import QEvent, QUrl, Qt,  pyqtSignal, QObject, pyqtSlot, QTimer
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QWidget, QPushButton, QSlider,
                             QVBoxLayout, QLabel, QSizePolicy, QSpacerItem)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

# my imports
import MyPaquets.subtitles as sub

import PyQt5.QtGui as QtGui


# My definitions
MY_PATH = "/home/lhvelasc/Documentos/MisProyectos/Tedict/"
SUB_PATH = "Subtitles/sub.srt"
VIDEO_PATH = "Videos/video.mp4"

_STATE_PAUSE = 0
_STATE_PLAY  = 1

MAX_NUM_LAB_SUB = 120



class mi_senal (QObject):
    sig = pyqtSignal(str)


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.my_state = _STATE_PLAY
        
        # Controles principales para organizar la ventana.
        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()    

        
        # Control de reproducción de video de Qt.
        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer()
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(MY_PATH + VIDEO_PATH)))
        self.media_player.setVideoOutput(self.video_widget)
        
        # Botones de reproducción y pausa.
        self.play_button = QPushButton("Pausa", self)
        self.stop_button = QPushButton("Detener", self)
        
        # Deslizadores para el volumen y transición del video.
        self.seek_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.media_player.volume())
        
        #self.volume_slider.sliderMoved.connect(self.media_player.setVolume)
        
        # actualizar la posicion 

        #self.seek_slider.sliderMoved.connect(self.change_media_player)
        


        #self.media_player.durationChanged.connect(self.change_duration)
        
        # Acomodar controles en la pantalla.
        self.layout.addWidget(self.video_widget)
        self.layout.addLayout(self.bottom_layout)

        self.layout.addWidget(self.seek_slider)



        self.bottom_layout.addWidget(self.play_button)
        self.bottom_layout.addWidget(self.stop_button)
        self.bottom_layout.addWidget(self.volume_slider)


        



              
        # Conectar los eventos con sus correspondientes funciones.
        self.play_button.clicked.connect(self.play_clicked)
        #self.stop_button.clicked.connect(self.stop_clicked)
        self.media_player.stateChanged.connect(self.state_changed)
        
        
        # Personalizar la ventana.
        self.setWindowTitle("Reproductor de video")
        self.resize(800, 600)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


        self.media_player.positionChanged.connect(self.pos_changed)
        
        # Reproducir el video.
        self.my_signal = mi_senal()
        self.my_signal.sig.connect(self.saySomeWords)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(500)
        self.parar = False

        self.media_player.setNotifyInterval(1000)
        self.media_player.play()

    def tick(self):
        #print ("este es mi timer")
        if self.parar == True:
            self.media_player.pause()
            self.timer.stop()

    # senales relacionadas a eventos
    @pyqtSlot(str)
    def saySomeWords(self, words):
        print (words)
        self.media_player.pause()


    def hand_my_signal(self):
        print ("Esta es mi senal")

    def play_clicked(self):
        """
        Comenzar o resumir la reproducción.
        """
        self.my_signal.sig.emit("hola a todo mundo")
        #if (self.media_player.state() in
        #    (QMediaPlayer.PausedState, QMediaPlayer.StoppedState)):
        #    self.media_player.play()
        #else:
        #    self.media_player.pause()

    def pos_changed(self, value):
        print ("la posicion es:%d" % (value))
        if value >= 4000:
            self.parar = True
        #    self.media_player.positionChanged.disconnect(self.pos_changed)
            
            #self.media_player.pause()

    def state_changed(self, newstate):
        print ("cambio de estado")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    print ("aaaaa")
    sys.exit(app.exec_())