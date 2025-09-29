import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from typing import Optional, List
from models.reparacion import Reparacion
from models.user import User
from models.pieza import Pieza
from db.reparacion_dao import ReparacionDAO
from db.vehiculo_dao import VehiculoDAO
from db.pieza_dao import PiezaDAO
from db.detalle_reparacion_dao import DetalleReparacionDAO
from views.base_form import BaseForm
import re

class ReparacionForm(BaseForm):
    def __init__(self, parent, user: User, folio: Optional[int] = None):
        super().__init__(parent, "Gestión de Reparación", 700, 600)
        self.user = user
        self.folio = folio
        self.reparacion_dao = ReparacionDAO()
        self.vehiculo_dao = VehiculoDAO()
        self.pieza_dao = PiezaDAO()
        self.detalle_dao = DetalleReparacionDAO()
        self.reparacion = None
        self.piezas_asignadas = []
        
        # Expresiones regulares para validación
        self.date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        
        self._create_widgets()
        self._load_data()
        self._setup_permissions()
    
    def _setup_permissions(self):
        """Configura los permisos según el tipo de usuario"""
        if self.user.perfil != 'admin':
            if self.folio:  # Si es una reparación existente
                self.vehiculo_combo.config(state='disabled')
                self.fecha_entrada_entry.config(state='disabled')
                self.fecha_salida_entry.config(state='disabled')
                self.estado_combo.config(state='disabled')
                
                # Solo admin puede eliminar reparaciones
                self.delete_btn.pack_forget()
    
    def _create_widgets(self):
        main_frame = self.create_frame(self)
        main_frame.columnconfigure(1, weight=1)
        
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(search_frame, text="Buscar Reparación por Folio:").pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_frame, width=10)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(
            search_frame, 
            text="Buscar", 
            command=self._search_reparacion
        ).pack(side='left', padx=5)
        
        # Combobox para vehículos
        row_offset = 1
        ttk.Label(main_frame, text="Vehículo:").grid(row=row_offset, column=0, sticky='e', padx=5, pady=5)
        self.vehiculo_combo = ttk.Combobox(main_frame, state='readonly')
        self.vehiculo_combo.grid(row=row_offset, column=1, sticky='ew', padx=5, pady=5)
        self._load_vehiculos()
        
        # Fecha de entrada con validación
        ttk.Label(main_frame, text="Fecha Entrada (YYYY-MM-DD):").grid(row=row_offset+1, column=0, sticky='e', padx=5, pady=5)
        self.fecha_entrada_entry = ttk.Entry(main_frame)
        self.fecha_entrada_entry.grid(row=row_offset+1, column=1, sticky='ew', padx=5, pady=5)
        self.fecha_entrada_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        self.fecha_entrada_entry.bind('<FocusOut>', self._validar_fecha_entrada)
        
        # Fecha de salida con validación después de escribir
        ttk.Label(main_frame, text="Fecha Salida (YYYY-MM-DD):").grid(row=row_offset+2, column=0, sticky='e', padx=5, pady=5)
        self.fecha_salida_entry = ttk.Entry(main_frame)
        self.fecha_salida_entry.grid(row=row_offset+2, column=1, sticky='ew', padx=5, pady=5)
        self.fecha_salida_entry.bind('<FocusOut>', self._validar_fecha_salida)

        # Estado
        ttk.Label(main_frame, text="Estado:").grid(row=row_offset+3, column=0, sticky='e', padx=5, pady=5)
        self.estado_combo = ttk.Combobox(main_frame, 
                                      values=['pendiente', 'en_proceso', 'completada'],
                                      state='readonly')
        self.estado_combo.grid(row=row_offset+3, column=1, sticky='ew', padx=5, pady=5)
        self.estado_combo.set('pendiente')
        
        # Sección para agregar piezas
        ttk.Label(main_frame, text="Piezas asignadas:").grid(row=row_offset+4, column=0, sticky='ne', padx=5, pady=5)
        
        self.piezas_frame = ttk.Frame(main_frame)
        self.piezas_frame.grid(row=row_offset+4, column=1, sticky='nsew', padx=5, pady=5)
        
        self.piezas_listbox = tk.Listbox(self.piezas_frame)
        self.piezas_listbox.pack(fill='both', expand=True, side='left')
        
        scrollbar = ttk.Scrollbar(self.piezas_frame, orient='vertical', command=self.piezas_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.piezas_listbox.config(yscrollcommand=scrollbar.set)
        
        # Frame para controles de piezas
        piezas_controls_frame = ttk.Frame(main_frame)
        piezas_controls_frame.grid(row=row_offset+5, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Button(
            piezas_controls_frame,
            text="Agregar Pieza",
            command=self._agregar_pieza
        ).pack(side='left', padx=5)
        
        ttk.Button(
            piezas_controls_frame,
            text="Quitar Pieza",
            command=self._quitar_pieza
        ).pack(side='left', padx=5)
        
        # Barra de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row_offset+6, column=0, columnspan=2, sticky='e', padx=5, pady=10)
        
        self.delete_btn = ttk.Button(
            button_frame, 
            text="Eliminar", 
            command=self._delete,
            style='Danger.TButton' if 'Danger.TButton' in self.style.map('TButton') else None
        )
        
        self.save_btn = ttk.Button(
            button_frame, 
            text="Guardar", 
            command=self._save,
            style='Accent.TButton'
        )
        self.save_btn.pack(side='left', padx=5)
        
        ttk.Button(
            button_frame, 
            text="Cancelar", 
            command=self.destroy
        ).pack(side='left', padx=5)
        
        # Solo mostrar botón eliminar si es admin
        if self.user.perfil == 'admin' and self.folio:
            self.delete_btn.pack(side='left', padx=5)
    
    def _get_piezas_disponibles(self):
        """Obtiene las piezas con existencias mayores a 0"""
        piezas = self.pieza_dao.get_all()
        return [p for p in piezas if p.existencias > 0]
    
    def _agregar_pieza(self):
        """Muestra un diálogo para agregar una pieza a la reparación directamente en el inventario."""
        if not self.folio:
            messagebox.showwarning("Advertencia", "Primero debe guardar la reparación antes de agregar piezas")
            return

        # Crear ventana de selección de piezas
        pieza_dialog = tk.Toplevel(self)
        pieza_dialog.title("Agregar Pieza")
        pieza_dialog.transient(self)
        pieza_dialog.grab_set()

        main_frame = ttk.Frame(pieza_dialog, padding=10)
        main_frame.pack(fill='both', expand=True)

        piezas = self._get_piezas_disponibles()
        if not piezas:
            messagebox.showwarning("Advertencia", "No hay piezas disponibles en inventario")
            pieza_dialog.destroy()
            return

        ttk.Label(main_frame, text="Seleccione pieza:").pack(pady=5)
        pieza_combo = ttk.Combobox(main_frame, state='readonly')
        pieza_combo['values'] = [f"{p.pieza_id} - {p.descripcion} (${p.precio}) - Stock: {p.existencias}" for p in piezas]
        pieza_combo.pack(pady=5)

        ttk.Label(main_frame, text="Cantidad:").pack(pady=5)
        cantidad_entry = ttk.Entry(main_frame)
        cantidad_entry.pack(pady=5)
        cantidad_entry.insert(0, "1")

        def agregar():
            seleccion = pieza_combo.get()
            cantidad_str = cantidad_entry.get()

            if not seleccion or not cantidad_str.isdigit():
                messagebox.showerror("Error", "Seleccione una pieza y especifique una cantidad válida")
                return

            pieza_id = int(seleccion.split(' - ')[0])
            cantidad_nueva = int(cantidad_str)

            pieza = next((p for p in piezas if p.pieza_id == pieza_id), None)
            if not pieza:
                messagebox.showerror("Error", "Pieza no encontrada")
                return

            if cantidad_nueva > pieza.existencias:
                messagebox.showerror("Error", f"No hay suficiente stock. Disponible: {pieza.existencias}")
                return

            # Verificar si ya existe en la lista, y sumar la cantidad si corresponde
            detalle_existente = next((p for p in self.piezas_asignadas if p['pieza_id'] == pieza_id), None)
            if detalle_existente:
                detalle_existente['cantidad'] += cantidad_nueva
                # Actualizar el detalle en la base de datos (sumar cantidad)
                nueva_cantidad = detalle_existente['cantidad']
                self.detalle_dao.delete_by_folio(self.folio)
                for p_asignada in self.piezas_asignadas:
                    self.detalle_dao.save(
                        folio=self.folio,
                        pieza_id=p_asignada['pieza_id'],
                        cantidad=p_asignada['cantidad'],
                        precio_unitario=p_asignada['precio_unitario']
                    )
            else:
                # Agregar la nueva pieza a la lista
                self.piezas_asignadas.append({
                    'pieza_id': pieza_id,
                    'descripcion': pieza.descripcion,
                    'cantidad': cantidad_nueva,
                    'precio_unitario': pieza.precio
                })
                # Guardar en la base de datos
                self.detalle_dao.save(
                    folio=self.folio,
                    pieza_id=pieza_id,
                    cantidad=cantidad_nueva,
                    precio_unitario=pieza.precio
                )

            # Actualizar stock de la pieza en la base de datos
            self.pieza_dao.update_stock(pieza_id, -cantidad_nueva)

            # Actualizar la lista visible
            self._actualizar_lista_piezas()
            pieza_dialog.destroy()

        ttk.Button(main_frame, text="Agregar", command=agregar).pack(pady=10)
    
    def _quitar_pieza(self):
        """Quita la pieza seleccionada de la lista"""
        if not self.piezas_asignadas:
            return
            
        seleccion = self.piezas_listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una pieza para quitar")
            return
            
        if messagebox.askyesno("Confirmar", "¿Está seguro de quitar esta pieza de la reparación?"):
            index = seleccion[0]
            pieza_removida = self.piezas_asignadas.pop(index)
            
            # Devolver stock de la pieza removida
            self.pieza_dao.update_stock(pieza_removida['pieza_id'], pieza_removida['cantidad'])

            # Borrar detalles existentes y reinsertar los que permanecen
            self.detalle_dao.delete_by_folio(self.folio)
            for p_asignada in self.piezas_asignadas:
                self.detalle_dao.save(
                    folio=self.folio,
                    pieza_id=p_asignada['pieza_id'],
                    cantidad=p_asignada['cantidad'],
                    precio_unitario=p_asignada['precio_unitario']
                )
            
            self._actualizar_lista_piezas()
    
    def _actualizar_lista_piezas(self):
        """Actualiza el listbox con las piezas asignadas"""
        self.piezas_listbox.delete(0, tk.END)
        
        for pieza in self.piezas_asignadas:
            texto = f"{pieza['pieza_id']} - {pieza['descripcion']} x{pieza['cantidad']} (${pieza['precio_unitario']} c/u)"
            self.piezas_listbox.insert(tk.END, texto)
    
    def _validar_fecha_entrada(self, event=None):
        """Valida la fecha de entrada cuando pierde el foco"""
        fecha_str = self.fecha_entrada_entry.get()
        if not fecha_str:
            return False
            
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return True
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            self.fecha_entrada_entry.focus_set()
            return False

    def _validar_fecha_salida(self, event=None):
        """Valida la fecha de salida cuando pierde el foco"""
        fecha_str = self.fecha_salida_entry.get()
        if not fecha_str:  # Campo vacío es válido
            return True
            
        # Primero validar formato
        try:
            fecha_salida = datetime.strptime(fecha_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            self.fecha_salida_entry.focus_set()
            return False
            
        # Luego validar que sea mayor que fecha entrada
        try:
            fecha_entrada_str = self.fecha_entrada_entry.get()
            if not fecha_entrada_str:
                return True
                
            fecha_entrada = datetime.strptime(fecha_entrada_str, '%Y-%m-%d')
            if fecha_salida < fecha_entrada:
                messagebox.showerror("Error", "La fecha de salida no puede ser anterior a la de entrada")
                self.fecha_salida_entry.focus_set()
                return False
        except ValueError:
            return True
            
        return True
    
    def _load_vehiculos(self):
        vehiculos = self.vehiculo_dao.get_all()
        self.vehiculos = {f"{v.matricula} - {v.marca} {v.modelo}": v.matricula for v in vehiculos}
        self.vehiculo_combo['values'] = list(self.vehiculos.keys())
    
    def _search_reparacion(self):
        folio = self.search_entry.get().strip()
        if not folio.isdigit():
            messagebox.showerror("Error", "Folio debe ser un número válido")
            return
        
        folio = int(folio)
        reparacion = self.reparacion_dao.get(folio)
        if not reparacion:
            messagebox.showerror("Error", f"No se encontró reparación con folio {folio}")
            return
        
        self.folio = folio
        self.reparacion = reparacion
        vehiculo_str = f"{reparacion.matricula} - {reparacion.info_vehiculo}"
        self.vehiculo_combo.set(vehiculo_str)
        self.fecha_entrada_entry.config(state='normal')
        self.fecha_entrada_entry.delete(0, tk.END)
        self.fecha_entrada_entry.insert(0, reparacion.fecha_entrada.strftime('%Y-%m-%d'))
        self.fecha_entrada_entry.config(state='readonly')
        
        self.fecha_salida_entry.config(state='normal')
        self.fecha_salida_entry.delete(0, tk.END)
        if reparacion.fecha_salida:
            self.fecha_salida_entry.insert(0, reparacion.fecha_salida.strftime('%Y-%m-%d'))
        
        self.estado_combo.set(reparacion.estado)
        
        # Solo admin puede eliminar reparaciones
        if self.user.perfil == 'admin':
            self.delete_btn.pack(side='left', padx=5)
        
        # Cargar piezas asignadas
        self._cargar_piezas_asignadas()
        
        messagebox.showinfo("Éxito", f"Reparación {folio} cargada correctamente")
    
    def _cargar_piezas_asignadas(self):
        """Carga las piezas asignadas a la reparación actual"""
        if not self.folio:
            return
            
        detalles = self.detalle_dao.get_by_folio(self.folio)
        self.piezas_asignadas = []
        
        for detalle in detalles:
            pieza = self.pieza_dao.get(detalle['pieza_id'])
            if pieza:
                self.piezas_asignadas.append({
                    'pieza_id': pieza.pieza_id,
                    'descripcion': pieza.descripcion,
                    'cantidad': detalle['cantidad'],
                    'precio_unitario': detalle['precio_unitario']
                })
        
        self._actualizar_lista_piezas()
    
    def _load_data(self):
        if self.folio:
            self.reparacion = self.reparacion_dao.get(self.folio)
            if self.reparacion:
                vehiculo_str = f"{self.reparacion.matricula} - {self.reparacion.info_vehiculo}"
                self.vehiculo_combo.set(vehiculo_str)
                self.fecha_entrada_entry.delete(0, tk.END)
                self.fecha_entrada_entry.insert(0, self.reparacion.fecha_entrada.strftime('%Y-%m-%d'))
                
                if self.reparacion.fecha_salida:
                    self.fecha_salida_entry.delete(0, tk.END)
                    self.fecha_salida_entry.insert(0, self.reparacion.fecha_salida.strftime('%Y-%m-%d'))
                
                self.estado_combo.set(self.reparacion.estado)
                
                # Cargar piezas asignadas
                self._cargar_piezas_asignadas()
    
    def _validate_dates(self, fecha_entrada_str: str, fecha_salida_str: str) -> bool:
        """Valida la lógica de las fechas"""
        try:
            fecha_entrada = datetime.strptime(fecha_entrada_str, '%Y-%m-%d').date()
            
            if fecha_salida_str:
                fecha_salida = datetime.strptime(fecha_salida_str, '%Y-%m-%d').date()
                if fecha_salida < fecha_entrada:
                    self.show_error("La fecha de salida no puede ser anterior a la de entrada")
                    return False
                    
            return True
        except ValueError:
            self.show_error("Formato de fecha inválido (use YYYY-MM-DD)")
            return False
    
    def _get_form_data(self) -> Optional[Reparacion]:
        vehiculo_str = self.vehiculo_combo.get()
        fecha_entrada_str = self.fecha_entrada_entry.get().strip()
        fecha_salida_str = self.fecha_salida_entry.get().strip()
        estado = self.estado_combo.get()
        
        if not all([vehiculo_str, fecha_entrada_str, estado]):
            self.show_error("Vehículo, fecha entrada y estado son obligatorios")
            return None
        
        if not self._validar_fecha_entrada():
            return None
            
        if not self._validar_fecha_salida():
            return None
            
        if not self._validate_dates(fecha_entrada_str, fecha_salida_str):
            return None
            
        try:
            matricula = self.vehiculos[vehiculo_str]
            fecha_entrada = date.fromisoformat(fecha_entrada_str)
            fecha_salida = date.fromisoformat(fecha_salida_str) if fecha_salida_str else None
            
            reparacion = Reparacion(
                folio=self.folio,
                matricula=matricula,
                fecha_entrada=fecha_entrada,
                fecha_salida=fecha_salida,
                estado=estado
            )
            
            reparacion.validate() # Esto puede lanzar ValueError
                
            return reparacion
        except ValueError as e:
            self.show_error(str(e))
            return None
        except KeyError:
            self.show_error("Seleccione un vehículo válido")
            return None
    
    def _save(self):
        reparacion = self._get_form_data()
        if not reparacion:
            return
            
        if self.folio:
            if self.user.perfil != 'admin':
                self.show_error("No tiene permisos para editar reparaciones")
                return
                
            success = self.reparacion_dao.update(reparacion)
            msg = "actualizada"
        else:
            success = self.reparacion_dao.save(reparacion)
            if success:
                self.folio = success  # Obtenemos el folio de la nueva reparación
            msg = "registrada"
            
        if success:
            # Guardar las piezas asignadas
            if self.folio and self.piezas_asignadas:
                # Primero eliminamos los detalles existentes
                self.detalle_dao.delete_by_folio(self.folio)
                
                # Luego agregamos los nuevos y actualizamos el stock
                for pieza in self.piezas_asignadas:
                    # Guardar el detalle
                    self.detalle_dao.save(
                        folio=self.folio,
                        pieza_id=pieza['pieza_id'],
                        cantidad=pieza['cantidad'],
                        precio_unitario=pieza['precio_unitario']
                    )
                    
                    # Actualizar el stock de la pieza
                    #self.pieza_dao.update_stock(pieza['pieza_id'], -pieza['cantidad'])
            
            self.show_success(f"Reparación {msg} correctamente")
            if self.user.perfil == 'admin':
                self._clear_form()
            else:
                self.destroy()
        else:
            self.show_error(f"No se pudo {msg} la reparación")
    
    def _delete(self):
        if not self.folio or self.user.perfil != 'admin':
            return
            
        if self.ask_confirmation("¿Está seguro de eliminar esta reparación?"):
            # Primero devolvemos las piezas al inventario
            detalles = self.detalle_dao.get_by_folio(self.folio)
            for detalle in detalles:
                self.pieza_dao.update_stock(detalle['pieza_id'], detalle['cantidad'])
            
            # Luego eliminamos los detalles asociados
            self.detalle_dao.delete_by_folio(self.folio)
            
            # Finalmente eliminamos la reparación
            if self.reparacion_dao.delete(self.folio):
                self.show_success("Reparación eliminada correctamente")
                self._clear_form()
            else:
                self.show_error("No se pudo eliminar la reparación")
    
    def _clear_form(self):
        """Limpia el formulario (solo para admin)"""
        if self.user.perfil != 'admin':
            return
            
        self.folio = None
        self.reparacion = None
        self.vehiculo_combo.set('')
        self.fecha_entrada_entry.config(state='normal')
        self.fecha_entrada_entry.delete(0, tk.END)
        self.fecha_entrada_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        self.fecha_salida_entry.config(state='normal')
        self.fecha_salida_entry.delete(0, tk.END)
        self.estado_combo.set('pendiente')
        self.piezas_asignadas = []
        self._actualizar_lista_piezas()
        
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, tk.END)
        
        self.delete_btn.pack_forget()