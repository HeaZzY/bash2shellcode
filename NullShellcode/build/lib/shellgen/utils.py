from typing import List
import re

def has_null_bytes(shellcode: bytes) -> bool:
    """
    Vérifie si un shellcode contient des null bytes.
    
    Args:
        shellcode: Le shellcode à vérifier
    
    Returns:
        bool: True si le shellcode contient des null bytes
    """
    return b'\x00' in shellcode

def find_null_byte_positions(shellcode: bytes) -> List[int]:
    """
    Trouve les positions des null bytes dans un shellcode.
    
    Args:
        shellcode: Le shellcode à analyser
    
    Returns:
        List[int]: Liste des positions des null bytes
    """
    return [i for i, byte in enumerate(shellcode) if byte == 0]

def sanitize_command(command: str) -> str:
    """
    Nettoie une commande shell pour éviter les injections.
    
    Args:
        command: La commande à nettoyer
    
    Returns:
        str: La commande nettoyée
    """
    # Supprime les caractères dangereux
    return re.sub(r'[;&|`]', '', command) 