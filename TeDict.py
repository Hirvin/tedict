#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from functools import partial
from PyQt5.QtCore import QEvent, QUrl, Qt, QTimer
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
_TIMER_TICK = 500
_NOTIFY_INTERVAL = 1000

class StatusLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.play_button = QPushButton("Pausa")
        self.stop_button = QPushButton("Detener")

        #labels
        self.frames = QLabel()
        self.num_frames = QLabel()
        self.aciertos = QLabel()
        self.num_aciertos = QLabel()
        self.fallos = QLabel()
        self.num_fallos = QLabel()

        #anadir elementos
        self.addWidget(self.play_button)
        self.addWidget(self.frames)
        self.addWidget(self.num_frames)
        self.addWidget(self.aciertos)
        self.addWidget(self.num_aciertos)
        self.addWidget(self.fallos)
        self.addWidget(self.num_fallos)
        self.addWidget(self.stop_button)

        self.frames.setText("Frame")
        self.num_frames.setText("0/31")
        self.aciertos.setText("Aciertos")
        self.num_aciertos.setText("0")
        self.fallos.setText("Fallos")
        self.num_fallos.setText("0")

class SubtitleLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()

        #layouts
        self.vLayout = QVBoxLayout()
        self.HSub1Layout = QHBoxLayout()
        self.HSub2Layout = QHBoxLayout()

        #labels
        self.labelSub1  = self.create_sub_labels(MAX_NUM_LAB_SUB)
        self.labelSub2  = self.create_sub_labels(MAX_NUM_LAB_SUB)


        #botones
        self.prev_button = QPushButton("Prev")
        self.next_button = QPushButton("Next")

        # llenar main layout
        self.addWidget(self.prev_button)
        self.addLayout(self.vLayout)
        self.addWidget(self.next_button)

        # llenar vertical layout
        self.vLayout.addLayout(self.HSub1Layout)
        self.vLayout.addLayout(self.HSub2Layout)
        self.add_lab_widget(self.HSub1Layout, self.labelSub1)
        self.add_lab_widget(self.HSub2Layout, self.labelSub2)

        # setear los tamanos adecuados de cada item del meu
        self.HSub1Layout.setSpacing(0)
        self.HSub2Layout.setSpacing(0)
        self.prev_button.setMaximumSize(50, 50)
        self.next_button.setMaximumSize(50, 50)


        # extras
        self.set_sub_text(self.labelSub1, "Hola a todos")
        self.set_sub_text(self.labelSub2, "Hola a todos")
        #self.labelSub1.setText("Hola a todos")   
        #self.labelSub2.setText("Karen")

    def create_sub_labels(self, n):
        l = []
        for i in range(n):
            l.append(QLabel())
        return l

    def add_lab_widget(self, parent, labs):
        for element in labs:
            parent.addWidget(element)

    def set_sub_text(self, lab, txt):
        if len(txt) > MAX_NUM_LAB_SUB:
            print ("No es posible imprimer el texto")
            print (len(txt))
            return

        if len(txt) != MAX_NUM_LAB_SUB:
            aux = MAX_NUM_LAB_SUB - len(txt)
            der = int(aux / 2)
            izq = int(aux - der)

        txt = " " * izq + txt + " " * der
        for i, t in enumerate(txt):
            lab[i].setText(t)  





class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.my_state = _STATE_PLAY
        
        # Controles principales para organizar la ventana.
        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()

        # status layout
        self.statusLayout = StatusLayout()

        # Sutitles layout
        self.subLayout = SubtitleLayout()

        # time stuff
        self.time_layout = QHBoxLayout()
        self.label_time = QLabel()
        self.label_mi = QLabel()
        self.label_end = QLabel()
        
        # inicializar subtitulos
        self.list_frames = sub.frames(MY_PATH + SUB_PATH)
        self.text_frame = self.list_frames.pop()
        
        # Control de reproducción de video de Qt.
        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer(None,  QMediaPlayer.VideoSurface)
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(MY_PATH + VIDEO_PATH)))
        self.media_player.setVideoOutput(self.video_widget)
        
        # Botones de reproducción y pausa.
        
        
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
        self.layout.addLayout(self.statusLayout)
        self.layout.addWidget(self.video_widget)
        self.layout.addLayout(self.bottom_layout)
        self.layout.addLayout(self.time_layout)
        self.layout.addWidget(self.seek_slider)

        # andir layout
        self.layout.addLayout(self.subLayout)
        #conections
        self.subLayout.prev_button.clicked.connect(self.click_prev)
        self.subLayout.next_button.clicked.connect(self.click_next)

        

        self.bottom_layout.addWidget(self.volume_slider)

        # time stuff
        self.time_layout.addWidget(self.label_time)
        self.time_layout.addWidget(self.label_mi)
        self.time_layout.addWidget(self.label_end)

        
        #self.set_sub_text(self.labels_sub2, self.frame.txt)
        self.subLayout.set_sub_text(self.subLayout.labelSub1, self.text_frame.f1.get_txt_conver_asteric())
        self.subLayout.set_sub_text(self.subLayout.labelSub2, self.text_frame.f2.get_txt_conver_asteric())
      
        # Conectar los eventos con sus correspondientes funciones.
        self.statusLayout.play_button.clicked.connect(self.play_clicked)
        self.statusLayout.stop_button.clicked.connect(self.stop_clicked)
        self.media_player.stateChanged.connect(self.state_changed)
        
        # Personalizar la ventana.
        self.setWindowTitle("Reproductor de video")
        self.resize(800, 600)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # setear Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_change_status)
        self.timer.start(_TIMER_TICK)
        
        # Reproducir el video.
        self.media_player.setNotifyInterval(_NOTIFY_INTERVAL)
        self.media_player.play()

    def miles_minutes(self, value):
        s,ms= divmod(value, 1000)
        m,s=divmod(s,60)
        h,m=divmod(m,60)
        return h,m,s,ms

# modificar el valor del seek
    def change_media_player(self, value):
        self.media_player.setPosition(value)

    def timer_change_status(self):
        #print ("timer")
        if self.my_state == _STATE_PAUSE:
            self.media_player.pause()
            self.timer.stop()

    def change_seek_bar(self, value):
        if self.my_state == _STATE_PLAY:
            # detiene la ejecusion del video si el frame ya acabo
            if value > self.text_frame.end:
                self.my_state = _STATE_PAUSE


        #if (value > self.text_frame.end and self.my_state == _STATE_PLAY):
        #    print ("pasa")
        #    self.media_player.pause()
        #    self.my_state = _STATE_PAUSE
            
            #self.text_frame = self.list_frames.pop()
            #if self.text_frame != None:
            #    self.sub_text_lab1       = self.text_frame.txt1
            #    self.sub_text_lab2       = self.text_frame.txt2
            #else :
            #    self.sub_text_lab1       = ""
            #    self.sub_text_lab2       = ""
            #    self.text_frame.end = 0

            #print ("casa")

            (h,m,s,ms) = self.miles_minutes(value)
            time = "%d:%d:%d.%d" % (h,m,s,ms)
            self.label_time.setText(time)
            self.label_mi.setText(str(value))
            self.label_end.setText(str(self.text_frame.end))
            


            #self.label_sub1.setText(self.frame.txt)
            #self.set_sub_text(self.labels_sub1, self.sub_text_lab1)
            #self.set_sub_text(self.labels_sub2, self.sub_text_lab2)
            self.seek_slider.setValue(value)

        return True

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

    def click_prev(self):
        if self.my_state == _STATE_PLAY:
            self.media_player.pause()
        self.timer.stop()
        self.media_player.setPosition(self.text_frame.start)
        self.timer.start(_TIMER_TICK)
        self.media_player.play()
        self.my_state = _STATE_PLAY

    def click_next(self):
        if self.my_state == _STATE_PLAY:
            self.media_player.pause()
        self.timer.stop()
        self.text_frame = self.list_frames.pop()
        self.media_player.setPosition(self.text_frame.start)
        self.timer.start(_TIMER_TICK)
        self.media_player.play()
        self.my_state = _STATE_PLAY

        self.subLayout.set_sub_text(self.subLayout.labelSub1, self.text_frame.f1.get_txt_conver_asteric())
        self.subLayout.set_sub_text(self.subLayout.labelSub2, self.text_frame.f2.get_txt_conver_asteric())

    
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
        self.statusLayout.play_button.setText(states[newstate])
        self.statusLayout.stop_button.setEnabled(newstate != QMediaPlayer.StoppedState)
    
    def eventFilter(self, obj, event):
        """
        Establecer o remover pantalla completa al obtener
        el evento MouseButtonDblClick.
        """
        if event.type() == QEvent.MouseButtonDblClick:
            obj.setFullScreen(not obj.isFullScreen())
        return False

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            if event.key() == Qt.Key_Space:
                print ("tecla space")
            else:
                #print (event.key())
                if self.text_frame.new_key(event.key()) == True:
                    print("cambiar al siguiente Frame")
                    self.text_frame = self.list_frames.pop()
                    if self.my_state == _STATE_PLAY:
                        self.media_player.pause()
                    self.media_player.setPosition(self.text_frame.start)
                    self.timer.start(_TIMER_TICK)
                    self.media_player.play()
                    self.my_state = _STATE_PLAY


                self.subLayout.set_sub_text(self.subLayout.labelSub1, self.text_frame.f1.get_txt_conver_asteric())
                self.subLayout.set_sub_text(self.subLayout.labelSub2, self.text_frame.f2.get_txt_conver_asteric())

            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())