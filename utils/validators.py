import re
from typing import Optional

def validate_rfc(rfc: str) -> bool:
    """Valida que el RFC tenga un formato válido"""
    pattern = r'^[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{2}[0-9A]$'
    return bool(re.fullmatch(pattern, rfc, re.IGNORECASE))

def validate_phone(phone: str) -> bool:
    """Valida que el teléfono tenga 10 dígitos"""
    return len(phone) == 10 and phone.isdigit()

def validate_password(password: str) -> Optional[str]:
    """Valida que la contraseña cumpla con los requisitos"""
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres"
    if not any(c.isupper() for c in password):
        return "La contraseña debe contener al menos una mayúscula"
    if not any(c.isdigit() for c in password):
        return "La contraseña debe contener al menos un número"
    return None