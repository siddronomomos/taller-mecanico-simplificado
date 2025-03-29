import tkinter as tk
from tkinter import messagebox, ttk
from dbVehiculos import dbVehiculo
from vehiculo import Vehiculo

class frmVehiculo:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CRUD Vehículos")
        self.db = dbVehiculo()

        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(main_frame, text="Matrícula:").grid(row=0, column=0, sticky="e", pady=5)
        self.matricula_entry = tk.Entry(main_frame)
        self.matricula_entry.grid(row=0, column=1, pady=5)

        tk.Label(main_frame, text="Serie:").grid(row=1, column=0, sticky="e", pady=5)
        self.serie_entry = tk.Entry(main_frame)
        self.serie_entry.grid(row=1, column=1, pady=5)

        tk.Label(main_frame, text="Modelo:").grid(row=2, column=0, sticky="e", pady=5)
        self.modelo_entry = tk.Entry(main_frame)
        self.modelo_entry.grid(row=2, column=1, pady=5)

        tk.Label(main_frame, text="Marca:").grid(row=3, column=0, sticky="e", pady=5)
        self.marca_entry = tk.Entry(main_frame)
        self.marca_entry.grid(row=3, column=1, pady=5)

        tk.Label(main_frame, text="Cliente ID:").grid(row=4, column=0, sticky="e", pady=5)
        self.cliente_id_combo = ttk.Combobox(main_frame, values=self.clientesList())
        self.cliente_id_combo.grid(row=4, column=1, pady=5)

        button_frame = tk.Frame(main_frame, pady=10)
        button_frame.grid(row=5, column=0, columnspan=2)

        tk.Button(button_frame, text="Guardar", command=self.save_vehiculo).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Actualizar", command=self.update_vehiculo).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Eliminar", command=self.delete_vehiculo).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Buscar", command=self.get_vehiculo).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Limpiar", command=self.clear_fields).grid(row=0, column=4, padx=5)

    def save_vehiculo(self):

        if self.matricula_entry.get() == "" or self.serie_entry.get() == "" or self.modelo_entry.get() == "" or self.marca_entry.get() == "" or self.cliente_id_combo.get() == "":
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return

        v = Vehiculo()
        v.setMatricula(self.matricula_entry.get())
        v.setSerie(self.serie_entry.get())
        v.setModelo(self.modelo_entry.get())
        v.setMarca(self.marca_entry.get())
        v.setClienteID(int(self.cliente_id_combo.get().split(" - ")[0]))

        if self.db.save(v):
            messagebox.showinfo("Éxito", "Vehículo guardado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo guardar el vehículo")

    def update_vehiculo(self):

        if self.matricula_entry.get() == "":
            messagebox.showerror("Error", "Se requiere una matrícula para actualizar un vehículo")
            return

        v = Vehiculo()
        v.setMatricula(self.matricula_entry.get())
        v.setSerie(self.serie_entry.get())
        v.setModelo(self.modelo_entry.get())
        v.setMarca(self.marca_entry.get())
        v.setClienteID(int(self.cliente_id_combo.get().split(" - ")[0]))

        if self.db.update(v):
            messagebox.showinfo("Éxito", "Vehículo actualizado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el vehículo")

    def delete_vehiculo(self):

        if self.matricula_entry.get() == "":
            messagebox.showerror("Error", "Se requiere una matrícula para eliminar un vehículo")
            return

        v = Vehiculo()
        v.setMatricula(self.matricula_entry.get())

        if self.db.delete(v):
            messagebox.showinfo("Éxito", "Vehículo eliminado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el vehículo")

    def get_vehiculo(self):

        if self.matricula_entry.get() == "":
            messagebox.showerror("Error", "Se requiere una matrícula para buscar un vehículo")
            return

        v = Vehiculo()
        v.setMatricula(self.matricula_entry.get())
        v = self.db.get(v)

        if v != None:
            self.serie_entry.delete(0, tk.END)
            self.serie_entry.insert(0, v.getSerie())
            self.modelo_entry.delete(0, tk.END)
            self.modelo_entry.insert(0, v.getModelo())
            self.marca_entry.delete(0, tk.END)
            self.marca_entry.insert(0, v.getMarca())
            self.cliente_id_combo.set(f"{v.getClienteID()} - {self.db.getCliente(v.getClienteID()).getNombre()}")
        else:
            messagebox.showerror("Error", "No se encontró el vehículo")

    def clear_fields(self):
        self.matricula_entry.delete(0, tk.END)
        self.serie_entry.delete(0, tk.END)
        self.modelo_entry.delete(0, tk.END)
        self.marca_entry.delete(0, tk.END)
        self.cliente_id_combo.set("")

    def clientesList(self) -> list[str]:
        from dbClientes import dbCliente
        dbcliente = dbCliente()
        clientes = dbcliente.getAll()
        clientes_list = []
        for c in clientes:
            clientes_list.append(f"{c.getID()} - {c.getNombre()}")
        return clientes_list
    

if __name__ == "__main__":
    root = tk.Tk()
    frmVehiculo(root)
    root.mainloop()