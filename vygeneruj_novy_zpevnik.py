#! /usr/bin/env python3

import subprocess

import locale


def set_czech_locale():
    for loc in ("czech", "cs_CZ.UTF-8", "cs_CZ.utf8"):
        try:
            locale.setlocale(locale.LC_ALL, loc)
            return
        except locale.Error:
            pass
    raise locale.Error("Czech locale is required")


set_czech_locale()

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
