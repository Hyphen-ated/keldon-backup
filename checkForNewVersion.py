#!/usr/bin/python3

#Before running this, do the following (one time):
# git clone <URL to your fork of MakeHanabiGreatAgain, USING THE SSH PROTOCOL>
# cd MakeHanabiGreatAgain
# git checkout keldon

# Imports
import shutil
import sys
import subprocess
import os
import urllib.request
import hashlib

# Configuration
backup_dir = 'MakeHanabiGreatAgain/'
src_dir = 'src/'
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
    old_thing = backup_dir + src_dir + thing
    old_data = open(old_thing, 'rb').read()

    response = urllib.request.urlopen('http://keldon.net/hanabi/' + thing)
    data = response.read()
    text = data.decode('utf-8')[:-1]
    open(thing, 'w').write(text)

    # confusingly, using the binary data straight from urllib gives me a different hash than if i roundtrip it to FS
    data = open(thing, 'rb').read()
    old_md5 = hashlib.md5(old_data).hexdigest()
    new_md5 = hashlib.md5(data).hexdigest()

    if old_md5 != new_md5:
        something_changed = True
        print(thing, 'changed:')
    else:
        print(thing, 'not changed.')

if something_changed:
    for thing in things_to_check:
        inner_path = backup_dir + src_dir + thing
        shutil.copyfile(thing, inner_path)
        os.chdir(backup_dir)
        os.system('git add ' + src_dir + thing)
        os.chdir('..')
    os.chdir(backup_dir)
    os.system('git commit -m "Changes from Keldon"')
    os.system('git push origin keldon')


