from tkinter import *
import tkinter as tk
from tkinter import messagebox
import hashlib
from model.conexion import *
import requests

class App:
	"""docstring for App"""
	def __init__(self, app):
		self.window = app
		self.Etiquetas()
		self.Inputs()
		self.Botones()
		self.VerificarInternet()

	def Etiquetas(self):
		lbNombre = Label(self.window, text='Usuario', bg='#146094', fg='white').place(x=175, y=90)
		lbPass = Label(self.window, text='Contraseña', bg='#146094', fg='white').place(x=175, y=140)
		titulo = Label(self.window, text='LOGIN', font='Arial 25', bg='#146094', fg='white').place(x=200, y=30)

	def Inputs(self):
		self.nombre = StringVar()
		self.password = StringVar()
		self.inpNombre = Entry(self.window, textvariable=self.nombre, relief='flat').place(x=175, y=110)
		self.inpPass = Entry(self.window, textvariable=self.password, show='*', relief='flat').place(x=175, y=160)

	def Botones(self):
		self.btnSubmit = Button(self.window, text='Ingresar', width=9, bg='#14CD17', fg='#ffffff', relief='flat', cursor='hand1', command= lambda: self.Ingresar()).place(x=100, y=200)
		self.btnCerrar = Button(self.window, text='Salir',width=9, bg='red', fg='#ffffff', relief='flat', cursor='hand1', command= lambda: self.Salir()).place(x=300, y=200)


	def Ingresar(self):
		self.user = self.nombre.get()
		self.con = self.password.get()
		if self.user != '':
			if self.con != '':
				self.contraseña_cifrada = hashlib.sha512(self.con.encode())
				self.contraseña_cifrada_hexa = self.contraseña_cifrada.hexdigest()
				if self.contraseña_cifrada_hexa:
					self.data = Data()
					self.login = self.data.Login(self.user, self.contraseña_cifrada_hexa)
					if self.login is True:
						print('inicio exitoso')
						self.window.destroy()
						from interfaz import Interfaz
					else:
						self.msb = messagebox.showwarning('Error', 'Verifique sus Credenciales')
			else:
				self.msb = messagebox.showwarning('Error', 'Ingrese una Contraseña')
		else:
			self.msb = messagebox.showwarning('Error', 'Ingrese un Usuario')

	def VerificarInternet(self):
		url = "https://s3.amazonaws.com/dolartoday/data.json"
		try:
		    request = requests.get(url, timeout=5)
		except (requests.ConnectionError, requests.Timeout):
		    self.msb = messagebox.showinfo('Atencion', 'No hay Conexion a Internet')
		else:
		    print("Con conexión a internet.")

	'''
	def Registrar(self):
		self.user = self.nombre.get()
		self.con = self.password.get()
		if self.user != '':
			if self.con != '':
				self.contraseña_cifrada = hashlib.sha512(self.con.encode())
				self.contraseña_cifrada_hexa = self.contraseña_cifrada.hexdigest()
				if self.contraseña_cifrada_hexa:
					self.data = Data()
					self.data.NuevoUsuario(self.user, self.contraseña_cifrada_hexa)
	'''
		
	def Salir(self):
		msb = messagebox.askquestion('Salir', 'Quires Salir?')
		if msb == 'yes':
			self.window.destroy()
			print('salio de la interfaz login')


ventana = Tk()
ventana.geometry('500x300')
ventana.title('Sistema de gestion')
ventana.configure(background='#146094')
ventana.tk.call('wm', 'iconphoto', ventana._w, tk.PhotoImage(file='img/logo_albo.png'))
ventana.resizable(0,0)
aplicacion = App(ventana)
ventana.mainloop()