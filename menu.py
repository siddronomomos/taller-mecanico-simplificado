import tkinter as tk
from tkinter import messagebox
from frmUser import frmUser
from frmCliente import frmCliente
from frmVehiculo import frmVehiculo


def abrir_usuarios():
    if user_role != "admin":
        messagebox.showerror("Acceso Denegado", "No tienes permiso para acceder a esta sección.")
        return
    ventana_usuarios = tk.Toplevel()
    ventana_usuarios.title("Formulario de Usuarios")
    ventana_usuarios.geometry("400x400")
    app = frmUser(ventana_usuarios)
def abrir_clientes():
    if user_role not in ["admin", "aux"]:
        messagebox.showerror("Acceso Denegado", "No tienes permiso para acceder a esta sección.")
        return
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Formulario de Clientes")
    ventana_clientes.geometry("400x400")
    app = frmCliente(ventana_clientes)

def abrir_vehiculos():
    if user_role not in ["admin", "aux"]:
        messagebox.showerror("Acceso Denegado", "No tienes permiso para acceder a esta sección.")
        return
    ventana_vehiculos = tk.Toplevel()
    ventana_vehiculos.title("Formulario de Vehículos")
    ventana_vehiculos.geometry("400x400")
    app = frmVehiculo(ventana_vehiculos)

def abrir_reparaciones():
    if user_role not in ["admin", "mecanico"]:
        messagebox.showerror("Acceso Denegado", "No tienes permiso para acceder a esta sección.")
        return
    messagebox.showinfo("Reparaciones", "Abrir Formulario de Reparaciones")

def abrir_piezas():
    if user_role not in ["admin", "mecanico"]:
        messagebox.showerror("Acceso Denegado", "No tienes permiso para acceder a esta sección.")
        return
    messagebox.showinfo("Piezas", "Abrir Formulario de Piezas")

def iniciar_menu(role):
    global user_role
    user_role = role

    ventana = tk.Tk()
    ventana.title("Menú Principal - Taller Mecánico")
    ventana.geometry("400x400")
    ventana.configure(bg="#f0f0f0")

    titulo = tk.Label(ventana, text="Menú Principal", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
    titulo.pack(pady=20)

    boton1 = tk.Button(ventana, text="Usuarios", font=("Arial", 12), bg="#4CAF50", fg="white", width=20, command=abrir_usuarios)
    boton1.pack(pady=10)

    boton2 = tk.Button(ventana, text="Clientes", font=("Arial", 12), bg="#2196F3", fg="white", width=20, command=abrir_clientes)
    boton2.pack(pady=10)

    boton3 = tk.Button(ventana, text="Vehículos", font=("Arial", 12), bg="#FF9800", fg="white", width=20, command=abrir_vehiculos)
    boton3.pack(pady=10)

    boton4 = tk.Button(ventana, text="Reparaciones", font=("Arial", 12), bg="#9C27B0", fg="white", width=20, command=abrir_reparaciones)
    boton4.pack(pady=10)

    boton5 = tk.Button(ventana, text="Piezas", font=("Arial", 12), bg="#F44336", fg="white", width=20, command=abrir_piezas)
    boton5.pack(pady=10)

    ventana.mainloop()