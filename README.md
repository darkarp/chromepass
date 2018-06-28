# Hacking Chrome Saved Passwords

### Pre Requisites:

(**This script should work for Windows XP all the way to Windows 10, both 32-bit and 64-bit**)

	1. Python 2.7	-  https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi 
			 (It has to be 2.7 32 bit (x86) or it won't work)
			 
	2. PyWin32	-  Installable by runing "pip install pypiwin32"
			 or "C:\Python27\Scripts\pip.exe install pywin32"
			 
	3. Requests	-  Installable by runing "pip install requests" 
			 or "C:\Python27\Scripts\pip.exe install requests"
			 
	4. py2exe 	-  https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/ 
			 (choose the 32-bit version for 2.7)
			 
### **IMPORTANT**: 
Enviroment Variables: Do not forget to include Python27 folder and Scripts folder in PATH environment variable. 


### Features:

	
	1. Grabs Google Chrome saved passwords and decrypts them.
	2. Sends these passwords to the attacker, saving it on a text file, 
	via HTTP (Passwords are saved in the same directory as the Client launched by the attacker)
	3. Option of having a fake Error Message appear
	4. Custom Icon

Victim will open the server and all the Google Chrome Passwords will be sent to the attacker remotely and saved as a text file on the attacker's computer. The connection is done by reverse-http.

PS: This was originally part of one of my malwares so I had to adjust. I didn't have time to clean it up yet that's why it looks so messy.

### Next version will include:
* Firefox Stealer


# Instructions:


## Local Exploitation (If your target is in the same network as you):
	

	1. If you want to activate the fake Error message, you should first uncomment line 147 (remove the # character). If you don't want a fake message to appear, skip this step.
	
	2. If you want a custom icon place the icon on the same directory as the scripts and rename it "icon.ico', replacing the file that was already there with the same name. If you don't want a custom icon, skip this step.
	
	3. Create server by runing the python script "create_server.py"
	It will then ask you for your ip, you must type your local ip (ex: 192.168.0.1)
	To find this ip open up CMD and type "ipconfig"
	
	4. Start the client.exe 
	(I recommend having the client, alongside all other files in a directory in "C:\", like "C:\ChromePass\[all_files]")
	
	5. Send the server.exe to your target 
	(choosing an appropriate name is always important)
	
	6. You will obtain a password text file in the same location as the client 
	with all the Google Chrome Passwords.

## Remote Exploitation (If target is NOT on the same network as you):

	1. If you want to activate the fake Error message, you should first uncomment line 147 (remove the # character). If you don't want a fake message to appear, skip this step.
	
	2. If you want a custom icon place the icon on the same directory as the scripts and rename it "icon.ico', replacing the file that was already there with the same name. If you don't want a custom icon, skip this step.	
	
	3. Create server by runing the python script "create_server.py". 
	It will then ask you for your ip, you must type your PUBLIC ip (ex: 152.162.93.12). 
	You can obtain your public ip by typing "WhatIsMyIp" on Google.
	
	4. Setup Port forwading. You want to forward the port 80 to your machine 
	(look up how to do that if you don't know)
	
	5. Start the client.exe
	(I recommend having the client, alongside all other files in a directory in "C:\", like "C:\ChromePass\[all_files]")
	
	6. Send the server.exe to your target 
	(choosing an appopriate name is always important)
	
	7. You will obtain a password text file in the same location as the client 
	with all the Google Chrome Passwords.

	
## NOTE:
	DO NOT change the name of the python scripts or text files. 
	  
	The "attacker_ip.txt" file exists only to create the server.exe. 
	  
	If everything seems to work but you aren't receiving the text file, try moving yor client.exe to 
	C:\ directory (i.e. "C:\client.exe") and run both client and server again.  
	  
	Make sure the client is runing before the server runs. 
	Password text file will be saved in the same diretory as the client.exe file.
	

### Any questions open up an issue on GitHub or contact me at: MarioNascimento@ITCrashSecurity.com
#### Please make sure your issue haven't been answered before, to avoid duplicate issues on Github page.


#### DISCLAIMER: I will not be held responsible for the misuse of these scripts. EDUCATIONAL or PROFESSIONAL use only
