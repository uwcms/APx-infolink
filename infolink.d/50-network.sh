#!/bin/bash

ADDRS4="$(ip addr list | egrep '\sinet '  | sed -re 's/.*inet (\S+) .*/\1/' | egrep -v '^127\.')"
ADDRS6="$(ip addr list | egrep '\sinet6 '  | sed -re 's/.*inet6 (\S+) .*/\1/' | egrep -v '^::1/')"
ADDRSE="$(ip addr list | egrep '\slink/ether '  | sed -re 's/.*link\/ether (\S+) .*/\1/')"
ADDRLIST4="\"$(echo $ADDRS4 | sed -re 's/ /", "/g')\""
ADDRLIST6="\"$(echo $ADDRS6 | sed -re 's/ /", "/g')\""
ADDRLISTE="\"$(echo $ADDRSE | sed -re 's/ /", "/g')\""
[ "$ADDRLIST4" = '""' ] && ADDRLIST4=''
[ "$ADDRLIST6" = '""' ] && ADDRLIST6=''
echo "{\"ipv4_addresses\": [${ADDRLIST4}], \"ipv6_addresses\": [${ADDRLIST6}], \"mac_addresses\": [${ADDRLISTE}], \"hostname\":\"$(hostname --fqdn)\"}"
