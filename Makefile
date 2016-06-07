# Použití:
#   make ... přeloží všechny zpěvníky (sériově)
#   make test ... přeloží Snakefile.test
#   make TP2011 TP2012 ... přeloží TP2011 a TP2012
#   make clean ... smaže všechny vygenerované soubory
#   make orizni ... ořízne okraje hlavních TP zpěvníků

Zpevniky = $(patsubst Snakefile.%,%,$(wildcard Snakefile.*))

.PHONY:	all clean cleanall orizni $(Zpevniky)

all:	$(Zpevniky)

$(Zpevniky):
	snakemake -p -s Snakefile.$@ --cores

clean:
	rm -fr output/*
	rm -fr cache/*

orizni:
	@cd output && for f in TP_zpevnik_*.pdf; do g=`basename $$f .pdf` && echo "$$g" && ../orizni_zpevnik.sh "$$f" "$$g.tablet.pdf"; done;


