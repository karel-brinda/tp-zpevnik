#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
from functools import *

try:
	locale.setlocale(locale.LC_ALL,'czech')
except:
	locale.setlocale(locale.LC_ALL,'cs_CZ.UTF-8')

##
## KONFIGURACE
##

#vstupni_pisne="zpevnik.idx_pisne"
#vystupni_pisne="zpevnik.ind_pisne"

#vstupni_interpreti="zpevnik.idx_interpreti"
#vystupni_interpreti="zpevnik.ind_interpreti"

##
## REJSTRIKY
##

def zaznamy2tex(zaznamy):
	tex = "\\begin{theindex}\n"
	
	predchoziPismeno="42"
	predchoziZ1="42"
	
	for z in zaznamy:
	
		Z1 = z[0]
		Z2 = z[1]
		strana = z[2]
		
		novePismeno = Z1[0]
	
		# nove prvni pismeno
		if novePismeno!=predchoziPismeno:
			tex += "\n\indexspace\n\n"
		
		# 2level/3level
		
		if Z2 == "":
			tex += "\item "+Z1+", "+strana+"\n"
		else:
			if Z1 != predchoziZ1:
				tex += "\item "+Z1+"\n"
			tex += "\subitem "+Z2+", "+strana+"\n"
			
		predchoziPismeno = novePismeno
		predchoziZ1 = Z1
		
	
	tex += "\n\\end{theindex}\n"
	
	return tex


def udelejRejstrik(vstup, vystup):
	vs = open(vstup, encoding='utf-8')
	zaznamy = []
	
	for line in vs:
		if line.strip()=="":
			break
	
		zaznam=["","",""]
		
		rozp = line.split("}{")
		strana = rozp[1].strip()
		strana = strana.replace("}","")
		zac = rozp[0] 
	
		zac = zac.replace("\\indexentry {","")
		
		zac = zac.split("!")
		
		zaznam[0]=zac[0]
		
		try:
			zaznam[1]=zac[1]
		except IndexError:
			pass
	
		zaznam[2]=strana
		
		zaznamy.append(zaznam)
		
	zaznamy = sorted(zaznamy, key = lambda zaznam: locale.strxfrm(zaznam[0].ljust(100)+zaznam[1]))
	#(key=cmp_to_key(locale.strcoll))
	vs.close()
	
	vys = open(vystup,"w+", encoding='utf-8')
	vys.write(zaznamy2tex(zaznamy))
	vys.close()

#udelejRejstrik(vstupni_pisne,vystupni_pisne)
#udelejRejstrik(vstupni_interpreti,vystupni_interpreti)
