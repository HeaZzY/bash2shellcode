#!/usr/bin/env python3
import os
import tempfile
import subprocess
from x64.generator import generate_shellcode
from x64.parseInput import makeArgumentsList

def extract_opcodes(obj_file):
    """Extract opcodes from object file using objdump, matching the shell command behavior."""
    try:
        # Run the equivalent of: objdump -d shellcode.o | grep "^ " | cut -f2
        objdump_cmd = ['objdump', '-d', obj_file]
        grep_cmd = ['grep', '^ ']
        cut_cmd = ['cut', '-f2']

        p1 = subprocess.Popen(objdump_cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(grep_cmd, stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(cut_cmd, stdin=p2.stdout, stdout=subprocess.PIPE)

        # Get the output
        output, _ = p3.communicate()
        output_str = output.decode('utf-8')

        # Process the output to get the opcodes
        opcodes = []
        for line in output_str.split('\n'):
            if line.strip():
                for byte_str in line.strip().split():
                    try:
                        opcodes.append(int(byte_str, 16))
                    except ValueError:
                        pass  # Skip if not a valid hex

        return bytearray(opcodes)

    except subprocess.CalledProcessError as e:
        raise Exception(f"Command pipeline failed: {str(e)}")
    except FileNotFoundError as e:
        raise Exception(f"Required tool not found: {str(e)}")

def bytearray_to_raw_shellcode(data):
    return ''.join(f'\\x{b:02x}' for b in data)

def assemblesasmscript(asm):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate assembly code using shellcode_generator
        asm_file = os.path.join(temp_dir, "shellcode.asm")
        with open(asm_file, 'w') as f:
            f.write(asm)

        obj_file = os.path.join(temp_dir, "shellcode.o")
        try:
            subprocess.run(['nasm', '-f', 'elf64', '-o', obj_file, asm_file], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"NASM compilation failed: {str(e)}")
        except FileNotFoundError:
            raise Exception("NASM is not installed. Please install NASM to use this tool.")

        # Extract opcodes using objdump
        shellcode = extract_opcodes(obj_file)

        return bytearray_to_raw_shellcode(shellcode)



def compile_asm_to_shellcode(command):
    """Compile NASM assembly to shellcode and apply XOR encoding."""
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate assembly code using shellcode_generator
        arguments = makeArgumentsList(command)
        asm_code = generate_shellcode(arguments)
        asm_file = os.path.join(temp_dir, "shellcode.asm")
        with open(asm_file, 'w') as f:
            f.write(asm_code)

        # Compile with NASM
        obj_file = os.path.join(temp_dir, "shellcode.o")
        try:
            subprocess.run(['nasm', '-f', 'elf64', '-o', obj_file, asm_file], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"NASM compilation failed: {str(e)}")
        except FileNotFoundError:
            raise Exception("NASM is not installed. Please install NASM to use this tool.")

        # Extract opcodes using objdump
        shellcode = extract_opcodes(obj_file)

        return shellcode

