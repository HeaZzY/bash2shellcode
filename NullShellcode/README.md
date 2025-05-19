# NullShellcode Generator

Ce projet permet de générer du shellcode à partir de commandes shell pour Windows 64-bit.

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python shellcode_generator.py "votre commande ici"
```

### Options

- `-o, --output`: Format de sortie (c, python, raw) [défaut: c]
- `-k, --key`: Clé XOR pour l'encodage [défaut: 0x01]
- `-h, --help`: Affiche l'aide

### Exemples

```bash
# Générer du shellcode pour la commande "whoami"
python shellcode_generator.py "whoami"

# Générer du shellcode en format Python
python shellcode_generator.py "whoami" -o python

# Générer du shellcode avec une clé XOR personnalisée
python shellcode_generator.py "whoami" -k 0x42
```

## Limitations

- Supporte uniquement Windows 64-bit pour le moment
- Les commandes complexes peuvent nécessiter des ajustements

## Avertissement

Ce projet est fourni à des fins éducatives uniquement. L'utilisation de ce code pour des activités malveillantes est strictement interdite.
