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


def check_config():
    config.read("config.ini")
    has_cargo = "true" == config["DEPENDENCIES"]["Cargo"]
    has_tools = "true" == config["DEPENDENCIES"]["BuildTools"]
    return has_cargo, has_tools


def check_tools():
    if "displayName" not in subprocess.run(
            ["powershell.exe", "./templates/resources/vswhere.exe -products Microsoft.VisualStudio.Product.BuildTools"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode():
        install_tools()
    else:
        config.set("DEPENDENCIES", "BuildTools", "true")


def check_cargo():
    if subprocess.run(
            ["powershell.exe", f"{refresh_env}cargo --version;"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stderr:
        install_cargo()
    else:
        config.set("DEPENDENCIES", "Cargo", "true")


def print_dependency_stage(has_cargo, has_tools, complete=False):
    if all((has_cargo, has_tools, complete)):
        print("[+] All dependencies installed successfully.")
        return True
    elif complete:
        print(
            f"[-] An error has occurred installing dependencies: Cargo -> {has_cargo} | Tools -> {has_tools}")
    else:
        print("[i] Checking dependencies...")
    return False


def dependencies_missing():
    has_cargo, has_tools = check_config()
    if print_dependency_stage(has_cargo, has_tools):
        return False
    check_tools()
    check_cargo()
    with open('config.ini', 'w') as f:
        config.write(f)
    has_cargo, has_tools = check_config()
    print_dependency_stage(has_cargo, has_tools, complete=True)


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
    musl_target = f"{refresh_env}rustup target add x86_64-unknown-linux-musl"
    run_command(command)
    config.set("DEPENDENCIES", "Cargo", "true")
    print("[+] Cargo installed successfully.")
    print("[i] Setting default nightly")
    run_command(nightly)
    run_command(musl_target)
    return True


if not all(check_config()):
    dependencies_missing()

if __name__ == "__main__":
    dependencies_missing()
