from functools import wraps
from tkinter import messagebox
from models.user import User

def admin_required(func):
    """Decorador para verificar que el usuario sea administrador"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'current_user') or not isinstance(self.current_user, User):
            messagebox.showerror("Acceso denegado", "No se ha identificado al usuario")
            return
            
        if self.current_user.perfil != 'admin':
            messagebox.showerror("Acceso denegado", "Se requieren privilegios de administrador")
            return
            
        return func(self, *args, **kwargs)
    return wrapper