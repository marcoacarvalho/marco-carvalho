#!/usr/bin/env python
# 
# blockreport: parse sendmail log file and send email reports to local users
#              listing emails addressed to them that were blocked by the server
#
# Christian Reis <kiko@async.com.br>
# cvs -d :pserver:anonymous@cvs.async.com.br:/cvs co async-scripts/blockreport

DOMAIN  = "async.com.br"
ABUSE   = "Async Spamcop <abuse@async.com.br>"
SUBJECT = "Emails bloqueados para %s"
HEADER  = """Este é um resumo das mensagens bloqueadas pelo nosso servidor de 
email por serem consideradas spam (mensagem não-solicitada).
Para dúvidas ou informes de erro, contactar abuse@async.com.br"""
TITLE   = "Emails bloqueados nesta semana para o endereço: %s@%s\n"

import sys, smtplib, os
from string import split, join, find, lower, strip

SAVE_LINES = 20
DEBUG      = 1
MAILLOG  = open("/var/log/mail")
ALIASES  = open("/etc/mail/aliases")
SENDMAIL = open("/etc/mail/sendmail.cf")
PASSWD   = open("/etc/passwd")
# Comment out if you don't use nis
YPPASSWD = os.popen("ypcat passwd", "r")

# Don't step beyond this line unless you want to get your hands dirty

def process_block(line):
    user = split(line, "arg1=")[1]
    user = split(user, "relay=")[0]
    if user[0] == "<":
        user = user[1:-3]
    else:
        user = user[:-2]
    id = split(line, " ")[5][:-1]
    reason = split(line, "reject=")[1]
    reason = join(split(reason)[3:])
    time = join(split(line)[0:3],"-")
    return lower(user), [id, time, reason]

def process_sender(line):
    sender = split(line, "from=")[1]
    sender = split(sender, "size=")[0]
    sender = sender[:-2]
    return sender

def make_header(recipient):
    subject = SUBJECT % recipient
    message = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" \
               % (ABUSE, recipient, subject)
    message = message + HEADER
    return message

def make_body(store, user):
    for domain in store[user].keys():
        message = "\n" + "-" * 80 + "\n" 
        message = message + TITLE % (user, domain) + "\n"
        i = 1
        for block in store[user][domain]:
            time = block[1]
            reason = block[2]
            sender = block[3]
            message = message + "%3s From: %-54s %s\n    %s\n\n" \
                                 % (i, sender, time,  reason)
            i = i+1
    return message

# XXX: this is very tied to being run local to the SMTP server, and doesn't
# support anything fancy like ldap or subdomains. Supports sendmail.cf and
# /etc/mail/local-host-names, and /etc/passwd, NIS, and aliases

def get_valid_domains():
    # Parse sendmail.cf to look for host names recognized as local
    valid_domains = []
    sendmail = SENDMAIL.readlines()
    for line in sendmail:
        line = strip(split(line, "#")[0])
        if line[:2] == "Cw":
            domain = strip(split(line, "Cw",1)[1])
            valid_domains.append(domain)
        elif line[:2] == "Fw":
            file = split(line, "Fw",1)[1]
            hosts = open(file).readlines()
            hosts = map(strip, hosts)
            valid_domains.extend(hosts)
    return valid_domains

def get_valid_users():
    # Find out what users are considered to be valid users
    valid_users = {}
    if globals().has_key("PASSWD"):
        passwd = PASSWD.readlines()
        for line in passwd:
            user = split(line,":")[0]
            # Skip special NIS entry
            if user == "+":
                continue
            valid_users[user] = user
    if globals().has_key("YPPASSWD"):
        passwd = YPPASSWD.readlines()
        for line in passwd:
            user = split(line,":")[0]
            valid_users[user] = user
    if globals().has_key("ALIASES"):
        aliases = ALIASES.readlines()
        for line in aliases:
            line = strip(split(line, "#")[0])
            if line:
                user = split(line,":")[0]
                valid_users[user] = user
    return valid_users.keys()

# Double hash keyed by user and domain to list of blocks
blocks = {}
# Same as blocks, but stores email that was sent to invalid addresses
bogus = {}
# Caches lines of sendmail.cf that are used to search for the sender line 
context = []

valid_users = get_valid_users()
valid_domains = get_valid_domains()

# XXX: arg handling, help, etc
if len(sys.argv) > 1:
    maillog = open(sys.argv[1])
else:
    maillog = MAILLOG

# Prefill context
while len(context) < SAVE_LINES:
    context.append(maillog.readline())

newline = 1
while newline:
    # get current line
    line=context[0]

    # Take care of keeping context full
    context.pop(0)
    newline = maillog.readline()
    if newline:
        context.append(newline)
    
    # Check if the line contains a block
    if find(line, "check_rcpt") == -1:
        continue

    # Grab the line data and store it in blocks
    user, data = process_block(line)
    # the ,1 is for email address with TWO @s - life in the real world
    user, domain=split(user,"@",1)
    if domain not in valid_domains or user not in valid_users:
        store = bogus
    else:
        store = blocks

    if not store.has_key(user):
        store[user]={}
    if not store[user].has_key(domain):
        store[user][domain]=[]
    store[user][domain].append(data)

    # look through the lines in context for the matching sender line
    id = data[0]
    for j in range(0,len(context)):
        newline = context[j]
        if find(newline, "lost input channel") != -1:
            # We don't want this line
            continue
        if find(newline, "check_rcpt") != -1:
            # When multiple recipients are from a single id
            continue
        if newline != line and find(newline, id) != -1:
            sender = process_sender(newline)
            break
    else:
        msg = "Couldn't find the matching sender line for block %s"
        raise AssertionError, msg % line

    # update blocks
    store[user][domain][-1].append(sender)
maillog.close()

server = smtplib.SMTP('localhost')

# Send reports to users
keys = blocks.keys()
keys.sort()
for user in keys:
    recipient = "<%s@%s>" % (user, DOMAIN)
    message = make_header(recipient) + make_body(blocks, user)
    if DEBUG:
        print message
    else:
        server.sendmail(ABUSE, recipient, message)

# Send single report to abuse for bogus recipients
keys = bogus.keys()
keys.sort()
message = make_header(ABUSE)
for user in keys:
    message = message + make_body(bogus,user)
if DEBUG:
    print message
else:
    server.sendmail(ABUSE, ABUSE, message)

server.quit()
