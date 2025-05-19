#!/usr/bin/env python3
import sys
import argparse
from src.shellgen.generator import generate_shellcode
from src.shellgen.parseUserInput import makeArgumentsList

def format_shellcode(shellcode, output_format):
    """Formate le shellcode selon le format demandé."""
    if output_format == 'c':
        return f"""// Shellcode en format C
unsigned char shellcode[] = {{{','.join(f"0x{b:02x}" for b in shellcode)}}};
// Taille: {len(shellcode)} bytes"""
    
    elif output_format == 'python':
        return f"""# Shellcode en format Python
shellcode = b'{''.join(f'\\x{b:02x}' for b in shellcode)}'
# Taille: {len(shellcode)} bytes"""
    
    elif output_format == 'raw':
        return ''.join(f'\\x{b:02x}' for b in shellcode)
    
    else:
        raise ValueError(f"Format de sortie non supporté: {output_format}")

def main():
    parser = argparse.ArgumentParser(
        description='Générateur de shellcode pour Windows 64-bit',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'command',
        help='La commande à convertir en shellcode'
    )
    
    parser.add_argument(
        '-o', '--output',
        choices=['c', 'python', 'raw'],
        default='c',
        help='Format de sortie (c, python, raw) [défaut: c]'
    )
    
    parser.add_argument(
        '-k', '--key',
        type=lambda x: int(x, 0),  # Permet les entrées en hex (0x...)
        default=0x01,
        help='Clé XOR pour l\'encodage [défaut: 0x01]'
    )
    
    args = parser.parse_args()
    
    try:
        # Générer le shellcode
        arguments = makeArgumentsList(args.command)
        shellcode = generate_shellcode(arguments, xor_key=args.key)
        
        # Afficher le résultat
        print(format_shellcode(shellcode, args.output))
        
    except Exception as e:
        print(f"Erreur: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 