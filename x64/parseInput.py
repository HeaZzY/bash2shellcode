from .encoder import encode_string


def toLittleIndian(chaine: str):
    return chaine.encode().decode('utf-8')


def makeArgumentsList(userInput: str) -> list[str]:
    """
    Convertit une chaîne d'entrée utilisateur en liste d'arguments.
    Gère correctement les arguments entre guillemets simples.

    Args:
        userInput: Chaîne contenant les arguments

    Returns:
        Une liste d'arguments extraits

    Example:
        - python app.py /bin/sh -c 'ls -la' -> ['/bin/sh','-c' , 'ls -la']
        - python app.py /bin/bash -p -> ['/bin/bash','-p']
    """
    result = []
    current_arg = ""
    in_quotes = False
    quote_char = None

    for char in userInput:
        if char in ['"', "'"]:
            if not in_quotes:
                # Début d'une section entre guillemets
                in_quotes = True
                quote_char = char
            elif char == quote_char:
                # Fin d'une section entre guillemets
                in_quotes = False
                quote_char = None
            else:
                # Un autre type de guillemet à l'intérieur d'une section déjà entre guillemets
                current_arg += char
        elif char.isspace() and not in_quotes:
            # Espace en dehors des guillemets = séparateur d'arguments
            if current_arg:
                result.append(current_arg)
                current_arg = ""
        else:
            # Ajouter le caractère à l'argument courant
            current_arg += char

    # Ajouter le dernier argument s'il existe
    if current_arg:
        result.append(current_arg)

    # Supprimer "python app.py" au début si présent
    if len(result) >= 2 and result[0] == "python" and "app.py" in result[1]:
        result = result[2:]

    return result


# def generate_shellcode(parsedCommandList: list[str], arch: str = 'x64', xor_key: int = 0x00) -> bytes:


def setupToShellcode(parsedCommandList: list[str]) -> list:
    list2return = []
    for command in parsedCommandList:
        encoded_values, length = encode_string(command)
        # Calculer la taille totale en octets (arrondie à 8 bytes)
        coef = length // 8
        reste = length % 8
        if reste != 0:
            coef += 1
        list2return.append((coef,encoded_values))
    return list2return