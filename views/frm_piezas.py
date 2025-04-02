import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from models.pieza import Pieza
from db.pieza_dao import PiezaDAO
from views.base_form import BaseForm
import re

class PiezasForm(BaseForm):
    def __init__(self, parent, pieza_id: Optional[int] = None):
        super().__init__(parent, "Gestión de Piezas", 500, 400)
        self.dao = PiezaDAO()
        self.pieza = None
        self.pieza_id = pieza_id
        
        self._create_widgets()
        self._load_data()
    
    def _create_widgets(self):
        main_frame = self.create_frame(self)
        main_frame.columnconfigure(1, weight=1)
        
        # Frame de búsqueda
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(search_frame, text="Buscar Pieza por ID:").pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_frame, width=10)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(
            search_frame, 
            text="Buscar", 
            command=self._search_pieza
        ).pack(side='left', padx=5)
        
        # Campos del formulario
        self.descripcion_entry = self.create_label_entry(main_frame, "Descripción:", 1)
        
        # Validación para existencias (solo números)
        vcmd_exist = (self.register(self._validate_numeric), '%P')
        self.existencias_entry = self.create_label_entry(main_frame, "Existencias:", 2)
        self.existencias_entry.config(validate="key", validatecommand=vcmd_exist)
        
        # Validación para precio (números con decimales)
        vcmd_precio = (self.register(self._validate_currency), '%P')
        self.precio_entry = self.create_label_entry(main_frame, "Precio:", 3)
        self.precio_entry.config(validate="key", validatecommand=vcmd_precio)
        
        # Barra de botones
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.grid(row=4, column=0, columnspan=2, sticky='e', padx=5, pady=10)
        
        # Botón Eliminar (solo visible cuando hay una pieza_id)
        self.delete_btn = ttk.Button(
            self.button_frame, 
            text="Eliminar", 
            command=self._delete,
            style='Danger.TButton' if 'Danger.TButton' in self.style.map('TButton') else None
        )
        
        # Botón Limpiar (siempre visible)
        ttk.Button(
            self.button_frame, 
            text="Limpiar", 
            command=self._clear_form,
            style='Secondary.TButton' if 'Secondary.TButton' in self.style.map('TButton') else None
        ).pack(side='left', padx=5)
        
        # Botón Guardar (siempre visible)
        ttk.Button(
            self.button_frame, 
            text="Guardar", 
            command=self._save,
            style='Accent.TButton'
        ).pack(side='left', padx=5)
        
        # Botón Cancelar (siempre visible)
        ttk.Button(
            self.button_frame, 
            text="Cancelar", 
            command=self.destroy
        ).pack(side='left', padx=5)
        
        # Mostrar el botón de eliminar si hay una pieza_id
        self._update_button_visibility()
    
    def _validate_numeric(self, new_text):
        """Valida que el campo solo contenga números enteros"""
        if not new_text:  # Permitir campo vacío para poder borrar
            return True
        return new_text.isdigit()
    
    def _validate_currency(self, new_text):
        """Valida que el campo sea un valor monetario válido"""
        if not new_text:  # Permitir campo vacío para poder borrar
            return True
        try:
            # Permitir números con hasta 2 decimales
            return bool(re.match(r'^\d*\.?\d{0,2}$', new_text))
        except:
            return False
    
    def _clear_form(self):
        """Limpia todos los campos del formulario y lo resetea a estado inicial"""
        # Limpiar campos de entrada
        self.descripcion_entry.delete(0, tk.END)
        self.existencias_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        
        # Resetear estado del formulario
        self.pieza_id = None
        self.pieza = None
        
        # Actualizar visibilidad de botones
        self._update_button_visibility()
        
        # Enfocar el primer campo
        self.descripcion_entry.focus_set()
    
    def _update_button_visibility(self):
        """Actualiza la visibilidad del botón Eliminar según si hay una pieza cargada"""
        if self.pieza_id is not None:
            self.delete_btn.pack(side='left', padx=5)
        else:
            self.delete_btn.pack_forget()
    
    def _search_pieza(self):
        """Busca una pieza por ID y carga sus datos"""
        pieza_id = self.search_entry.get().strip()
        if not pieza_id.isdigit():
            messagebox.showerror("Error", "ID debe ser un número válido")
            return
        
        pieza_id = int(pieza_id)
        pieza = self.dao.get(pieza_id)
        if not pieza:
            messagebox.showerror("Error", f"No se encontró pieza con ID {pieza_id}")
            return
        
        # Cargar datos de la pieza encontrada
        self.pieza_id = pieza_id
        self.pieza = pieza
        self.descripcion_entry.delete(0, tk.END)
        self.descripcion_entry.insert(0, pieza.descripcion)
        self.existencias_entry.delete(0, tk.END)
        self.existencias_entry.insert(0, str(pieza.existencias))
        self.precio_entry.delete(0, tk.END)
        self.precio_entry.insert(0, f"{pieza.precio:.2f}")
        
        # Actualizar visibilidad del botón Eliminar
        self._update_button_visibility()
        
        messagebox.showinfo("Éxito", f"Pieza {pieza.descripcion} cargada correctamente")
    
    def _load_data(self):
        if self.pieza_id is not None:
            self.pieza = self.dao.get(self.pieza_id)
            if self.pieza:
                self.descripcion_entry.insert(0, self.pieza.descripcion)
                self.existencias_entry.insert(0, str(self.pieza.existencias))
                self.precio_entry.insert(0, f"{self.pieza.precio:.2f}")
                self._update_button_visibility()
    
    def _get_form_data(self) -> Optional[Pieza]:
        descripcion = self.descripcion_entry.get().strip()
        existencias = self.existencias_entry.get().strip()
        precio = self.precio_entry.get().strip()
        
        if not all([descripcion, existencias, precio]):
            self.show_error("Todos los campos son obligatorios")
            return None
            
        try:
            pieza = Pieza(
                pieza_id=self.pieza_id,
                descripcion=descripcion,
                existencias=int(existencias),
                precio=float(precio)
            )
            
            if not pieza.validate():
                self.show_error("Datos de la pieza no válidos")
                return None
                
            return pieza
        except ValueError as e:
            self.show_error(f"Datos numéricos no válidos: {str(e)}")
            return None
    
    def _save(self):
        pieza = self._get_form_data()
        if not pieza:
            return
            
        if self.pieza_id:
            success = self.dao.update(pieza)
            msg = "actualizada"
        else:
            success = self.dao.save(pieza)
            msg = "guardada"
            
        if success:
            self.show_success(f"Pieza {msg} correctamente")
            self._clear_form()  # Limpiar el formulario después de guardar
        else:
            self.show_error(f"No se pudo {msg} la pieza")
    
    def _delete(self):
        if self.pieza_id is None:
            return
            
        if self.ask_confirmation("¿Está seguro de eliminar esta pieza?"):
            if self.dao.delete(self.pieza_id):
                self.show_success("Pieza eliminada correctamente")
                self._clear_form()  # Limpiar el formulario después de eliminar
            else:
                self.show_error("No se pudo eliminar la pieza")