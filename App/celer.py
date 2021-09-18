
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
		self.canvas = tk.Canvas(self)
		scrollbar = tk.Scrollbar(self, orient = "vertical", command = self.canvas.yview)
		self.scrollable_frame = tk.Canvas(self.canvas)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: self.canvas.configure(
				scrollregion=self.canvas.bbox("all")
			)
		)
		
		#self.scrollable_frame.pack(fill = "both", expand  = True)
		self.canvas.create_window((0, 0), window = self.scrollable_frame, anchor = "nw")
		self.canvas.configure(yscrollcommand = scrollbar.set)
		
		scrollbar.pack(side = "left", fill = "y")
		self.canvas.pack(side = "left", fill = "both", expand=True)

	def clear(self):
		# Destroying and recreating the canvas
		self.scrollable_frame.destroy()

		self.scrollable_frame = tk.Canvas(self.canvas)
		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: self.canvas.configure(
				scrollregion=self.canvas.bbox("all")
			)
		)

		self.canvas.create_window((0, 0), window = self.scrollable_frame, anchor = "nw")


class Celer:
	def __init__(self, user, network):
		self.user = user
		self.network = network
		self.running = True
	
		self.labels = []

		#-- User datas
		self.key = None			# Key of the server we currently are
		self.sv_code = None		# Key of the server when we look in sv info
		self.server_list = []
	
		#-- Calling startup functions
		self.__setup_window()	

		#-- Fonts
		self.font = tk.font.Font(family = 'Bahnschrift Light', size = 15)
		self.font_2 = tk.font.Font(family = "Bahnschrift Light", size = 10)

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

	#----------------#
	# Event Handlers #
	#----------------#

	def __create_sv_ui(self):
		self.create_sv_window = tk.Toplevel(self.canvas)
		
		# Settings for window
		self.create_sv_window.resizable(False, False)
		self.create_sv_window.title("Create Server")
		self.create_sv_window.geometry("390x180")

		# Adding widgets
		label = tk.Label(self.create_sv_window, text = 'Server Name', font = self.font_2)
		label.place(x = 45, y = 65)

		self.sv_name_entry = tk.Entry(self.create_sv_window, width = 20, font = self.font)
		self.sv_name_entry.place(relx = 0.1, rely = 0.5, relwidth = 0.8, relheight = 0.2)

		self.sv_name_entry.bind("<Return>", self.__create_sv)

	def __get_join_data(self, e):
		sv_code = self.sv_key_entry.get()
		self.__join_sv(sv_code)

	def __join_sv_ui(self):		
		self.join_sv_window = tk.Toplevel(self.canvas)

		# Setting up window
		self.join_sv_window.resizable(False, False)
		self.join_sv_window.title("Join Server")
		self.join_sv_window.geometry("390x180")

		# Adding widgets
		label = tk.Label(self.join_sv_window, text = 'Server Key', font = self.font_2)
		label.place(x = 45, y = 65)

		self.sv_key_entry = tk.Entry(self.join_sv_window, width = 20, font = self.font)
		self.sv_key_entry.place(relx = 0.1, rely = 0.5, relwidth = 0.8, relheight = 0.2)

		self.sv_key_entry.bind("<Return>", self.__get_join_data)
		
	def __add_button_popup(self):
		# Displays the selection between create or join server
		
		x = self.root.winfo_pointerx()
		y = self.root.winfo_pointery()

		self.popup_1 = tk.Menu(self.canvas, tearoff = 0)

		self.popup_1.add_command(label = "Create server", command = self.__create_sv_ui)
		self.popup_1.add_command(label = "Join server"  , command = self.__join_sv_ui)

		self.popup_1.tk_popup(x, y, 0)

	def __show_sv_info(self, e):
		# Shows some information about the server u just selected

		label = e.widget
		sv_id = label.cget("text").split(":")[0]
		self.sv_code = self.server_list[int(sv_id)][0]	

		x = self.root.winfo_pointerx()
		y = self.root.winfo_pointery()

		self.popup_2 = tk.Menu(self.canvas, tearoff = 0)

		self.popup_2.add_command(label = self.sv_code)
		self.popup_2.add_command(label = "Leave server", command = self.__leave_server)
	
		self.popup_2.tk_popup(x, y, 0)


	#-------------#
	# Ui Elements #
	#-------------#

	def __draw_sv_list(self):
		self.sv_list = ScrollableFrame(self.canvas)
		self.sv_list.config(width = 10)
		self.sv_list.place(relx = 0.02, rely = 0.13, relwidth = 0.052, relheight = 0.85)

	def __draw_chat_box(self):
		self.chat_box = tk.Text(self.canvas)
		#self.chat_box.place(relx = 0.1, rely = 0.13, relwidth = 0.75, relheight = 0.78)
		self.chat_box.configure(state = "disabled")

	def __draw_text_entry(self):
		self.text_entry = tk.Entry(self.canvas)
		#self.text_entry.place(relx = 0.1, rely = 0.93, relwidth = 0.75, relheight = 0.05)
		self.text_entry.bind("<Return>", self.__send_msg)

	def __draw_member_list(self):
		#[TODO] make a member list
		pass

	def __add_button(self):
		self.add_button = tk.Button(self.canvas, text = "+", command = self.__add_button_popup)
		self.add_button.place(relx = 0.02, rely = 0.05, relwidth = 0.052, relheight = 0.05)
		

	#------------#
	# Networking #
	#------------#

	def __create_sv(self, e):
		if e != "retry":
			self.sv_name = self.sv_name_entry.get()
			self.create_sv_window.destroy()
		
		# Sending the server the info about creating a server
		token = "[NEW_SV]"
		self.key = generate_key()
		info = f"{token} key:{self.key} name:{self.sv_name}"
		self.network.send(info)

	def __join_sv(self, key):	
		# Sending the server the info about joining a server
		token = "[JOIN]"
		info = f"{token} name:{self.user} key:{key}"
		self.network.send(info)

	def __leave_server(self):
		token = "[LEAVE]"
		info = f"{token} username:{self.user} key:{self.sv_code}"
		self.network.send(info)

		# Reseting the key
		if self.key == self.sv_code:
			self.key == None

	def __select_server(self, e):
		for i in self.labels:
			i.configure(bg = "white")

		label = e.widget
		label.configure(bg = "#37d3ff")
		sv_id = label.cget("text").split(":")[0]
		self.key = self.server_list[int(sv_id)][0]	
		
		# Sending the server which server I selected
		token = "[SELECT]"
		info = f"{token} {self.key}"

		self.network.send(info)
		
		# Redrawing the chatbox and text entry
		self.chat_box.place(relx = 0.1, rely = 0.13, relwidth = 0.75, relheight = 0.78)
		self.text_entry.place(relx = 0.1, rely = 0.93, relwidth = 0.75, relheight = 0.05)
		
		self.chat_box.config(state = "normal")
		self.chat_box.delete("1.0", "end")
		self.chat_box.config(state = "disabled")

	def __send_msg(self, e):
		if self.key:	# Only if we have selected a server
			msg = self.text_entry.get()
			if msg != "":
				# Clearing the text entry
				self.text_entry.delete(0, "end")

				# Sending the encrypted msg to server
				token = "[MSG]"
				enc_msg = encrypt(f"[{self.user}]: {msg}\n", self.key)
				info = f"{token} {enc_msg}"
				self.network.send(info)

	def __receiver(self):
		# Listens for the upcoming data from the server

		while self.running:
			recv_info = self.network.recv()
			tokens = recv_info.split(" ")

			if tokens[0] == "[DISCONNECT]":
				self.running = False

			elif tokens[0] == "[SERVER]":
				tokens.pop(0)
				
				# Resetting
				self.key = None
				self.chat_box.place_forget()
				self.text_entry.place_forget()

				# Refreshing client side server storage
				self.server_list.clear()
				for i in tokens:
					key  = i.split(":")[0]
					name = i.split(":")[1]
					self.server_list.append((key, name))

				# Pushing server names
				self.sv_list.clear()
				self.labels.clear()

				for n, i in enumerate(tokens):
					server = i.split(":")
					name = server[1]
				
					if len(name) > 1:
						new_name = str(n) + ":" + name[0] + name[1]
					else:
						new_name = str(n) + ":" + name[0]

					label = tk.Label(self.sv_list.scrollable_frame, text = new_name, bg = "white", width=4, height=2, borderwidth=1, relief="solid", font=self.font)
					label.pack(side = "top", fill = "x", expand = True)
					label.bind("<Button-1>", self.__select_server)
					label.bind("<Button-3>", self.__show_sv_info)

					self.labels.append(label)

			# When it catches a msg
			elif tokens[0] == "[MSG]":
				if len(tokens) > 1:
					self.chat_box.config(state = "normal")

					tokens.pop(0)
					enc_msg = " ".join(tokens)
					dec_msg = decrypt(enc_msg, self.key)
					self.chat_box.insert("end", dec_msg)
					
					self.chat_box.see("end")
					self.chat_box.config(state = "disabled")
		
			# When server creation failed
			elif tokens[0] == "[REJECTED]":
				self.__create_sv("retry")	
			elif tokens[0] == "[ACCEPTED]":
				self.__join_sv(self.key)

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
		self.__add_button()

	def run(self):
		self.__render()
		self.__launch_reciver()
		self.root.mainloop()


