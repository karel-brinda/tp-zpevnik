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

def cb_list():
	return os.path.join(cache_dir(),"_list.tex".format(chordbook))

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
		xelatex_command = """xelatex -interaction nonstopmode -include-directory "{dir}" -aux-directory "{dir}" -output-directory "{dir}" "{texfile}" """.format(
				dir=os.path.basedir(xelatex_file),
				texfile=xelatex_file,
			)
	else:
		xelatex_command = """
			cd "{dir}"
			xelatex -interaction nonstopmode "{texfile}"
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
		os.path.join("tpcb","template.tex"),
	output:
		cb_tex(),
		cb_list(),
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
		with open(output[0],"w+",encoding="utf-8") as f:
			main_tex = os.linesep.join(["\\def\\{}{{}}".format(x) for x in options])+"\n"
			main_tex += "\\def\\RHEAD{{{}}}\n".format(RHEAD)
			main_tex += "\\def\\LHEAD{{{}}}\n".format(LHEAD)
			try:
				main_tex += "\\def\\FRONTCOVER{{{}}}\n".format(os.path.basename(cover_front))
			except NameError:
				pass
			try:
				main_tex += "\\def\\BACKCOVER{{{}}}\n".format(os.path.basename(cover_back))
			except NameError:
				pass
			main_tex += "\n\input{template.tex}\n"
			f.write(main_tex)
		with open(output[1],"w+",encoding="utf-8") as f:
			list_tex = os.linesep.join(
					["\input {{{}}}".format(os.path.relpath(sc_tex(x),cache_dir()))
						for x in songs_dict.keys()]
				)
			f.write(list_tex)
		shutil.copyfile(os.path.join("tpcb","template.tex"),os.path.join(cache_dir(),"template.tex"))
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
