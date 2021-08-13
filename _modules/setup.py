import subprocess
import logging
import configparser

try:
    logging.basicConfig(filename=f'logs.log',
                        encoding='ISO-8859-1', level=logging.DEBUG)
except:
    logging.basicConfig(filename=f'logs.log', level=logging.DEBUG)
config = configparser.ConfigParser()
config.read("config.ini")
refresh_env = '$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User");'


def run_command(command):
    process = subprocess.Popen(
        ["powershell.exe", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, b''):
        line = line.decode(encoding="ISO-8859-1").strip()
        print(line)
        logging.debug(line)


def dependencies_missing():
    config.read("config.ini")
    has_cargo = config["DEPENDENCIES"]["Cargo"]
    has_tools = config["DEPENDENCIES"]["BuildTools"]

    if "false" in [has_cargo, has_tools]:
        print("[i] Checking dependencies...")
        if "displayName" not in subprocess.run(
                ["powershell.exe", "./templates/resources/vswhere.exe -products Microsoft.VisualStudio.Product.BuildTools"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode():
            install_tools()
        else:
            config.set("DEPENDENCIES", "BuildTools", "true")
        if subprocess.run(
                ["powershell.exe", f"{refresh_env}cargo --version;"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr:
            install_cargo()
        else:
            config.set("DEPENDENCIES", "Cargo", "true")
        with open('config.ini', 'w') as f:
            config.write(f)
        config.read("config.ini")
        has_cargo = config["DEPENDENCIES"]["Cargo"]
        has_tools = config["DEPENDENCIES"]["BuildTools"]
        if not ("false" in [has_cargo, has_tools]):
            print("[+] All dependencies installed successfully.")
    else:
        return False


def install_tools():
    print("[i] Installing build tools...")
    command = "cd templates/resources;$p = Start-Process -Wait -PassThru -FilePath buildtools.exe -ArgumentList '--add Microsoft.VisualStudio.Workload.VCTools --passive --nocache --includeRecommended --norestart --wait';"
    run_command(command)
    config.set("DEPENDENCIES", "BuildTools", "true")
    print("[+] Build tools installed successfully.")
    return True


def install_cargo():
    print("[i] Installing cargo...")
    command = f"{refresh_env}cd templates/resources;./rustup-init.exe -y;"
    nightly = f"{refresh_env}rustup default nightly"
    run_command(command)
    config.set("DEPENDENCIES", "Cargo", "true")
    print("[+] Cargo installed successfully.")
    print("[i] Setting default nightly")
    run_command(nightly)
    return True


dependencies_missing()
if dependencies_missing():
    print("There was an error in the installation. Please report this bug.")

if __name__ == "__main__":
    dependencies_missing()
# Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force -Scope CurrentUser;
# Install-Module VSSetup -Scope CurrentUser -Force;
# Get-VSSetupInstance | Select-VSSetupInstance -Latest -Require Microsoft.VisualStudio.Component.VC.Tools.x86.x64;
