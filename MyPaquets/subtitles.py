#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

_STATE_NUM_FRAME = 1
_STATE_TIME = 2
_STATE_TXT = 3

_SUB_PATTERN = "[a-zA-Z0-9]"
_SUB_REPLACE = "*"

class sub_text_frame():
    def __init__(self, f1, f2):
        self.f1 = f1
        self.start = f1.start


        if f2 != None:
            self.f2 = f2
            self.end   = f2.end
        else:
            self.f2 = None
            self.end = f1.end

    def new_key(self, key_int):
        key = chr(key_int)

        if self.f1.is_buffer_empty() == False:
            self.f1.pop()
            return False
        
        
        print ("entra")
        self.f2.pop()
        return self.f2.is_buffer_empty()
       
        return False

        return True


        if self.f1.pop() == False:
            if self.f2.pop() == False:
                return True
        
        






class frame():
    def __init__(self, num, time, txt):
        self.num_frame = int(num)
        self.start = 0
        self.end = 0
        self.txt = txt
        self.get_time(time)
        self.bufer_start = []
        self.bufer_end = list(txt)

    def conv_asterisc(self, str):
        return re.sub(_SUB_PATTERN, _SUB_REPLACE, str)

    def get_txt_conver_asteric(self):
        return self.get_bufer_start() + self.conv_asterisc(self.get_bufer_end())

    def get_bufer_start(self):
        return"".join(str(x) for x in self.bufer_start)

    def get_bufer_end(self):
        return "".join(str(x) for x in self.bufer_end)


    def reset(self):
        self.bufer_start = []
        self.bufer_end = list(txt)

    def is_buffer_empty(self):
        if self.bufer_end == []:
            return True

        while re.match(_SUB_PATTERN, self.bufer_end[0]) == None:
            self.bufer_start.append(self.bufer_end.pop(0))
            if self.bufer_end == []:
                return True

        return False

    def pop(self):
        while self.bufer_end != []:

            c = self.bufer_end.pop(0)
            self.bufer_start.append(c)
            match = re.match(_SUB_PATTERN, c)
            if match != None:
                return True

        return False


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
        self.list_sub_text_frame = []
        self.get_frame()
        self.get_sub_text()
        self.Index = 0

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

    def get_sub_text(self):
        while self.list_frames != []:
            f1 = self.list_frames.pop(0)

            if self.list_frames != []:
                f2 = self.list_frames.pop(0)
            else :
                f2 = None
            self.list_sub_text_frame.append(sub_text_frame(f1, f2))

    def pop(self):
        if self.Index > len(self.list_sub_text_frame):
            return None

        text_frame = self.list_sub_text_frame[self.Index]
        self.Index = self.Index + 1
        return text_frame

    def reset_index(self):
        self.Index = 0


    def print_frames(self):
        for f in self.list_frames:
            print(f)


#f = frames(_PATH)
#f.print_frames()