# mass-wake-on-lan
## Overview:
A python3 script that reads from a json file to send wake on lan calls using etherwake.
Default json file is macaddrs.json.

## Dependencies:
- `etherwake` 
    - Debian Based (Ubuntu, raspiOS, etc...):
        - `sudo apt install etherwake`
    - Arch Linux
        - `yay -S etherwake`
