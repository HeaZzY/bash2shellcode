#  bash2shellcode

**bash2shellcode** is a Linux x86_64 shellcode generator that converts any bash command into shellcode (ASM or raw format), ready for use in exploits or payloads.



https://github.com/user-attachments/assets/48210537-d447-4d70-b500-9441262015b8


---

##  Features

- Converts any bash command to Linux x86_64 shellcode.
- Supported output formats:
  - c : C-style byte array (unsigned char shellcode[] = ...)
  - cfile : standalone .c file with main() to test the shellcode
  - asm : raw assembly code
  - raw : plain shellcode string (\x..)
- Supports forbidden bytes (e.g. \x00, \xff)

---

---

## Requirements

- nasm 
- ld 
- objdump

### Install required packages:
```bash
sudo apt install binutils nasm objdump
```

### Install python requirements:

```bash
pip install -r requirements.txt
```

---



##  Usage

python3 bash2shellcode.py [-h] [-o {c,cfile,asm,raw}] [-f FILE] [--nobytes NOBYTES] command

### Positional arguments

- command : the bash command to convert to shellcode

### Options

- -o, --output : output format (c, cfile, asm, raw) [default: c]
- -f, --file : output file name (if not specified, prints to stdout)
- --nobytes : forbidden bytes in hex (e.g. "\x00\xff")
- -h, --help : show help and exit

---

##  Example
```bash
python3 bash2shellcode.py "/bin/bash -c 'echo shellcodeTheWorld'" -o raw
```
**Output:**
```raw
\x48\x31\xc0\x50\xbf\x68\x00\x00\x00\x57\x48\xbf\x2f\x62\x69\x6e\x2f\x62\x61\x73\x57\xbe\x2d\x63\x00\x00\x56\x48\xbe\x65\x57\x6f\x72\x6c\x64\x00\x00\x56\x48\xbe\x6c\x6c\x63\x6f\x64\x65\x54\x68\x56\x48\xbe\x65\x63\x68\x6f\x20\x73\x68\x65\x56\x48\x89\xe7\xeb\x00\x48\x31\xc0\x50\x48\x89\xe2\x48\x83\xc7\x20\x48\x8d\x77\xe0\x56\x48\x8d\x77\xf8\x56\x57\x48\x89\xe6\xb0\x3b\x0f\x05
```
---

## ⚠ Limitations

- Only supports Linux x64 shellcode generation. (working on x86 architecture support)
- Shellcode is based on executing the command using /bin/bash -c 'yourcmdthere'.
- No support (yet) for other OS or architectures.
- May not work sometimes with forbidden bytes (working on it)

---

##  Output Format Examples

### Format c
unsigned char shellcode[] = "\x48\x31\xc0...";

### Format cfile
A complete .c file with a main() that runs the shellcode using a function pointer.

### Format asm
Intel syntax assembly code for manual inspection or use with an assembler.

### Format raw
Raw shellcode string with escaped hex bytes (\x...), ready to be used in exploits or injectors.

---

##  Author

- Heazzy (https://github.com/heazzy)

---

