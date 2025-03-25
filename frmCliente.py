import tkinter as tk
from tkinter import messagebox, ttk
from dbClientes import dbCliente
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

        tk.Label(main_frame, text="Usuario ID:").grid(row=4, column=0, sticky="e", pady=5)
        self.usuario_id_combo = ttk.Combobox(main_frame, values=self.usuariosList())
        self.usuario_id_combo.grid(row=4, column=1, pady=5)

        button_frame = tk.Frame(main_frame, pady=10)
        button_frame.grid(row=5, column=0, columnspan=2)

        tk.Button(button_frame, text="Guardar", command=self.save_cliente).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Actualizar", command=self.update_cliente).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Eliminar", command=self.delete_cliente).grid(row=0, column=2, padx=5) 
        tk.Button(button_frame, text="Buscar", command=self.get_cliente).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Limpiar", command=self.clear_fields).grid(row=0, column=4, padx=5)

    def save_cliente(self):

        if self.id_entry.get() != "":
            messagebox.showerror("Error", "No se puede guardar un cliente con ID")
            return
        
        if self.nombre_entry.get() == "" or self.telefono_entry.get() == "" or self.rfc_entry.get() == "" or self.usuario_id_combo.get() == "":
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return

        c = Cliente()
        c.setNombre(self.nombre_entry.get())
        c.setTelefono(self.telefono_entry.get())
        c.setRFC(self.rfc_entry.get())
        c.setUsuarioID(int(self.usuario_id_combo.get().split(" - ")[0]))

        if self.db.save(c):
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo guardar el cliente")

    def update_cliente(self):

        if self.id_entry.get() == "":
            messagebox.showerror("Error", "No se puede actualizar un cliente sin ID")
            return
        
        if self.nombre_entry.get() == "" or self.telefono_entry.get() == "" or self.rfc_entry.get() == "" or self.usuario_id_combo.get() == "":
            messagebox.showerror("Error", "Todos los campos son requeridos")

        c = Cliente()
        c.setID(int(self.id_entry.get()))
        c.setNombre(self.nombre_entry.get())
        c.setTelefono(self.telefono_entry.get())
        c.setRFC(self.rfc_entry.get())
        c.setUsuarioID(int(self.usuario_id_combo.get().split(" - ")[0]))

        if self.db.update(c):
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el cliente")

    def delete_cliente(self):

        if self.id_entry.get() == "":
            messagebox.showerror("Error", "No se puede eliminar un cliente sin ID")
            return

        c = Cliente()
        c.setID(int(self.id_entry.get()))

        if self.db.delete(c):
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el cliente")

    def get_cliente(self):

        if self.id_entry.get() == "":
            messagebox.showerror("Error", "Se requiere un ID para buscar un cliente")
            return

        c = Cliente()
        c.setID(int(self.id_entry.get()))
        c = self.db.get(c)

        if c != None:
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, c.getNombre())
            self.telefono_entry.delete(0, tk.END)
            self.telefono_entry.insert(0, c.getTelefono())
            self.rfc_entry.delete(0, tk.END)
            self.rfc_entry.insert(0, c.getRFC())
            self.usuario_id_combo.set(f"{c.getUsuarioID()} - {c.getUsuarioID()}")
        else:
            messagebox.showerror("Error", "Cliente no encontrado")

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.rfc_entry.delete(0, tk.END)
        self.usuario_id_combo.set("")

    def usuariosList(self) -> list[str]:
        from dbUsers import dbUser
        db = dbUser()
        usuarios = db.getAll()
        usuarios_list = []
        for u in usuarios:
            usuarios_list.append(f"{u.getID()} - {u.getNombre()}")
        return usuarios_list
    
if __name__ == "__main__":
    root = tk.Tk()
    frmCliente(root)
    root.mainloop()