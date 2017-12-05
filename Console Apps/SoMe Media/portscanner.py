#!/usr/bin/env python3.6
import socket
import subprocess
import sys
from datetime import datetime

# Clear the screen
subprocess.call('clear', shell=True)

# Ask for input
remoteServer = input(r'Enter the remote host to scan: ')
remoteServerIP = socket.gethostbyname(remoteServer)

# Print a nice banner with information on which host we are about to scan
print("-" * 60)
print(f'Please wait, scanning {remoteServer}')
print("-" * 60)

# Check what time the scan started
start_time = datetime.now()

# Using the range function to specify ports (here it will scan all ports between 1 and 1024)

# We also put in some error handling for catching errors

try:
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print(f'Port {port}: 	 Open')
        sock.close()

except KeyboardInterrupt:
    print("You pressed Ctrl+C")
    sys.exit()

except socket.gaierror:
    print("Hostname could not be resolved. Exiting")
    sys.exit()

except socket.error:
    print("Couldn't connect to server")
    sys.exit()

# Checking the time again
end_time = datetime.now()

# Calculates the difference of time, to see how long it took to run the script
elapsed_time = end_time - start_time

# Printing the information to screen
print(f'Scanning Completed in: {elapsed_time}')
