#! /usr/bin/env python3

import sys
import subprocess

cmd='cd output && find . -type f -name "*.pdf" | sort'
				   
def html_pisen(fn):
	return '\n\t<li><a href="{url}">{url}</a></li>'.format(url=fn.replace("./",""))

if __name__ == '__main__':
	res=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.read()
	fns=str(res)
	fns=fns.split()
	#list_singles=[html_pisen(url) for url in fns if "TP_zpevnik_komplet_singles" in url]
	#list_singles=[html_pisen(url) for url in fns if "TP_zpevnik_komplet_singles" in url]

	list_tp_zpevniky=[]
	list_ostatni_zpevniky=[]
	list_singles=[]

	for fn in fns:
		url=html_pisen(fn)
		if fn.find("TP_zpevnik_komplet_singles")!=-1:
			list_singles.append(url)
		elif fn.find("TP_zpevnik")!=-1:
			list_tp_zpevniky.append(url)
		else:
			list_ostatni_zpevniky.append(url)



	html = """
		<h3>TP zpěvníky</h3>

		<ul>{tp_zpevniky}
		</ul>

		<h3>Ostatní zpěvníky</h3>

		<ul>{ostatni_zpevniky}
		</ul>

		<h3>Singles</h3>

		<ul>{singles}
		</ul>
	""".format(
		tp_zpevniky="".join(list_tp_zpevniky),
		ostatni_zpevniky="".join(list_ostatni_zpevniky),
		singles="".join(list_singles),
	)

	with open('index_template.html') as f:
		content = f.read()

	print(content.replace("##zpevniky##",html))
