import tkinter as tk
from tkinter import ttk, messagebox
from pieza import Pieza
from dbPiezas import dbPiezas

class frmPiezas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Piezas")
        self.root.geometry("500x400")
        
        self.db = dbPiezas()
        
        # Labels y Entradas
        ttk.Label(root, text="Descripción:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.descripcion_entry = ttk.Entry(root, width=40)
        self.descripcion_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(root, text="Existencias:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.existencias_entry = ttk.Entry(root, width=40)
        self.existencias_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Botones
        self.btn_guardar = ttk.Button(root, text="Guardar", command=self.guardar_pieza)
        self.btn_guardar.grid(row=2, column=0, padx=10, pady=5)
        
        self.btn_eliminar = ttk.Button(root, text="Eliminar", command=self.eliminar_pieza)
        self.btn_eliminar.grid(row=2, column=1, padx=10, pady=5)
        
        # Lista de piezas
        self.tree = ttk.Treeview(root, columns=("ID", "Descripción", "Existencias"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Existencias", text="Existencias")
        self.tree.column("ID", width=50)
        self.tree.column("Descripción", width=250)
        self.tree.column("Existencias", width=100)
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        
        self.cargar_piezas()

    def cargar_piezas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        piezas = self.db.getAll()
        for pieza in piezas:
            self.tree.insert("", "end", values=(pieza.getID(), pieza.getDescripcion(), pieza.getExistencias()))
    
    def guardar_pieza(self):
        descripcion = self.descripcion_entry.get()
        existencias = self.existencias_entry.get()
        
        if not descripcion or not existencias.isdigit():
            messagebox.showerror("Error", "Ingrese datos válidos")
            return
        
        pieza = Pieza()
        pieza.setDescripcion(descripcion)
        pieza.setExistencias(int(existencias))
        
        if self.db.save(pieza):
            messagebox.showinfo("Éxito", "Pieza guardada correctamente")
            self.cargar_piezas()
        else:
            messagebox.showerror("Error", "No se pudo guardar la pieza")
    
    def eliminar_pieza(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una pieza para eliminar")
            return
        
        pieza_id = self.tree.item(selected_item, "values")[0]
        pieza = Pieza()
        pieza.setID(pieza_id)
        
        if self.db.delete(pieza):
            messagebox.showinfo("Éxito", "Pieza eliminada correctamente")
            self.cargar_piezas()
        else:
            messagebox.showerror("Error", "No se pudo eliminar la pieza")

if __name__ == "__main__":
    root = tk.Tk()
    app = frmPiezas(root)
    root.mainloop()
