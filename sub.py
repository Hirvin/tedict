#!/usr/bin/python3
# -*- coding: utf-8 -*-

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


f = frames(_PATH)
f.print_frames()