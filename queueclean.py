#!/usr/bin/env python
"""Postfix mailqueue cleaning tool (interactive)

Allows easy deletion of e.g. outbound messages to bogus spammer domains
Caveat administrator: this script contains no error checking
"""

__author__ = "Paul Bissex <pb@e-scribe.com>"
__license__ = "MIT"

import commands, re

q = commands.getoutput("mailq").split("\n")

if len(q) == 1:
    print "Postfix mail queue is empty."
else:
    # print last line -- this tells us how many items are in the queue
    print "\n\nMail queue:", q[-1], "\n"
    for line in q:
        id = re.match("^([A-F0-9]+)", line)
        if id:
            msg = id.group(1)
            
        # blank line between entries is our cue to prompt user
        if line == "":
            reply = raw_input("===> Delete message " + msg + " (y/n)?")
            if reply == "y":
                print commands.getoutput("sudo postsuper -d " + msg)
        else:
            print line

