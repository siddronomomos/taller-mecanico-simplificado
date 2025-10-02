from __future__ import annotations

import argparse
from getpass import getpass

from db.user_dao import UserDAO
from models.user import User


def create_admin_user(username: str, password: str, nombre: str) -> bool:
    dao = UserDAO()

    existing = dao.get_by_username(username)
    if existing:
        print(f"El usuario '{username}' ya existe (ID {existing.usuario_id}).")
        return False

    user = User(nombre=nombre, user_name=username, password=password, perfil='admin')
    if not user.validate():
        print("Los datos del usuario no son válidos (mínimo 6 caracteres de contraseña, username >= 4).")
        return False

    if dao.save(user):
        print(f"Usuario admin creado correctamente: {username}")
        return True

    print("No se pudo crear el usuario admin. Revise los registros de la API.")
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Crear un usuario administrador usando la API REST")
    parser.add_argument("--username", default="admin", help="Nombre de usuario para el administrador (por defecto: admin)")
    parser.add_argument("--nombre", default="Administrador", help="Nombre completo del administrador")
    parser.add_argument("--password", help="Contraseña del administrador. Si se omite, se solicitará de forma interactiva")
    args = parser.parse_args()

    password = args.password or getpass("Contraseña del administrador: ")
    if not password:
        print("Debe proporcionar una contraseña válida.")
        return

    create_admin_user(args.username, password, args.nombre)


if __name__ == "__main__":
    main()