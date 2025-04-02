import tkinter as tk
from tkinter import ttk
from config import Config
from models.user import User

class MenuApp:
    def __init__(self, root: tk.Tk, user: User):
        self.root = root
        self.user = user
        self.root.title(f"{Config.APP_TITLE} - {user.perfil.capitalize()}")
        self.root.geometry("600x400")
        self.root.focus_force()
        self._create_widgets()
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        banner_frame = ttk.Frame(main_frame)
        banner_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(banner_frame, 
                 text=f"Bienvenido, {self.user.nombre}",
                 font=('Arial', 14)).pack(side='left')
        
        ttk.Label(banner_frame, 
                 text=f"Perfil: {self.user.perfil}",
                 font=('Arial', 12)).pack(side='right')
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='both', expand=True)
        
        buttons = []
        
        if self.user.perfil == 'admin':
            buttons.extend([
                ("Usuarios", self._open_users),
                ("Clientes", self._open_clientes),
                ("Vehículos", self._open_vehiculos),
                ("Reparaciones", self._open_reparaciones),
                ("Piezas", self._open_piezas)
            ])
        elif self.user.perfil == 'aux':
            buttons.extend([
                ("Clientes", self._open_clientes),
                ("Vehículos", self._open_vehiculos)
            ])
        elif self.user.perfil == 'mecanico':
            buttons.extend([
                ("Reparaciones", self._open_reparaciones),
            ])
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(buttons_frame, 
                           text=text, 
                           command=command,
                           style='Accent.TButton')
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            buttons_frame.rowconfigure(i//2, weight=1)
            buttons_frame.columnconfigure(i%2, weight=1)
        
        ttk.Button(main_frame, 
                  text="Cerrar Sesión", 
                  command=self._logout).pack(pady=(20, 0))
    
    def _open_users(self):
        from views.frm_user import UserForm
        UserForm(self.root)
    
    def _open_clientes(self):
        from views.frm_cliente import ClienteForm
        ClienteForm(self.root, self.user)
    
    def _open_vehiculos(self):
        from views.frm_vehiculo import VehiculoForm
        VehiculoForm(self.root, self.user)
    
    def _open_reparaciones(self):
        from views.frm_reparacion import ReparacionForm
        ReparacionForm(self.root, self.user)
    
    def _open_piezas(self):
        from views.frm_piezas import PiezasForm
        PiezasForm(self.root)
    
    def _logout(self):
        self.root.destroy()
        from app import App
        App()