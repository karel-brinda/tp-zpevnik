#! /usr/bin/env python3

import snakemake
import subprocess

import locale

try:
	locale.setlocale(locale.LC_ALL,'czech')
except:
	locale.setlocale(locale.LC_ALL,'cs_CZ.UTF-8')


cmd="find tp-songs -type f -name '*.tex'"

res=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.read()
fns=str(res)
fns=fns.split("\n")
fns=sorted(fns, key=locale.strxfrm)

print("""# -*-coding: utf-8 -*-
chordbook="jmeno_souboru"

options = [
 	"SKIPCHECK",
 	"ONESIDE",
	"SINGLEPAGE",
]

songs=[""")

for fn in fns:
	#if fn is not None:
	if fn!="":
		print('#\t("{}",0),'.format(fn))

print("""]

include:"tpcb/snake_incl.py"

rule all:
        input:
                run()

""")