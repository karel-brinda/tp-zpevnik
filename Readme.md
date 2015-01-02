# TP zpěvník

Na tomto místě naleznete podklady k sestavení TP zpěvníků z let 2011 – 2013.

Co tento systém umožňuje:
*	Sestavit existující TP zpěvníky.
*	Opravit případné chyby.
*	Vytvořit si vlastní zpěvník na bázi TP zpěvníku (s libovolnými vlastními písněmi).
*	Jednoduše transponovat jednotlivé písně do jiné tóniny.

## Základní informace

Od roku 2011 jsou TP zpěvníky sázeny v LaTeXu způsobem, jakým se obvykle připravují např. diplomové práce nebo knihy.

Tento githubový repozitář poskytuje jednotný přístup k těmto zpěvníkům a všem jejich zdrojovým datům. Původní způsob sázení byl sice mírně odlišný, ale výsledek by měl být téměř totožný.

## Vyžadovaný software

* **Podporovaný OS**
  * Linux – vše funguje bez problémů
  * MacOS – zatím netestováno, vše by mělo fungovat bez problémů
  * Windows – překlad ve Windows je zatím možný pouze z prostředí Cygwin
*	**Python 3** (včetně programu **easy_install**) – nejjednodušší instalace je pravděpodobně v rámci balíku Anacoda (k dispozici pro Windows i Linux)
  *	**Balík pypdf2**, nainstalovat lze např. příkazem
  ```
    easy_install-3 pypdf2
  ```
  * **Snakemake** – program podobný Make s mnohem většími možnostmi, který je postaven na Pythonu, slouží k sestavení celého zpěvníku. Nainstalujete ho pomocí
  ```
    easy_install-3 snakemake
  ```
*	**XeLaTeX** – stačí mít standardně nainstalovaný TeX (v případě Windows MikTex, v případě Linuxu standardní latexové balíčky z repozitáře)
*	**GIT** – program pro práci s repozitáři zdrojových kódů, pro všechny OS k dispozici na …

## Organizace repozitářů

Samotné písně naleznete v adresáři *tp-songs*, který dále obsahuje 4 podadresáře podle skupin písní v TP zpěvnících (obdobná logika jako v modré Já písničce).

## Jak sestavit zpěvníky

1.	V konzoli přejděte do adresáře, ve kterém chcete pracovat.
2.	Stáhněte aktuální verzi zpěvníku příkazem
    ```
    git clone http://github.com/karel-brinda/tp-zpevnik
    ```
3.	Přejděte do adresáře zpěvníku pomocí
```
  cd tp-zpevnik
```
4.	Inicializujte a stáhněte externí repozitáře (obsahují obálky zpěvníků a pak vlastní skripty pro sestavování zpěvníků) pomocí
```
  git submodule init
  git submodule update
```
Nyní byste měli mít k dispozici všechny potřebné soubory.
5.	Celé sestavení provedete zadáním příkazu
```
  snakemake
```
Pokud chcete sestavit pouze některý zpěvník z TP 2011, zadejte
```
  snakemake –s tp2011.snakemake
```
Obdobně pro ostatní zpěvníky.

## Jak opravit chybu v písni

1.	Vytvořte vlastní fork repozitáře http://github.com/karel-brinda/tp-zpevnik.
2.	Naklonujte zpěvník ze svého nového repozítáře (vzniklého forknutím) včetně externích repozitářů (soubory v nich modifikovat nebudete, pro ty tedy fork vytvářet nemusíte).
3.	Opravte chyby.
4.	Otestujte, zda se zpěvník správně přeloží (a neskončí např. xelatexovou chybou). Důkladně zkontrolujte, jestli po vysázení vypadá daná píseň správně.
5.	Odešlete změny na server pomocí příkazů
```
git add jmeno_upraveneho_souboru_1.tex jmeno_upraveneho_souboru_2.tex
git commit –m 'kratky popis zmen – co konkretne jste opravili'
git push
```
6.	Na GitHub.com mě požádejte mě o merge (propuštění změn do původních repozitářů). Pokud bude změna korektní, schválím ji.

## Jak přidat novou píseň do databáze písní

Postupujte obdobným způsobem jako v minulém bodu. Místo opravy vytvořte soubor pro píseň z nějaké již existující.
Dodržujte, prosím, logiku celého zpěvníku (co se týče pojmenování a zařazení do kategorií).

## Jak vytvořit vlastní zpěvník

 1. Do adresáře, kde si chcete vlastní zpěvník vytvořit, naklonujte tyto dva repozitáře:
```
  git clone http://github.com/karel-brinda/tpcb
  git clone http://github.com/karel-brinda/tp-zpevnik
```
 2. První bude obsahovat potřebné skripty, druhý již zpracované písně. Nyní vytvořte soubor Snakefile s následujícím obsahem:

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
 3. Spusťte ```snakemake```

Měl by se vám vysázet zpěvník s písní Let it be transponovanou o 5 půltóny nahoru a s písní Love me do.

### Používané značky

* ```\zp{jméno písně}{autor písně nebo interpret}``` - začátek písně
* ```\kp``` - konec písně
* ```\zr``` - začátek refrénu
* ```\kr``` - konec refrénu
* ```\zs``` - začátek sloky
* ```\ks``` - konec sloky
* ```\ch{Dmi}{Text, nad kterým bude akord}``` - akord

### Poznámky

* Používejte evropskou hudební notaci (*B* = *A#*).
* Mollové akordy používejte *mi*, tedy např. *Ami*
* Do jedné značky ```\ch``` vkládejte právě jeden akordy (pokud jich tam bude více, pravděpodobně nebude správně fungovat transpozice)
