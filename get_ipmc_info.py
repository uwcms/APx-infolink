#!/usr/bin/python3

import sys
import json
import socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
for i in range(0, 3):
	try:
		sock.connect('/var/run/elmlinkd/Info')
	except:
		pass
	else:
		break
else:
	print('Unable to establish connection to IPMC InfoLink via ELMLink daemon.', file=sys.stderr)
	raise SystemExit(1)

sock.send(b'GET_INFO')
while True:
	ret = sock.recv(102400)
	if ret[:5] == b'INFO ':
		print(json.dumps(json.loads(ret[5:].decode('utf8')), indent='  '))
		break
