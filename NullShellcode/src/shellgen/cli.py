import click
from .generator import generate_shellcode
from .encoder import encode_shellcode

@click.group()
def main():
    """Outil de génération de shellcode optimisé et obfusqué."""
    pass

@main.command()
@click.argument('command')
@click.option('--arch', default='x64', help='Architecture cible (x86, x64)')
def generate(command, arch):
    """Génère un shellcode à partir d'une commande."""
    try:
        shellcode = generate_shellcode(command, arch)
        click.echo(f"Shellcode généré : {shellcode.hex()}")
    except Exception as e:
        click.echo(f"Erreur : {str(e)}", err=True)

@main.command()
@click.argument('shellcode')
@click.option('--method', default='xor', help='Méthode d\'obfuscation (xor, ...)')
@click.option('--key', default='0x41', help='Clé d\'encodage')
def encode(shellcode, method, key):
    """Encode/obfusque un shellcode."""
    try:
        encoded = encode_shellcode(bytes.fromhex(shellcode), method, int(key, 16))
        click.echo(f"Shellcode encodé : {encoded.hex()}")
    except Exception as e:
        click.echo(f"Erreur : {str(e)}", err=True)

if __name__ == '__main__':
    main() 