from keystone import *
import struct
from .parseInput import *



def generate_shellcode(parsedCommandList: list[str], arch: str = 'x64') -> bytes:
    accumulatedSize = 0
    listArguments = setupToShellcode(parsedCommandList)
    totalSize = 0
    for i in listArguments:
        totalSize += i[0]
    if arch == 'x64':
        if 1 == 1:
            # Start of shellcode
            asm = """
            bits 64

            initshellcode:
                xor rax, rax
                push rax            ; NULL terminator envp
            """

            # Add encoded values
            for value in reversed(listArguments[0][1]):
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
                    asm += f"""
                mov rsi, {hex(value)}   ; Encoded argument part
                push rsi
                    """

            asm += """
                mov rdi, rsp
                """

            asm += f"""
                jmp shellcodeExecution

            shellcodeExecution:
                xor rax, rax
                push rax            ; NULL
                mov rdx, rsp        ; rdx = envp
                add rdi, {8*(totalSize - listArguments[0][0])}
                """

            for i in range(len(listArguments)-1, 0, -1):
                accumulatedSize += listArguments[i][0]
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
                syscall"""
            return asm

    elif arch == 'x86':
        raise NotImplementedError("x86 is not supported for the moment")

    return None