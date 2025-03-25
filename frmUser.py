import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dbUser import dbUser
from user import User

class frmUser:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD Usuarios")
        self.db = dbUser()
        
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        tk.Label(main_frame, text="ID:").grid(row=0, column=0, sticky="e", pady=5)
        self.id_entry = tk.Entry(main_frame)
        self.id_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(main_frame, text="Nombre:").grid(row=1, column=0, sticky="e", pady=5)
        self.nombre_entry = tk.Entry(main_frame)
        self.nombre_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(main_frame, text="Usuario:").grid(row=2, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(main_frame)
        self.username_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(main_frame, text="Contraseña:").grid(row=3, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(main_frame, show="*")
        self.password_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(main_frame, text="Perfil:").grid(row=4, column=0, sticky="e", pady=5)
        self.perfil_combobox = ttk.Combobox(main_frame, values=["Admin", "Auxiliar", "Mecánico"])
        self.perfil_combobox.grid(row=4, column=1, pady=5)
        
        button_frame = tk.Frame(main_frame, pady=10)
        button_frame.grid(row=5, column=0, columnspan=2)
        
        tk.Button(button_frame, text="Guardar", command=self.save_user).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Actualizar", command=self.update_user).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Eliminar", command=self.delete_user).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Buscar", command=self.get_user).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Limpiar", command=self.clear_fields).grid(row=0, column=4, padx=5)
        
    def save_user(self):
        u = User()
        u.setNombre(self.nombre_entry.get())
        u.setUserName(self.username_entry.get())
        u.setPassword(self.password_entry.get())
        u.setPerfil(self.perfil_combobox.get())
        
        if self.db.save(u):
            messagebox.showinfo("Éxito", "Usuario guardado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo guardar el usuario")
        
    def update_user(self):
        u = User()
        u.setID(int(self.id_entry.get()))
        u.setNombre(self.nombre_entry.get())
        u.setUserName(self.username_entry.get())
        u.setPassword(self.password_entry.get())
        u.setPerfil(self.perfil_combobox.get())
        
        if self.db.update(u):
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el usuario")
        
    def delete_user(self):
        u = User()
        u.setID(int(self.id_entry.get()))
        
        if self.db.delete(u):
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el usuario")
        
    def get_user(self):
        u = User()
        u.setID(int(self.id_entry.get()))
        result = self.db.get(u)
        
        if result:
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, result.getNombre())
            
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, result.getUserName())
            
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, result.getPassword())
            
            self.perfil_combobox.set(result.getPerfil())
        else:
            messagebox.showerror("Error", "Usuario no encontrado")
    
    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.perfil_combobox.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = frmUser(root)
    root.mainloop()