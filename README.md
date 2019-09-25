# Chromepass - Hacking Chrome Saved Passwords
<p align="center">
    <img src="https://img.shields.io/badge/Platform-Windows-green" />
	<a href="https://github.com/darkarp/chromepass/releases">
	<img src="https://img.shields.io/github/v/release/darkarp/chromepass" alt="Release" />
	</a>
		
  <a href="https://travis-ci.org/darkarp/chrome-password-hacking.svg?branch=master">
    <img src="https://travis-ci.org/darkarp/chrome-password-hacking.svg?branch=master" alt="Build Status on CircleCI" />
	</a>
    <img src="https://img.shields.io/maintenance/yes/2021" />
	</br>
<a href="https://github.com/darkarp/chromepass/releases">
	<img src="https://img.shields.io/github/downloads/darkarp/chromepass/total" />
	</a>
  
  <a href="https://github.com/darkarp/chromepass/commits/master">
    <img src="https://img.shields.io/github/last-commit/darkarp/chromepass" />
  </a>
<a href="https://github.com/darkarp/chromepass/blob/master/LICENSE">
    <img src="http://img.shields.io/github/license/darkarp/chromepass" />
  </a>
  </br>
  <a href="https://discord.gg/beczNYP">
    <img src="https://img.shields.io/badge/discord-join-7289DA.svg?logo=discord&longCache=true&style=flat" />
  </a>

Chromepass is a python-based console application that generates a windows executable with the following features:

  - Decrypt Chrome saved paswords
  - Send a file with the login/password combinations remotely (email or reverse-http)
  - Custom icon
  - Completely undetectable by AntiVirus Engines

# AV Detection!
Due to the way this has been coded, it is currently fully undetected. Here are some links to scans performed using a variety of websites
  - [VirusTotal Scan](https://www.virustotal.com/gui/file/9ca69d2c60f0db6c09e9959b6f9c8bfdf66ddbe2e28f9f7539fd2856b62315c0/detection) (0/68) 24-09-2019
  - [AntiScan](https://antiscan.me/scan/new/result?id=kmpsMNccfuRJ) (0/26) 24-09-2019
  - [Hibrid Analysis](https://www.hybrid-analysis.com/sample/9ca69d2c60f0db6c09e9959b6f9c8bfdf66ddbe2e28f9f7539fd2856b62315c0) All Clean (CrowdStrike Falcon, MetaDefender and Virustotal) 24-09-2019

### Dependencies and Requirements

This is a very simple application, which uses only:

* [Python] - Only tested on 3.7.4 but should work in 3.6+

### Installation

Chromepass requires [Python] 3.6+ to run.

Install the dependencies:

```powershell
> cd chromepass
> pip install -r requirements.txt
```

If any errors occur make sure you're running on the proper environment (if applcable) and that you have python 3.6+ (preferably 3.7.4).
If the errors persist, try:
```powershell
> python -m pip install --upgrade pip
> python -m pip install -r requirements.txt
```

### Running

Chromepass is very straightforward. Start by running:
```powershell
> python create_server.py
```
It will ask you to select between two options:
*  **(1) via email**  _[_To be fixed_]_
    * This will ask you for an ***email*** address and a ***password***
    * It will then ask you if you wish to send to another address or to yourself
    * Next, you're asked if you want to display an error message. This is a fake message that if enabled will appear when the victim opens the executable, after the passwords have been transferred.
    * You can then write your own message or leave it blank
    * You're done! Wait for the executable to be generated and then it's ready.
    
*  **(2) via client.exe** _[Recommended at the moment]_
    * First you're asked to input an ***IP Address*** for a reverse connection. This is the address that belongs to the attacker. It can be a ***local IP address*** or a ***remote IP Address***. If a remote address is chosen, [Port Forwarding](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide/) needs to be in place.
    * You're then asked if you want to display an error message. This is a fake message that if enabled will appear when the victim opens the executable, after the passwords have been transferred.
    * You can then write your own message or leave it blank
    * You're done! Wait for the executables to be generated and then it's ready.
    * The **client.exe** must be started before the **server_ip.exe**. The **server_ip.exe** is the file the victim receives.
* Note: To set a custom icon, replace ***icon.ico*** by the desired icon with the same name and format.


### Todo
 - Sending Real-time precise location of the victim (***completed, releases next update***)
 - Also steal Firefox passwords (***Completed, releases next update***)
 - Option of installing a backdoor allowing remote control of the victim's computer (***completed, releases next update***)
 - Support for more email providers (***in progress***)
 - Also steal passwords from other programs, such as keychains(***in progress***)
 - Add Night Mode (***in progress***)
 
### Errors and Bugs

If you find an error or a bug, please report it as an issue.

### Learn More

For access to a community full of aspiring computer security experts, ranging from the complete beginner to the seasoned veteran,
join our Discord Server: [WhiteHat Hacking](https://discord.gg/beczNYP)

If you wish to contact me, you can do so via: marionascimento@itsec.us

### Disclaimer
I am not responsible for what you do with the information and code provided. This is intended for professional or educational purposes only.

License
----

[MIT](https://github.com/darkarp/chromepass/blob/master/LICENSE)

   
[Python]: <https://www.python.org/downloads/>
