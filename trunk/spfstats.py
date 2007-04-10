#!/usr/bin/env python
"""Postfix SPF stats report generator

Displays statistics relating to Postfix SPF activity. Output is formatted
using Markdown for easy conversion to HTML.
"""


__author__ = "Paul Bissex <pb@e-scribe.com>"
__version__ = "0.3.0"
__date__ = "2005-06-27"
__usage__ = "spfstats.py [days]"
__license__ = "GPL"


import os, sys, string, re, time


SPF_MESSAGE_TYPES = ['fail', 'softfail']
DATE_FORMAT = "%a %b %d"
SPF_NOTICE_PATTERN = "sender=(?:.*?%40)?(.+?)&ip=(.+?)&"
CURRENT_LOGFILE = "/var/log/mail.log"
ROTATED_LOGFILE_TEMPLATE = "/var/log/mail.log.%d.gz"


class LogfileNotFound(Exception):
    pass
class SPFStatsError(Exception):
    pass


def get_maillog_lines(days_ago, text):
    """Grep a Postfix maillog file for lines containing 'text'"""
    if days_ago == 0:
        (command, file) = ("cat", CURRENT_LOGFILE)
    elif days_ago == 1:
        (command, file) = ("cat", CURRENT_LOGFILE+".0")
    else:
        (command, file) = ("gunzip -c", ROTATED_LOGFILE_TEMPLATE % (days_ago - 1))
    if not os.path.isfile(file):
        raise LogfileNotFound, file
    full_command = "%s %s | grep '%s'" % (command, file, text)
    output = os.popen(full_command).readlines()
    return map(string.strip, output)


def get_raw_stats(days):
    """Gather raw stats (logfile lines)"""
    stats = {}
    for type in SPF_MESSAGE_TYPES:
        stats[type] = {}
        for day in range(days):
            stats[type][day] = get_maillog_lines(day, "SPF %s:" % type)
    return stats


def header(level, text):
    tag = "#" * level
    return "\n%s %s %s" % (tag, text, tag)


def day_label(days_ago):
    """Return a formatted date label"""
    then = time.time() - days_ago * 60 * 60 * 24
    date_text = time.strftime(DATE_FORMAT, time.localtime(then))
    return date_text


def domains_report(log_data, days):
    """Tally domains found in log data"""
    sender_ip_counts = {}
    corrupt_log_lines = []
    for days_ago in range(days):
        print "\n" + header(2, day_label(days_ago))
        for type in SPF_MESSAGE_TYPES:
            data = log_data[type][days_ago]
            if len(data) == 0:
                print header(3, "No '%s' responses" % type)
            else:
                domain_counts = {}
                for line in data:
                    try:
                        (domain, sender) = re.search(SPF_NOTICE_PATTERN, line).groups()
                    except AttributeError:
                        corrupt_log_lines.append(line)
                    # We collect sender data but reporting is unfinished
                    if sender not in sender_ip_counts:
                        sender_ip_counts[sender] = 0
                    sender_ip_counts[sender] += 1
                        
                    if domain not in domain_counts:
                        domain_counts[domain] = 0
                    domain_counts[domain] += 1

                print header(3, "%d '%s' responses involving %d domains" % \
                  (len(data), type, len(domain_counts)))
                domains = domain_counts.keys()
                domains.sort()
                for domain in domains:
                    print "  * %3d\t%s" % (domain_counts[domain], domain)

    if len(corrupt_log_lines):
        print "\n" + header(2, "%d possible corrupt log lines" % len(corrupt_log_lines))
        for line in corrupt_log_lines:
            print line


def report(days=8):
    """Main function: display report"""
    print "\n" + header(1, "[SPF](http://spf.pobox.com/) forgery rejection report")
    days = max(days, 1)
    days = min(days, 4)
    try:
        log_data = get_raw_stats(days)
    except LogfileNotFound, file:
        print "# ERROR: Couldn't find %s when fetching log data. #" % file
        return
    domains_report(log_data, days)


if __name__ == '__main__':
    try:
        report(int(sys.argv[1]))
    except IndexError:
        report()
