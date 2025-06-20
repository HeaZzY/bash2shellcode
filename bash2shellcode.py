#!/usr/bin/env python3
import sys
import argparse
from asmCompiler import *
from x64.reaper import *
from encode_insert_compile import insertIntoDecoder
def formatAsShellcode(shellcode):
    return ''.join(f'\\x{b:02x}' for b in shellcode)

def formatAsNasm(shellcode):
        # Format as NASM assembly
        asm_code = ""
        hex_values = ', '.join(f'0x{b:02x}' for b in shellcode)
        asm_code += f"shellcode: db {hex_values}"
        return asm_code


def format_shellcode(shellcode, output_format):
    """Format the shellcode according to the requested format."""
    if output_format == 'c':
        return f"""// Shellcode in C format
unsigned char shellcode[] = {{{','.join(f"0x{b:02x}" for b in shellcode)}}};
// Size: {len(shellcode)} bytes"""

    elif output_format == 'cfile':
        return f"""#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

// Ton shellcode
unsigned char shellcode[] =
{''.join(f'"\\x{b:02x}"' for b in shellcode)};

int main() {{
    size_t size = sizeof(shellcode);

    // Alloue une mémoire exécutable
    void *exec = mmap(NULL, size, PROT_READ | PROT_WRITE | PROT_EXEC,
                      MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);

    if (exec == MAP_FAILED) {{
        perror("mmap");
        return 1;
    }}

    // Copie le shellcode dedans
    memcpy(exec, shellcode, size);

    // Appelle le shellcode
    ((void(*)())exec)();

    return 0;
}}
"""

    elif output_format == 'asm':
        asm_code = "section .text\n"
        asm_code += "global _start\n"
        asm_code += "_start:\n"
        asm_code += "    ; Shellcode\n"

        return asm_code + formatAsNasm(shellcode)

    elif output_format == 'raw':
        return ''.join(f'\\x{b:02x}' for b in shellcode)

    else:
        raise ValueError(f"Unsupported output format: {output_format}")

def main():
    parser = argparse.ArgumentParser(
        description='Linux Shellcode Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'command',
        help='Command to convert to shellcode'
    )

    parser.add_argument(
        '-o', '--output',
        choices=['c', 'cfile', 'asm', 'raw'],
        default='c',
        help='Output format (c, cfile, asm, raw) [default: c]'
    )

    parser.add_argument(
        '-f', '--file',
        help='Output file name (if not specified, prints to stdout)'
    )

    #'''    parser.add_argument(
    #    '-e', '--encode',
    #    choices=['\xHEXKEY'],
    #    help='Xor encoding method juste add the key'
    #)'''

    parser.add_argument(
        '--nobytes',
        help='Forbidden bytes in hex format, e.g. "\\x00\\xff"'
    )

    args = parser.parse_args()

    try:
        bad_chars = []
        if args.nobytes:
            bad_chars = [int(b, 16) for b in args.nobytes.split('\\x') if b]
            # Generate shellcode using the asm compiler
            shellcode = encodeShellcode(compile_asm_to_shellcode(args.command),bad_chars=bad_chars)
            shellcode = formatAsNasm(bytes(int(b, 16) for b in shellcode.split('\\x') if b))
            asmtemplate = insertIntoDecoder(shellcode)
            shellcode = assemblesasmscript(asmtemplate)        
            # Convert encoded_shellcode (\x format string) back to bytes
            shellcode_bytes = bytes(int(b, 16) for b in shellcode.split('\\x') if b)

            formatted_output = format_shellcode(shellcode_bytes, args.output)
        else:
            shellcode = compile_asm_to_shellcode(args.command)       
            # Convert encoded_shellcode (\x format string) back to bytes

            formatted_output = format_shellcode(shellcode, args.output)


        if args.file:
            with open(args.file, 'w') as f:
                f.write(formatted_output + '\n')
        else:
            print(formatted_output)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
if __name__ == "__main__":
    main()