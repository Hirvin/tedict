#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from functools import partial
from PyQt5.QtCore import QEvent, QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QWidget, QPushButton, QSlider,
                             QVBoxLayout, QLabel)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

####### temporal
_PATH = "sub.srt"
_STATE_NUM_FRAME = 1
_STATE_TIME = 2
_STATE_TXT = 3


class frame():
    def __init__(self, num, time, txt):
        self.num_frame = int(num)
        self.start = 0
        self.end = 0
        self.txt = txt
        self.get_time(time)

    def cov_milis(self, value):
        data = value.split(":")
        h = int(data[0]) * 3600 * 1000
        m = int(data[1]) * 60 * 1000
        d2 = data[2].split(',')
        s = int(d2[0]) * 1000
        mi = int(d2[1])

        return h + m + s + mi 

    def get_time(self, time):
        data = time.split(' --> ')
        self.start = self.cov_milis(data[0])
        self.end = self.cov_milis(data[1])

    def __str__(self):
        text = "num: %s \ntiempo: %s - %s\ntext: %s\n" %(str(self.num_frame), self.start, self.end, self.txt)
        return str(text)

class frames():
    def __init__(self, path):
        f = open(path, "r")
        self.text = f.read()
        f.close()
        self.list_frames = []
        self.get_frame()

    def get_frame(self):
        self.text = self.text.split("\n")


        # eliminando caracte raro del inicio
        if self.text[0] != '1':
            self.text[0] = '1'

        state = _STATE_NUM_FRAME
        for t in self.text:
            if t != '':
                if state == _STATE_NUM_FRAME:
                    num = int(t)
                    state = _STATE_TIME
                    continue
                if state == _STATE_TIME:
                    time = t
                    state = _STATE_TXT
                    continue
                if state == _STATE_TXT:
                    txt = t
                    state = _STATE_NUM_FRAME
                    self.list_frames.append(frame(num, time, txt))
                    continue

    def pop(self):
        return self.list_frames.pop(0)

    def print_frames(self):
        for f in self.list_frames:
            print(f)

#####################







# Ruta del archivo.
VIDEO_PATH = "/home/lhvelasc/Documentos/MisProyectos/Tedict/video.mp4"
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        # Controles principales para organizar la ventana.
        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()

        
        # time stuff
        self.time_layout = QHBoxLayout()
        self.label_time = QLabel()
        self.label_mi = QLabel()
        self.label_end = QLabel()


        self.label_sub = QLabel()

        # inicializar subtitulos
        self.list_frames = frames(_PATH)
        self.frame = self.list_frames.pop()
        
        # Control de reproducción de video de Qt.
        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer()
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(VIDEO_PATH)))
        self.media_player.setVideoOutput(self.video_widget)
        
        # Botones de reproducción y pausa.
        self.play_button = QPushButton("Pausa", self)
        self.stop_button = QPushButton("Detener", self)
        
        # Deslizadores para el volumen y transición del video.
        self.seek_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.media_player.volume())
        
        self.volume_slider.sliderMoved.connect(self.media_player.setVolume)
        
        # actualizar la posicion 

        self.seek_slider.sliderMoved.connect(self.change_media_player)
        self.media_player.positionChanged.connect(self.change_seek_bar)


        self.media_player.durationChanged.connect(self.change_duration)
        
        # Acomodar controles en la pantalla.
        self.layout.addWidget(self.video_widget)
        self.layout.addLayout(self.bottom_layout)
        self.layout.addLayout(self.time_layout)
        self.bottom_layout.addWidget(self.play_button)
        self.bottom_layout.addWidget(self.stop_button)
        self.bottom_layout.addWidget(self.volume_slider)

        # time stuff
        self.time_layout.addWidget(self.label_time)
        self.time_layout.addWidget(self.label_mi)
        self.time_layout.addWidget(self.label_end)

        self.layout.addWidget(self.seek_slider)
        self.layout.addWidget(self.label_sub)
        
        # Conectar los eventos con sus correspondientes funciones.
        self.play_button.clicked.connect(self.play_clicked)
        self.stop_button.clicked.connect(self.stop_clicked)
        self.media_player.stateChanged.connect(self.state_changed)
        
        
        # Personalizar la ventana.
        self.setWindowTitle("Reproductor de video")
        self.resize(800, 600)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        # Reproducir el video.
        self.media_player.play()
        

    def miles_minutes(self, value):
        s,ms= divmod(value, 1000)
        m,s=divmod(s,60)
        h,m=divmod(m,60)
        return h,m,s,ms

# modificar el valor del seek
    def change_media_player(self, value):
        self.media_player.setPosition(value)

    def change_seek_bar(self, value):

        if value > self.frame.end:
            self.frame = self.list_frames.pop()

        (h,m,s,ms) = self.miles_minutes(value)
        time = "%d:%d:%d.%d" % (h,m,s,ms)
        self.label_time.setText(time)
        self.label_mi.setText(str(value))
        self.label_end.setText(str(self.frame.end))
        


        self.label_sub.setText(self.frame.txt)
        self.seek_slider.setValue(value)

# se modifico la duracion
    def change_duration(self, value):
        self.seek_slider.setRange(0,value)

# senales relacionadas a eventos
    def play_clicked(self):
        """
        Comenzar o resumir la reproducción.
        """
        if (self.media_player.state() in
            (QMediaPlayer.PausedState, QMediaPlayer.StoppedState)):
            self.media_player.play()
        else:
            self.media_player.pause()
    
    def stop_clicked(self):
        """
        Detener la reproducción.
        """
        self.media_player.stop()
    
    def state_changed(self, newstate):
        """
        Actualizar el texto de los botones de reproducción y pausa.
        """
        states = {
            QMediaPlayer.PausedState: "Resumir",
            QMediaPlayer.PlayingState: "Pausa",
            QMediaPlayer.StoppedState: "Reproducir"
        }
        self.play_button.setText(states[newstate])
        self.stop_button.setEnabled(newstate != QMediaPlayer.StoppedState)
    
    def eventFilter(self, obj, event):
        """
        Establecer o remover pantalla completa al obtener
        el evento MouseButtonDblClick.
        """
        if event.type() == QEvent.MouseButtonDblClick:
            obj.setFullScreen(not obj.isFullScreen())
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())