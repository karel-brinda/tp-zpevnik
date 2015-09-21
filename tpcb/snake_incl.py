# -*-coding: utf-8 -*-

import collections
import os
import PyPDF2
import shutil
import platform

ruleorder:
	song_tex > main_tex

from chords import *
from index import *

def cache_dir():
	return "cache.{}".format(chordbook)

def cb_pdf():
	return "_{}.pdf".format(chordbook)

#def empty_tex():
#	return os.path.join(cache_dir(),"empty.tex")
#
#def empty_pdf():
#	return os.path.join(cache_dir(),"empty.pdf")

def cb_tex():
	return os.path.join(cache_dir(),"_{}.tex".format(chordbook))

def cb_idx():
	return os.path.join(cache_dir(),"_{}.idx".format(chordbook))

def cb_ind():
	return os.path.join(cache_dir(),"_{}.ind".format(chordbook))

def sc_tex(song):
	return os.path.join(cache_dir(),"0_{}.tex".format(song))


#####
##### SETTING ALL PARAMS
#####

try:
	LHEAD=left_page_head
except NameError:
	LHEAD=""
try:
	RHEAD=right_page_head
except NameError:
	RHEAD=""

try:
	options=options
except NameError:
	options=[]

songs_prop = []
for x in songs:
	# no transposition
	if isinstance(x,str):
		songs_prop.append((
			x,
			0,
			os.path.basename(x).replace(".tex","")
		))
	# transposition ... must be a list
	else:
		songs_prop.append((
			x[0],
			int(x[1]),
			os.path.basename(x[0]).replace(".tex","")
		))

songs_dict = OrderedDict(
				[
					(x[2],x[0]) for x in songs_prop
				]
			)

songs_dict_transp = OrderedDict(
				[
					(x[2],x[1]) for x in songs_prop
				]
			)

# zpevnik.tex => zpevnik.pdf
rule main_pdf:
	output:
		cb_pdf()
	input:
		#empty_pdf(),
		cb_tex(),
		[sc_tex(x) for x in songs_dict.keys()],
		workflow.snakefile,
	run:
		#empty_page=input[0]

		if platform.system()=="Windows":
			print("WINDOWS")
			xelatex_command = """xelatex -include-directory "{dir}" -aux-directory "{dir}" -output-directory "{dir}" "{texfile}" """.format(
					dir=cache_dir(),
					texfile=cb_tex(wildcards.file),
				)
		else:
			xelatex_command = """
				cd "{dir}"
				xelatex "{texfile}"
				""".format(
					dir=cache_dir(),
					texfile=os.path.relpath(cb_tex(),cache_dir()),
				)

		#if not os.path.isfile(cb_ind()+"_pisne") or not os.path.isfile(cb_ind()+"_interpreti"):
		ind_pisne=cb_ind()+"_pisne"
		ind_interpreti=cb_ind()+"_interpreti"
		idx_pisne=cb_idx()+"_pisne"
		idx_interpreti=cb_idx()+"_interpreti"
		if (not os.path.isfile(ind_pisne) or not os.path.isfile(ind_interpreti)) or \
		(os.path.getmtime(ind_pisne) < os.path.getmtime(workflow.snakefile)):
			shell(xelatex_command)

		#udelejRejstrik(cb_idx()+"_pisne",cb_ind()+"_pisne"); 
		#udelejRejstrik(cb_idx()+"_interpreti",cb_ind()+"_interpreti"); 
		udelejRejstrik(idx_pisne,idx_pisne);
		udelejRejstrik(idx_interpreti,ind_interpreti);

		shell(xelatex_command)
		main_pdf=cb_tex().replace(".tex",".pdf");
		os.rename(main_pdf, os.path.basename(main_pdf));
		
#		main_pdf=cb_tex().replace(".tex",".pdf")
#		merger = PyPDF2.PdfFileMerger()
#
#		# 0
#		try:
#			p=PyPDF2.PdfFileReader(open(cover_front,'rb'))
#			cover_front_pages = p.getNumPages()
#			merger.append(PyPDF2.PdfFileReader(open(cover_front, 'rb')))
#			if cover_front_pages%2==1:
#				merger.append(PyPDF2.PdfFileReader(open(empty_page, 'rb')))
#		except NameError:
#			pass
#
#		# 1
#		main_pages = PyPDF2.PdfFileReader(open(main_pdf,'rb')).getNumPages()
#		merger.append(PyPDF2.PdfFileReader(open(main_pdf, 'rb')))
#
#		# 2
#		try:
#			p = PyPDF2.PdfFileReader(open(cover_back,'rb'))
#			cover_back_pages = p.getNumPages()
#			if (main_pages + cover_back_pages) % 2 == 1:
#				merger.append(PyPDF2.PdfFileReader(open(empty_page, 'rb')))
#			merger.append(PyPDF2.PdfFileReader(open(cover_back, 'rb')))
#		except NameError:
#			pass
#
#		merger.write(os.path.basename(main_pdf))
#
#		#shell("cp {} ./".format(cb_tex(wildcards.file).replace(".tex",".pdf")))
#		# count = countPages(cb_tex(wildcards.file).replace(".tex",".pdf"))
#		p = PyPDF2.PdfFileReader(open(cb_tex().replace(".tex",".pdf"),"rb"))
#		#print("COUNT ",p.getNumPages())

# cache/pisen.tex, cache/pisen2.tex => zpevnik.tex
rule main_tex:
	input:
		workflow.snakefile,
		[sc_tex(x) for x in songs_dict.keys()],
	output:
		cb_tex()
	run:
		try:
			shutil.copy(cover_front, os.path.join(cache_dir(),os.path.basename(cover_front)))
		except NameError:
			pass
		try:
			shutil.copy(cover_back, os.path.join(cache_dir(),os.path.basename(cover_back)))
		except NameError:
			pass
		# todo: only filename
		with open(output[0],"w+",encoding="utf-8") as f:
			main_tex=r"""% -*-coding: utf-8 -*-
				\documentclass[11pt,a4paper{}]{{book}}""".format(",oneside" if "ONESIDE" in options else "") + \
				os.linesep.join(["\\def\\{}{{}}".format(x) for x in options]) \
				+ r"""
				\usepackage[czech]{babel}
				\usepackage{pdfpages}
				\usepackage{fancyhdr}
				\usepackage{fontspec}
				\usepackage[chordbk]{songbook}
        \usepackage[xetex,pdfpagelabels=false]{hyperref}
        \usepackage{refcount}

				\usepackage{index}
				\newindex[cisloPisne]{default}{idx_pisne}{ind_pisne}{Rejstřík písní}
				\newindex[cisloPisne]{interpreti}{idx_interpreti}{ind_interpreti}{Rejstřík interpretů}

				\selectlanguage{czech}

				\newcounter{cisloPisne}
				\newcommand\cisloPisne{\arabic{cisloPisne}}

				\newcommand\zp[2]{
					\stepcounter{cisloPisne}
          \label{pis.\cisloPisne}
					\begin{song}{#1}{}{}{}{#2}{}
					\index{#1}
					\index[interpreti]{#2!#1}
				}
				\newcommand\kp{\end{song}}
				\newcommand\zs{\begin{SBVerse}}
				\newcommand\ks{\end{SBVerse}}
				\newcommand\zr{\begin{SBChorus}}
				\newcommand\kr{\end{SBChorus}}

				\renewcommand\CpyRt{}
				\renewcommand\SBChorusTag{R:}
				\renewcommand\SBBaseLang{Czech}
				\renewcommand\SBUnknownTag{}
				\renewcommand\SBWAndMTag{}

				%\DeclareOption{compactallsongs}{\CompactAllModetrue}

				%%%
				% nejaky blbosti, vypinam, co se da
				%%%
				\font\myTinySF=cmss8 at 8pt
				\renewcommand{\CpyRt}{}
				\renewcommand{\SBRef}{}
				\renewcommand{\SBIntro}{}
				\renewcommand{\SBExtraKeys}{}

				%%%
				% Hlavicky
				%%%

				\ifdefined\NOHEADER
					\pagestyle{empty}
				\else
					\pagestyle{fancy}
					\fancyhead[RE]{""" + RHEAD + r"""}
					\fancyhead[LO]{""" + LHEAD + r"""}
					\fancyhead[RO]{}
					\fancyhead[LE]{}
					\fancyfoot{}
				\fi

				\begin{document}

				%%%
				% Uncomment "\maketitle" statement to make a title page.
				%%%
				%\maketitle

				\mainmatter
				\ifWordBk
				  \twocolumn
				\fi

				\setcounter{page}{0}
			"""
			try:
				# Pokud přední obálka existuje, vloží ji a volnou stranu za ni (mimo ONESIDE)
				# Předpokládá automaticky, že obálka má jen jednu stranu
				open(cover_front,'rb')
				main_tex += "\\shipout\\vbox{\XeTeXpdffile "+os.path.basename(cover_front)+" }\stepcounter{page}\n"
				if "ONESIDE" in options:
					main_tex += "\n"
				else:
					main_tex += "\\shipout\\vbox to \\vsize{\\hbox to \\hsize{}}\stepcounter{page}\n\n"
			except NameError:
				pass
			main_tex += os.linesep.join(
					["\input {{{}}}".format(os.path.relpath(sc_tex(x),cache_dir()))
						for x in songs_dict.keys()]
				) + r"""

				%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
				%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
				%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


				% rejstrik podle interpretu
				\fancyfoot{}
				\printindex[interpreti]
				% rejstrik podle pisni
				\fancyfoot{}
				\printindex

			"""
			try:
				open(cover_back,'rb')
				# Vložit jednu nebo dvě prázdné stránky tak, aby zadní obálka (pokud existuje) přišla nalevo (mimo ONESIDE)
				if not "ONESIDE" in options:
					main_tex += "\\ifodd\\value{page}\\shipout\\vbox to \\vsize{\\hbox to \\hsize{}}\stepcounter{page}\\fi\n"
					main_tex += "\\shipout\\vbox to \\vsize{\\hbox to \\hsize{}}\stepcounter{page}\n"
				main_tex += "\\shipout\\vbox{\XeTeXpdffile "+os.path.basename(cover_back)+" }\n\n"
			except NameError:
				pass
			main_tex += "\end{document}";
			f.write(main_tex)
			shutil.copyfile(os.path.join("tpcb","songbook.sty"),os.path.join(cache_dir(),"songbook.sty"))
			#shell("cp tpcb/songbook.sty {}".format(cache_dir()))
# o1/pisen.tex   =>  cache/pisen.tex
# o2/pisen2.tex  =>  cache/pisen2.tex
rule song_tex:
	output:
		sc_tex("{song}")
	input:
		lambda wildcards: songs_dict[wildcards.song],
		workflow.snakefile
	run:
		song=""
		song2=""
		with open(input[0],"r",encoding="utf-8") as f:
			song=f.read()
			song2=transposition_song(song,songs_dict_transp[wildcards.song])
		with open(output[0],"w+",encoding="utf-8") as f:
			f.write(song2)
		#shell("cp {} {}".format(input[0],output[0]))

#rule empty_page:
#	output:
#		empty_tex(),
#		empty_pdf()
#	run:
#		with open(empty_tex(),"w+") as f:
#			f.write(r"""\documentclass[a4page]{article} 
#\begin{document}
#\thispagestyle{empty}
#~
#\end{document}
#				""")
#		#shell("xelatex \"{}\"".format(output[0]))
#		xelatex_command = """cd {dir} && xelatex "{texfile}" """.format(
#				dir=cache_dir(),
#				texfile=os.path.basename(empty_tex()),
#			)
#		shell(xelatex_command)
#		#xelatex_command = """xelatex -include-directory "{dir}" -aux-directory "{dir}" -output-directory "{dir}" "{texfile}" """.format(
#		#		dir=cache_dir(),
#		#		texfile=empty_tex(),
#		#	)
