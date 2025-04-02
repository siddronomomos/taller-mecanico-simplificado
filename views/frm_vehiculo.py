import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from models.vehiculo import Vehiculo
from models.user import User
from db.vehiculo_dao import VehiculoDAO
from db.cliente_dao import ClienteDAO
from views.base_form import BaseForm

class VehiculoForm(BaseForm):
    def __init__(self, parent, user: User, matricula: Optional[str] = None):
        super().__init__(parent, "Gestión de Vehículo", 600, 450)
        self.user = user
        self.matricula = matricula
        self.vehiculo_dao = VehiculoDAO()
        self.cliente_dao = ClienteDAO()
        self.vehiculo = None
        
        self._create_widgets()
        self._load_data()
        self._setup_permissions()
    
    def _setup_permissions(self):
        """Configura los permisos según el tipo de usuario"""
        if self.user.perfil != 'admin' and self.matricula:
            # Para usuarios no-admin con vehículo existente
            self.matricula_entry.config(state='disabled')
            self.serie_entry.config(state='disabled')
            self.modelo_entry.config(state='disabled')
            self.marca_entry.config(state='disabled')
            self.anio_entry.config(state='disabled')
            self.cliente_combo.config(state='disabled')
            
            # Ocultar botones no permitidos
            for btn in [self.delete_btn, self.save_btn]:
                btn.pack_forget()
    
    def _create_widgets(self):
        main_frame = self.create_frame(self)
        main_frame.columnconfigure(1, weight=1)
        
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(search_frame, text="Buscar Vehículo por Matrícula:").pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_frame, width=15)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(
            search_frame, 
            text="Buscar", 
            command=self._search_vehiculo
        ).pack(side='left', padx=5)
        
        # Campos del formulario
        row_offset = 1
        
        # Matrícula
        ttk.Label(main_frame, text="Matrícula:").grid(row=row_offset, column=0, sticky='e', padx=5, pady=5)
        self.matricula_entry = ttk.Entry(main_frame)
        self.matricula_entry.grid(row=row_offset, column=1, sticky='ew', padx=5, pady=5)
        
        # Serie
        ttk.Label(main_frame, text="Serie:").grid(row=row_offset+1, column=0, sticky='e', padx=5, pady=5)
        self.serie_entry = ttk.Entry(main_frame)
        self.serie_entry.grid(row=row_offset+1, column=1, sticky='ew', padx=5, pady=5)
        
        # Modelo
        ttk.Label(main_frame, text="Modelo:").grid(row=row_offset+2, column=0, sticky='e', padx=5, pady=5)
        self.modelo_entry = ttk.Entry(main_frame)
        self.modelo_entry.grid(row=row_offset+2, column=1, sticky='ew', padx=5, pady=5)
        
        # Marca
        ttk.Label(main_frame, text="Marca:").grid(row=row_offset+3, column=0, sticky='e', padx=5, pady=5)
        self.marca_entry = ttk.Entry(main_frame)
        self.marca_entry.grid(row=row_offset+3, column=1, sticky='ew', padx=5, pady=5)
        
        # Año
        ttk.Label(main_frame, text="Año:").grid(row=row_offset+4, column=0, sticky='e', padx=5, pady=5)
        self.anio_entry = ttk.Entry(main_frame)
        self.anio_entry.grid(row=row_offset+4, column=1, sticky='ew', padx=5, pady=5)
        
        # Combobox para cliente
        ttk.Label(main_frame, text="Cliente:").grid(row=row_offset+5, column=0, sticky='e', padx=5, pady=5)
        self.cliente_combo = ttk.Combobox(main_frame, state='readonly')
        self.cliente_combo.grid(row=row_offset+5, column=1, sticky='ew', padx=5, pady=5)
        self._load_clientes()
        
        # Barra de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row_offset+6, column=0, columnspan=2, sticky='e', padx=5, pady=10)
        
        # Botón Eliminar (solo para admin)
        self.delete_btn = ttk.Button(
            button_frame, 
            text="Eliminar", 
            command=self._delete,
            style='Danger.TButton' if 'Danger.TButton' in self.style.map('TButton') else None
        )
        
        # Botón Limpiar (solo para admin)
        self.clear_btn = ttk.Button(
            button_frame,
            text="Limpiar",
            command=self._clear_form,
            style='Secondary.TButton' if 'Secondary.TButton' in self.style.map('TButton') else None
        )
        
        # Botón Guardar
        self.save_btn = ttk.Button(
            button_frame, 
            text="Guardar", 
            command=self._save,
            style='Accent.TButton'
        )
        self.save_btn.pack(side='left', padx=5)
        
        # Botón Cancelar
        ttk.Button(
            button_frame, 
            text="Cancelar", 
            command=self.destroy
        ).pack(side='left', padx=5)
        
        # Mostrar botones según permisos
        if self.user.perfil == 'admin':
            self.clear_btn.pack(side='left', padx=5)
            if self.matricula:
                self.delete_btn.pack(side='left', padx=5)
    
    def _load_clientes(self):
        clientes = self.cliente_dao.get_all()
        self.clientes = {f"{c.nombre} ({c.rfc})": c.cliente_id for c in clientes}
        self.cliente_combo['values'] = list(self.clientes.keys())
    
    def _search_vehiculo(self):
        """Busca un vehículo por matrícula"""
            
        matricula = self.search_entry.get().strip().upper()
        if not matricula:
            messagebox.showerror("Error", "Ingrese una matrícula válida")
            return
        
        vehiculo = self.vehiculo_dao.get(matricula)
        if not vehiculo:
            messagebox.showerror("Error", f"No se encontró vehículo con matrícula {matricula}")
            return
        
        # Cargar datos del vehículo encontrado
        self.matricula = matricula
        self.vehiculo = vehiculo
        self._load_vehiculo_data()
        
        # Actualizar visibilidad de botones
        self.delete_btn.pack(side='left', padx=5)
        
        messagebox.showinfo("Éxito", f"Vehículo {matricula} cargado correctamente")
    
    def _load_vehiculo_data(self):
        """Carga los datos del vehículo en los campos del formulario"""
        if not self.vehiculo:
            return
            
        self.matricula_entry.config(state='normal')
        self.matricula_entry.delete(0, tk.END)
        self.matricula_entry.insert(0, self.vehiculo.matricula)
        
        self.serie_entry.delete(0, tk.END)
        self.serie_entry.insert(0, self.vehiculo.serie)
        
        self.modelo_entry.delete(0, tk.END)
        self.modelo_entry.insert(0, self.vehiculo.modelo)
        
        self.marca_entry.delete(0, tk.END)
        self.marca_entry.insert(0, self.vehiculo.marca)
        
        self.anio_entry.delete(0, tk.END)
        if self.vehiculo.anio:
            self.anio_entry.insert(0, str(self.vehiculo.anio))
        
        # Seleccionar cliente
        cliente = self.cliente_dao.get(self.vehiculo.cliente_id)
        if cliente:
            cliente_str = f"{cliente.nombre} ({cliente.rfc})"
            self.cliente_combo.set(cliente_str)
    
    def _load_data(self):
        if self.matricula:
            self.vehiculo = self.vehiculo_dao.get(self.matricula)
            if self.vehiculo:
                self._load_vehiculo_data()
    
    def _clear_form(self):
        """Limpia el formulario (solo para admin)"""
        if self.user.perfil != 'admin':
            return
            
        self.matricula = None
        self.vehiculo = None
        
        self.matricula_entry.config(state='normal')
        self.matricula_entry.delete(0, tk.END)
        
        self.serie_entry.delete(0, tk.END)
        self.modelo_entry.delete(0, tk.END)
        self.marca_entry.delete(0, tk.END)
        self.anio_entry.delete(0, tk.END)
        self.cliente_combo.set('')
        
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, tk.END)
        
        self.delete_btn.pack_forget()
    
    def _get_form_data(self) -> Optional[Vehiculo]:
        matricula = self.matricula_entry.get().strip().upper()
        serie = self.serie_entry.get().strip()
        modelo = self.modelo_entry.get().strip()
        marca = self.marca_entry.get().strip()
        anio_str = self.anio_entry.get().strip()
        cliente_str = self.cliente_combo.get()
        
        if not all([matricula, serie, modelo, marca, cliente_str]):
            self.show_error("Matrícula, serie, modelo, marca y cliente son obligatorios")
            return None
            
        try:
            anio = int(anio_str) if anio_str else None
            cliente_id = self.clientes[cliente_str]
            
            vehiculo = Vehiculo(
                matricula=matricula,
                serie=serie,
                modelo=modelo,
                marca=marca,
                anio=anio,
                cliente_id=cliente_id
            )
            
            if not vehiculo.validate():
                self.show_error("Datos del vehículo no válidos")
                return None
                
            return vehiculo
        except ValueError:
            self.show_error("El año debe ser un número válido")
            return None
        except KeyError:
            self.show_error("Seleccione un cliente válido")
            return None
    
    def _save(self):
        vehiculo = self._get_form_data()
        if not vehiculo:
            return
            
        if self.matricula:
            if self.user.perfil != 'admin':
                self.show_error("No tiene permisos para editar vehículos")
                return
                
            success = self.vehiculo_dao.update(vehiculo)
            msg = "actualizado"
        else:
            success = self.vehiculo_dao.save(vehiculo)
            msg = "registrado"
            
        if success:
            self.show_success(f"Vehículo {msg} correctamente")
            if self.user.perfil == 'admin':
                self._clear_form()
            else:
                self.destroy()
        else:
            self.show_error(f"No se pudo {msg} el vehículo")
    
    def _delete(self):
        if not self.matricula or self.user.perfil != 'admin':
            return
            
        if self.ask_confirmation("¿Está seguro de eliminar este vehículo?"):
            if self.vehiculo_dao.delete(self.matricula):
                self.show_success("Vehículo eliminado correctamente")
                self._clear_form()
            else:
                self.show_error("No se pudo eliminar el vehículo")