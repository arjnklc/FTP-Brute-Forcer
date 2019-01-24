# FTP-Brute-Forcer
Brute force script with python for ftp servers.

**Original author :** https://github.com/arjnklc/FTP-Brute-Forcer

### Changes made:
1. works with both python2 and python3
2. takes target hosts from file
3. checks if server is allowing connection on port 21 before attacking
4. write the output to a markdown friendly [file](/results/ftpBrute.md)
5. doesn't bruteforce hosts that has anonymous login enabled

```
>> python3 ftpBrute.py

Usage: ./ftpBrute.py [options]

Options: -t, --target    <hostname/ip>   |   Target
         -tfile, --targetfile <filename> |   target list
         -w, --wordlist  <filename>      |   Wordlist
         -h, --help      <help>          |   print help
Example: ./ftpBrute.py -t 192.168.1.1 -w wordlist.txt
```

#### screenshots:

[![screen1](https://raw.githubusercontent.com/bugbaba/FTP-Brute-Forcer/master/screen1.PNG)](https://raw.githubusercontent.com/bugbaba/FTP-Brute-Forcer/master/screen1.PNG)


[![screen2](https://raw.githubusercontent.com/bugbaba/FTP-Brute-Forcer/master/screen2.PNG)](https://raw.githubusercontent.com/bugbaba/FTP-Brute-Forcer/master/screen2.PNG)


---
For any queiries/feedback you can [contact me](https://bugbaba.blogspot.in/p/about-me.html)
