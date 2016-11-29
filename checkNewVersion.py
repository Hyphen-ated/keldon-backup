#!/usr/bin/python3

# Imports
import sys
import subprocess
import re

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
for thing in things_to_check:
	old_thing = backup_dir + '/' + thing
	run_command(['wget', 'http://keldon.net/hanabi/' + thing, '--quiet'])
	old_md5 = run_command(['md5sum', old_thing]).decode('utf-8').strip()
	old_md5 = re.search(r'^(.+?) ', old_md5).group(1)
	new_md5 = run_command(['md5sum', thing]).decode('utf-8').strip()
	new_md5 = re.search(r'^(.+?) ', new_md5).group(1)
	if old_md5 != new_md5:
		print(thing, 'changed:')
		print(run_command(['diff', thing, old_thing]))
	else:
		print(thing, 'not changed.')	
	run_command(['rm', thing])
