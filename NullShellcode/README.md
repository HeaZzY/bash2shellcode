# Shellcode Generator

Un outil en ligne de commande pour générer des shellcodes optimisés et obfusqués.

## Fonctionnalités

- Génération de shellcode à partir de commandes Linux
- Optimisation pour éliminer les null bytes
- Techniques d'obfuscation (XOR, etc.)
- Support de différentes architectures

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python -m shellgen generate "/bin/cat /etc/passwd"
python -m shellgen encode --method xor --key 0x41 <shellcode>
```

## Développement

Pour installer l'environnement de développement :

```bash
pip install -r requirements.txt
pytest  # Pour lancer les tests
```
