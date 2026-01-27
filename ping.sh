#!/bin/bash

# -c 1 -> send only 1 packet
# -W 1 -> wait 1 second max
# if checks exit status
# ping returns:
# 	0 - at least one reply
# 	non-zero - no reply / error
# Output doesn't matter
# > /dev/null only hides text

for i in {0..255}; do
	ip="10.0.0.$i"
	if ping -c 1 -W 1 "$ip" > /dev/null 2>&1; then
		echo "Host alive: $ip"
	fi
done
