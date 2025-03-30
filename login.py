import tkinter as tk
from tkinter import messagebox
from menu import iniciar_menu
from dbUsers import dbUser
from user import User


def verificar_login(usuario, contrasena, ventana_login):
    if usuario == "" or contrasena == "":
        messagebox.showerror("Error", "Usuario y contraseña son requeridos")
        return
    db = dbUser()
    user = User()
    user.setUserName(usuario)
    user.setPassword(contrasena)
    user = db.login(user)
    if user == False:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        return
    ventana_login.destroy()
    if user.getPerfil() == "admin":
        iniciar_menu("admin")
    elif user.getPerfil() == "aux":
        iniciar_menu("aux")
    elif user.getPerfil() == "mecanico":
        iniciar_menu("mecanico")
    return True

def main():
    ventana_login = tk.Tk()
    ventana_login.title("Login - Taller Mecánico")
    ventana_login.geometry("300x200")
    ventana_login.configure(bg="#f0f0f0")

    tk.Label(ventana_login, text="Usuario:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    entry_usuario = tk.Entry(ventana_login, font=("Arial", 12))
    entry_usuario.pack(pady=5)

    tk.Label(ventana_login, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    entry_contrasena = tk.Entry(ventana_login, font=("Arial", 12), show="*")
    entry_contrasena.pack(pady=5)

    boton_login = tk.Button(
        ventana_login, text="Iniciar Sesión", font=("Arial", 12), bg="#4CAF50", fg="white",
        command=lambda: verificar_login(entry_usuario.get(), entry_contrasena.get(), ventana_login)
    )
    boton_login.pack(pady=20)

    ventana_login.mainloop()

if __name__ == "__main__":
    main()