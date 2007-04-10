#!/usr/bin/env python

import os
import sys
import cgi
import re

def header():
    print """<html>
        <head>
            <title>WebCommands</title>
        </head>
        <body>"""

def valid_ip(ip):
    return re.match('([0-9]{1,3}\.){3}[0-9]{1,3}', ip)

def main():
    header()
    body()
    footer()

def body():
    form = cgi.FormContentDict()

    print '<h1>Host</h1>'
    print '<form method="get">'
    if form.has_key('ip'):
        ip = form.dict['ip'][0]
        print '<p>IP: <input type="text" name="ip" value="%s"></p>' % (ip)
    else:
        print '<p>IP: <input type="text" name="ip"></p>'
    print '<p>'
    print '<input type="submit" name="command" value="Ping">'
    print '<input type="submit" name="command" value="Traceroute">'
    print '<input type="submit" name="command" value="NMap">'
    print '</form>'

    if not valid_ip(ip):
        print "<p>Error: invalid ip address</p>"
        return

    if form.has_key('command'):
        print "<h1>Command Result</h1>"
        if not do_command(form.dict['command'][0].lower(), ip):
            print "<p class='error'>Error: invalid command</p>"
        return

def footer():
    print "</body>"
    print "</html>"

def do_command(cmd, ip):
    print "teste"
    if cmd == 'ping':
        p = '/bin'
        c = 'ping'
    elif cmd == 'traceroute':
        p = '/usr/sbin'
        c = 'traceroute'
    elif cmd == 'nmap':
        p = '/usr/bin'
        c = 'nmap'
    else:
        return 0

    try:
        pid, fd = os.forkpty()
    except:
        sys.stderr.write("cannot fork()\n")
        sys.exit(1)

    if pid == 0:
        os.execv("%s/%s" % (p, c), [c] + [ip])
        sys.exit(0)

    print "<pre>"
    buffer = ""
    while 1:
        try:
            data = os.read(fd, 32)
        except:
            break

        buffer = buffer + data
        res = buffer.split("\n", 1)

        if len(res) != 2:
            continue

        line, buffer = res

        line = line.strip()
        print "%s" % (line)
        sys.stdout.flush()

    print "</pre>"

    os.close(fd)

    return 1

if __name__ == '__main__':
    print "Content-type: text/html\n"
    main()
