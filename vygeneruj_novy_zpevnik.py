#! /usr/bin/env python3

import snakemake
import subprocess

cmd="find tp-songs -type f -name '*.tex'"

res=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.read()
fns=str(res)

print("""# -*-coding: utf-8 -*-
chordbook="jmeno_souboru"

options = [
 	"SKIPCHECK",
 	"ONESIDE",
	"SINGLEPAGE",
]

songs=[""")

for fn in fns.split("\n"):
	#if fn is not None:
	if fn!="":
		print('#\t"{}",'.format(fn))

print("""]

include:"tpcb/snake_incl.py"

rule all:
        input:
                run()

""")