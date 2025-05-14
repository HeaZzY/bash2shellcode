def xor_encode(shellcode: bytes, key: int) -> bytes:
    """
    Encode un shellcode en utilisant XOR.
    
    Args:
        shellcode: Le shellcode à encoder
        key: La clé XOR (un octet)
    
    Returns:
        bytes: Le shellcode encodé
    """
    return bytes(b ^ key for b in shellcode)

def encode_shellcode(shellcode: bytes, method: str = 'xor', key: int = 0x41) -> bytes:
    """
    Encode un shellcode selon la méthode spécifiée.
    
    Args:
        shellcode: Le shellcode à encoder
        method: Méthode d'encodage ('xor', etc.)
        key: Clé d'encodage
    
    Returns:
        bytes: Le shellcode encodé
    """
    if method == 'xor':
        return xor_encode(shellcode, key)
    else:
        raise ValueError(f"Méthode d'encodage '{method}' non supportée") 