import tkinter as tk
from tkinter import messagebox, ttk
from dbCliente import dbCliente
from cliente import Cliente

class frmCliente:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CRUD Clientes")
        self.db = dbCliente()

        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(main_frame, text="ID:").grid(row=0, column=0, sticky="e", pady=5)
        self.id_entry = tk.Entry(main_frame)
        self.id_entry.grid(row=0, column=1, pady=5)

        tk.Label(main_frame, text="Nombre:").grid(row=1, column=0, sticky="e", pady=5)
        self.nombre_entry = tk.Entry(main_frame)
        self.nombre_entry.grid(row=1, column=1, pady=5)

        tk.Label(main_frame, text="Teléfono:").grid(row=2, column=0, sticky="e", pady=5)
        self.telefono_entry = tk.Entry(main_frame)
        self.telefono_entry.grid(row=2, column=1, pady=5)

        tk.Label(main_frame, text="RFC:").grid(row=3, column=0, sticky="e", pady=5)
        self.rfc_entry = tk.Entry(main_frame)
        self.rfc_entry.grid(row=3, column=1, pady=5)

        

        button_frame = tk.Frame(main_frame, pady=10)
        button_frame.grid(row=4, column=0, columnspan=2)

        tk.Button(button_frame, text="Guardar", command=self.save_cliente).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Actualizar", command=self.update_cliente).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Eliminar", command=self.delete_cliente).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Buscar", command=self.get_cliente).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Limpiar", command=self.clear_fields).grid(row=0, column=4, padx=5)

    def save_cliente(self):
        c = Cliente()
        c.setID(int(self.id_entry.get()))
        c.setNombre(self.nombre_entry.get())
        c.setTelefono(self.telefono_entry.get())
        c.setRFC(self.rfc_entry.get())

        if self.db.save(c):
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo guardar el cliente")

    def update_cliente(self):
        c = Cliente()
        c.setID(int(self.id_entry.get()))
        c.setNombre(self.nombre_entry.get())
        c.setTelefono(self.telefono_entry.get())
        c.setRFC(self.rfc_entry.get())

        if self.db.update(c):
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el cliente")

    def delete_cliente(self):
        c = Cliente()
        c.setID(int(self.id_entry.get()))

        if self.db.delete(c):
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el cliente")

    def get_cliente(self):
        c = Cliente()
        c.setID(int(self.id_entry.get()))
        c = self.db.get(c)

        if c is not None:
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, c.getNombre())
            self.telefono_entry.delete(0, tk.END)
            self.telefono_entry.insert(0, c.getTelefono())
            self.rfc_entry.delete(0, tk.END)
            self.rfc_entry.insert(0, c.getRFC())
        else:
            messagebox.showerror("Error", "No se encontró el cliente")

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.rfc_entry.delete(0, tk.END)
