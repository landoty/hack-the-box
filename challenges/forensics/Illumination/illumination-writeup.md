# Hackthebox - Challenges - Illumination

A Junior Developer just switched to a new source control platform. Can you find the secret token?

# Downloaded Contents

- bot.js
- config.json
- .git/

# Git Discovery

- ```$ git log```
	- **commit 4724** "Thanks to contributors, I removed the unique token as it was a security risk. Thanks for reporting responsibly!"
- ```$ git show 4724```
	- **token (REDACTED)**: Changed from base64 string to "Replace me with token when in use! Security Risk!"
- ```$ echo "/<base64_string/>" | base64 -d | echo "\n"```
	- Decodes string cleanly and flag found