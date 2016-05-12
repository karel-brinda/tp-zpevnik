#!/usr/bin/env python
 
# index_gen.py
 
import os
import os.path
import sys
 
class SimpleHtmlFilelistGenerator:
    # start from this directory
    base_dir = None
 
    def __init__(self, dir):
        self.base_dir = dir
 
    def print_html_header(self):
        print """<html>
<body>
<code>
""",
 
    def print_html_footer(self):
        print """</code>
</body>
</html>
""",
 
    def processDirectory ( self, args, dirname, filenames ):
        print '<strong>', dirname + '/', '</strong>', '<br>'
        for filename in sorted(filenames):
            rel_path = os.path.join(dirname, filename)
            if rel_path in [sys.argv[0], './index.html']:
                continue   # exclude this generator script and the generated index.html
            if os.path.isfile(rel_path):
                href = "<a href=\"%s\">%s</a>" % (rel_path, filename)
                print '&nbsp;' * 4, href, '<br>'
 
    def start(self):
        self.print_html_header()
        os.path.walk( self.base_dir, self.processDirectory, None )
        self.print_html_footer()
 
# class SimpleHtmlFilelistGenerator
 
if __name__ == "__main__":
    base_dir = '.'
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    gen = SimpleHtmlFilelistGenerator(base_dir)
    gen.start()