rule All:
	input:
		"_TP_zpevnik_komplet.pdf",
		"_TP_zpevnik_2011.pdf",
		"_TP_zpevnik_2012.pdf",
		"_TP_zpevnik_2013.pdf",
		"_TP_zpevnik_2015.pdf",
		"_TPBAND_zpevnik.pdf"

rule AllSongs:
	output:
		"_TP_zpevnik_komplet.pdf"
	shell:
		"snakemake -s Snakefile.AllSongs"

rule TP2011:
	output:
		"_TP_zpevnik_2011.pdf"
	shell:
		"snakemake -s Snakefile.TP2011"


rule TP2012:
	output:
		"_TP_zpevnik_2012.pdf"
	shell:
		"snakemake -s Snakefile.TP2012"

rule TP2013:
	output:
		"_TP_zpevnik_2013.pdf"
	shell:
		"snakemake -s Snakefile.TP2013"

rule TP2015:
	output:
		"_TP_zpevnik_2015.pdf"
	shell:
		"snakemake -s Snakefile.TP2015"

rule TPBAND:
	output:
		"_TPBAND_zpevnik.pdf"
	shell:
		"snakemake -s Snakefile.TPBAND"

