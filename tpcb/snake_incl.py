# -*-coding: utf-8 -*-

import collections
import os
import PyPDF2
import shutil
import platform
import filecmp

ruleorder:
	song_tex > main_tex

from chords import *
from index import *

def cache_dir():
	return "cache.{}".format(chordbook)

def cb_pdf():
	return "_{}.pdf".format(chordbook)

def cb_tex():
	return os.path.join(cache_dir(),"_{}.tex".format(chordbook))

def cb_idx():
	return os.path.join(cache_dir(),"_{}.idx".format(chordbook))

def cb_ind():
	return os.path.join(cache_dir(),"_{}.ind".format(chordbook))

def sc_tex(song):
	return os.path.join(cache_dir(),"0_{}.tex".format(song))


def ind_pisne():
	return cb_ind()+"_pisne"

def	ind_interpreti():
	return cb_ind()+"_interpreti"

def idx_pisne():
	return cb_idx()+"_pisne"

def idx_interpreti():
	return cb_idx()+"_interpreti"

def call_xelatex(xelatex_file):
	if platform.system()=="Windows":
		xelatex_command = """xelatex -include-directory "{dir}" -aux-directory "{dir}" -output-directory "{dir}" "{texfile}" """.format(
				dir=os.path.basedir(xelatex_file),
				texfile=xelatex_file,
			)
	else:
		xelatex_command = """
			cd "{dir}"
			xelatex "{texfile}"
			""".format(
				dir=os.path.dirname(xelatex_file),
				texfile=os.path.basename(xelatex_file),
			)
	shell(xelatex_command)

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
		cb_pdf(),
		ind_pisne(),
		idx_pisne(),
		idx_pisne()+".old",
		ind_interpreti(),
		idx_interpreti(),
	input:
		cb_tex(),
		[sc_tex(x) for x in songs_dict.keys()],
		workflow.snakefile,
	run:
		volat_xelatex_dvakrat=False
		xelatex_zavolan=0

		if not os.path.isfile(ind_pisne()) or not os.path.isfile(ind_interpreti()):
			call_xelatex(input[0])
			udelejRejstrik(idx_pisne(),ind_pisne()); 
			udelejRejstrik(idx_interpreti(),ind_interpreti());
			shutil.copyfile(idx_pisne(),idx_pisne()+".old")
		else:
			shutil.copyfile(idx_pisne(),idx_pisne()+".old")
			udelejRejstrik(idx_pisne(),ind_pisne()); 
			udelejRejstrik(idx_interpreti(),ind_interpreti());

		call_xelatex(input[0])

		if not filecmp.cmp(idx_pisne(),idx_pisne()+".old"):
			udelejRejstrik(idx_pisne(),ind_pisne()); 
			udelejRejstrik(idx_interpreti(),ind_interpreti());
			call_xelatex(input[0])

		main_pdf=cb_tex().replace(".tex",".pdf")
		shutil.copyfile(main_pdf,os.path.basename(main_pdf))

# cache/pisen.tex, cache/pisen2.tex => zpevnik.tex
rule main_tex:
	input:
		workflow.snakefile,
		[sc_tex(x) for x in songs_dict.keys()],
	output:
		cb_tex(),
		os.path.join(cache_dir(),"songbook.sty"),
	run:
		try:
			shutil.copyfile(cover_front, os.path.join(cache_dir(),os.path.basename(cover_front)))
		except NameError:
			pass
		try:
			shutil.copyfile(cover_back, os.path.join(cache_dir(),os.path.basename(cover_back)))
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
				\usepackage{refcount}
				\usepackage[xetex,pdfpagelabels=false]{hyperref}
				\usepackage{forloop}

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
					\twopagecheck
					\global\lastsong={#1}
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

				\newcounter{insertCur}
				\newcounter{insertTotal}
				\newcommand\insertPage[2]{\shipout\vbox{\XeTeXpdffile #1 page #2 }\stepcounter{page}}
				\newcommand\countPages[1]{\setcounter{insertTotal}{\XeTeXpdfpagecount #1 }}
				\newcommand\insertPDF[1]{\countPages{#1}\stepcounter{insertTotal}
					\forloop{insertCur}{1}{\value{insertCur} < \value{insertTotal}}{%
						\insertPage{#1}{\value{insertCur}}}}

				\newcounter{lastpage}
				\newcounter{numpages}
				\newtoks\lastsong
				\newcommand\twopagecheck{%
				  \unless\ifdefined\ONESIDE
						\setcounter{numpages}{\value{page}}
						\addtocounter{numpages}{-\value{lastpage}}
						\ifnum\value{numpages}>2
							\errmessage{^^J Píseň "\the\lastsong" má víc dvě stránky.^^J Enter = pokračovat, X = přerušit.^^J}
						\else\ifnum\value{numpages}>1
						  \unless\ifodd\value{page}
							  \errmessage{^^J Píseň "\the\lastsong" začala na pravé a skončila na levé straně.^^J Enter = pokračovat, X = přerušit.^^J}
							\fi\fi
						\fi
						\setcounter{lastpage}{\value{page}}
					\fi
				}

				\newcommand\emptyPage{\shipout\vbox to \vsize{\hbox to \hsize{}}\stepcounter{page}}

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
				# Pokud přední obálka existuje, vloží ji a jednu nebo dvě volné strany za ni (mimo ONESIDE),
				# aby první stránka zpěvníku vyšla napravo
				open(cover_front,'rb')
				main_tex += "\insertPDF{"+os.path.basename(cover_front)+"}\n"
				if not "ONESIDE" in options:
					main_tex += r"""
					\emptyPage
					\ifodd\value{page}\emptyPage\fi
					"""
			except NameError:
				pass
			main_tex += os.linesep.join(
					["\input {{{}}}".format(os.path.relpath(sc_tex(x),cache_dir()))
						for x in songs_dict.keys()]
				) + r"""
				\twopagecheck

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
				# Vložit jednu nebo dvě prázdné stránky tak, aby poslední strana zadní obálky (pokud existuje)
				# vyšla nalevo (mimo ONESIDE)
				if not "ONESIDE" in options:
					main_tex += r"""
					\emptyPage
					\countPages{"""+os.path.basename(cover_back)+r"""}
					\addtocounter{insertTotal}{\value{page}}
					\ifodd\value{insertTotal}\emptyPage\fi
					"""
				main_tex += "\insertPDF{"+os.path.basename(cover_back)+"}\n\n"
			except NameError:
				pass
			main_tex += "\end{document}";
			f.write(main_tex)
			shutil.copyfile(os.path.join("tpcb","songbook.sty"),os.path.join(cache_dir(),"songbook.sty"))

# o1/pisen.tex   =>  cache/pisen.tex
# o2/pisen2.tex  =>  cache/pisen2.tex
rule song_tex:
	output:
		sc_tex("{song}"),
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
