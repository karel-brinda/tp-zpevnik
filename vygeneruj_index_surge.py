#! /usr/bin/env python3

import sys
import subprocess
import locale

try:
	locale.setlocale(locale.LC_ALL,'czech')
except:
	locale.setlocale(locale.LC_ALL,'cs_CZ.UTF-8')


cmd='cd output && find . -type f -name "*.pdf" | grep -v "muj_novy_zpevnik"'
				   
def html_pisen(fn):
	fn=fn.replace("./","")
	return '\n\t<li><a href="{url}">{name}</a></li>'.format(
			url=fn,
			name=fn.replace("TP_zpevnik_komplet_singles/",""),
		)

if __name__ == '__main__':
	res=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.read()
	fns=str(res)
	fns=fns.split()

	fns = sorted(fns, key=locale.strxfrm)

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
