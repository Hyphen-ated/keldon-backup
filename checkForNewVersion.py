#!/usr/bin/python3

# Imports
import sys
import subprocess
import os
import urllib.request
import hashlib

# Configuration
backup_dir = 'nov29'
things_to_check = [
	'index.html',
	'hanabi.css',
	'constants.js',
	'lobby.js',
	'ui.js'
]

# Subroutines
def error(message):
	print(message)
	sys.exit(1)

def run_command(command):
	try:
		return subprocess.check_output(command)
	except Exception as e:
		error('Failed to run "' + command + '": ' + e)

# Check all the things
something_changed = False
for thing in things_to_check:
	old_thing = backup_dir + '/' + thing
	old_data = open(old_thing, 'rb').read()

	response = urllib.request.urlopen('http://keldon.net/hanabi/' + thing)
	data = response.read()
	text = data.decode('utf-8')[:-1]
	open(thing, 'w').write(text)

	#confusingly, using the binary data straight from urllib gives me a different hash than if i roundtrip it to FS
	data = open(thing, 'rb').read()
	old_md5 = hashlib.md5(old_data).hexdigest()
	new_md5 = hashlib.md5(data).hexdigest()

	if old_md5 != new_md5:
		something_changed = True
		print(thing, 'changed:')
	else:
		print(thing, 'not changed.')


if something_changed:
	print("changes!")
