#!/usr/bin/python
"""Quota overrun notifier"""


__AUTHOR__ = "Paul Bissex <pb@e-scribe.com>"
__VERSION__ = "0.2 2005-05-06"
__LICENSE__ = "MIT"


import os, commands, time


# Modify the following values as needed
LOCATIONS = ["/Volumes/Raid_1", "/Volumes/Raid_2"]
SKIP = [".", "..", ".DS_Store", "Desktop DB", "Desktop DF", "Temporary Items", "_Drop_Boxes"]
LIMIT = 1000000   # size in K; 1000000 = 1GB
USER_REPORT_FILE = "/Library/WebServer/Documents/quota_by_user.txt"
SIZE_REPORT_FILE = "/Library/WebServer/Documents/quota_by_size.txt"
NOTE_FILENAME = "OVER-QUOTA-READ-ME.txt"


def generate_note(fullpath, size):
        user = os.path.split(fullpath)[-1]
        text = """%s

OVER QUOTA WARNING:

Server limit per user: %d megabytes
You (%s) are currently using: %d megabytes

Please get yourself back under the limit!

Every four hours the server is checked automatically, and this note is updated (if you are still over the limit) or removed (if you are under it).

Thanks!
""" % (time.asctime(), LIMIT/1000, user, size/1000)
        return text


def leave_note(fullpath, size):
        note = generate_note(fullpath, size)
        notepath = os.path.join(fullpath, NOTE_FILENAME)
        notefile = open(notepath, "w")
        notefile.write(note)
        notefile.close()


def remove_note(fullpath):
        notepath = os.path.join(fullpath, NOTE_FILENAME)
        if os.path.isfile(notepath):
                os.remove(notepath)
                return 1  # "True" in Python 2.3+
        else:
                return 0  # "False" in Python 2.3+


def user_report(data):
        report = open(USER_REPORT_FILE, "w")
        report.write("Server quota report -- %s\n\n" % time.asctime())
        for fullpath, size in data:
                report.write("%32s %12d M \n" % (fullpath, size/1000))
        report.close()


def size_cmp(datum1, datum2):
        """Compare second item in tuple (user's directory size); descending"""
        return cmp(datum2[1], datum1[1])


def size_report(data):
        report = open(SIZE_REPORT_FILE, "w")
        report.write("Server quota report -- %s\n\n" % time.asctime())
        data.sort(size_cmp)
        for fullpath, size in data:
                report.write("%32s %12d M \n" % (fullpath, size/1000))
        report.close()


def generate_reports():
        lusers = []
        for location in LOCATIONS:
                dirs = os.listdir(location)
                dirs = [d for d in dirs if d not in SKIP]
                for dir in dirs:
                        fullpath = os.path.join(location, dir)
                        command = "du -k %s | tail -n1 | colrm 9" % fullpath
                        try:
                                size = int(commands.getoutput(command))
                        except ValueError:
                                print "ERROR: %s \n" % fullpath
                        if size > LIMIT:
                                lusers.append((fullpath, size))
                                leave_note(fullpath, size)
                        else:
                                remove_note(fullpath)
        user_report(lusers)
        size_report(lusers)


if __name__ == "__main__":
        print "Server quota reports: running..."
        generate_reports()
        print "Server quota reports: complete."
        print "Server quota report by user:", USER_REPORT_FILE
        print "Server quota report by size:", SIZE_REPORT_FILE
