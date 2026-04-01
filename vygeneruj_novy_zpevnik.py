#! /usr/bin/env python3

import subprocess

import locale

try:
    locale.setlocale(locale.LC_ALL, 'czech')
except:
    locale.setlocale(locale.LC_ALL, 'cs_CZ.UTF-8')

cmd = "find songs -type f -name '*.tex'"

res = subprocess.Popen(cmd,
                       shell=True,
                       stdout=subprocess.PIPE,
                       universal_newlines=True).stdout.read()
fns = str(res)
fns = fns.split("\n")
fns = sorted(fns, key=locale.strxfrm)

print("""# -*-coding: utf-8 -*-
chordbook="jmeno_souboru"

options = [
 	"SKIPCHECK",
 	"ONESIDE",
]

songs=[""")

for fn in fns:
    #if fn is not None:
    if fn != "":
        print('#\t("{}",0),'.format(fn))

print("""]

include:"tpcb/include.smk"

rule all:
        input:
                run()

""")
