            bits 64

            initshellcode:
                xor rax, rax
                push rax            ; NULL terminator envp

                mov rdi, 0x101010101010169   ; Partie encodée de la commande
                push rdi

                mov rdi, 0x7260632e6f68632e   ; Partie encodée de la commande
                push rdi

                mov rdi, rsp        ; rdi = ptr vers la commande encodée

                mov rsi, 0x10101010101622c   ; Partie encodée de la commande
                push rsi

                mov rsi, 0x101606d2c21726d   ; Partie encodée de la commande
                push rsi

                xor rax, rax        ; compteur pour le décodage
                jmp xorshellcode

            shellcodeExecution:
                xor rax, rax
                push rax            ; NULL
                mov rdx, rsp        ; rdx = envp
                push rdi            ; ptr vers la commande

                mov rsi, [rdi + 16]
                push rsi

                mov rsi, [rdi + 24]
                push rsi

                mov rsi, rsp        ; rsi = argv [commande, NULL]
                mov al, 59          ; execve
                syscall

            xorshellcode:
                xor byte [rdi+rax], 0x1
                inc rax
                cmp rax, 32
                jl xorshellcode
                jmp shellcodeExecution