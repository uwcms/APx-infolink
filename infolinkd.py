#!/usr/bin/python3

import json
import os
import pathlib
import socket
import stat
import subprocess

IL_DIR = pathlib.Path('/etc/infolink.d')


def generate_info() -> dict:
	info = {}
	for fn in sorted(os.listdir(IL_DIR)):
		if fn == '.' or fn == '..':
			continue
		st = os.stat(IL_DIR / fn)
		if not stat.S_ISREG(st.st_mode):
			continue
		elif os.access(IL_DIR / fn, os.X_OK):
			try:
				info.update(
				    json.loads(subprocess.run([IL_DIR / fn], stdout=subprocess.PIPE, check=True).stdout.decode('utf8'))
				)
			except:
				pass
		elif os.access(IL_DIR / fn, os.R_OK) and fn.endswith('.json'):
			try:
				info.update(json.load(open(IL_DIR / fn, 'r')))
			except:
				pass
	return info


sock = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
for i in range(0, 3):
	try:
		sock.connect('/var/run/elmlinkd/Info')
	except:
		pass
	else:
		break
else:
	print('Unable to establish connection to IPMC InfoLink via ELMLink daemon.')
	raise SystemExit(1)

while True:
	ret = sock.recv(102400)
	if ret == b'GET_INFO':
		sock.send(b'INFO ' + json.dumps(generate_info(), sort_keys=True, indent='  ').encode('utf8'))
