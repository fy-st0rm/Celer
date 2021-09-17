
#-- Ui lib imports
import tkinter as tk
import tkinter.font
from tkinter import ttk
from tkinter import messagebox


class Login:
	def __init__(self, network):
		self.network = network

		#-- Setting up window
		self.tk = tk.Tk()
		self.tk.geometry("900x600")
		self.tk.resizable(False, False)
		
		self.font = tk.font.Font( family = 'Bahnschrift Light', size = 20)

		#-- Calling functions
		self.__load_image()
		self.__background()	
		self.__init_notebook()

	def __load_image(self):
		self.background_image = tk.PhotoImage(file = "Ui/Images/bg.png")

		self.signin_active = tk.PhotoImage(file = "Ui/Images/signin_active.png")
		self.signin_inactive = tk.PhotoImage(file = "Ui/Images/signin_inactive.png")

		self.signup_active = tk.PhotoImage(file = "Ui/Images/signup_active.png")
		self.signup_inactive = tk.PhotoImage(file = "Ui/Images/signup_inactive.png")
	
	#------#
	# UIs  #
	#------#
	
	def __background(self):
		self.background = tk.Label(image = self.background_image)
		self.background.place(x = -1, y = 0)

	def __init_notebook(self):
		self.notebook = ttk.Notebook(self.tk, style = "TNotebook")
	
	def __tab_1(self):
		self.tab_1 = tk.Frame(self.notebook, width = 350, height = 500, bg = "white")

		#-- Initializing
		self.title_signin 			= tk.Label (self.tab_1, text = 'celer\nSign in Window', font = self.font, fg = '#6e6e6e', bg ='white')
		self.title_username_signin 	= tk.Label (self.tab_1, text = 'Username:', font = self.font, fg = '#6e6e6e', bg ='white')
		self.title_password_signin 	= tk.Label (self.tab_1, text = 'Password:', font = self.font, fg = '#6e6e6e', bg ='white')
		self.username_signin 		= tk.Entry (self.tab_1, bg = '#d6d6d6', width = 15, borderwidth = 0, font = self.font)
		self.password_signin 		= tk.Entry (self.tab_1, bg = '#d6d6d6', width = 15, borderwidth = 0, font = self.font, show = '*')
		self.button_signin 			= tk.Button(self.tab_1, image = self.signin_inactive, bg = 'white', borderwidth = 0, relief='sunken', highlightthickness=0, bd=0, command = self.__get_signin_info)
		
		#-- Rendering
		self.title_signin.place(x = 80, y = 0)
		self.title_username_signin.place(x = 30, y = 160)
		self.username_signin.place(x = 30, y = 200, height = 40)
		self.title_password_signin.place(x = 30, y = 260)
		self.password_signin.place(x = 30, y = 300, height = 40)
		self.button_signin.place(x = 40, y = 400)

	def __tab_2(self):
		self.tab_2 = tk.Frame(self.notebook, width = 350, height = 500, bg = "white")

		#i-- Initializing
		self.title_signup 			= tk.Label	(self.tab_2, text = 'celer\nSign up Window', font = self.font, fg = '#6e6e6e', bg ='white')
		self.title_username_signup 	= tk.Label	(self.tab_2, text = 'Username:', font = self.font, fg = '#6e6e6e', bg ='white')
		self.title_password_signup 	= tk.Label	(self.tab_2, text = 'Password:', font = self.font, fg = '#6e6e6e', bg ='white')
		self.username_signup 		= tk.Entry	(self.tab_2, bg = '#d6d6d6', width = 15, borderwidth = 0, font = self.font)
		self.password_signup 		= tk.Entry	(self.tab_2, bg = '#d6d6d6', width = 15, borderwidth = 0, font = self.font, show = '*')
		self.button_signup 			= tk.Button	(self.tab_2, image = self.signup_inactive, bg = 'white', borderwidth = 0, relief='sunken', highlightthickness=0, bd=0, command = self.__get_signup_info)	
		
		#-- Rendering
		self.title_signup.place(x = 80, y = 0)
		self.title_username_signup.place(x = 30, y = 160)
		self.username_signup.place(x = 30,y = 200, height = 40)
		self.title_password_signup.place(x = 30, y = 260)
		self.password_signup.place(x = 30, y = 300,height = 40)
		self.button_signup.place(x = 40, y = 400)

	#----------------#
	# Data transfers #
	#----------------#

	def __signin(self, username, password):	
		token = "[LOGIN]"
		info = f"{token} username:{username} password:{password}"
		self.network.send(info)

		# Reciving the reply from the server
		reply = self.network.recv()
		
		if reply == "[ACCEPTED]":
			self.tk.destroy()

		elif reply == "[REJECTED]":
			tk.messagebox.showerror("error", "username or password is wrong!")

	def __signup(self, username, password):
		if len(password) != 8:
			tk.messagebox.showerror("error", "Password should be 8 character long")
		else:
			token = "[SIGNUP]"
			info = f"{token} username:{username} password:{password}"
			self.network.send(info)

			# Reciving the reply from the server
			reply = self.network.recv()

			if reply == "[ACCEPTED]":
				self.tk.destroy()

			elif reply == "[REJECTED]":
				tk.messagebox.showerror("error", "username already exsists!")	

	#----------------#
	# Event Handlers #
	#----------------#
	
	def __get_signin_info(self):
		self.button_signin.config(image = self.signin_active)

		username = self.username_signin.get()
		password = self.password_signin.get()

		self.__signin(username, password)

	def __get_signup_info(self):
		self.button_signup.config(image = self.signup_active)

		username = self.username_signup.get()
		password = self.password_signup.get()
		
		self.__signup(username, password)

	#------#
	# Main #
	#------#

	def __render(self):
		self.__tab_1()
		self.__tab_2()

		self.notebook.place(x = 490,y = 30)
		
		self.tab_1.place(x = 0,y = 0, anchor = 'center')
		self.tab_2.place(x = 0,y = 0, anchor = 'center')
		self.notebook.add(self.tab_1, text = 'Signin')
		self.notebook.add(self.tab_2, text = 'Signup')	

	def run(self):
		self.__render()

		self.tk.mainloop()


