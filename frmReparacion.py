import tkinter as tk
from tkinter import ttk, messagebox
from dbReparacion import dbReparacion
from dbVehiculos import dbVehiculo
from reparacion import Reparacion

class frmReparacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Reparaciones")
        self.root.geometry("400x300")
        
        self.db_reparacion = dbReparacion()
        self.db_vehiculo = dbVehiculo()
        
        # Matricula
        ttk.Label(root, text="Matrícula:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.matricula_var = tk.StringVar()
        self.matricula_combobox = ttk.Combobox(root, textvariable=self.matricula_var, state="readonly")
        self.matricula_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.load_matriculas()
        
        # Fecha entrada
        ttk.Label(root, text="Fecha Entrada:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.fecha_entrada = tk.Entry(root)
        self.fecha_entrada.grid(row=1, column=1, padx=10, pady=5)
        
        # Fecha salida
        ttk.Label(root, text="Fecha Salida:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.fecha_salida = tk.Entry(root)
        self.fecha_salida.grid(row=2, column=1, padx=10, pady=5)
        
        # Botón Guardar
        self.btn_guardar = ttk.Button(root, text="Guardar", command=self.guardar_reparacion)
        self.btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)
        
    def load_matriculas(self):
        vehiculos = self.db_vehiculo.getAll()
        matriculas = [v.getMatricula() for v in vehiculos]
        self.matricula_combobox["values"] = matriculas
    
    def guardar_reparacion(self):
        matricula = self.matricula_var.get()
        fecha_entrada = self.fecha_entrada.get()
        fecha_salida = self.fecha_salida.get()
        
        if not matricula or not fecha_entrada or not fecha_salida:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        reparacion = Reparacion()
        reparacion.setMatricula(matricula)
        reparacion.setFechaEntrada(fecha_entrada)
        reparacion.setFechaSalida(fecha_salida)
        
        if self.db_reparacion.save(reparacion):
            messagebox.showinfo("Éxito", "Reparación guardada exitosamente")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar la reparación")

if __name__ == "__main__":
    root = tk.Tk()
    app = frmReparacion(root)
    root.mainloop()
