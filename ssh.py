#! /usr/bin/python
# Author: Me
# Purpose: SSH into list of devices and run list of commands

import getopt,sys,paramiko,time,glob,sftp,os,stat
from os import path

# Ensuring variables exist
password, commandfile, username, devicefile = "default", "default", "default", "default"

def usage():
	print "\nOptions: \n-h: help \n-u: username  \n-p: password \n-l: device list \n-c: command list \n\nUsage: python ssh.py -u username -p password -l device-list.txt -c command-list.txt\n"
	return

# This will error if unsupported parameters are received.
try:
	# This grabs input parameters. If the paramater requires an argument, it should have a colon ':' after. IE, -h does not require argument, -l, -u, -c do, so they get colons
	opts, args = getopt.getopt(sys.argv[1:], "hl:u:c:d:p:")
except getopt.GetoptError, err:
	# print help information and exit:
	print str(err) # will print something like "option -a not recognized"
	usage()
	sys.exit(2)

# This loops through the given parameters and sets the variables. The letters o and a are arbitrary, anything can be used.
# The logic is 'if paramater = x, set variable'.
for o, a in opts:
	if o == "-l":
		devicefile = a
	elif o in ("-h"):
		usage()
		sys.exit()
	elif o in ("-u"):
		username = a
	elif o in ("-c"):
		commandfile = a
	elif o in ("-p"):
		password = a
	else:
		assert False, "unhandled option"

# This prints the given arugments
print "Username: ", username
print "Password: ", password
print "Device List: ", devicefile
print "Command List: ", commandfile


# Opens files in read mode
f1 = open(devicefile,"r")
f2 = open(commandfile,"r")

# Creates list based on f1 and f2
devices = f1.readlines()
commands = f2.readlines()


# This function loops through devices. No real need for a function here, just doing it.
def connect_to(x):
	for device in x:
		# This strips \n from end of each device (line) in the devices list
		device = device.rstrip()
		# This opens an SSH session and loops for every command in the file
		for command in commands:
			# This strips \n from end of each command (line) in the commands list
			command = command.rstrip()
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(device, username=username, password=password)
			stdin, stdout, stderr = ssh.exec_command(command)
			output = open(device + "_" + command + "_" + time.strftime("%m-%d-%Y") + "_" + time.strftime("%H:%M:%S") + ".kore", "w")
			output.write("\n\nCommand Issued: "+command+"\n")
			output.writelines(stdout)
			output.write("\n")
			print "Your file has been updated, it is ", device + "_" + command + "_" + time.strftime("%m-%d-%Y") + "_" + time.strftime("%H:%M:%S") + ".kore"
			ssh.close()
connect_to(devices)
f1.close()
f2.close()

#for items in glob.glob("/home/lkiser/Downloads/*.kore"):
#	os.chmod(items, 0o777);

host = "10.69.74.6"
port = 22

sftpusername = "lkiser"
sftppassword = "password"

local_dir = "/home/lkiser/Downloads/*.kore"
remote_dir = "/home/lkiser/Desktop/Kore_Files"
with sftp.Server(sftpusername, sftppassword, host, port) as server:
	for image in glob.glob(local_dir):
		base = path.basename(image)
		server.upload(image, path.join(remote_dir, base))

server.close()
print 'Upload to remote directory complete.'

for files in glob.glob("/home/lkiser/Downloads/*.kore"):
	os.remove(files)

print 'Files deleted from local directory.'
