#!/usr/bin/python -u
# Author: Guy Baconniere & Matteo Castelli
# From an idea of Arnas Kupsys

import sys, signal, re

# Customizations

# Enable linestopping mechanism

lineStop = False
lineStopToken = '#!QUIT!'
removeAnsiCodes = True


fullContent = ''

def sendToClipBoard(string):
	if removeAnsiCodes == True:
		r= re.compile("\033\[[0-9;]+m") 
		string = r.sub("", string)

	from AppKit import NSPasteboard,NSObject,NSStringPboardType
	pasteboard = NSPasteboard.generalPasteboard()
	emptyOwner = NSObject.alloc().init()
	pasteboard.declareTypes_owner_([NSStringPboardType], emptyOwner)
	pasteboard.setString_forType_(string, NSStringPboardType)

def signal_handler(signal, frame):
        sendToClipBoard(fullContent)
        sys.exit(0)


if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	signal.signal(signal.SIGPIPE, signal_handler)


	while 1:
		try:
			line = sys.stdin.readline()
		except KeyboardInterrupt:
			break

		if not line:
			break

		# Stop the code when the lineStopToken is received in the buffer
		if lineStop == True:
			if lineStopToken in line:
				break

		fullContent += line

	sendToClipBoard(fullContent)

