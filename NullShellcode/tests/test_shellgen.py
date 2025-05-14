import pytest
from shellgen.generator import generate_shellcode
from shellgen.encoder import encode_shellcode, xor_encode
from shellgen.utils import has_null_bytes, find_null_byte_positions, sanitize_command

def test_shellcode_generation():
    """Test la génération basique de shellcode."""
    shellcode = generate_shellcode("/bin/ls")
    assert isinstance(shellcode, bytes)
    assert len(shellcode) > 0

def test_xor_encoding():
    """Test l'encodage XOR."""
    test_bytes = b"Hello, World!"
    key = 0x41
    encoded = xor_encode(test_bytes, key)
    decoded = xor_encode(encoded, key)
    assert decoded == test_bytes

def test_null_byte_detection():
    """Test la détection des null bytes."""
    assert has_null_bytes(b"Hello\x00World")
    assert not has_null_bytes(b"HelloWorld")

def test_command_sanitization():
    """Test le nettoyage des commandes."""
    assert sanitize_command("ls -la; rm -rf /") == "ls -la rm -rf /"
    assert sanitize_command("cat file | grep pattern") == "cat file  grep pattern" 