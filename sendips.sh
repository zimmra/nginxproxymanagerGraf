#!/bin/sh

tail -f /logs/proxy-host*_access.log | grep -E " ([0-9]{1,3}[\.]){3}[0-9]{1,3}" | while read line;
do
  domain=`echo ${line} | grep -m 1 -o -E " [a-z0-9\-]*\.[a-z0-9]*\.(de|net|org|com)"`
  ipaddressnumber=$(echo $line | grep -o -m 1 -E "([0-9]{1,3}[\.]){3}[0-9]{1,3}" | head -n 1 | grep -E -v "^10\.|^172\.(1[6-9]|2[0-9]|3[0-1])\.|^192\.168\.")
  length=`echo $line | awk -F ' ' '{print$14}' | grep -m 1 -o '[[:digit:]]*'`

  if [ -z "$domain" ]; then
    domain="empty"
  fi

  if [ ! -z "$ipaddressnumber" ]; then
    echo "$length = $ipaddressnumber = $domain"
    python /root/.config/NPMGRAF/Getipinfo.py "$ipaddressnumber" "$domain" "$length"
  fi
done
reboot