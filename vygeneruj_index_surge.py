#! /usr/bin/env python3

import sys
import subprocess

cmd='cd output && find . -type f -name "*.pdf" | sort'
				   
if __name__ == '__main__':
	res=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.read()
	fns=str(res)
	fns=fns.split()
	lis=['\n\t<li><a href="{url}">{url}</a></li>'.format(url=x.replace("./","")) for x in fns ]
	table = "<ul>\n" + "".join(lis) + "\n</ul>\n"

	with open('index_template.html') as f:
		content = f.read()

	print(content.replace("##zpevniky##",table))
