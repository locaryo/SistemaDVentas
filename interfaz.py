from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from model.conexion import *
import requests


class Interfaz:
	"""docstring for Interfaz"""
	def __init__(self, interfaz):
		self.window_interfaz = interfaz
		self.Etiquetas()
		self.Inputs()
		self.Botones()
		self.Lista('')
		self.Carrito()
		self.ApiDolar()

	def Etiquetas(self):
		lbNombre = Label(self.window_interfaz, text='Producto', bg='#146094', fg='white').place(x=180, y=160)
		titulo = Label(self.window_interfaz, text='PRODUCTOS', font='Arial 25', bg='#146094', fg='white').place(x=100, y=100)
		precio_d = Label(self.window_interfaz, text='Dolar:', bg='#146095', fg='white').place(x=814, y=520)
		self.lbTotal = Label(self.window_interfaz, text='Bs:', fg='white', bg='#146094').place(x=831, y=413)
		self.lbTotalDolar = Label(self.window_interfaz, text='Dolar:', fg='white', bg='#146094').place(x=814, y=435)
		lbTools = Label(self.window_interfaz, text='Herramientas', fg='white', bg='#146094', font='Arial 19').place(x=120, y=300)

	def Inputs(self):
		self.nombre = StringVar()
		self.suma = DoubleVar()
		self.s = DoubleVar()
		self.total = DoubleVar()
		self.total = 0.0
		self.d = DoubleVar()
		self.pd = DoubleVar()

		self.inpNombre = Entry(self.window_interfaz, textvariable=self.nombre, relief='flat').place(x=130, y=180)
		self.inpTotal = Entry(self.window_interfaz, textvariable=self.suma, relief='flat', state='readonly', fg='red', bg='white').place(x=864, y=413, width=90)
		self.inpTotalDolar = Entry(self.window_interfaz, textvariable=self.pd, relief='flat', state='readonly', fg='red', bg='white').place(x=864, y=435, width=90)
		self.precio = Entry(self.window_interfaz, textvariable=self.d, relief='flat',bg='#146094', state='readonly', fg='green', width='13').place(x=864, y=520)


	def Botones(self):
		self.btnSubmit = Button(self.window_interfaz, text='Consultar', width=9, bg='#14CD17', fg='#ffffff', relief='flat' , cursor='hand1', command= lambda: self.consulta()).place(x=80, y=240)
		self.btnCerrar = Button(self.window_interfaz, text='Salir',width=9, bg='red', fg='#ffffff', relief='flat', cursor='hand1', command=lambda: self.Salir()).place(x=250, y=240)
		self.btnFacturar = Button(self.window_interfaz,text='Facturar', width='10', bg='#14CD17', fg='#ffffff', relief='flat', cursor='hand1').place(x=500, y=430)
		self.btnNuevoProducto = Button(self.window_interfaz, text='Nuevo Producto', width=13, bg='#14CD17', fg='#ffffff', relief='flat', cursor='hand1', command= lambda: self.nuevoItem()).place(x=50, y=350)
		self.btnRemover = Button(self.window_interfaz, text='Remover', width=10, bg='red', fg='#ffffff', relief='flat', cursor='hand1', command= lambda: self.removerCarrito()).place(x=660, y=430)
		self.btnPeso = Button(self.window_interfaz, text='Precio Peso', width=13, bg='#14CD17', fg='#ffffff', relief='flat', cursor='hand1').place(x=250, y=350)



	def Lista(self, ref):
		self.vista = ttk.Treeview(self.window_interfaz, columns=(0,1,2,3,4), show='headings')
		self.vista.heading(0, text='Producto')
		self.vista.heading(1, text='Peso')
		self.vista.heading(2, text='Categoria')
		self.vista.heading(3, text='Marca')
		self.vista.heading(4, text='Precio')
		self.vista.column(0, width='150', minwidth='150', stretch=NO, anchor=CENTER)
		self.vista.column(1, width='60', minwidth='60', stretch=NO)
		self.vista.column(2, width='100', minwidth='100', stretch=NO, anchor=CENTER)
		self.vista.column(3, width='120', minwidth='120',stretch=NO, anchor=CENTER)
		self.vista.column(4, width='90', minwidth='90',stretch=NO, anchor=CENTER)
		estilo = ttk.Style()
		estilo.theme_use('clam')
		estilo.configure('Treeview.Heading', relief='flat', background='#125EF5', foreground='white')
		self.vista.place(x=450, y=30, height='140')

		#Mostrar Producto en la lista
		d = Data()
		if d:
			print('base de datos traida')
			pro = d.Buscar(ref)
			if pro:
				self.vista.insert('', 'end', values=pro)
				print('datos en lista')
			else:
				ca = d.BuscarCategoria(ref)
				for x in ca or []:
					self.vista.insert('', 'end', values=x)

		#Agregar Item al Carrito
		self.vista.bind('<Double 1>', self.agregarCarrito)

	def Carrito(self):
		self.carrito = ttk.Treeview(self.window_interfaz, columns=(0,1,2), show='headings')
		self.carrito.heading(0, text='Producto')
		self.carrito.heading(1, text='Peso')
		self.carrito.heading(2, text='Precio')
		self.carrito.column(0, width='150', minwidth='150', stretch=NO, anchor=CENTER)
		self.carrito.column(1, width='150', minwidth='150', stretch=NO, anchor=CENTER)
		self.carrito.column(2, width='150', minwidth='150',stretch=NO, anchor=CENTER)
		estilo = ttk.Style()
		estilo.theme_use('clam')
		estilo.configure('Treeview.Heading', relief='flat', background='#125EF5', foreground='white')
		self.carrito.place(x=500, y=210, height='200')


	def consulta(self):
		self.producto =  self.nombre.get()
		if self.producto !='':
			self.Lista(self.producto)
			print('recibido')
		else:
			self.vista.delete(*self.vista.get_children())
			print('Llene el campo')
			print('campo limpio')


	def agregarCarrito(self, event):
		producto_c = StringVar()
		peso_c = StringVar()
		precio_c = StringVar()
		self.total = self.suma.get()
		self.a = 0.0
		fila = self.vista.identify_row(event.y)
		item = self.vista.item(self.vista.focus())
		if item:
			producto_f = item['values'][0]
			peso_f = item['values'][1]
			precio_f = item['values'][4]
			self.carrito.insert('', 'end', values=[producto_f, peso_f, precio_f])
			print('item agregado')
			if precio_f:
				self.a = self.total + float(precio_f)
				if self.a:
					ss = self.suma.set(self.a)
					#return ss
					self.PrecioEnDolar(self.a, self.dolar)
					

	def removerCarrito(self):
		selected_item = self.carrito.selection()
		self.resta = 0.0
		if selected_item:
			delete = self.carrito.delete(selected_item)
			b = self.carrito.get_children()
			for x in b:
				re = self.carrito.item(x)['values'][2]
				self.resta = self.resta - float(-re)
			print('item removido')	
			self.suma.set(self.resta)
			self.PrecioEnDolar(self.resta, self.dolar)


	def nuevoItem(self):
		#Ventana PopUp
		self.pop_nuevoItem = Toplevel(self.window_interfaz, background='#146094')
		self.pop_nuevoItem.geometry('400x400')
		#Consulta
		self.d = Data()
		self.categoria = self.d.LeerCategoria()
		self.marca = self.d.LeerMarca()
		#Labels
		Label(self.pop_nuevoItem, text='Nuevo Producto', bg='#146094', fg='white', font='Arial 20').place(x=100, y=5)
		Label(self.pop_nuevoItem, text='Nuevo Producto:', bg='#146094', fg='white').place(x=50, y=43)
		Label(self.pop_nuevoItem, text='Peso:', bg='#146094', fg='white').place(x=63, y=83)
		Label(self.pop_nuevoItem, text='Categoria:', bg='#146094', fg='white').place(x=63, y=123)
		Label(self.pop_nuevoItem, text='Marca:', bg='#146094', fg='white').place(x=63, y=163)
		Label(self.pop_nuevoItem, text='Precio:', bg='#146094', fg='white').place(x=63, y=203)
		Label(self.pop_nuevoItem, text='Codigo:', bg='#146094', fg='white').place(x=63, y=243)
		#Variables
		self.newProducto = StringVar()
		self.newPeso = StringVar()
		self.newCategoria = StringVar()
		self.newMarca = StringVar()
		self.newPrecio = IntVar()
		self.newCodigo = StringVar()
		#Entrys
		self.nuevo_producto = Entry(self.pop_nuevoItem, bd=0, textvariable=self.newProducto).place(x=170, y=43, width=120)
		self.nuevo_peso = Entry(self.pop_nuevoItem, bd=0, textvariable=self.newPeso).place(x=170, y=83, width=90)
		self.nuevo_categoria = ttk.Combobox(self.pop_nuevoItem, values=self.categoria, state='readonly', textvariable=self.newCategoria).place(x=170, y=123, width=120)
		self.nuevo_marca = ttk.Combobox(self.pop_nuevoItem, values=self.marca, textvariable=self.newMarca, state='readonly').place(x=170, y=163, width=120)
		self.nuevo_precio = Entry(self.pop_nuevoItem, bd=0, textvariable=self.newPrecio).place(x=170, y=203, width=90)
		self.nuevo_codigo = Entry(self.pop_nuevoItem, bd=0, textvariable=self.newCodigo).place(x=170, y=243, width=100)
		#Botones
		self.add_producto = Button(self.pop_nuevoItem, text='Registrar', width=9, bg='#14CD17', fg='#ffffff', relief='flat' , cursor='hand1', command=lambda: self.EnviarNuevoProducto()).place(x=50, y=300)
		self.add_cerrar = Button(self.pop_nuevoItem, text='Salir',width=9, bg='red', fg='#ffffff', relief='flat', cursor='hand1', command=self.pop_nuevoItem.destroy).place(x=250, y=300)
		

	def EnviarNuevoProducto(self):
		self.data = Data()
		a,b,c,d,e,f = self.newProducto.get(), self.newPeso.get(), self.newCategoria.get(), self.newMarca.get(), self.newPrecio.get(), self.newCodigo.get()
		if a != '' and b !='' and c != False and d != False and e != 0:
			producto_agregado = self.data.NuevoProducto(a,b,c,d,e,f)
			if producto_agregado is True:
				self.msb = messagebox.showinfo('Agregado', 'Producto Agregado')	
		else:
			Label(self.pop_nuevoItem, text='Llene todos los campos', bg='#146094', fg='red', font=25).place(x=110, y=350)

	def PrecioPeso(self):
		pass

	def Salir(self):
		msb = messagebox.askquestion('Salir', 'Quires Salir?')
		if msb == 'yes':
			self.window_interfaz.destroy()
			print('salio de la interfaz')


	def ApiDolar(self):
		url = "https://s3.amazonaws.com/dolartoday/data.json"
		response = requests.get(url)
		#print(response)
		    
		if response.status_code == 200:
			response_json = response.json()
			self.dolar = response_json['USD']['transferencia']
			return self.d.set(self.dolar)			
		
	def PrecioEnDolar(self, producto=(), usd=()):
		if producto != 0.0:
			multiplicacion = (float(producto) * 1)
			division = (multiplicacion / float(usd))
			resultado = round(division, 2)
			return self.pd.set(resultado)
		if producto == 0.0:
			cero = producto - producto
			return self.pd.set(cero)

ventana_interfaz = Tk()
ventana_interfaz.geometry('1000x550')
ventana_interfaz.title('Sistema de Ventas')
ventana_interfaz.configure(background='#146094')
ventana_interfaz.iconphoto(True, tk.PhotoImage(file='img/logo_albo.png'))
ventana_interfaz.resizable(0,0)
aplicacion = Interfaz(ventana_interfaz)
ventana_interfaz.mainloop()