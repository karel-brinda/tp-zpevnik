# Použití:
#   make ... přeloží všechny zpěvníky (sériově)
#   make test ... přeloží Snakefile.test
#   make TP2011 TP2012 ... přeloží TP2011 a TP2012
#   make clean ... smaže všechny vygenerované soubory
#   make surge ... zkompiluj zpevniky a uploadni na surge.sh

Zpevniky = $(patsubst Snakefile.%,%,$(wildcard Snakefile.*))

.PHONY:	all clean cleanall orizni surge singles $(Zpevniky)

all:	$(Zpevniky)

$(Zpevniky):
	snakemake -p -s Snakefile.$@ --cores

clean:
	rm -fr cache/*
	$(MAKE) -C output

surge: $(Zpevniky) singles
	$(MAKE) -C output surge

singles:
	TRAVIS_BRANCH=surge snakemake -p -s Snakefile.AllSongs --cores
