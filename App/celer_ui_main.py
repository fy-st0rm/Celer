import tkinter as tk
import tkinter.font
from tkinter import messagebox
from tkinter import ttk
from tkinter import messagebox
import platform
import threading
import socket

from encrypt import *


class main_ui:
	def __init__(self, user, network):
		self.window = tk.Tk(className = 'celer')

		# Networking stuff
		self.network = network
		self.running = True
		self.user = user
		self.key = ""

		#Importing stuff
		self.add_server_button_normal = tk.PhotoImage(file = 'Ui/Images/server_add_normal.png')
		self.join_server_button_normal = tk.PhotoImage(file = 'Ui/Images/server_join_normal.png')
		self.ok_button = tk.PhotoImage(file = 'Ui/Images/ok.png')
		self.logo = tk.PhotoImage(file = 'Ui/Images/logo.png')
		self.leave_server = tk.PhotoImage(file = 'Ui/Images/leave_server.png')

		#Defining General font
		self.font = tk.font.Font( family = 'Bahnschrift Light', size = 20)
		self.font2 = tk.font.Font( family = 'Bahnschrift Light', size = 10)
		self.font3 = tk.font.Font( family = 'Bahnschrift Light', size = 15)

		#Color list
		self.bgColor = 'white'
		self.secondarybgColor = '#f2f3f5'
		self.thirdbgColor = '#e3e5e8'
		self.fourthbgColor = '#d1d3d7'
		self.textColor = '#060607'
		self.selectColor = '#4f5660'
		self.primaryColor = '#b5b2ff'
		self.greyColor = '#878787'
		self.primaryfadedColor = '#bfbdff'
		self.primarydarkerColor = '#8682ff'

		#Defining stuff
		self.top_frame = tk.Frame(self.window, bg = self.bgColor)

		self.chatEntry = tk.Entry(self.window, width = 60, font = self.font, borderwidth = 0, bg = self.primaryfadedColor, fg= self.greyColor, text = 'Message!') #Chat text box!
		self.chatDisplay = tk.Text(self.window, width = 60, height = 18, font = self.font, bg = self.secondarybgColor, borderwidth = 0, relief='solid', highlightthickness=0, fg = self.primarydarkerColor)
		self.serverList = tk.Listbox(self.window, width = 0, height = 100,font = self.font, bg = self.secondarybgColor, fg = self.textColor, selectforeground=self.textColor, selectbackground = self.primaryColor, activestyle='none', borderwidth = 0, relief='solid', highlightthickness=0)
		self.serverSelect = self.serverList.curselection()
		self.serverCreatebutton = tk.Button(self.top_frame, command = self.createServer, image = self.add_server_button_normal, borderwidth = 0, relief='sunken', bg = self.bgColor, activebackground= self.primaryColor, highlightthickness=0, bd=0)
		self.serverJoinbutton = tk.Button(self.top_frame, command = self.joinServer, image = self.join_server_button_normal, borderwidth = 0, relief='sunken', bg = self.bgColor, activebackground=self.primaryColor, highlightthickness=0, bd=0)
		self.serverLeavebutton = tk.Button(self.top_frame, command = self.leaveServer, image = self.leave_server, borderwidth = 0, relief='sunken', bg = self.bgColor, activebackground=self.primaryColor, highlightthickness=0, bd=0)
		self.logo_img = tk.Label(self.window, image = self.logo, bg = self.bgColor)
		self.logo_text = tk.Label(self.window, text = 'Celer', bg = self.bgColor, font = self.font)

		self.infobox_create = tk.Label(self.window, width = 20, height = 5, text = 'Create your\n own server!', font = self.font2, bg = self.primaryfadedColor)
		self.infobox_join = tk.Label(self.window, width = 20, height = 5, text = "Join your\n friend's server!", font = self.font2, bg = self.primaryfadedColor)

		
		#Checks if enter is pressed
		self.chatEntry.bind('<Return>', self.chatEntryDataGet)

		#Checks if mouse 1 is pressed in the server list
		self.serverList.bind('<1>',self.connectServerselected)

		#Server list number temporary variable
		self.varNum = 0
		self.used = False

		#Gets the data of selected item from the list
		self.selectionServer = self.serverList.curselection()

		#Checks for the type of the os for fullscreen
		if platform.system() == "Linux":
			self.window.attributes('-zoomed', True)
		elif platform.system() == "Windows":
			self.window.state("zoomed")	

		self.serverCreatebutton.bind("<Enter>", self.change_color_create)	
		self.serverCreatebutton.bind("<Leave>", self.change_color_def_create)


		self.serverJoinbutton.bind("<Enter>", self.change_color_join)	
		self.serverJoinbutton.bind("<Leave>", self.change_color_def_join)	

		self.serverLeavebutton.bind("<Enter>", self.change_color_leave)
		self.serverLeavebutton.bind("<Leave>", self.change_color_def_leave)
	
	
		self.chatEntry.bind("<Enter>", self.del_lableText)

		self.chatEntry.insert(1,"Type your text here!")

	def __chat_ui(self):	
		self.chatDisplay.pack(side = 'top')
		self.chatEntry.pack(side = 'bottom')

		self.chatDisplay.config(state = "normal")
		self.chatDisplay.delete(1.0, "end")
		self.chatDisplay.config(state = "disabled")

	def winUI(self):
		self.window.geometry('940x500')
		self.window.wm_minsize(940, 500) #User can resize up to 940,500
		self.window.configure(bg=self.bgColor )
		self.window.mainloop()	

	def chatEntryDataGet(self,event):
		self.chatEntryData = self.chatEntry.get() #Puts the data in the variable
		self.chatEntry.delete(0, 'end')#Deletes the data written in entry
		
		# Sending the msg to server
		token = "[MSG]"
		enc_data = encrypt(f"[{self.user}]: {self.chatEntryData}\n", self.key)
		data = f"{token} {enc_data}"
		self.network.send(data)

	def __receiver(self):
		while self.running:
			recv_info = self.network.recv()
			tokens = recv_info.split(" ")

			if tokens[0] == "[DISCONNECT]":
				self.running = False

			elif tokens[0] == "[SERVER]":
				tokens.pop(0)
				self.serverList.delete(0,'end')#Deletes the old list to remove repeating list
				
				if len(tokens) > 0:
					for i in tokens:
						key = i.split(":")[0]
						name = i.split(":")[1]
						self.varNum+=1 #Server's position in the list
						self.serverNames = key+":"+name 
						self.serverList.insert(self.varNum,self.serverNames)#Inserts server list
				else:
					self.chatDisplay.pack_forget()
					self.chatEntry.pack_forget()

			# When server creation failed
			elif tokens[0] == "[REJECTED]":
				self.key = self.__create_sv(self.svName)	
				self.__join_sv(self.key)
			elif tokens[0] == "[ACCEPTED]":
				self.__join_sv(self.key)

			# When it catches a msg
			elif tokens[0] == "[MSG]":
				if len(tokens) > 1:
					self.chatDisplay.config(state = "normal")

					tokens.pop(0)
					enc_msg = " ".join(tokens)
					dec_msg = decrypt(enc_msg, self.key)
					self.chatDisplay.insert("end", dec_msg)
				
					self.chatDisplay.config(state = "disabled")

	def drawUI(self):
		self.logo_img.place(x=0,y=0)
		self.logo_text.place(x = 32, y=0)
		self.top_frame.pack(side = 'top')
		self.serverList.pack(side = 'left')
		self.serverCreatebutton.pack(side = "left")
		self.serverJoinbutton.pack(side = "left")
		self.serverLeavebutton.pack(side = 'left')
		



	def startUI(self):
		recv_thread = threading.Thread(target = self.__receiver)
		recv_thread.start()

		#Starts ui code
		self.drawUI()
		self.winUI()
		

	"""--------- Create server functions ----------"""
	def createServer(self):
		self.serverCreatewindow = tk.Toplevel(self.window) #Defining new window

		#Defining stuff
		self.serverName = tk.Entry(self.serverCreatewindow,width = 20, font = self.font3, borderwidth = 0, bg = self.primaryfadedColor, fg = self.textColor )
		self.serverCreatelabel = tk.Label(self.serverCreatewindow, text = 'Enter the name of the server:', font = self.font2, bg = self.secondarybgColor, fg = self.textColor)
		self.server_Createbutton = tk.Button(self.serverCreatewindow, command = self.revServername, image = self.ok_button, bg = self.secondarybgColor,relief='sunken', activebackground=self.primaryColor, borderwidth = 0, highlightthickness=0, bd=0)

		#Drawing stuff
		self.serverCreatelabel.place(x=100,y=0)
		self.serverName.place(x=80,y=60)
		self.server_Createbutton.place( x = 180, y = 140)

		self.server_Createbutton.bind("<Enter>", self.change_color_sv_Create)	
		self.server_Createbutton.bind("<Leave>", self.change_color_def_sv_Create)
		
		#Window property stuff
		self.serverCreatewindow.resizable(False, False)
		self.serverCreatewindow.title("Create Server")
		self.serverCreatewindow.geometry("390x180")
		self.serverCreatewindow.configure(bg = self.secondarybgColor)


	def revServername(self):
		self.svName = self.serverName.get()#Server Name data!
		if self.svName:
			self.key = self.__create_sv(self.svName)
			self.serverCreatewindow.destroy()#Destroys server create window
			tk.messagebox.showinfo("Information", "Server Created!") #Messages user that the server is created!

	def __create_sv(self, name):	
		# Sending the information about the creation of new server
		token = "[NEW_SV]"
		sv_key = generate_key()
		info = f"{token} key:{sv_key} name:{name}"
		self.network.send(info)
		return sv_key

	"""---------- Join server functions ----------"""
	def joinServer(self):
		self.serverJoinwindow = tk.Toplevel(self.window) #Defining new window

		#Defining stuff
		self.serverCode = tk.Entry(self.serverJoinwindow,width = 20, font = self.font3, borderwidth = 0, bg = self.primaryfadedColor, fg = self.textColor  )
		self.serverJoinlabel = tk.Label(self.serverJoinwindow, text = 'Enter the code of the server:', font = self.font2, bg = self.secondarybgColor, fg = self.textColor)
		self.serverJoin_button = tk.Button(self.serverJoinwindow, command = self.revServercode, image = self.ok_button, bg = self.secondarybgColor,relief='sunken', activebackground=self.primaryColor, borderwidth = 0, highlightthickness=0, bd=0)

		#Drawing stuff
		self.serverJoinlabel.place(x=100,y=0)
		self.serverCode.place(x=80,y=60)
		self.serverJoin_button.place( x = 180, y = 140)
		
		#Window property stuff
		self.serverJoinwindow.resizable(False, False)
		self.serverJoinwindow.title("Join Server")
		self.serverJoinwindow.geometry("390x180")
		self.serverJoinwindow.configure(bg = self.secondarybgColor)	

	def revServercode(self):
		self.svCode = self.serverCode.get()#Server code data!	
		if self.svCode:
			self.__join_sv(self.svCode)	
			self.serverJoinwindow.destroy()

	def __join_sv(self, key):	
		# Joining the sv
		token = "[JOIN]"
		info = f"{token} name:{self.user} key:{key}"
		self.network.send(info)

	def connectServerselected(self,event):
		self.selectedServer = self.serverList.get('anchor')#Gets the data from the selected itemr
		
		# Telling the server that we selected a server
		self.key = self.selectedServer.split(":")[0]
		self.network.send("[SELECT] " + self.key)

		self.chatEntry.pack_forget()
		self.chatDisplay.pack_forget()

		self.__chat_ui()

		"""---------- Leave server functions ----------"""	
	def leaveServer(self):
		self.serverLeavewindow = tk.Toplevel(self.window) #Defining new window

		#Defining stuff
		self.serverCodeL = tk.Entry(self.serverLeavewindow,width = 20, font = self.font3, borderwidth = 0, bg = self.primaryfadedColor, fg = self.textColor  )
		self.serverLeavelabel = tk.Label(self.serverLeavewindow, text = 'Enter the code of the server:', font = self.font2, bg = self.secondarybgColor, fg = self.textColor)
		self.serverLeave_button = tk.Button(self.serverLeavewindow, command = self.revServercode_leave, image = self.ok_button, bg = self.secondarybgColor,relief='sunken', activebackground=self.primaryColor, borderwidth = 0, highlightthickness=0, bd=0)

		#Drawing stuff
		self.serverLeavelabel.place(x=100,y=0)
		self.serverCodeL.place(x=80,y=60)
		self.serverLeave_button.place( x = 180, y = 140)
		
		#Window property stuff
		self.serverLeavewindow.resizable(False, False)
		self.serverLeavewindow.title("Leave Server")
		self.serverLeavewindow.geometry("390x180")
		self.serverLeavewindow.configure(bg = self.secondarybgColor)	


	def revServercode_leave(self):
		svCode = self.serverCodeL.get() 
		token = "[LEAVE]"
		info = f"{token} username:{self.user} key:{svCode}"
		self.network.send(info)

	def change_color_create(self,event):
		self.serverCreatebutton.config(bg  = self.primaryColor)	
		if self.window.state() == 'zoomed':
			self.infobox_create.place(x = 600, y = 50)


	def change_color_def_create(self,event):
		self.serverCreatebutton.config(bg = self.bgColor)
		self.infobox_create.place_forget()	

	
	def change_color_join(self,event):
		self.serverJoinbutton.config(bg  = self.primaryColor)
		if self.window.state() == 'zoomed':	
			self.infobox_join.place(x = 640, y = 50)


	def change_color_def_join(self,event):
		self.serverJoinbutton.config(bg = self.bgColor)	
		self.infobox_join.place_forget()

	def del_lableText(self,event):
		if self.used == False:
			self.chatEntry.config(fg = self.textColor)
			self.chatEntry.delete(0,"end")
			self.used = True		

	def change_color_sv_Create(self,event):
		self.server_Createbutton.config(bg = self.primaryColor)	

	def change_color_def_sv_Create(self,event):
		self.server_Createbutton.config(bg = self.secondarybgColor)	

	def change_color_leave(self,event):
		self.serverLeavebutton.config(bg = self.secondarybgColor)

	def change_color_def_leave(self,event):
		self.serverLeavebutton.config(bg = self.bgColor)	

