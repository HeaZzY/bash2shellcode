import sys
from src.shellgen.generator import generate_shellcode
from src.shellgen.parseUserInput import makeArgumentsList
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test_shellcode.py <command>")
        sys.exit(1)

    # Générer le shellcode avec la commande fournie
    command = sys.argv[1]
    print(command)
    arguments = makeArgumentsList(command)
    print(arguments)
    shellcode = generate_shellcode(arguments, xor_key=0x01)
    
'''    # Afficher en format C
    print("// Shellcode en format C")
    print("unsigned char shellcode[] = {", end="")
    print(",".join(f"0x{b:02x}" for b in shellcode), end="")
    print("};")
    print(f"// Taille: {len(shellcode)} bytes\n")
    
    # Afficher en format Python
    print("# Shellcode en format Python")
    print(f"shellcode = b'{''.join(f'\\x{b:02x}' for b in shellcode)}'")'''

if __name__ == "__main__":
    main()