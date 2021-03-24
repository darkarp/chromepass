import ctypes
import subprocess
import logging
import os
import sys

logging.basicConfig(filename=f'logs.log',
                    encoding='ISO-8859-1', level=logging.DEBUG)
refresh_env = "Set-ExecutionPolicy Bypass -Scope Process -Force;Import-Module \"$env:ProgramData\chocolatey\helpers\chocolateyInstaller.psm1\"; Update-SessionEnvironment;"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_command(command):
    process = subprocess.Popen(
        ["powershell.exe", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, b''):
        line = line.decode(encoding="ISO-8859-1")
        print(line)
        logging.debug(line)


def dependencies_missing():
    print("[i] Checking dependencies...")
    missing_refresh = subprocess.run(
        ["powershell.exe", f"cargo --version;"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr
    if missing_refresh:
        missing = subprocess.run(
            ["powershell.exe", f"{refresh_env}cargo --version;"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr
        if not missing:
            print("[i] Dependencies exist but aren't loaded.")
            print("[-] Please close and reopen the powershell window.")
            sys.exit(0)
        return True
    return False


def install_dependencies():
    install_requirements = "pip install -r requirements.txt"
    install_choco = "Set-ExecutionPolicy Bypass -Scope Process -Force;[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'));"
    install_vcbuild = "choco install --verbose -y vcbuildtools --force"
    install_rust = """$exePath = "$env:TEMP\\rustup-init.exe";(New-Object Net.WebClient).DownloadFile('https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe', $exePath);cmd /c start /wait $exePath -y;Remove-Item $exePath;"""
    update_cargo = "cd templates\\chromepass-build; cargo update;"
    run_command(install_requirements)
    run_command(install_choco)
    run_command(refresh_env + install_vcbuild)
    run_command(refresh_env + install_rust)
    run_command(refresh_env + update_cargo)
    if dependencies_missing():
        print("There was an error in the installation. Please")
        return False
    print("Setup was successful")
    return True


def setup():
    if is_admin():
        return install_dependencies()
    else:
        print("Please run this in an Admin powershell window")
    sys.exit()


def dependency_manager():
    install = input(
        "Dependencies missing, do you want to install them automaticaly? (y/n): ").lower()
    while install not in ["y", "n"]:
        install = input(
            "Dependencies missing, do you want to install them automaticaly? (y/n): ")
    if install == "y":
        print("[i] This will take a while... Go grab a coffee.")
        return setup()
    sys.exit(0)


if "--setup" in sys.argv:
    setup()
    dependency_manager()
try:
    if dependencies_missing():
        dependency_manager()
    import PyInstaller.__main__
except Exception as e:
    dependency_manager()

if __name__ == "__main__":
    if is_admin():
        print(os.getcwd())
        os.chdir("../")
        print(os.getcwd())
        # install_dependencies()
        # print("Setup Complete!")
    else:
        print(os.getcwd())
        os.chdir("../")
        print(os.getcwd())
        print("Please run this in an Admin powershell window")
