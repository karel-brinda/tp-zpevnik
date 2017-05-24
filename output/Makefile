.PHONY: all clean orizni surge

SHELL=/usr/bin/env bash -o pipefail -c
ZPEVNIKY=$(shell find . -name "*.pdf" | grep -v tablet)
ZPEVNIKY_T=$(patsubst %.pdf,%.tablet.pdf,$(ZPEVNIKY))

.SECONDARY:

all: orizni index.html Snakefile.sablona

orizni: $(ZPEVNIKY_T)

%.tablet.pdf: %.pdf
	set -x;\
	tmp=$$(mktemp -d);\
	cp $< $${tmp}/1.pdf;\
	(\
	cd $$tmp;\
	pdfcrop --margins '0 -25 0 0' 1.pdf 2.pdf;\
	/usr/bin/env gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -sOutputFile=3.pdf 2.pdf;\
	);\
	cp $${tmp}/3.pdf $@;

surge: orizni index.html Snakefile.sablona
	surge -d tp-zpevnik.surge.sh

Snakefile.sablona:
	p=$$(pwd) && cd .. && ./vygeneruj_novy_zpevnik.py > $$p/$@

index.html:
	p=$$(pwd) && cd .. && ./vygeneruj_index_surge.py > $$p/$@

clean:
	rm -f *.tablet.pdf index.html

