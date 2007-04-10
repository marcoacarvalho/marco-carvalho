#!/usr/bin/python
r"""Usage: pyregex.py [options] "-"|filename regex [replacement [count]]

Test Python regular expressions. Specify test data's filename or use "-"
to enter test text from console. Optionally specify a replacement text.

Options:
-f      filter mode
-n nnn  limit to examine the first nnn lines. default no limit.
-m      show only matched line. default False


Regular Expression Syntax

Special Characters
------------------------------------------------------------------------
.       matches any character except a newline
^       matches the start of the string
$       matches the end of the string or just before the newline at the end of
        the string
*       matches 0 or more repetitions of the preceding RE
+       matches 1 or more repetitions of the preceding RE
?       matches 0 or 1 repetitions of the preceding RE
{m}     exactly m copies of the previous RE should be matched
{m,n}   matches from m to n repetitions of the preceding RE
\       either escapes special characters or signals a special sequence
[]      indicate a set of characters. Characters can be listed individually,
        or a range of characters can be indicated by giving two characters and
        separating them by a "-". Special characters are not active inside sets
        Including a "^" as the first character match the complement of the set
|       A|B matches either A or B
(...)   indicates the start and end of a group
(?...)  this is an extension notation. See documentation for detail
(?iLmsux) I ignorecase; L locale; M multiline; S dotall; U unicode; X verbose

*, +, ? and {m,n} are greedy. Append the ? qualifier to match non-greedily.


Special Sequences
------------------------------------------------------------------------
\number matches the contents of the group of the same number. Groups are
        numbered starting from 1
\A      matches only at the start of the string
\b      matches the empty string at the beginning or end of a word
\B      matches the empty string not at the beginning or end of a word
\d      matches any decimal digit
\D      matches any non-digit character
\g<name>use the substring matched by the group named 'name' for sub()
\s      matches any whitespace character
\S      matches any non-whitespace character
\w      matches any alphanumeric character and the underscore
\W      matches any non-alphanumeric character
\Z      matches only at the end of the string


See the Python documentation on Regular Expression Syntax for more detail

http://docs.python.org/lib/re-syntax.html
"""

__author__ = "Wai Yip Tung"
__version__ = "0.5"
__url__ = "http://tungwaiyip.info/software/pyregex.html"
__license__ = "Public Domain"

#2006-03-08 support unicode?
#2006-03-08 no multiline support?

import re
import sys

# select console coloring option
USE_ANSI = True
USE_WIN32CONSOLE = False

if 'win32' in sys.platform.lower():
    try:
        import win32console
        import pywintypes
    except ImportError:
        pass
    else:
        USE_ANSI = False
        win32_stdout = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
        try:
            win32_orig_attr = win32_stdout.GetConsoleScreenBufferInfo()['Attributes']
            USE_WIN32CONSOLE = True
        except pywintypes.error, e:
            # output redirected?
            pass


def writeColor(s):
    """ write with hightlighted color """
    if USE_WIN32CONSOLE:
        # windows console
        win32_stdout.SetConsoleTextAttribute(31)
        sys.stdout.write(s)
        win32_stdout.SetConsoleTextAttribute(win32_orig_attr)
    elif USE_ANSI:
        sys.stdout.write('\x1b[1;44m')
        sys.stdout.write(s)
        sys.stdout.write('\x1b[0m')
    else:
        # ASCII mode
        sys.stdout.write('[')
        sys.stdout.write(s)
        sys.stdout.write(']')


def open_text(p):
    """
    generator to return lines from filename
    note line is stripped of trailing \n
    """
    if p.filename == '-':
        if not p.filter_mode:
            print 'Enter the text below. End with EOF.'
        #get all input first
        lines = []
        while True:
            try:
                line = raw_input('')
            except EOFError:
                break
            lines.append(line)
        for line in lines:
            yield line
    else:
        fp = file(p.filename)
        for line in fp:
            yield line.rstrip()
        fp.close()


def scan(fp, r, p):
    if not p.filter_mode:
        print
    count = 0
    first_match = None
    for i,line in enumerate(fp):

        if p.number_of_lines and i >= p.number_of_lines:
            break

        # find/replace pattern
        # build matches as a list of (match obj, match text)
        if p.repl:
            matches = []
            def substitute(m):
                text = m.expand(p.repl)
                matches.append((m, text))
                return text
            r.sub(substitute, line, p.rcount)
        else:
            matches = [(m, m.group()) for m in r.finditer(line)]

        if p.match_only and not matches:
            continue

        # show result line
        cp = 0
        if not p.filter_mode:
            sys.stdout.write('%2d: ' % (i+1))

        for m,text in matches:
            count += 1
            if not first_match:
                first_match = m
            if m.start() > cp:
                sys.stdout.write(line[cp:m.start()])
            if not p.filter_mode:
                writeColor(text)
            else:
                sys.stdout.write(text)
            cp = m.end()
        if cp < len(line):
            sys.stdout.write(line[cp:])
        sys.stdout.write('\n')

    # show group (first_macth)
    if not p.filter_mode:
        if first_match and first_match.lastindex:
            print '\nGroups:'
            print '\\0: "%s"' % first_match.group(0)
            for i, g in enumerate(first_match.groups()):
                print '\%s: "%s"' % (i+1,g)
            for n,v in first_match.groupdict().items():
                print '%s: "%s"' % (n,v)

    # show final stat
    if not p.filter_mode:
        if count:
            print '\nNumber of matches: %s\n' % count
        else:
            print '\nNo match\n'


def main(p):
    try:
        r = re.compile(p.regex)
    except re.error, e:
        print >>sys.stderr, '%s: "%s"' % (e, p.regex)
        sys.exit(-1)
    fp = open_text(p)
    scan(fp, r, p)


class Parameters:
    def __init__(self):
        self.filename = '-'
        self.filter_mode = False
        self.number_of_lines = 0
        self.match_only = False
        self.regex = ''
        self.repl = ''
        self.rcount = 0


def print_usage():
    print __doc__
    sys.exit(-1)


if __name__ =='__main__':
    argv = sys.argv[1:]

    p = Parameters()

    # parse options
    while argv:
        if argv[0] == '-f':
            argv.pop(0)
            p.filter_mode = True
        elif argv[0] == '-m':
            argv.pop(0)
            p.match_only = True
        elif argv[0] == '-n':
            argv.pop(0)
            if argv and argv[0].isdigit():
                p.number_of_lines = int(argv.pop(0))
            else:
                print_usage()
        else:
            break

    if not argv:
        print_usage()
    p.filename = argv.pop(0)

    if not argv:
        print_usage()
    p.regex = argv.pop(0)

    if argv:
        p.repl = argv.pop(0)

    if argv and argv[0].isdigit():
        p.rcount = int(argv.pop(0))

    main(p)
