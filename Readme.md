# TP zpěvník
[![Build Status](https://travis-ci.org/karel-brinda/tp-zpevnik.svg?branch=master)](https://travis-ci.org/karel-brinda/tp-zpevnik)

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
	./zkompiluj_vse_seriove.sh
	```

	Pokud chcete sestavit pouze některý zpěvník, např. z TP 2011, zadejte
	```bash
	snakemake -s Snakefile.TP2011
	```

	Obdobně pro ostatní zpěvníky.

## Jak opravit chybu v písni

### Jednodušší varianta

Opravte soubor přímo přes webové rozhraní GitHubu (musíte být ale přihlášeni). Pak mi zašlete pull request.

### Složitější varianta (ale preferovaná)

1.	Vytvořte vlastní fork repozitáře http://github.com/karel-brinda/tp-zpevnik (ve web gui klikněte na tlačítko "fork" vpravo nahoře).

2.	Naklonujte zpěvník ze svého nového repozitáře (vzniklého forknutím) včetně externích repozitářů (soubory v nich modifikovat nebudete, pro ty tedy fork vytvářet nemusíte).
	```bash
	git clone --recursive http://github.com/<vase-username-na-githubu>/tp-zpevnik
	```

3.	Opravte chyby.

4.	Otestujte, zda se zpěvník správně přeloží (a neskončí např. xelatexovou chybou). Důkladně zkontrolujte, jestli po vysázení vypadá daná píseň správně.

5.	Odešlete změny na server pomocí příkazů
	```bash
	git add jmeno_upraveneho_souboru_1.tex jmeno_upraveneho_souboru_2.tex
	git commit -m 'kratky popis zmen - co konkretne jste opravili'
	git push
	```

6.	Na GitHub.com mě požádejte mě o merge (propuštění změn do původních repozitářů – zelené tlačítko Pull request). Pokud bude změna korektní, schválím ji.

## Jak přidat novou píseň do databáze písní

Postupujte obdobným způsobem jako v minulém bodu. Místo opravy vytvořte soubor pro píseň z nějaké již existující.
Dodržujte, prosím, logiku celého zpěvníku:

1.	Pojmenujte píseň podle vzoru `Celé_Jméno_Interpreta____Jméno_písně.tex`.
	*	Jestliže se jiná píseň od interpreta ve zpěvníku už vyskytuje, ověřte, že je jeho jméno v přesně stejné formě.
	*	V případě nejistoty si ověřte křestní jméno nebo pravopis na Google.
	*	Jména písní by měla velké jen první písmeno a pak tam, kde patří podle jiných pravidel (vlastní jména, anglické dny v týdnu a měsíce apod.)
	*	Dodržujte prosím právě čtyři podtržítka mezi jménem interpreta a písně.

2.	Prosím, nekopírujte nekriticky text z jiné stránky. Minimálně si jej vložte nejdřív do textového editoru a nechte ověřit překlepy.

3.	Ověřte správnost akordů a jejich umístění nad *začátky* slabik, a to i uprostřed slov (předložky k, s, v, z slabiku nezačínají).
	*	Jestli píseň akordy ve vašem zdroji nemá uvedené, zkuste najít jiný.
	*	Zkontrolujte, jestli zdrojový text nepoužíval anglické označení *B* / *Bb* místo českého *H* / *B*. Dodržujeme striktně české, a to i v zahraničních písních.
	*	Opravte označení mollových akordů z *"Am"* na *"Ami"*. Nezapomeňte na případy *"mi7"*.

4.	"Sólo", "předehra" / "intro", "mezihra" a podobné nepotřebují text a vlastní `\zs ... \ks` (výjimkou je sloka nahrazená sólem beze zpívání). Stačí v odpovídajícím místě napsat řadu akordů s prázdným textem.

5.	České písně by měly mít texty psané jako celé věty včetně kompletní interpunkce, zalámané do veršů. Písničky v angličtině a několika dalších jazycích mají velké písmeno na začátku každé řádky a interpunkce na jejich koncích (kromě té se speciálním významem), včetně tečky na konci věty, se ruší.

6.	Po zavedení písně zpěvník přeložte a zkontrolujte, zda vypadá v pořádku a jak dlouhá se vysází. Jestli přesahuje jednu stránku jen o několik řádek, zkuste ji upravit, aby se vešla na jednu A4 celá:
	*	Sekvenci akordů, které se v průběhu písně nebo v jejích částech opakuje v přesně stejném sledu, stačí napsat jen jednou.
	*	Řádky od druhé sloky dále pospojovat po dvou nebo po celých slokách.
	*	Zkrátit opakovaný text pomocí repetic `/: ... :/` nebo tří teček, refrény vynechat.
	*	Vynechat od druhé sloky dále výplně jako u Zítra ráno v pět nebo u Milionáře od Nohavici.
	*	Když se vtěsnat na jednu stránku nepovede, využijte dobře prostor obou stránek. Je možno i ponechat na výběr dvě verze (viz Veličenstvo Kat).

## Jak vytvořit vlastní zpěvník

1.	Do adresáře, kde si chcete vlastní zpěvník vytvořit, naklonujte tento repozitář:
	```bash
	git clone --recursive http://github.com/karel-brinda/tp-zpevnik
	```

2.	Vytvořte soubor `Snakefile.muj`. Ukázkový soubor najdete pod názvem `Snakefile.test`. Ilustruje vložení písní Let it be a Love me do od Beatles a žádost o automatické spočítání transpozice u Let it be:
	```python
	# -*-coding: utf-8 -*-
	
	left_page_head="Levá hlavička"
	right_page_head="Pravá hlavička"
	chordbook="muj_novy_zpevnik"
	#cover_front="obalka_predni.pdf"
	#cover_back="obalka_zadni.pdf"
	
	songs=[
		("./tp-songs/03_zahranicni/Beatles____Let_it_be.tex", 5), # 5 = transpozice o 5 půltónů nahoru
		"./tp-songs/03_zahranicni/Beatles____Love_me_do.tex",
	]

	include:"tpcb/snake_incl.py"

	rule all:
		input:
			cb_pdf()
	```	

3.      Jestliže chcete písničky vysázet nezávisle na sobě jako jednotlivé 
        soubory PDF, nahraďte poslední řádku `cb_pdf()` za `singles`. Jestliže si 
        přejete vygenerovat oba výstupy, oddělte je čárkou.
	
4.	Spusťte
	```bash
	snakemake -s Snakefile.muj
	```

	Měl by se vám vysázet zpěvník `_muj_novy_zpevnik.pdf`.

### Používané značky

* ```\zp{jméno písně}{autor písně nebo interpret}``` - začátek písně
* ```\kp``` - konec písně
* ```\zr``` - začátek refrénu
* ```\kr``` - konec refrénu
* ```\zs``` - začátek sloky
* ```\ks``` - konec sloky
* ```<Dmi>Text, nad kterým bude akord``` - akord

### Poznámky

* Používejte evropskou hudební notaci (*B* = *A#*).
* Pro mollové akordy používejte *mi*, tedy např. *Ami*.
* Do jedné značky ```<...>``` vkládejte právě jeden akordy (pokud jich tam bude více, program ohlásí neznámý formát akordové značky).
