
#-- UI lib imports
import tkinter as tk
import tkinter.font
from tkinter import messagebox

#-- Utils
import platform
import threading

#-- Celer libs
from encrypt import *


# A scrollable Frame
class ScrollableFrame(tk.Frame):
	def __init__(self, container, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		canvas = tk.Canvas(self)
		scrollbar = tk.Scrollbar(self, orient = "vertical", command = canvas.yview)
		self.scrollable_frame = tk.Frame(canvas)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: canvas.configure(
				scrollregion=canvas.bbox("all")
			)
		)
		
		#self.scrollable_frame.pack(fill = "both", expand  = True)
		canvas.create_window((0, 0), window = self.scrollable_frame, anchor = "nw")
		canvas.configure(yscrollcommand = scrollbar.set)
		
		scrollbar.pack(side = "left", fill = "y")
		canvas.pack(side = "left", fill = "both", expand=True)


class Celer:
	def __init__(self, user, network):
		self.user = user
		self.network = network
		self.running = True

		#-- Calling startup functions
		self.__setup_window()
	
		self.font = tk.font.Font(family = 'Bahnschrift Light', size = 15)

	def __setup_window(self):	
		#-- Settingup window
		self.root = tk.Tk()
		
		#Checks for the type of the os for fullscreen
		if platform.system() == "Linux":
			self.root.attributes('-zoomed', True)
		elif platform.system() == "Windows":
			self.root.state("zoomed")	
		
		self.canvas = tk.Canvas(self.root, bg = "gray")
		self.canvas.pack(fill = "both", expand = True)

	#-------------#
	# Ui Elements #
	#-------------#

	def __draw_sv_list(self):
		self.sv_list = ScrollableFrame(self.canvas)
		self.sv_list.config(width = 10)

		for i in range(100):
			label = tk.Label(self.sv_list.scrollable_frame, text=str(i), width=4, height=2, borderwidth=1, relief="solid", font=self.font)
			label.pack(side = "top", fill = "x", expand = True)

		self.sv_list.place(relx = 0.02, rely = 0.13, relwidth = 0.052, relheight = 0.85)

	def __draw_chat_box(self):
		self.chat_box = tk.Text(self.canvas)
		self.chat_box.place(relx = 0.1, rely = 0.13, relwidth = 0.75, relheight = 0.78)
		self.chat_box.configure(state = "disabled")

	def __draw_text_entry(self):
		self.text_entry = tk.Entry(self.canvas)
		self.text_entry.place(relx = 0.1, rely = 0.93, relwidth = 0.75, relheight = 0.05)

	def __draw_member_list(self):
		#[TODO] make a member list
		pass

	#------------#
	# Networking #
	#------------#
	def __receiver(self):
		while self.running:
			recv_info = self.network.recv()
			tokens = recv_info.split(" ")

			if tokens[0] == "[DISCONNECT]":
				self.running = False

			elif tokens[0] == "[SERVER]":
				tokens.pop(0)
				#[TODO] Push server names
			
			# When it catches a msg
			elif tokens[0] == "[MSG]":
				if len(tokens) > 1:
					self.chat_box.config(state = "normal")

					tokens.pop(0)
					enc_msg = " ".join(tokens)
					dec_msg = decrypt(enc_msg, self.key)
					self.chat_box.insert("end", dec_msg)
				
					self.chat_box.config(state = "disabled")
			"""
			# When server creation failed
			elif tokens[0] == "[REJECTED]":
				self.key = self.__create_sv(self.svName)	
				self.__join_sv(self.key)
			elif tokens[0] == "[ACCEPTED]":
				self.__join_sv(self.key)
			"""



	def __launch_reciver(self):
		recv_thread = threading.Thread(target = self.__receiver)
		recv_thread.start()

	#------#
	# Main #
	#------#

	def __render(self):
		self.__draw_sv_list()
		self.__draw_chat_box()
		self.__draw_text_entry()

	def run(self):
		self.__render()
		self.__launch_reciver()
		self.root.mainloop()


