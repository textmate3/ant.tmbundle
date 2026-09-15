#!/usr/bin/env python3

import sys, os.path, re, os

matcher = re.compile(
    r'(/.*?):(\d+):\s*(.*)$'
)

buildfile = None
proj_dir = None

print("""
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="file://%s/ant.css" />
    </head>

    <body>
""" % (os.environ['TM_BUNDLE_SUPPORT']))

sys.stdout.flush()

## read all data from stdin
lastLine = None
line = sys.stdin.readline()
while line:
    line = line.rstrip()

    ## find the buildfile, and from that, the project directory
    if line.startswith("Buildfile"):
        buildfile = line[(line.find(":") + 2):]
        proj_dir = os.path.dirname(buildfile) + "/"

    match = matcher.search(line)

    print("<pre>")

    if not match:
        print(line)
    else:
        fn = match.group(1)

        if proj_dir and fn.startswith(proj_dir):
            short_name = fn[len(proj_dir):]
        else:
            short_name = fn

        colInd = 0

        print(line[:match.start()].rstrip(), end=' ')
        print('<a href="txmt://open?url=file://%s&line=%s&column=%d">%s:%s: %s</a>' % (
            fn, match.group(2), colInd, short_name, match.group(2), match.group(3)
        ), end=' ')
        print(line[match.end():])

    print("</pre>")
    sys.stdout.flush()

    ## read next line
    lastLine = line
    line = sys.stdin.readline()

print("""
    </body>
</html>
""")
