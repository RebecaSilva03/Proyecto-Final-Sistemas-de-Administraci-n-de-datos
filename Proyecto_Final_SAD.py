import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def conectar_base_datos():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="rebeca",       # Cambiar según tu configuración
            password="21712rbk.",
            database="Proyecto_final"
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error conectando a la base de datos: {err}")
        return None
def gestionar_productos():
    ventana_productos = tk.Toplevel()
    ventana_productos.title("Gestión de Productos")
    ventana_productos.geometry("400x200")
    
    tk.Label(ventana_productos, text="Gestión de Productos", font=("Courier New", 14)).pack(pady=10)
    
    tk.Button(ventana_productos, text="Agregar Producto",font=("Courier New", 10), command=abrir_formulario_producto,).pack(pady=5)
    tk.Button(ventana_productos, text="Listar Productos",font=("Courier New", 10), command=listar_productos).pack(pady=5)
    tk.Button(ventana_productos, text="Cerrar",font=("Courier New", 10), command=ventana_productos.destroy).pack(pady=10)
def abrir_formulario_producto():
    ventana_form = tk.Toplevel()
    ventana_form.title("Agregar Producto")
    ventana_form.geometry("400x300")
    
    tk.Label(ventana_form, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
    combo_nombre = ttk.Combobox(ventana_form, values=["NavyBlue", "RedCherry", "PearlWhite", "OceanBlack"])
    combo_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Tamaño:").grid(row=1, column=0, padx=10, pady=5)
    combo_tamaño = ttk.Combobox(ventana_form, values=["Chico", "Mediano", "Grande"])
    combo_tamaño.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(ventana_form, text="Precio:").grid(row=2, column=0, padx=10, pady=5)
    entry_precio = tk.Entry(ventana_form)
    entry_precio.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(ventana_form, text="Estado:").grid(row=3, column=0, padx=10, pady=5)
    combo_estado = ttk.Combobox(ventana_form, values=["Activo", "Inactivo"])
    combo_estado.grid(row=3, column=1, padx=10, pady=5)
    
    def guardar_producto():
        nombre = combo_nombre.get()
        tamaño = combo_tamaño.get()
        precio = entry_precio.get()
        estado = combo_estado.get()
        
        if not nombre or not tamaño or not precio or not estado:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        conexion = conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                    INSERT INTO producto (pro_nombre, pro_tamaño, pro_precio, pro_fecha_creacion, pro_estado)
                    VALUES (%s, %s, %s, NOW(), %s)
                """
                cursor.execute(query, (nombre, tamaño, precio, estado))
                conexion.commit()
                messagebox.showinfo("Éxito", "Producto agregado correctamente.")
                ventana_form.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo agregar el producto: {err}")
            finally:
                conexion.close()

    tk.Button(ventana_form, text="Guardar", command=guardar_producto).grid(row=4, column=0, columnspan=2, pady=10)
def listar_productos():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Productos")
    ventana_lista.geometry("800x500")

    tk.Label(ventana_lista, text="Lista de Productos", font=("Arial", 14)).pack(pady=20)

    # Configuración del Treeview
    tree = ttk.Treeview(ventana_lista, columns=("ID", "Nombre", "Tamaño", "Precio", "Estado"), show="headings")
    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Nombre", text="Nombre", anchor="center")
    tree.heading("Tamaño", text="Tamaño", anchor="center")
    tree.heading("Precio", text="Precio", anchor="center")
    tree.heading("Estado", text="Estado", anchor="center")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    tree.column("ID", width=50, anchor="center")
    tree.column("Nombre", width=150, anchor="center")
    tree.column("Tamaño", width=200, anchor="center")
    tree.column("Precio", width=200, anchor="center")
    tree.column("Estado", width=150, anchor="center")

    # Botón de eliminar producto
    tk.Button(ventana_lista, text="Agregar Producto",font=("Courier New", 10), command=abrir_formulario_producto).pack(pady=5)
    tk.Button(ventana_lista, text="Eliminar Producto",font=("Courier New", 10), command=lambda: eliminar_producto(tree)).pack(pady=10)

    # Cargar productos desde la base de datos
    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT producto_id, pro_nombre, pro_tamaño, pro_precio, pro_estado FROM producto"
            cursor.execute(query)
            productos = cursor.fetchall()
            for producto in productos:
                tree.insert("", "end", values=producto)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo cargar la lista de productos: {err}")
        finally:
            conexion.close()
def eliminar_producto(tree):
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para eliminar.")
        return

    producto = tree.item(seleccionado)['values']
    producto_id = producto[0]
    producto_nombre = producto[1]

    confirmar = messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Estás seguro de eliminar el producto '{producto_nombre}' (ID: {producto_id})?"
    )
    if not confirmar:
        return

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "DELETE FROM producto WHERE producto_id = %s"
            cursor.execute(query, (producto_id,))
            conexion.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Producto '{producto_nombre}' eliminado correctamente.")
                tree.delete(seleccionado)
            else:
                messagebox.showwarning("Advertencia", "No se encontró el producto para eliminar.")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ROW_IS_REFERENCED_2:
                messagebox.showerror(
                    "Error",
                    f"No se pudo eliminar el producto '{producto_nombre}' porque está asociado a otros registros."
                )
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {err}")
        finally:
            conexion.close()
def gestionar_clientes():
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Gestión de Clientes")
    ventana_clientes.geometry("500x400")
    
    tk.Label(ventana_clientes, text="Gestión de Clientes", font=("Courier New", 14)).pack(pady=10)
    
    tk.Button(ventana_clientes, text="Agregar Cliente",font=("Courier New", 10), command=abrir_formulario_cliente).pack(pady=5)
    tk.Button(ventana_clientes, text="Listar Clientes",font=("Courier New", 10), command=listar_clientes).pack(pady=5)
    tk.Button(ventana_clientes, text="Cerrar",font=("Courier New", 10), command=ventana_clientes.destroy).pack(pady=10)
def listar_clientes():
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Lista de Clientes")
    ventana_clientes.geometry("800x400")

    tk.Label(ventana_clientes, text="Lista de Clientes", font=("Arial", 12)).pack(pady=1)

    tree = ttk.Treeview(ventana_clientes, columns=("ID", "Nombre", "Correo", "Teléfono", "Dirección", "Ciudad", "País", "Codigo Postal"), show="headings")
    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Nombre", text="Nombre",anchor="center")
    tree.heading("Correo", text="Correo",anchor="center")
    tree.heading("Teléfono", text="Teléfono",anchor="center")
    tree.heading("Dirección", text="Dirección",anchor="center")
    tree.heading("Ciudad", text="Ciudad",anchor="center")
    tree.heading("País", text="País",anchor="center")
    tree.heading("Codigo Postal", text="Codigo Postal",anchor="center")
    tree.pack(fill="both", expand=True, padx=20, pady=20)
    tree.column("ID", width=50, anchor="center")
    tree.column("Nombre", width=150, anchor="center")
    tree.column("Correo", width=200, anchor="center")
    tree.column("Teléfono", width=100, anchor="center")
    tree.column("Dirección", width=250, anchor="center")
    tree.column("Ciudad", width=100, anchor="center")
    tree.column("País", width=100, anchor="center")
    tree.column("Codigo Postal", width=100, anchor="center")

    tk.Button(ventana_clientes, text="Eliminar Cliente", command=lambda: eliminar_cliente(tree)).pack(pady=10)

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
                SELECT c.cliente_id, c.cli_nombre, c.cli_correo, c.cli_telefono, 
                       d.dir_direccion, d.dir_ciudad, d.dir_codigo_postal, d.dir_pais
                FROM clientes c
                LEFT JOIN direcciones d ON c.cliente_id = d.cliente_id
            """
            cursor.execute(query)
            clientes = cursor.fetchall()

            for cliente in clientes:
                tree.insert("", "end", values=cliente)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo obtener la lista de clientes: {err}")
        finally:
            conexion.close()
def eliminar_cliente(tree):

    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un cliente para eliminar.")
        return

    cliente = tree.item(seleccionado)['values']
    cliente_id = cliente[0]
    cliente_nombre = cliente[1] 
    confirmar = messagebox.askyesno(
        "Confirmar Eliminación", 
        f"¿Estás seguro de eliminar al cliente '{cliente_nombre}' (ID: {cliente_id})?"
    )
    if not confirmar:
        return

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "DELETE FROM clientes WHERE cliente_id = %s"
            cursor.execute(query, (cliente_id,))
            conexion.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Cliente '{cliente_nombre}' eliminado correctamente.")
                tree.delete(seleccionado)
            else:
                messagebox.showwarning("Advertencia", "No se encontró al cliente para eliminar.")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ROW_IS_REFERENCED_2:
                messagebox.showerror(
                    "Error", 
                    f"No se puede eliminar al cliente '{cliente_nombre}' porque está asociado a otros registros."
                )
            else:
                messagebox.showerror("Error", f"No se pudo eliminar al cliente: {err}")
        finally:
            conexion.close()
def abrir_formulario_cliente():
    ventana_form = tk.Toplevel()
    ventana_form.title("Agregar Cliente")
    ventana_form.geometry("400x400")
    
    tk.Label(ventana_form, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(ventana_form)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Correo:").grid(row=1, column=0, padx=10, pady=5)
    entry_correo = tk.Entry(ventana_form)
    entry_correo.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Teléfono:").grid(row=2, column=0, padx=10, pady=5)
    entry_telefono = tk.Entry(ventana_form)
    entry_telefono.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Dirección:").grid(row=3, column=0, padx=10, pady=5)
    entry_direccion = tk.Entry(ventana_form)
    entry_direccion.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Ciudad:").grid(row=4, column=0, padx=10, pady=5)
    entry_ciudad = tk.Entry(ventana_form)
    entry_ciudad.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="País:").grid(row=5, column=0, padx=10, pady=5)
    entry_pais = tk.Entry(ventana_form)
    entry_pais.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Codigo postal:").grid(row=6, column=0, padx=10, pady=5)
    entry_codigo = tk.Entry(ventana_form)
    entry_codigo.grid(row=6, column=1, padx=10, pady=5)

    def guardar_cliente():
        nombre = entry_nombre.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()
        direccion = entry_direccion.get()
        ciudad = entry_ciudad.get()
        pais = entry_pais.get()
        codigo = entry_codigo.get()
        
        if not nombre or not correo or not telefono or not direccion or not ciudad or not pais or not codigo:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        conexion = conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query_cliente = """
                INSERT INTO clientes (cli_nombre, cli_correo, cli_telefono)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query_cliente, (nombre, correo, telefono))
                cliente_id = cursor.lastrowid
                query_direccion = """
                    INSERT INTO direcciones (cliente_id, dir_direccion, dir_ciudad, dir_pais, dir_codigo_postal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query_direccion, (cliente_id, direccion, ciudad, pais, codigo))
                
                conexion.commit()
                messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
                ventana_form.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo agregar el cliente: {err}")
            finally:
                conexion.close()

    tk.Button(ventana_form, text="Guardar", command=guardar_cliente).grid(row=7, column=0, columnspan=2, pady=10)
def gestionar_empleados():
    ventana_empleados = tk.Toplevel()
    ventana_empleados.title("Gestión de Empleados")
    ventana_empleados.geometry("500x400")
    
    tk.Label(ventana_empleados, text="Gestión de Empleados",font=("Courier New", 10)).pack(pady=10)
    
    tk.Button(ventana_empleados, text="Agregar Empleado",font=("Courier New", 10), command=abrir_formulario_empleado).pack(pady=5)
    tk.Button(ventana_empleados, text="Listar Empleados",font=("Courier New", 10), command=listar_empleados).pack(pady=5)
    tk.Button(ventana_empleados, text="Cerrar",font=("Courier New", 10), command=ventana_empleados.destroy).pack(pady=10)
def abrir_formulario_empleado():
    ventana_form = tk.Toplevel()
    ventana_form.title("Agregar Empleado")
    ventana_form.geometry("400x300")
    
    tk.Label(ventana_form, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(ventana_form)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(ventana_form, text="Fecha Nac. (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
    entry_fecha_nac = tk.Entry(ventana_form)
    entry_fecha_nac.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(ventana_form, text="Cargo:").grid(row=2, column=0, padx=10, pady=5)
    entry_cargo = tk.Entry(ventana_form)
    entry_cargo.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(ventana_form, text="Salario:").grid(row=3, column=0, padx=10, pady=5)
    entry_salario = tk.Entry(ventana_form)
    entry_salario.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(ventana_form, text="Teléfono:").grid(row=4, column=0, padx=10, pady=5)
    entry_telefono = tk.Entry(ventana_form)
    entry_telefono.grid(row=4, column=1, padx=10, pady=5)
    
    def guardar_empleado():
        nombre = entry_nombre.get()
        fecha_nac = entry_fecha_nac.get()
        cargo = entry_cargo.get()
        salario = entry_salario.get()
        telefono = entry_telefono.get()

        if not nombre or not fecha_nac or not cargo or not salario or not telefono:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        conexion = conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                    INSERT INTO empleados (emp_nombre, emp_fecha_nac, emp_cargo, emp_salario, emp_telefono)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nombre, fecha_nac, cargo, salario, telefono))
                conexion.commit()
                messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
                ventana_form.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo agregar el empleado: {err}")
            finally:
                conexion.close()

    tk.Button(ventana_form, text="Guardar", command=guardar_empleado).grid(row=6, column=0, columnspan=2, pady=10)
def listar_empleados():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Empleados")
    ventana_lista.geometry("700x400")

    tk.Label(ventana_lista, text="Lista de Empleados", font=("Arial", 14)).pack(pady=20)

    tree = ttk.Treeview(ventana_lista, columns=("ID", "Nombre", "Fecha Nac.", "Cargo", "Salario", "Fecha Contratacion", "Telefono"), show="headings")
    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Nombre", text="Nombre", anchor="center")
    tree.heading("Fecha Nac.", text="Fecha Nac.", anchor="center")
    tree.heading("Cargo", text="Cargo", anchor="center")
    tree.heading("Salario", text="Salario", anchor="center")
    tree.heading("Fecha Contratacion", text="Fecha Contratación", anchor="center")
    tree.heading("Telefono", text="Teléfono", anchor="center")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    tree.column("ID", width=50, anchor="center")
    tree.column("Nombre", width=150, anchor="center")
    tree.column("Fecha Nac.", width=100, anchor="center")
    tree.column("Cargo", width=150, anchor="center")
    tree.column("Salario", width=100, anchor="center")
    tree.column("Fecha Contratacion", width=150, anchor="center")
    tree.column("Telefono", width=150, anchor="center")

    tk.Button(ventana_lista, text="Eliminar Empleado", command=lambda: eliminar_empleado(tree)).pack(pady=10)
    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT empleado_id, emp_nombre, emp_fecha_nac, emp_cargo, emp_salario, emp_fecha_contratacion, emp_telefono FROM empleados"
            cursor.execute(query)
            empleados = cursor.fetchall()
            for empleado in empleados:
                tree.insert("", "end", values=empleado)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo cargar la lista de empleados: {err}")
        finally:
            conexion.close()
def eliminar_empleado(tree):
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un empleado para eliminar.")
        return
    empleado = tree.item(seleccionado)['values']
    empleado_id = empleado[0]
    empleado_nombre = empleado[1]

    confirmar = messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Estás seguro de eliminar al empleado '{empleado_nombre}' (ID: {empleado_id})?"
    )
    if not confirmar:
        return
    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Intentar eliminar el empleado
            query = "DELETE FROM empleados WHERE empleado_id = %s"
            cursor.execute(query, (empleado_id,))
            conexion.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Empleado '{empleado_nombre}' eliminado correctamente.")
                tree.delete(seleccionado)
            else:
                messagebox.showwarning("Advertencia", "No se encontró al empleado para eliminar.")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ROW_IS_REFERENCED_2:
                messagebox.showerror(
                    "Error",
                    f"No se puede eliminar al empleado '{empleado_nombre}' porque tiene registros asociados (por ejemplo, asistencia)."
                )
            else:
                messagebox.showerror("Error", f"No se pudo eliminar al empleado: {err}")
        finally:
            conexion.close()
def gestionar_asistencia():
    ventana_asistencia = tk.Toplevel()
    ventana_asistencia.title("Gestión de Asistencia")
    ventana_asistencia.geometry("500x400")
    
    tk.Label(ventana_asistencia, text="Gestión de Asistencia",font=("Courier New", 10)).pack(pady=10)
    
    tk.Button(ventana_asistencia, text="Registrar Asistencia",font=("Courier New", 10), command=abrir_formulario_asistencia).pack(pady=5)
    tk.Button(ventana_asistencia, text="Listar Asistencias",font=("Courier New", 10), command=listar_asistencias).pack(pady=5)
    tk.Button(ventana_asistencia, text="Cerrar",font=("Courier New", 10), command=ventana_asistencia.destroy).pack(pady=10)
def abrir_formulario_asistencia():
    ventana_form = tk.Toplevel()
    ventana_form.title("Registrar Asistencia")
    ventana_form.geometry("400x400")
    tk.Label(ventana_form, text="ID del Empleado:").grid(row=0, column=0, padx=10, pady=5)
    entry_empleado_id = tk.Entry(ventana_form)
    entry_empleado_id.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(ventana_form, text="Registro (Entrada / Salida):").grid(row=1, column=0, padx=10, pady=5)
    combo_registro = ttk.Combobox(ventana_form, values=["Entrada", "Salida"])
    combo_registro.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(ventana_form, text="Estado (A tiempo / Retardo):").grid(row=2, column=0, padx=10, pady=5)
    combo_estado = ttk.Combobox(ventana_form, values=["A tiempo", "Retardo"])
    combo_estado.grid(row=2, column=1, padx=10, pady=5)
    
    def guardar_asistencia():
        empleado_id = entry_empleado_id.get()
        registro = combo_registro.get()
        estado = combo_estado.get()

        if not empleado_id or not registro or not estado:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        conexion = conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                    INSERT INTO asistencia (empleado_id, asi_registro, asi_estado)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (empleado_id, registro, estado))
                conexion.commit()
                messagebox.showinfo("Éxito", "Asistencia registrada correctamente.")
                ventana_form.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo registrar la asistencia: {err}")
            finally:
                conexion.close()

    tk.Button(ventana_form, text="Guardar", command=guardar_asistencia).grid(row=4, column=0, columnspan=2, pady=10)
def listar_asistencias():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Asistencias")
    ventana_lista.geometry("700x400")

    tk.Label(ventana_lista, text="Lista de Asistencias", font=("Arial", 14)).pack(pady=20)

    tree = ttk.Treeview(ventana_lista, columns=("ID", "Empleado ID", "Registro", "Hora Registro", "Estado"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Empleado ID", text="Empleado ID")
    tree.heading("Registro", text="Registro")
    tree.heading("Hora Registro", text="Hora Registro")
    tree.heading("Estado", text="Estado")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT asistencia_id, empleado_id, asi_registro, asi_hora_salida, asi_estado FROM asistencia")
            asistencias = cursor.fetchall()

            for asistencia in asistencias:
                tree.insert("", "end", values=asistencia)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo obtener la lista de asistencias: {err}")
        finally:
            conexion.close()
def registrar_pedido():
    ventana_pedido = tk.Toplevel()
    ventana_pedido.title("Registrar Pedido")
    ventana_pedido.geometry("700x600")

    tk.Label(ventana_pedido, text="Registrar Pedido", font=("Arial", 14)).pack(pady=10)
    tk.Label(ventana_pedido, text="Cliente ID:").pack(pady=5)
    entry_cliente_id = tk.Entry(ventana_pedido)
    entry_cliente_id.pack()

    tk.Label(ventana_pedido, text="Dirección ID:").pack(pady=5)
    entry_direccion_id = tk.Entry(ventana_pedido)
    entry_direccion_id.pack()

    tk.Label(ventana_pedido, text="Notas:").pack(pady=5)
    entry_notas = tk.Entry(ventana_pedido, width=50)
    entry_notas.pack()

    productos = []
    frame_productos = tk.Frame(ventana_pedido)
    frame_productos.pack(pady=10)

    def agregar_producto():
        producto_id = entry_producto_id.get()
        cantidad = entry_cantidad.get()
        if not producto_id or not cantidad:
            messagebox.showerror("Error", "Debes llenar todos los campos del producto.")
            return
        productos.append((producto_id, cantidad))
        entry_producto_id.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        actualizar_lista_productos()

    def actualizar_lista_productos():
        listbox_productos.delete(0, tk.END)
        for i, producto in enumerate(productos):
            listbox_productos.insert(i, f"Producto ID: {producto[0]}, Cantidad: {producto[1]}")

    tk.Label(frame_productos, text="Producto ID:").grid(row=0, column=0, padx=5)
    entry_producto_id = tk.Entry(frame_productos)
    entry_producto_id.grid(row=0, column=1, padx=5)

    tk.Label(frame_productos, text="Cantidad:").grid(row=1, column=0, padx=5)
    entry_cantidad = tk.Entry(frame_productos)
    entry_cantidad.grid(row=1, column=1, padx=5)
    
    tk.Label(frame_productos, text="Precio:").grid(row=2, column=0, padx=5)
    entry_precio = tk.Entry(frame_productos, state='readonly')  # Solo lectura
    entry_precio.grid(row=2, column=1, padx=5)

    def obtener_precio_producto():
            producto_id = entry_producto_id.get()
            if producto_id:
                conexion = conectar_base_datos()
                if conexion:
                    try:
                        cursor = conexion.cursor()
                        query_precio = "SELECT pro_precio FROM producto WHERE producto_id = %s"
                        cursor.execute(query_precio, (producto_id,))
                        precio = cursor.fetchone()
                        if precio:
                            entry_precio.config(state='normal')
                            entry_precio.delete(0, tk.END)
                            entry_precio.insert(0, f"{precio[0]:.2f}")  
                            entry_precio.config(state='readonly')  
                        else:
                            entry_precio.config(state='normal')
                            entry_precio.delete(0, tk.END)
                            entry_precio.insert(0, "No encontrado")
                            entry_precio.config(state='readonly')
                    except mysql.connector.Error as err:
                        messagebox.showerror("Error", f"No se pudo obtener el precio: {err}")
                    finally:
                        conexion.close()

    entry_producto_id.bind("<FocusOut>", lambda event: obtener_precio_producto())
    
    tk.Button(frame_productos, text="Agregar Producto", command=agregar_producto).grid(row=3, column=0, columnspan=2, pady=5)

    tk.Label(ventana_pedido, text="Lista de Productos:").pack(pady=5)
    listbox_productos = tk.Listbox(ventana_pedido, width=80, height=2)
    listbox_productos.pack()
    tk.Label(ventana_pedido, text="Método de Pago:").pack(pady=5)
    metodo_pago_opciones = ["Tarjeta Credito/Debito", "Paypal", "Efectivo en puntos de pago"]
    entry_metodo_pago = tk.StringVar(ventana_pedido)
    entry_metodo_pago.set(metodo_pago_opciones[2])  # Valor predeterminado
    dropdown_metodo_pago = tk.OptionMenu(ventana_pedido, entry_metodo_pago, *metodo_pago_opciones)
    dropdown_metodo_pago.pack(pady=5)

    def guardar_pedido():
        cliente_id = entry_cliente_id.get()
        direccion_id = entry_direccion_id.get()
        notas = entry_notas.get()
        metodo_pago = entry_metodo_pago.get() 
        if not cliente_id or not direccion_id or not productos or not metodo_pago:
            messagebox.showerror("Error", "Todos los campos y al menos un producto son obligatorios.")
            return

        conexion = conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query_pedido = "INSERT INTO pedidos (cliente_id, direcciones_id, ped_notas, ped_metodo_pago) VALUES (%s, %s, %s, %s)"
                cursor.execute(query_pedido, (cliente_id, direccion_id, notas, metodo_pago))
                pedido_id = cursor.lastrowid  

                for producto_id, cantidad in productos:
                    query_precio = "SELECT pro_precio FROM producto WHERE producto_id = %s"
                    cursor.execute(query_precio, (producto_id,))
                    precio_unitario = cursor.fetchone()[0]  
                    precio_total = int(cantidad) * precio_unitario
                    query_producto = """
                        INSERT INTO detalle_pedido (pedido_id, producto_id, det_cantidad, det_precio_total) 
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_producto, (pedido_id, producto_id, cantidad, precio_total))

                conexion.commit()
                messagebox.showinfo("Éxito", "Pedido registrado correctamente.")
                ventana_pedido.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo registrar el pedido: {err}")
            finally:
                conexion.close()

    tk.Button(ventana_pedido, text="Guardar Pedido", command=guardar_pedido).pack(pady=20)
def listar_pedidos():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Pedidos")
    ventana_lista.geometry("700x400")

    tk.Label(ventana_lista, text="Lista de Pedidos", font=("Arial", 14)).pack(pady=20)

    tree = ttk.Treeview(ventana_lista, columns=("ID", "Cliente ID", "Dirección ID", "Fecha", "Método Pago", "Notas"), show="headings")
    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Cliente ID", text="Cliente ID", anchor="center")
    tree.heading("Dirección ID", text="Dirección ID", anchor="center")
    tree.heading("Fecha", text="Fecha", anchor="center")
    tree.heading("Método Pago", text="Método Pago", anchor="center")
    tree.heading("Notas", text="Notas", anchor="center")
    tree.pack(fill="both", expand=True, padx=20, pady=20)
    tree.column("ID", width=50, anchor="center")
    tree.column("Cliente ID", width=100, anchor="center")
    tree.column("Dirección ID", width=100, anchor="center")
    tree.column("Fecha", width=100, anchor="center")
    tree.column("Método Pago", width=150, anchor="center")
    tree.column("Notas", width=200, anchor="center")

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
                SELECT p.pedido_id, p.cliente_id, p.direcciones_id, p.ped_fecha, dp.ped_metodo_pago, p.ped_notas
                FROM pedidos p
                JOIN detalle_pedido dp ON p.pedido_id = dp.pedido_id
            """
            cursor.execute(query)
            pedidos = cursor.fetchall()
            for pedido in pedidos:
                tree.insert("", "end", values=pedido)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo cargar la lista de pedidos: {err}")
        finally:
            conexion.close()
def gestionar_pedidos():
    ventana_pedidos = tk.Toplevel()
    ventana_pedidos.title("Gestión de Pedidos")
    ventana_pedidos.geometry("500x400")
    
    tk.Label(ventana_pedidos, text="Gestión de Pedidos",font=("Courier New", 10)).pack(pady=10)
    
    tk.Button(ventana_pedidos, text="Listar Pedidos",font=("Courier New", 10), command=listar_pedidos).pack(pady=5)
    tk.Button(ventana_pedidos, text="Cerrar",font=("Courier New", 10), command=ventana_pedidos.destroy).pack(pady=10)
def abrir_formulario_pedido():
    ventana_pedido = tk.Toplevel()
    ventana_pedido.title("Registrar Pedido")
    ventana_pedido.geometry("700x600")

    tk.Label(ventana_pedido, text="Registrar Pedido", font=("Arial", 14)).pack(pady=10)

    tk.Label(ventana_pedido, text="Cliente ID:").pack(pady=5)
    entry_cliente_id = tk.Entry(ventana_pedido)
    entry_cliente_id.pack()

    tk.Label(ventana_pedido, text="Dirección ID:").pack(pady=5)
    entry_direccion_id = tk.Entry(ventana_pedido)
    entry_direccion_id.pack()

    tk.Label(ventana_pedido, text="Fecha (YYYY-MM-DD):").pack(pady=5)
    entry_fecha = tk.Entry(ventana_pedido)
    entry_fecha.pack()

    tk.Label(ventana_pedido, text="Notas:").pack(pady=5)
    entry_notas = tk.Entry(ventana_pedido, width=50)
    entry_notas.pack()

    productos = []
    frame_productos = tk.Frame(ventana_pedido)
    frame_productos.pack(pady=10)

    def agregar_producto():
        producto_id = entry_producto_id.get()
        cantidad = entry_cantidad.get()
        if not producto_id or not cantidad:
            messagebox.showerror("Error", "Debes llenar todos los campos del producto.")
            return
        productos.append((producto_id, cantidad))
        entry_producto_id.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        actualizar_lista_productos()

    def actualizar_lista_productos():
        listbox_productos.delete(0, tk.END)
        for i, producto in enumerate(productos):
            listbox_productos.insert(i, f"Producto ID: {producto[0]}, Cantidad: {producto[1]}")

    tk.Label(frame_productos, text="Producto ID:").grid(row=0, column=0, padx=5)
    entry_producto_id = tk.Entry(frame_productos)
    entry_producto_id.grid(row=0, column=1, padx=5)

    tk.Label(frame_productos, text="Cantidad:").grid(row=1, column=0, padx=5)
    entry_cantidad = tk.Entry(frame_productos)
    entry_cantidad.grid(row=1, column=1, padx=5)
    
    tk.Label(frame_productos, text="Precio:").grid(row=2, column=0, padx=5)
    entry_precio = tk.Entry(frame_productos, state='readonly')  # Solo lectura
    entry_precio.grid(row=2, column=1, padx=5)

    def obtener_precio_producto():
        producto_id = entry_producto_id.get()
        if producto_id:
            conexion = conectar_base_datos()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query_precio = "SELECT pro_precio FROM producto WHERE producto_id = %s"
                    cursor.execute(query_precio, (producto_id,))
                    precio = cursor.fetchone()
                    if precio:
                        entry_precio.config(state='normal')  
                        entry_precio.delete(0, tk.END)
                        entry_precio.insert(0, f"{precio[0]:.2f}") 
                        entry_precio.config(state='readonly')  
                    else:
                        entry_precio.config(state='normal')
                        entry_precio.delete(0, tk.END)
                        entry_precio.insert(0, "No encontrado")
                        entry_precio.config(state='readonly')
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"No se pudo obtener el precio: {err}")
                finally:
                    conexion.close()
    entry_producto_id.bind("<FocusOut>", lambda event: obtener_precio_producto())
    
    tk.Button(frame_productos, text="Agregar Producto", command=agregar_producto).grid(row=3, column=0, columnspan=2, pady=5)

    tk.Label(ventana_pedido, text="Lista de Productos:").pack(pady=5)
    listbox_productos = tk.Listbox(ventana_pedido, width=80, height=2)
    listbox_productos.pack()


    tk.Label(ventana_pedido, text="Método de Pago:").pack(pady=5)
    metodo_pago_opciones = ["Tarjeta Credito/Debito", "Paypal", "Efectivo en puntos de pago"]
    entry_metodo_pago = tk.StringVar(ventana_pedido)
    entry_metodo_pago.set(metodo_pago_opciones[2])  # Valor predeterminado
    dropdown_metodo_pago = tk.OptionMenu(ventana_pedido, entry_metodo_pago, *metodo_pago_opciones)
    dropdown_metodo_pago.pack(pady=5)

    def guardar_pedido():
        cliente_id = entry_cliente_id.get()
        direccion_id = entry_direccion_id.get()
        fecha = entry_fecha.get()
        notas = entry_notas.get()
        metodo_pago = entry_metodo_pago.get()

        if not cliente_id or not direccion_id or not fecha or not productos or not metodo_pago:
            messagebox.showerror("Error", "Todos los campos y al menos un producto son obligatorios.")
            return

        conexion = conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()

                query_pedido = "INSERT INTO pedidos (cliente_id, direcciones_id, ped_fecha, ped_notas, ped_metodo_pago) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query_pedido, (cliente_id, direccion_id, fecha, notas, metodo_pago))
                pedido_id = cursor.lastrowid

                for producto_id, cantidad in productos:
                    query_precio = "SELECT pro_precio FROM producto WHERE producto_id = %s"
                    cursor.execute(query_precio, (producto_id,))
                    precio_unitario = cursor.fetchone()[0] 

                    precio_total = int(cantidad) * precio_unitario

                    query_producto = """
                        INSERT INTO detalle_pedido (pedido_id, producto_id, det_cantidad, det_precio_total) 
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_producto, (pedido_id, producto_id, cantidad, precio_total))

                    query_inventario = """
                        SELECT inv_cantidad, inventario_productos_id 
                        FROM inventario_productos 
                        WHERE producto_id = %s
                    """
                    cursor.execute(query_inventario, (producto_id,))
                    inventario = cursor.fetchone()

                    if inventario:
                        nueva_cantidad = inventario[0] - int(cantidad)
                        inventario_productos_id = inventario[1]

                        if nueva_cantidad >= 0:  
                            query_actualizar_inventario = """
                                UPDATE inventario_productos 
                                SET inv_cantidad = %s, inv_ultima_actualizacion = NOW() 
                                WHERE inventario_productos_id = %s
                            """
                            cursor.execute(query_actualizar_inventario, (nueva_cantidad, inventario_productos_id))

                    
                            query_movimiento = """
                                INSERT INTO movimientos_inv_productos (inventario_productos_id, mov_tipo_movimiento, mov_cantidad, mov_descripcion) 
                                VALUES (%s, 'Salida', %s, 'Venta de producto: %s')
                            """
                            cursor.execute(query_movimiento, (inventario_productos_id, cantidad, producto_id))
                        else:
                            messagebox.showerror("Error de inventario", f"No hay suficiente stock de producto ID: {producto_id}.")
                            conexion.rollback() 
                            return

                conexion.commit()
                messagebox.showinfo("Éxito", "Pedido registrado correctamente y inventario actualizado.")
                ventana_pedido.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo registrar el pedido: {err}")
                conexion.rollback()
            finally:
                conexion.close()
    tk.Button(ventana_pedido, text="Guardar Pedido", command=guardar_pedido).pack(pady=20)
def listar_pedidos():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Pedidos")
    ventana_lista.geometry("700x400")

    tk.Label(ventana_lista, text="Lista de Pedidos", font=("Arial", 14)).pack(pady=20)

    # Configuración del Treeview
    tree = ttk.Treeview(ventana_lista, columns=("ID", "Dirección ID", "Fecha", "Método Pago", "Notas"), show="headings")
    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Dirección ID", text="Dirección ID", anchor="center")
    tree.heading("Fecha", text="Fecha", anchor="center")
    tree.heading("Método Pago", text="Método Pago", anchor="center")
    tree.heading("Notas", text="Notas", anchor="center")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    tree.column("ID", width=50, anchor="center")
    tree.column("Dirección ID", width=150, anchor="center")
    tree.column("Fecha", width=100, anchor="center")
    tree.column("Método Pago", width=150, anchor="center")
    tree.column("Notas", width=200, anchor="center")

    # Cargar datos desde la base de datos
    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT pedido_id, direcciones_id, ped_fecha, ped_metodo_pago, ped_notas FROM pedidos"
            cursor.execute(query)
            pedidos = cursor.fetchall()
            for pedido in pedidos:
                tree.insert("", "end", values=pedido)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo cargar la lista de pedidos: {err}")
        finally:
            conexion.close()
def gestionar_envios():
    ventana_pedidos = tk.Toplevel()
    ventana_pedidos.title("Gestión de Pedidos")
    ventana_pedidos.geometry("500x400")
    
    tk.Label(ventana_pedidos, text="Gestión de Pedidos",font=("Courier New", 10)).pack(pady=10)
    
    tk.Button(ventana_pedidos, text="Generar Envio",font=("Courier New", 10), command=abrir_formulario_envio).pack(pady=5)
    tk.Button(ventana_pedidos, text="Listar Pedidos",font=("Courier New", 10), command=listar_envios).pack(pady=5)
    tk.Button(ventana_pedidos, text="Cerrar",font=("Courier New", 10), command=ventana_pedidos.destroy).pack(pady=10)
def abrir_formulario_envio():
    ventana_envio = tk.Toplevel()
    ventana_envio.title("Registrar Envío")
    ventana_envio.geometry("700x600")

    tk.Label(ventana_envio, text="Registrar Envío", font=("Arial", 14)).pack(pady=10)

    # Inputs para el envío
    tk.Label(ventana_envio, text="Pedido ID").pack(pady=5)
    entry_pedido_id = tk.Entry(ventana_envio)
    entry_pedido_id.pack()

    tk.Label(ventana_envio, text="Cliente ID:").pack(pady=5)
    entry_cliente_id = tk.Entry(ventana_envio)
    entry_cliente_id.pack()

    tk.Label(ventana_envio, text="Método de Envío:").pack(pady=5)
    metodo_envio_opciones = ["Estandar", "Express"]
    entry_metodo_envio = tk.StringVar(ventana_envio)
    entry_metodo_envio.set(metodo_envio_opciones[0]) 
    dropdown_metodo_envio = tk.OptionMenu(ventana_envio, entry_metodo_envio, *metodo_envio_opciones)
    dropdown_metodo_envio.pack(pady=5)

    tk.Label(ventana_envio, text="Estado del Envío:").pack(pady=5)
    estado_envio_opciones = ["Entregado", "En transito", "Por enviar"]
    entry_estado_envio = tk.StringVar(ventana_envio)
    entry_estado_envio.set(estado_envio_opciones[2])
    dropdown_estado_envio = tk.OptionMenu(ventana_envio, entry_estado_envio, *estado_envio_opciones)
    dropdown_estado_envio.pack(pady=5)

    tk.Label(ventana_envio, text="Número de Seguimiento:").pack(pady=5)
    entry_seguimiento = tk.Entry(ventana_envio)
    entry_seguimiento.pack()

    tk.Label(ventana_envio, text="Costo de Envío:").pack(pady=5)
    entry_costo_envio = tk.Entry(ventana_envio)
    entry_costo_envio.pack()

    def guardar_envio():
        pedido_id = entry_pedido_id.get()
        cliente_id = entry_cliente_id.get()
        metodo_envio = entry_metodo_envio.get()
        estado_envio = entry_estado_envio.get()
        seguimiento = entry_seguimiento.get()
        costo_envio = entry_costo_envio.get()

        # Validación para asegurar que todos los campos están completos
        if not pedido_id or not pedido_id or not metodo_envio or not estado_envio or not seguimiento or not costo_envio:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        conexion = conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()

                # Insertar el envío en la tabla `envios`
                query_envio = """
                    INSERT INTO envios (pedido_id, cliente_id, env_estado, env_metodo_envio, env_seguimiento, env_costo_envio)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_envio, (pedido_id, cliente_id, estado_envio, metodo_envio, seguimiento, costo_envio))
                conexion.commit()

                messagebox.showinfo("Éxito", "Envío registrado correctamente.")
                ventana_envio.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo registrar el envío: {err}")
            finally:
                conexion.close()


    tk.Button(ventana_envio, text="Guardar Envío", command=guardar_envio).pack(pady=20)
def listar_envios():
    ventana_listado_envios = tk.Toplevel()
    ventana_listado_envios.title("Listado de Envíos")
    ventana_listado_envios.geometry("800x600")

    columnas = ("ID Envío", "Fecha", "Estado", "Método de Envío", "Seguimiento", "Costo Envío", "Producto ID", "Cantidad", "Cliente ID", "Dirección")
    tree = ttk.Treeview(ventana_listado_envios, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill=tk.BOTH, expand=True)

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
                SELECT 
                    e.envio_id, 
                    e.env_fecha, 
                    e.env_estado, 
                    e.env_metodo_envio, 
                    e.env_seguimiento, 
                    e.env_costo_envio, 
                    dp.producto_id, 
                    dp.det_cantidad, 
                    c.cliente_id, 
                    d.dir_direccion, 
                    d.dir_ciudad, 
                    d.dir_codigo_postal, 
                    d.dir_pais
                FROM 
                    envios e
                JOIN 
                    detalle_pedido dp ON e.pedido_id = dp.pedido_id
                JOIN 
                    pedidos p ON dp.pedido_id = p.pedido_id
                JOIN 
                    clientes c ON p.cliente_id = c.cliente_id
                JOIN 
                    direcciones d ON p.direcciones_id = d.direcciones_id
                ORDER BY 
                    e.env_fecha DESC;
            """
            cursor.execute(query)
            envios = cursor.fetchall()

            for envio in envios:
                tree.insert("", "end", values=envio)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo obtener los envíos: {err}")
        finally:
            conexion.close()
def listar_almacenes():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Almacenes")
    ventana_lista.geometry("600x400")

    tk.Label(ventana_lista, text="Lista de Almacenes", font=("Arial", 14)).pack(pady=20)

    tree = ttk.Treeview(ventana_lista, columns=("ID", "Nombre", "Ubicación"), show="headings")
    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Nombre", text="Nombre", anchor="center")
    tree.heading("Ubicación", text="Ubicación", anchor="center")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    tree.column("ID", width=50, anchor="center")
    tree.column("Nombre", width=150, anchor="center")
    tree.column("Ubicación", width=200, anchor="center")

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT almacen_id, alm_nombre, alm_ubicacion FROM almacenes"
            cursor.execute(query)
            almacenes = cursor.fetchall()
            for almacen in almacenes:
                tree.insert("", "end", values=almacen)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo cargar la lista de almacenes: {err}")
        finally:
            conexion.close()

    tk.Button(ventana_lista, text="Agregar Almacén", command=abrir_formulario_almacen).pack(pady=5)
    tk.Button(ventana_lista, text="Eliminar Almacén", command=lambda: eliminar_almacen(tree)).pack(pady=5)
def gestionar_almacenes():
    ventana_almacenes = tk.Toplevel()
    ventana_almacenes.title("Gestión de Almacenes")
    ventana_almacenes.geometry("500x400")
    
    tk.Label(ventana_almacenes, text="Gestión de Almacenes",font=("Courier New", 10)).pack(pady=10)
    
    tk.Button(ventana_almacenes, text="Agregar Almacen",font=("Courier New", 10), command=abrir_formulario_almacen).pack(pady=5)
    tk.Button(ventana_almacenes, text="Listar Almacenes",font=("Courier New", 10), command=listar_almacenes).pack(pady=5)
    tk.Button(ventana_almacenes, text="Cerrar",font=("Courier New", 10), command=ventana_almacenes.destroy).pack(pady=10)
def abrir_formulario_almacen():
    ventana_formulario = tk.Toplevel()
    ventana_formulario.title("Agregar Almacén")
    ventana_formulario.geometry("400x300")

    tk.Label(ventana_formulario, text="Nombre del Almacén:").pack(pady=5)
    entrada_nombre = tk.Entry(ventana_formulario)
    entrada_nombre.pack(pady=5)

    tk.Label(ventana_formulario, text="Ubicación del Almacén:").pack(pady=5)
    entrada_ubicacion = tk.Entry(ventana_formulario)
    entrada_ubicacion.pack(pady=5)

    def guardar_almacen():
        nombre = entrada_nombre.get()
        ubicacion = entrada_ubicacion.get()

        if not nombre or not ubicacion:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        conexion = conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "INSERT INTO almacenes (alm_nombre, alm_ubicacion) VALUES (%s, %s)"
                cursor.execute(query, (nombre, ubicacion))
                conexion.commit()
                messagebox.showinfo("Éxito", "Almacén agregado correctamente.")
                ventana_formulario.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo agregar el almacén: {err}")
            finally:
                conexion.close()

    tk.Button(ventana_formulario, text="Guardar", command=guardar_almacen).pack(pady=20)
def eliminar_almacen(tree):
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un almacén para eliminar.")
        return

    almacen = tree.item(seleccionado)['values']
    almacen_id = almacen[0]
    almacen_nombre = almacen[1]

    confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el almacén '{almacen_nombre}' (ID: {almacen_id})?")
    if not confirmar:
        return

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "DELETE FROM almacenes WHERE almacen_id = %s"
            cursor.execute(query, (almacen_id,))
            conexion.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Almacén '{almacen_nombre}' eliminado correctamente.")
                tree.delete(seleccionado)
            else:
                messagebox.showwarning("Advertencia", "No se encontró el almacén para eliminar.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo eliminar el almacén: {err}")
        finally:
            conexion.close()
def gestionar_proveedores():
    ventana_proveedores = tk.Toplevel()
    ventana_proveedores.title("Gestión de Materiales")
    ventana_proveedores.geometry("500x400")
    
    tk.Label(ventana_proveedores, text="Gestión de Proveedores",font=("Courier New", 10)).pack(pady=10)
    
    tk.Button(ventana_proveedores, text="Agregar Proveedor",font=("Courier New", 10), command=abrir_formulario_proveedor).pack(pady=5)
    tk.Button(ventana_proveedores, text="Listar Proveedores",font=("Courier New", 10), command=listar_proveedores).pack(pady=5)
    tk.Button(ventana_proveedores, text="Cerrar",font=("Courier New", 10), command=ventana_proveedores.destroy).pack(pady=10)
def abrir_formulario_proveedor():
    ventana_form = tk.Toplevel()
    ventana_form.title("Agregar Proveedor")
    ventana_form.geometry("400x400")
    
    tk.Label(ventana_form, text="Nombre del Proveedor:").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(ventana_form)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Contacto:").grid(row=1, column=0, padx=10, pady=5)
    entry_contacto = tk.Entry(ventana_form)
    entry_contacto.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Teléfono:").grid(row=2, column=0, padx=10, pady=5)
    entry_telefono = tk.Entry(ventana_form)
    entry_telefono.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Correo:").grid(row=3, column=0, padx=10, pady=5)
    entry_correo = tk.Entry(ventana_form)
    entry_correo.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Dirección:").grid(row=4, column=0, padx=10, pady=5)
    entry_direccion = tk.Entry(ventana_form)
    entry_direccion.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(ventana_form, text="Material:").grid(row=5, column=0, padx=10, pady=5)
    entry_material = tk.Entry(ventana_form)
    entry_material.grid(row=5, column=1, padx=10, pady=5)

    def guardar_proveedor():
        nombre = entry_nombre.get()
        contacto = entry_contacto.get()
        telefono = entry_telefono.get()
        correo = entry_correo.get()
        direccion = entry_direccion.get()
        material = entry_material.get()
        
        if not nombre or not telefono or not direccion or not material:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        conexion = conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                    INSERT INTO proveedores (material_id, prov_nombre, prov_contacto, prov_telefono, prov_correo, prov_direccion)
                    VALUES ((SELECT material_id FROM material WHERE mat_nombre = %s), %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (material, nombre, contacto, telefono, correo, direccion))
                conexion.commit()
                messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")
                ventana_form.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo agregar el proveedor: {err}")
            finally:
                conexion.close()

    tk.Button(ventana_form, text="Guardar", command=guardar_proveedor).grid(row=6, column=0, columnspan=2, pady=10)
def listar_proveedores():
    ventana_listado = tk.Toplevel()
    ventana_listado.title("Listar Proveedores")
    ventana_listado.geometry("600x400")

    treeview = ttk.Treeview(ventana_listado, columns=("ID", "Nombre", "Material", "Teléfono", "Correo", "Dirección"), show="headings")
    treeview.grid(row=0, column=0, padx=10, pady=10)

    treeview.heading("ID", text="ID")
    treeview.heading("Nombre", text="Nombre")
    treeview.heading("Material", text="Material")
    treeview.heading("Teléfono", text="Teléfono")
    treeview.heading("Correo", text="Correo")
    treeview.heading("Dirección", text="Dirección")

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
                SELECT p.proveedor_id, p.prov_nombre, m.mat_nombre, p.prov_telefono, p.prov_correo, p.prov_direccion
                FROM proveedores p
                JOIN material m ON p.material_id = m.material_id
            """
            cursor.execute(query)
            proveedores = cursor.fetchall()
            
            for proveedor in proveedores:
                treeview.insert("", tk.END, values=proveedor)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudieron obtener los proveedores: {err}")
        finally:
            conexion.close()
def gestionar_materiales():
    ventana_empleados = tk.Toplevel()
    ventana_empleados.title("Gestión de Materiales")
    ventana_empleados.geometry("500x400")
    
    tk.Label(ventana_empleados, text="Gestión de Materiales",font=("Courier New", 10)).pack(pady=10)
    
    tk.Button(ventana_empleados, text="Agregar Material",font=("Courier New", 10), command=abrir_formulario_material).pack(pady=5)
    tk.Button(ventana_empleados, text="Listar Materiales",font=("Courier New", 10), command=listar_materiales).pack(pady=5)
    tk.Button(ventana_empleados, text="Cerrar",font=("Courier New", 10), command=ventana_empleados.destroy).pack(pady=10)  
def listar_materiales():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Materiales")
    ventana_lista.geometry("600x400")

    tk.Label(ventana_lista, text="Lista de Materiales", font=("Arial", 14)).pack(pady=20)

    tree = ttk.Treeview(ventana_lista, columns=("ID", "Nombre", "Descripción"), show="headings")
    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Nombre", text="Nombre", anchor="center")
    tree.heading("Descripción", text="Descripción", anchor="center")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    tree.column("ID", width=50, anchor="center")
    tree.column("Nombre", width=150, anchor="center")
    tree.column("Descripción", width=300, anchor="center")
    
    tk.Button(ventana_lista, text="Eliminar Material", command=lambda: eliminar_material(tree)).pack(pady=5)

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT material_id, mat_nombre, mat_descripcion FROM material"
            cursor.execute(query)
            materiales = cursor.fetchall()
            for material in materiales:
                tree.insert("", "end", values=material)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo cargar la lista de materiales: {err}")
        finally:
            conexion.close()
def abrir_formulario_material():
    ventana_formulario = tk.Toplevel()
    ventana_formulario.title("Agregar Material")
    ventana_formulario.geometry("400x300")

    tk.Label(ventana_formulario, text="Nombre del Material:").pack(pady=5)
    entrada_nombre = tk.Entry(ventana_formulario)
    entrada_nombre.pack(pady=5)

    tk.Label(ventana_formulario, text="Descripción del Material:").pack(pady=5)
    entrada_descripcion = tk.Text(ventana_formulario, height=5, width=40)
    entrada_descripcion.pack(pady=5)

    def guardar_material():
        nombre = entrada_nombre.get()
        descripcion = entrada_descripcion.get("1.0", tk.END).strip()

        if not nombre or not descripcion:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        conexion = conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "INSERT INTO material (mat_nombre, mat_descripcion) VALUES (%s, %s)"
                cursor.execute(query, (nombre, descripcion))
                conexion.commit()
                messagebox.showinfo("Éxito", "Material agregado correctamente.")
                ventana_formulario.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo agregar el material: {err}")
            finally:
                conexion.close()

    tk.Button(ventana_formulario, text="Guardar", command=guardar_material).pack(pady=20)
def eliminar_material(tree):
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un material para eliminar.")
        return

    material = tree.item(seleccionado)['values']
    material_id = material[0]
    material_nombre = material[1]

    confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el material '{material_nombre}' (ID: {material_id})?")
    if not confirmar:
        return

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "DELETE FROM material WHERE material_id = %s"
            cursor.execute(query, (material_id,))
            conexion.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Material '{material_nombre}' eliminado correctamente.")
                tree.delete(seleccionado)
            else:
                messagebox.showwarning("Advertencia", "No se encontró el material para eliminar.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo eliminar el material: {err}")
        finally:
            conexion.close()            


    # Obtener el elemento seleccionado en el Treeview
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para eliminar.")
        return

   
    producto_almacen = tree.item(seleccionado)['values']
    producto_almacen_id = producto_almacen[0]
    producto_nombre = producto_almacen[1]  
    almacen_nombre = producto_almacen[2]  


    confirmar = messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Estás seguro de eliminar el producto '{producto_nombre}' del almacén '{almacen_nombre}'?"
    )
    if not confirmar:
        return

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "DELETE FROM productos_almacen WHERE producto_almacen_id = %s"
            cursor.execute(query, (producto_almacen_id,))
            conexion.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"El producto '{producto_nombre}' fue eliminado correctamente del almacén '{almacen_nombre}'.")
                tree.delete(seleccionado)
            else:
                messagebox.showwarning("Advertencia", "No se encontró el producto para eliminar.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo eliminar el producto del almacén: {err}")
        finally:
            conexion.close()
def abrir_formulario_inventario():
    ventana = tk.Toplevel()
    ventana.title("Registrar Inventario")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="ID Almacén:").grid(row=0, column=0, padx=10, pady=5)
    entry_almacen_id = tk.Entry(ventana)
    entry_almacen_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="ID Material:").grid(row=1, column=0, padx=10, pady=5)
    entry_material_id = tk.Entry(ventana)
    entry_material_id.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Cantidad Inicial:").grid(row=2, column=0, padx=10, pady=5)
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.grid(row=2, column=1, padx=10, pady=5)

    def guardar_inventario():
        try:
            almacen_id = int(entry_almacen_id.get())
            material_id = int(entry_material_id.get())
            cantidad = int(entry_cantidad.get())

            if cantidad < 0:
                raise ValueError("La cantidad inicial no puede ser negativa.")

            conexion = conectar_base_datos()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = """
                        INSERT INTO inventario_materiales (almacen_id, material_id, inv_cantidad)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query, (almacen_id, material_id, cantidad))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Inventario registrado correctamente.")
                    ventana.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error al registrar el inventario: {err}")
                finally:
                    conexion.close()
        except ValueError as ve:
            messagebox.showerror("Error", f"{ve}")

    tk.Button(ventana, text="Guardar",font=("Courier New", 10), command=guardar_inventario).grid(row=3, column=0, columnspan=2, pady=10)
def registrar_movimiento(inventario_id, tipo_movimiento, cantidad, descripcion):
    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            query_cantidad = "SELECT inv_cantidad FROM inventario_materiales WHERE inventario_materiales_id = %s"
            cursor.execute(query_cantidad, (inventario_id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError("El inventario especificado no existe.")
            
            cantidad_actual = resultado[0]
            nueva_cantidad = cantidad_actual + cantidad if tipo_movimiento == 'Entrada' else cantidad_actual - cantidad

            if nueva_cantidad < 0:
                raise ValueError("Saldo insuficiente para realizar la salida.")
            query_movimiento = """
                INSERT INTO movimientos_inv_materiales (inventario_materiales_id, mov_pro_tipo_movimiento, mov_pro_cantidad, mov_pro_descripcion)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_movimiento, (inventario_id, tipo_movimiento, cantidad, descripcion))

            query_actualizar = "UPDATE inventario_materiales SET inv_cantidad = %s WHERE inventario_materiales_id = %s"
            cursor.execute(query_actualizar, (nueva_cantidad, inventario_id))

            conexion.commit()
            messagebox.showinfo("Éxito", "Movimiento registrado y cantidad actualizada exitosamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error de base de datos: {err}")
        except ValueError as ve:
            messagebox.showerror("Error", f"{ve}")
        finally:
            conexion.close()
def mostrar_inventarios():
    ventana = tk.Toplevel()
    ventana.title("Lista de Inventarios")
    ventana.geometry("600x400")

    tabla = ttk.Treeview(ventana, columns=("ID", "Almacén", "Material", "Cantidad", "Última Actualización"), show="headings")
    tabla.heading("ID", text="ID Inventario")
    tabla.heading("Almacén", text="ID Almacén")
    tabla.heading("Material", text="ID Material")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Última Actualización", text="Última Actualización")

    tabla.column("ID", width=100, anchor="center")
    tabla.column("Almacén", width=100, anchor="center")
    tabla.column("Material", width=100, anchor="center")
    tabla.column("Cantidad", width=100, anchor="center")
    tabla.column("Última Actualización", width=200, anchor="center")
    tabla.pack(fill=tk.BOTH, expand=True)

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            query = """
                SELECT im.inventario_materiales_id, a.almacen_id, m.material_id, im.inv_cantidad, im.inv_mat_ultima_actualizacion
                FROM inventario_materiales im
                JOIN almacenes a ON im.almacen_id = a.almacen_id
                JOIN material m ON im.material_id = m.material_id
            """
            cursor.execute(query)
            inventarios = cursor.fetchall()
            for inventario in inventarios:
                tabla.insert("", "end", values=(
                    inventario["inventario_materiales_id"],
                    inventario["almacen_id"],
                    inventario["material_id"],
                    inventario["inv_cantidad"],
                    inventario["inv_mat_ultima_actualizacion"]
                ))
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar los inventarios: {err}")
        finally:
            conexion.close()

    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
def listar_movimientos():
    ventana = tk.Toplevel()
    ventana.title("Lista de Movimientos")
    ventana.geometry("600x400")

    tabla = ttk.Treeview(ventana, columns=("ID", "ID Inventario", "Tipo", "Cantidad", "Fecha", "Descripción"), show="headings")
    tabla.heading("ID", text="ID Movimiento")
    tabla.heading("ID Inventario", text="ID Inventario")
    tabla.heading("Tipo", text="Tipo Movimiento")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Descripción", text="Descripción")

    tabla.column("ID", width=100, anchor="center")
    tabla.column("ID Inventario", width=100, anchor="center")
    tabla.column("Tipo", width=100, anchor="center")
    tabla.column("Cantidad", width=100, anchor="center")
    tabla.column("Fecha", width=150, anchor="center")
    tabla.column("Descripción", width=150, anchor="center")
    tabla.pack(fill=tk.BOTH, expand=True)

    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            query = """
                SELECT mm.movimiento_inv_materiales_id, im.inventario_materiales_id, mm.mov_pro_tipo_movimiento, mm.mov_pro_cantidad,
                       mm.mov_pro_fecha_movimiento, mm.mov_pro_descripcion
                FROM movimientos_inv_materiales mm
                JOIN inventario_materiales im ON mm.inventario_materiales_id = im.inventario_materiales_id
            """
            cursor.execute(query)
            movimientos = cursor.fetchall()
            for movimiento in movimientos:
                tabla.insert("", "end", values=(
                    movimiento["movimiento_inv_materiales_id"],
                    movimiento["inventario_materiales_id"],
                    movimiento["mov_pro_tipo_movimiento"],
                    movimiento["mov_pro_cantidad"],
                    movimiento["mov_pro_fecha_movimiento"],
                    movimiento["mov_pro_descripcion"]
                ))
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar los movimientos: {err}")
        finally:
            conexion.close()
    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
def abrir_formulario_movimiento():
    ventana = tk.Toplevel()
    ventana.title("Registrar Movimiento")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="ID Inventario:").grid(row=0, column=0, padx=10, pady=5)
    entry_inventario_id = tk.Entry(ventana)
    entry_inventario_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Tipo Movimiento:").grid(row=1, column=0, padx=10, pady=5)
    combo_tipo_movimiento = ttk.Combobox(ventana, values=["Entrada", "Salida"])
    combo_tipo_movimiento.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Cantidad:").grid(row=2, column=0, padx=10, pady=5)
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Descripción:").grid(row=3, column=0, padx=10, pady=5)
    entry_descripcion = tk.Entry(ventana)
    entry_descripcion.grid(row=3, column=1, padx=10, pady=5)

    def guardar_movimiento():
        try:
            inventario_id = int(entry_inventario_id.get())
            tipo_movimiento = combo_tipo_movimiento.get()
            cantidad = int(entry_cantidad.get())
            descripcion = entry_descripcion.get()

            if not tipo_movimiento:
                raise ValueError("El tipo de movimiento es obligatorio.")
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero.")

            registrar_movimiento(inventario_id, tipo_movimiento, cantidad, descripcion)
            ventana.destroy()
        except ValueError as ve:
            messagebox.showerror("Error", f"{ve}")

    tk.Button(ventana, text="Guardar", command=guardar_movimiento).grid(row=4, column=0, columnspan=2, pady=10)
def gestionar_inventarios():
    root = tk.Tk()
    root.title("Sistema de Control de Inventarios")
    root.geometry("400x200")

    tk.Button(root, text="Registrar Inventario",font=("Courier New", 10), command=abrir_formulario_inventario).pack(pady=10)
    tk.Button(root, text="Registrar Movimiento",font=("Courier New", 10), command=abrir_formulario_movimiento).pack(pady=10)
    tk.Button(root, text="Listar Inventarios",font=("Courier New", 10), command=mostrar_inventarios).pack(pady=10)
    tk.Button(root, text="Listar Movimientos",font=("Courier New", 10), command=listar_movimientos).pack(pady=10)
    root.mainloop()
def abrir_formulario_inventario_productos():
    ventana = tk.Toplevel()
    ventana.title("Registrar Inventario de Producto")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="ID Almacén:").grid(row=0, column=0, padx=10, pady=5)
    entry_almacen_id = tk.Entry(ventana)
    entry_almacen_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="ID Producto:").grid(row=1, column=0, padx=10, pady=5)
    entry_producto_id = tk.Entry(ventana)
    entry_producto_id.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Cantidad Inicial:").grid(row=2, column=0, padx=10, pady=5)
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.grid(row=2, column=1, padx=10, pady=5)

    def guardar_inventario_producto():
        try:
            almacen_id = int(entry_almacen_id.get())
            producto_id = int(entry_producto_id.get())
            cantidad = int(entry_cantidad.get())

            if cantidad < 0:
                raise ValueError("La cantidad inicial no puede ser negativa.")

            conexion = conectar_base_datos()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = """
                        INSERT INTO inventario_productos (almacen_id, producto_id, inv_cantidad)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query, (almacen_id, producto_id, cantidad))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Inventario de producto registrado correctamente.")
                    ventana.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error al registrar el inventario de producto: {err}")
                finally:
                    conexion.close()
        except ValueError as ve:
            messagebox.showerror("Error", f"{ve}")

    tk.Button(ventana, text="Guardar", command=guardar_inventario_producto).grid(row=3, column=0, columnspan=2, pady=10)
def abrir_formulario_movimiento_productos():
    ventana = tk.Toplevel()
    ventana.title("Registrar Movimiento de Producto")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="ID Inventario Producto:").grid(row=0, column=0, padx=10, pady=5)
    entry_inventario_producto_id = tk.Entry(ventana)
    entry_inventario_producto_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Tipo de Movimiento:").grid(row=1, column=0, padx=10, pady=5)
    combo_tipo_movimiento = ttk.Combobox(ventana, values=["Entrada", "Salida"])
    combo_tipo_movimiento.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Cantidad:").grid(row=2, column=0, padx=10, pady=5)
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Descripción:").grid(row=3, column=0, padx=10, pady=5)
    entry_descripcion = tk.Entry(ventana)
    entry_descripcion.grid(row=3, column=1, padx=10, pady=5)

    def guardar_movimiento_producto():
        try:
            inventario_producto_id = int(entry_inventario_producto_id.get())
            tipo_movimiento = combo_tipo_movimiento.get()
            cantidad = int(entry_cantidad.get())
            descripcion = entry_descripcion.get()

            if tipo_movimiento not in ['Entrada', 'Salida']:
                raise ValueError("Tipo de movimiento debe ser 'Entrada' o 'Salida'.")
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            conexion = conectar_base_datos()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    query = """
                        INSERT INTO movimientos_inv_productos (inventario_productos_id, mov_tipo_movimiento, mov_cantidad, mov_descripcion)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (inventario_producto_id, tipo_movimiento, cantidad, descripcion))
                    conexion.commit()

                    # Actualizar inventario según el tipo de movimiento
                    if tipo_movimiento == "Entrada":
                        cursor.execute("""
                            UPDATE inventario_productos 
                            SET inv_cantidad = inv_cantidad + %s 
                            WHERE inventario_productos_id = %s
                        """, (cantidad, inventario_producto_id))
                    elif tipo_movimiento == "Salida":
                        cursor.execute("""
                            UPDATE inventario_productos 
                            SET inv_cantidad = inv_cantidad - %s 
                            WHERE inventario_productos_id = %s
                        """, (cantidad, inventario_producto_id))

                    conexion.commit()
                    messagebox.showinfo("Éxito", "Movimiento de producto registrado correctamente.")
                    ventana.destroy()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error al registrar el movimiento de producto: {err}")
                finally:
                    conexion.close()
        except ValueError as ve:
            messagebox.showerror("Error", f"{ve}")

    tk.Button(ventana, text="Guardar", command=guardar_movimiento_producto).grid(row=4, column=0, columnspan=2, pady=10)
def mostrar_inventarios_producto():
    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT inventario_productos_id, almacen_id, producto_id, inv_cantidad, inv_ultima_actualizacion FROM inventario_productos")
            inventarios = cursor.fetchall()

            ventana_listado = tk.Toplevel()
            ventana_listado.title("Inventarios de Productos")
            ventana_listado.geometry("600x400")

            tree = ttk.Treeview(ventana_listado, columns=("ID", "Almacén", "Producto", "Cantidad", "Última Actualización"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Almacén", text="Almacén")
            tree.heading("Producto", text="Producto")
            tree.heading("Cantidad", text="Cantidad")
            tree.heading("Última Actualización", text="Última Actualización")
            tree.pack(fill=tk.BOTH, expand=True)

            for inventario in inventarios:
                tree.insert("", tk.END, values=inventario)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo obtener los inventarios: {err}")
        finally:
            conexion.close()
def listar_movimientos_producto():
    conexion = conectar_base_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT m.movimiento_id, m.mov_tipo_movimiento, m.mov_cantidad, m.mov_fecha_movimiento, m.mov_descripcion, 
                       i.inv_cantidad, m.inventario_productos_id
                FROM movimientos_inv_productos m
                JOIN inventario_productos i ON m.inventario_productos_id = i.inventario_productos_id
            """)
            movimientos = cursor.fetchall()

            ventana_listado = tk.Toplevel()
            ventana_listado.title("Movimientos de Productos")
            ventana_listado.geometry("700x400")

            tree = ttk.Treeview(ventana_listado, columns=("ID", "Tipo", "Cantidad", "Fecha", "Descripción", "Inventario Actual", "ID Inventario"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Tipo", text="Tipo")
            tree.heading("Cantidad", text="Cantidad")
            tree.heading("Fecha", text="Fecha")
            tree.heading("Descripción", text="Descripción")
            tree.heading("Inventario Actual", text="Inventario Actual")
            tree.heading("ID Inventario", text="ID Inventario")
            tree.pack(fill=tk.BOTH, expand=True)

            for movimiento in movimientos:
                tree.insert("", tk.END, values=movimiento)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo obtener los movimientos: {err}")
        finally:
            conexion.close()
def gestionar_inventarios_producto():
    root = tk.Tk()
    root.title("Sistema de Control de Inventarios de Productos")
    root.geometry("400x350")

    tk.Button(root, text="Registrar Inventario Producto",font=("Courier New", 10), command=abrir_formulario_inventario_productos).pack(pady=10)
    tk.Button(root, text="Registrar Movimiento Producto",font=("Courier New", 10), command=abrir_formulario_movimiento_productos).pack(pady=10)
    tk.Button(root, text="Listar Inventarios Producto",font=("Courier New", 10), command=mostrar_inventarios_producto).pack(pady=10)
    tk.Button(root, text="Listar Movimientos Producto",font=("Courier New", 10), command=listar_movimientos_producto).pack(pady=10)

    root.mainloop()
def verificar_contraseña():
    def validar():
        contraseña_ingresada = entry_contraseña.get()
        if contraseña_ingresada == "123": 
            ventana_contraseña.destroy()
            abrir_menu_administrador()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta. Inténtalo de nuevo.")
    ventana_contraseña = tk.Toplevel()
    ventana_contraseña.title("Verificación de Contraseña")
    ventana_contraseña.geometry("300x150")
    ventana_contraseña.resizable(False, False)
    
    tk.Label(ventana_contraseña, text="Introduce la contraseña:",font=("Courier New", 10)).pack(pady=10)
    entry_contraseña = tk.Entry(ventana_contraseña, show="*", width=25)
    entry_contraseña.pack(pady=5)

    tk.Button(ventana_contraseña, text="Ingresar",font=("Courier New", 10), command=validar).pack(pady=10)
def abrir_menu_administrador():
    ventana_admin = tk.Tk()
    ventana_admin.title("Menú Principal")
    ventana_admin.geometry("400x500")

    tk.Label(ventana_admin, text="Menú Principal",font=("Courier New", 14)).pack(pady=10)
    
    tk.Button(ventana_admin, text="Gestión de Productos",font=("Courier New", 10), command=gestionar_productos).pack(pady=5)
    tk.Button(ventana_admin, text="Gestión de Clientes",font=("Courier New", 10), command=gestionar_clientes).pack(pady=5)
    tk.Button(ventana_admin, text="Gestión de Empleados",font=("Courier New", 10), command=gestionar_empleados).pack(pady=5)
    tk.Button(ventana_admin, text="Gestión de Asistencia",font=("Courier New", 10), command=gestionar_asistencia).pack(pady=5)
    tk.Button(ventana_admin, text="Gestion Pedidos",font=("Courier New", 10), command=gestionar_pedidos).pack(pady=5)
    tk.Button(ventana_admin, text="Gestion Envios",font=("Courier New", 10), command=gestionar_envios).pack(pady=5)
    tk.Button(ventana_admin, text="Gestion Almacenes",font=("Courier New", 10), command=gestionar_almacenes).pack(pady=5)
    tk.Button(ventana_admin, text="Gestion Proveedores",font=("Courier New", 10), command=gestionar_proveedores).pack(pady=5)
    tk.Button(ventana_admin, text="Gestion Materiales",font=("Courier New", 10), command=gestionar_materiales).pack(pady=5)
    tk.Button(ventana_admin, text="Gestion Inventario Materiales",font=("Courier New", 10), command=gestionar_inventarios).pack(pady=5)
    tk.Button(ventana_admin, text="Gestion Inventario Productos",font=("Courier New", 10), command=gestionar_inventarios_producto).pack(pady=5)
    tk.Button(ventana_admin, text="Salir",font=("Courier New", 10), command=ventana_admin.destroy).pack(pady=10)

    ventana_admin.mainloop()
def abrir_menu_usuario():
    ventana_usuario = tk.Toplevel()
    ventana_usuario.title("Menú de Usuario")
    ventana_usuario.geometry("300x200")
    
    tk.Label(ventana_usuario,font=("Courier New", 14)).pack(pady=10)
    
    tk.Button(ventana_usuario, text="Registrar Pedido ",font=("Courier New", 10), command=registrar_pedido).pack(pady=5)
    tk.Button(ventana_usuario, text="Salir",font=("Courier New", 10), command=ventana_usuario.destroy).pack(pady=10)
def menu_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("Sistema Empresarial",)
    ventana_principal.geometry("300x200")
    
    tk.Label(ventana_principal, text="Bienvenido", font=("Courier New", 14)).pack(pady=10)
    tk.Button(ventana_principal, text="Administrador", font=("Courier New", 10),command=verificar_contraseña).pack(pady=5)
    tk.Button(ventana_principal, text="Usuario",font=("Courier New", 10), command=abrir_menu_usuario).pack(pady=5)
    tk.Button(ventana_principal, text="Salir",font=("Courier New", 10), command=ventana_principal.destroy).pack(pady=10)
    
    ventana_principal.mainloop()

menu_principal()