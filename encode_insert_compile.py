#!/usr/bin/env python3
import os
import subprocess
import tempfile
import argparse

def insertIntoDecoder(shellcodeBytes):
    DECODER_TEMPLATE = f"""
    section .text
    _start:
        xor   rax, rax
        xor   rcx, rcx

        mov   dl, 0x45
        jmp   short call_decoder

    decoder:
        pop   rsi
        lea   rdi, [rsi]

    decode:
        add   rdi, rcx
        mov   bl, byte [rdi]
        sub   rdi, rcx
        mov   bh, bl

        mov   al, dl
        xor   al, bl
        jz    short shellcode

        add   rdi, rcx
        mov   ax, word [rdi + 1]
        sub   rdi, rcx
        xor   ax, bx

        mov   word [rdi], ax

        inc   rcx
        lea   rdi, [rdi + 2]
        jmp   short decode

    call_decoder:
        call  decoder
        {shellcodeBytes}
    """
    return DECODER_TEMPLATE


if __name__ == "__main__":
    main()