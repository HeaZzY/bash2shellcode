#!/usr/bin/env python3
import sys
import argparse
from asmCompiler import compile_asm_to_shellcode

def format_shellcode(shellcode, output_format):
    """Format the shellcode according to the requested format."""
    if output_format == 'c':
        return f"""// Shellcode in C format
unsigned char shellcode[] = {{{','.join(f"0x{b:02x}" for b in shellcode)}}};
// Size: {len(shellcode)} bytes"""
    
    elif output_format == 'asm':
        # Format as NASM assembly
        asm_code = "section .text\n"
        asm_code += "global _start\n"
        asm_code += "_start:\n"
        asm_code += "    ; Shellcode\n"
        for i in range(0, len(shellcode), 16):
            chunk = shellcode[i:i+16]
            hex_values = ' '.join(f'0x{b:02x}' for b in chunk)
            asm_code += f"    db {hex_values}\n"
        return asm_code
    
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
        choices=['c', 'asm', 'raw'],
        default='c',
        help='Output format (c, asm, raw) [default: c]'
    )
    
    parser.add_argument(
        '-k', '--key',
        type=lambda x: int(x, 0),  # Allows hex input (0x...)
        default=0x01,
        help='XOR key for encoding [default: 0x01]'
    )
    
    args = parser.parse_args()
    
    try:
        # Generate shellcode using the asm compiler
        shellcode = compile_asm_to_shellcode(args.command, xor_key=args.key)
        
        # Display the result
        print(format_shellcode(shellcode, args.output))
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 