# Hacking Chrome Saved Passwords

### Pre Requisites:
	1. Python 2.7	-  https://www.python.org/downloads/. 
			 (It has to be 2.7 or it won't work)
			 
	2. PyWin32	-  Installable by runing "pip install pypiwin32"
			 or "C:\Python27\Scripts\pip.exe install pywin32"
			 
	3. Requests	-  Installable by runing "pip install requests" 
			 or "C:\Python27\Scripts\pip.exe install requests"
			 
	4. py2exe 	-  https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/ 
			 (choose the 32-bit version for 2.7)
			 
### **IMPORTANT**: 
Enviroment Variables: Do not forget to include Python27 folder and Scripts folder in PATH environment variable. A simple way to do it is to run Powershell (Windows key + R and type "powershell") and run the following command:
```Powershell
[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")
```
**NOTE**: This command assumes Python was installed in the default directory
### Features:

	1. Grabs Google Chrome saved passwords and decrypts them.
	2. Sends these passwords to the attacker, saving it on a text file, 
	via HTTP (Passwords are saved in the same directory as the Client launched by the attacker)

Victim will open the server and all the Google Chrome Passwords will be sent to the attacker remotely and saved as a text file on the attacker's computer. The connection is done by reverse-http.

PS: This was originally part of one of my malwares so I had to adjust. I didn't have time to clean it up yet that's why it looks so messy.


# Instructions:


## Local Exploitation (If your target is in the same network as you):

	1. Create server by runing the python script "create_server.py". 
	It will then ask you for your ip, you must type your local ip (ex: 192.168.0.1)
	To find this ip open um CMD and type "ipconfig"
	
	2. Start the client.exe (I recommend having the client in a directory in "C:\", like "C:\ChromePass\client.exe")
	
	3. Send the server.exe to your target (choosing an appropriate name is always important)
	
	4. You will obtain a password text file in the same location as the client with all the Google Chrome Passwords.

## Remote Exploitation (If target is NOT on the same network as you):

	1. Create server by runing the python script "create_server.py". 
	It will then ask you for your ip, you must type your PUBLIC ip (ex: 152.162.93.12). 
	You can obtain your public ip by typing "WhatIsMyIp" on Google.
	
	2. Setup Port forwading. You want to forward the port 80 and 8080 to your machine 
	(look up how to do that if you don't know)
	
	3. Start the client.exe
	
	4. Send the server.exe to your target (choosing an appopriate name is always important)
	
	5. You will obtain a password text file in the same location as the client with all the Google Chrome Passwords.


## NOTE:
	DO NOT change the name of the python scripts or text files. The "attacker_ip.txt" file exists only to create the server.exe
	If everything seems to work but you aren't receiving the text file, try moving yor client.exe to 
	C:\ directory (i.e. "C:\client.exe") and run both client and server again. Make sure the client is runing before the server runs. Password text file will be saved in the same diretory as the client.exe file.
	

### Any questions open up an issue on GitHub or contact me at: MarioNascimento@ITCrashSecurity.com
#### Please make sure your issue haven't been answered before, to avoid duplicate issues on Github page.


#### DISCLAIMER: I will not be held responsible for the misuse of these scripts. EDUCATIONAL or PROFESSIONAL use only
