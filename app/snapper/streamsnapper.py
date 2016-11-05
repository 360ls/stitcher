from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import Tkinter as tk
import threading
import datetime
import imutils
import cv2
import os

class StreamSnapper:

	def __init__(self, video_stream, output_path):
		self.video_stream = video_stream
		self.output_path = output_path
		self.frame = None
		self.thread = None
		self.stop_event = None

		self.root = tk.Tk()
		self.panel = None

		snap_button = tk.Button(self.root, text="Take Snap", command=self.take_snap)
		snap_button.pack(side="bottom", fill="both", expand="yes", padx=20, pady=20)

		self.stop_event = threading.Event()
		self.thread = threading.Thread(target=self.video_loop, args=())
		self.thread.start()

		self.root.wm_title("Stream Snapper")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)

	def video_loop(self):
			
			try:
				while not self.stop_event.is_set():
					# grab the frame from the video stream and resize it to
					# have a maximum width of 300 pixels
					self.frame = self.video_stream.read()
					self.frame = imutils.resize(self.frame, width=300)
			
					# OpenCV represents images in BGR order; however PIL
					# represents images in RGB order, so we need to swap
					# the channels, then convert to PIL and ImageTk format
					image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
					image = Image.fromarray(image)
					image = ImageTk.PhotoImage(image)
			
					# if the panel is not None, we need to initialize it
					if self.panel is None:
						self.panel = tk.Label(image=image)
						self.panel.image = image
						self.panel.pack(side="left", padx=10, pady=10)
			
					# otherwise, simply update the panel
					else:
						self.panel.configure(image=image)
						self.panel.image = image
	 
			except RuntimeError, e:
				print("[INFO] Caught a RuntimeError")

	def take_snap(self):
		timestamp = datetime.datetime.now()
		filename= "{}.jpg".format(timestamp.strftime("%Y-%m%d_%H-%M-%S"))
		target_path = os.path.sep.join((self.output_path, filename))

		cv2.imwrite(target_path, self.frame.copy())
		print("[INFO] Saved snapshot: {}".format(filename))

	def on_close(self):
		print("[INFO] Stopping Stream Snapper")
		self.stop_event.set()
		self.video_stream.stop()
		self.root.quit()

