# Použití:
#   make ... přeloží všechny zpěvníky (sériově)
#   make test ... přeloží Snakefile.test
#   make TP2011 TP2012 ... přeloží TP2011 a TP2012
#   make clean ... smaže všechny vygenerované soubory

Zpevniky = $(patsubst Snakefile.%,%,$(wildcard Snakefile.*))

.PHONY:	all clean cleanall $(Zpevniky)

all:	$(Zpevniky)

$(Zpevniky):
	snakemake -s Snakefile.$@ --cores

clean:
	rm -fr output/*

