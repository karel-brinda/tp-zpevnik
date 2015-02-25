# TP zpěvník

Na tomto místě naleznete podklady k sestavení TP zpěvníků z let 2011 – 2013. Vysázené zpěvníky naleznete na http://karel-brinda.github.io/tp-zpevnik.

Co tento systém umožňuje:
*	Sestavit existující TP zpěvníky.
*	Opravit chyby.
*	Vytvořit si vlastní zpěvník na bázi TP zpěvníku (s libovolnými vlastními písněmi).
*	Jednoduše transponovat jednotlivé písně do jiné tóniny.

## Základní informace

Od roku 2011 jsou TP zpěvníky sázeny v LaTeXu způsobem, jakým se obvykle připravují např. diplomové práce nebo knihy.

Tento githubový repozitář poskytuje jednotný přístup k těmto zpěvníkům a všem jejich zdrojovým datům. Původní způsob sázení byl sice mírně odlišný, ale výsledek by měl být téměř totožný.

## Vyžadovaný software

* **Podporovaný OS**
	* Linux
	* MacOS
	* Windows
* **Python 3** (včetně programu **pip**) – nejjednodušší instalace je pravděpodobně v rámci balíku Anacoda (k dispozici pro Windows, Linux i MacOS)
	* **Balík pypdf2**, nainstalovat lze např. příkazem

		```bash
		pip install pypdf2
		```

	* **Snakemake** (http://bitbucket.org/johanneskoester/snakemake/) – program podobný Make s mnohem většími možnostmi, který je postaven na Pythonu, slouží k sestavení celého zpěvníku. Nainstalujete ho pomocí

		```bash
		pip install snakemake
		```

*	**XeLaTeX** – stačí mít standardně nainstalovaný TeX (v případě Windows MikTex, v případě Linuxu standardní latexové balíčky z repozitáře)
*	**GIT** (http://git-scm.com/) – program pro práci s repozitáři zdrojových kódů

## Organizace repozitářů

Samotné písně naleznete v adresáři *tp-songs*, který dále obsahuje 4 podadresáře podle skupin písní v TP zpěvnících (obdobná logika jako v modré Já písničce).

## Jak sestavit zpěvníky

1.	V konzoli přejděte do adresáře, ve kterém chcete pracovat.
2.	Stáhněte aktuální verzi zpěvníku vč. dalších vyžadovaných repozitářů příkazem
	```bash
	git clone --recursive http://github.com/karel-brinda/tp-zpevnik
	```
	
3.	Přejděte do adresáře zpěvníku a sestavte všechny zpěvníky pomocí
	```bash
	cd tp-zpevnik
	snakemake
	```

	Pokud chcete sestavit pouze některý zpěvník, např. z TP 2011, zadejte
	```bash
	snakemake –s tp2011.snakemake
	```

	Obdobně pro ostatní zpěvníky.

## Jak opravit chybu v písni

### Jednodušší varianta

Opravte soubor přímo přes webové rozhraní GitHubu (musíte být ale přihlášeni). Pak mi zašlete pull request.

### Složitější varianta (ale preferovaná)

1.	Vytvořte vlastní fork repozitáře http://github.com/karel-brinda/tp-zpevnik.
2.	Naklonujte zpěvník ze svého nového repozítáře (vzniklého forknutím) včetně externích repozitářů (soubory v nich modifikovat nebudete, pro ty tedy fork vytvářet nemusíte).
3.	Opravte chyby.
4.	Otestujte, zda se zpěvník správně přeloží (a neskončí např. xelatexovou chybou). Důkladně zkontrolujte, jestli po vysázení vypadá daná píseň správně.
5.	Odešlete změny na server pomocí příkazů
	```bash
	git add jmeno_upraveneho_souboru_1.tex jmeno_upraveneho_souboru_2.tex
	git commit –m 'kratky popis zmen – co konkretne jste opravili'
	git push
	```

6.	Na GitHub.com mě požádejte mě o merge (propuštění změn do původních repozitářů). Pokud bude změna korektní, schválím ji.

## Jak přidat novou píseň do databáze písní

Postupujte obdobným způsobem jako v minulém bodu. Místo opravy vytvořte soubor pro píseň z nějaké již existující.
Dodržujte, prosím, logiku celého zpěvníku (co se týče pojmenování a zařazení do kategorií).

## Jak vytvořit vlastní zpěvník

1.	Do adresáře, kde si chcete vlastní zpěvník vytvořit, naklonujte tyto dva repozitáře:
	```bash
	git clone http://github.com/karel-brinda/tpcb
	git clone http://github.com/karel-brinda/tp-zpevnik
	```

2.	První bude obsahovat potřebné skripty, druhý již zpracované písně. Nyní vytvořte soubor Snakefile s následujícím obsahem:
	```python
	# -*-coding: utf-8 -*-
	
	left_page_head="Levá hlavička"
	right_page_head="Pravá hlavička"
	chordbook="muj_novy_zpevnik"
	#cover_front="obalka_predni.pdf"
	#cover_back="obalka_zadni.pdf"
	
	songs=[
		("tp-zpevnik/tp-songs/03_zahranicni/Beatles____Let_it_be.tex", 5), # 5 = transpozice o 5 půltónů nahoru
		"tp-zpevnik/tp-songs/03_zahranicni/Beatles____Love_me_do.tex",
	]

	include:"tpcb/snake_incl.py"

	rule all:
		input:
			cb_pdf(chordbook)
	```	
	
3.	Spusťte
	```bash
	snakemake
	```

	Měl by se vám vysázet zpěvník s písní Let it be transponovanou o 5 půltóny nahoru a s písní Love me do.

### Používané značky

* ```\zp{jméno písně}{autor písně nebo interpret}``` - začátek písně
* ```\kp``` - konec písně
* ```\zr``` - začátek refrénu
* ```\kr``` - konec refrénu
* ```\zs``` - začátek sloky
* ```\ks``` - konec sloky
* ```\Ch{Dmi}{Text, nad kterým bude akord}``` - akord

### Poznámky

* Používejte evropskou hudební notaci (*B* = *A#*).
* Mollové akordy používejte *mi*, tedy např. *Ami*.
* Do jedné značky ```\Ch``` vkládejte právě jeden akordy (pokud jich tam bude více, pravděpodobně nebude správně fungovat transpozice).
