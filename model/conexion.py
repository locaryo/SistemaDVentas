import sqlite3

class Data():
	"""docstring for Data"""
	def __init__(self):
		self.db = sqlite3.connect('app.db')
		self.cursor = self.db.cursor()

	def Buscar(self, pro=()):
		
		sql = "SELECT nombreP, peso , CATEGORIA.categoria as CATEGORIA , MARCA.marca as MARCA , precio FROM PRODUCTOS INNER JOIN CATEGORIA ON CATEGORIA.id = PRODUCTOS.id_categoria INNER JOIN MARCA ON MARCA.id = PRODUCTOS.id_marca WHERE nombreP = '{}'".format(pro)
		if pro:
			if self.cursor.execute(sql) :
				print('sql producto procesado')
				self.result = self.cursor.fetchone()
				if self.result:
					print('producto encontrado')
					print('producto retornado')
					print(self.result)
					return self.result
					
				else:
					print('No se encontro resultado')
					self.BuscarCategoria(pro)
			else:
				print('error sql')
		
		
	def BuscarCategoria(self, ref=()):
		sqlm = "SELECT id FROM CATEGORIA WHERE categoria = '{}'".format(ref)
		self.cursor.execute(sqlm)
		self.categoria = self.cursor.fetchall()
		for x in self.categoria:
			sql_m = "SELECT nombreP, peso , CATEGORIA.categoria as CATEGORIA , MARCA.marca as MARCA , precio FROM PRODUCTOS INNER JOIN CATEGORIA ON CATEGORIA.id = PRODUCTOS.id_categoria INNER JOIN MARCA ON MARCA.id = PRODUCTOS.id_marca WHERE id_categoria = ?"	
			if self.cursor.execute(sql_m, x):
				print('sql categoria procesada')
				result_m = self.cursor.fetchall()
				if result_m:
					print('categoria encontrada')
					print('categira retornada')
					return result_m
				else:
					pass

	def LeerCategoria(self):
		sql_leer_categoria = 'SELECT categoria FROM CATEGORIA'
		self.cursor.execute(sql_leer_categoria)
		self.result_categoria = self.cursor.fetchall()
		return self.result_categoria

	def LeerMarca(self):
		sql_leer_marca = 'SELECT marca FROM MARCA'
		self.cursor.execute(sql_leer_marca)
		self.result_marca = self.cursor.fetchall()
		return self.result_marca

	def NuevoProducto(self, nombre=(), peso=(), categoria=(), marca=(), precio=(), codigo=()):
		if categoria != False:
			sql_leer_categoria = "SELECT id FROM CATEGORIA WHERE categoria = '{}'".format(categoria)
			self.cursor.execute(sql_leer_categoria)
			self.id_categoria = self.cursor.fetchone()[0]
			print(self.id_categoria)
		if marca != False and self.id_categoria:
			sql_leer_marca = "SELECT id FROM MARCA WHERE marca = '{}'".format(marca)
			self.cursor.execute(sql_leer_marca)
			self.id_marca = self.cursor.fetchone()[0]
			print(self.id_marca)
		if self.id_categoria and self.id_marca != False:
			sql_insertar = "INSERT INTO PRODUCTOS (nombreP, peso, id_categoria, id_marca, precio, codigo) VALUES('{}','{}','{}','{}','{}','{}')".format(nombre, peso, self.id_categoria, self.id_marca, precio, codigo)
			if sql_insertar:
				print('sql insertar procesado')
				self.cursor.execute(sql_insertar)
				print('sql insertar ejecuta')
				self.db.commit()
				print('sql insertar exitoso')
				return True
	
	def NuevoUsuario(self, user=(), password=()):
		sql_insertar = "INSERT INTO login (user, pass) VALUES('{}','{}')".format(user, password)
		self.cursor.execute(sql_insertar)
		self.db.commit()
		print('sql insertar exitoso')

	def Login(self, user=(), password=()):
		iniciar = "SELECT user, pass FROM login WHERE user = '{}' and pass = '{}'".format(user, password)
		if iniciar:
			if self.cursor.execute(iniciar):
				self.result_login = self.cursor.fetchall()
				if self.result_login:
					#self.datos = {'user': 'admin', 'is_logged': True}
					return True	
				else:
					return False