import tkinter as tk
import tkinter.font
from tkinter import messagebox
from tkinter import ttk
from tkinter import messagebox
from celer_ui_main import*
import os
import json


class log_ui:
	def __init__(self, network):
		self.window = tk.Tk(className = 'celer')
		self.network = network


		#Importing stuff
		self.bg_img = tk.PhotoImage(file = 'Ui/Images/bg.png')
		self.button_nopressed = tk.PhotoImage(file = 'Ui/Images/notpressed.png')
		self.button_pressed = tk.PhotoImage( file = 'Ui/Images/pressed.png')
		self.button_nopressed_up = tk.PhotoImage( file = 'Ui/Images/notpressed_up.png')
		self.button_pressed_up = tk.PhotoImage( file = 'Ui/Images/pressed_up.png')

		#background
		self.bg = tk.Label(image = self.bg_img)

		#Tabs Setup
		self.notebook = ttk.Notebook(self.window,style="TNotebook")
		self.tab1 = tk.Frame(self.notebook, width = 350, height = 500, bg = 'white')
		self.tab2 = tk.Frame(self.notebook, width = 350, height = 500, bg = 'white')

		#Defining General font
		self.font = tk.font.Font( family = 'Bahnschrift Light', size = 20)

		#Wigets in tab1
		self.title_signin = tk.Label(self.tab1,text = 'celer\nSign in Window', font = self.font, fg = '#6e6e6e', bg ='white')
		self.title_username_signin = tk.Label(self.tab1,text = 'Username:', font = self.font, fg = '#6e6e6e', bg ='white')
		self.username_signin = tk.Entry(self.tab1, bg = '#d6d6d6', width = 15, borderwidth = 0, font = self.font)
		self.title_password_signin = tk.Label(self.tab1,text = 'Password:', font = self.font, fg = '#6e6e6e', bg ='white')
		self.password_signin = tk.Entry(self.tab1, bg = '#d6d6d6', width = 15, borderwidth = 0, font = self.font, show = '*')
		self.button_singnin = tk.Button(self.tab1, text = 'Signin!', command = self.getdataSignin, image = self.button_nopressed, bg = 'white', borderwidth = 0, relief='sunken', highlightthickness=0, bd=0)

		#Wigets in tab2
		self.title_signup = tk.Label(self.tab2,text = 'celer\nSign up Window', font = self.font, fg = '#6e6e6e', bg ='white')
		self.title_username_signup = tk.Label(self.tab2,text = 'Username:', font = self.font, fg = '#6e6e6e', bg ='white')
		self.username_signup = tk.Entry(self.tab2, bg = '#d6d6d6', width = 20, borderwidth = 0, font = self.font)
		self.title_password_signup = tk.Label(self.tab2,text = 'Password:', font = self.font, fg = '#6e6e6e', bg ='white')
		self.password_signup = tk.Entry(self.tab2, bg = '#d6d6d6', width = 20, borderwidth = 0, font = self.font, show = '*')
		self.button_singnup = tk.Button(self.tab2, text = 'Signup!', command = self.getdataSignup, image = self.button_nopressed_up, bg = 'white', borderwidth = 0, relief='sunken', highlightthickness=0, bd=0)	
		
	def drawUI(self):
		self.bg.place(x=-1, y=0)
		self.notebook.place(x=490,y=30)#Drawing notebook

		#Drawing widgets in tab1
		self.title_signin.place(x=80,y=0)
		self.title_username_signin.place(x = 30, y = 160)
		self.username_signin.place(x=30, y=200, height = 40)
		self.title_password_signin.place(x = 30, y = 260)
		self.password_signin.place(x = 30, y = 300, height = 40)
		self.button_singnin.place(x=40, y= 400)

		#Drawing widgets in tab2
		self.title_signup.place(x=80,y=0)
		self.title_username_signup.place(x=30,y=160)
		self.username_signup.place(x=30,y=200, height = 40)
		self.title_password_signup.place(x=30,y=260)
		self.password_signup.place(x=30,y=300,height=40)
		self.button_singnup.place(x=40,y=400)

		#Tab drawing stuff
		self.tab1.place(x =0,y=0, anchor = 'center')
		self.tab2.place(x =0,y=0, anchor = 'center')
		self.notebook.add(self.tab1, text = 'Signin')
		self.notebook.add(self.tab2, text = 'Signup')

	def __save_login_data(self, username, password):
		data = {"username": username, "password": password}
		
		with open(".celer", "w") as w:
			json.dump(data, w)

	def __read_login_data(self):
		data = {}
		
		with open(".celer", "r") as r:
			data = json.load(r)

		return data

	def __auto_login(self):
		if os.path.isfile(".celer"):
			data = self.__read_login_data()
			self.__login(data["username"], data["password"])


	def __login(self, username, password):
		token = "[LOGIN]"
		info = f"{token} username:{username} password:{password}"
		self.network.send(info)

		# Reciving the reply from the server
		reply = self.network.recv()
		
		if reply == "[ACCEPTED]":
			self.__save_login_data(username, password)

			self.window.destroy()
			self.mainUi = main_ui(username, self.network)
			self.mainUi.startUI()
			
		elif reply == "[REJECTED]":
			tk.messagebox.showerror("error", "username or password is wrong!")

	def getdataSignin(self):
		self.button_singnin.config(image = self.button_pressed)
		username = self.username_signin.get()#Variable for username of Tab1
		password = self.password_signin.get()#Variable for password of Tab1

		self.__login(username, password)

	def getdataSignup(self):
		self.button_singnup.config(image = self.button_pressed_up)
		username = self.username_signup.get()#Variable for username of Tab2
		password = self.password_signup.get()	#Variable for password of Tab2
		
		if len(password) != 8:
			tk.messagebox.showerror("error", "password limit is 8 characters!")		
		else:
			token = "[SIGNUP]"
			info = f"{token} username:{username} password:{password}"
			self.network.send(info)
			# Reciving the reply from the server
			reply = self.network.recv()

			if reply == "[ACCEPTED]":
				self.__save_login_data(username, password)
				
				self.window.destroy()
				self.mainUi = main_ui(username, self.network)
				self.mainUi.startUI()
			elif reply == "[REJECTED]":
				tk.messagebox.showerror("error", "username already exsists!")	

	def winUI(self):
		#Window setup
		self.window.geometry('900x600')	
		self.window.resizable(False, False)
	
		self.__auto_login()
		self.window.mainloop()
   
