# TP zpěvník
<!-- vim-markdown-toc GFM -->

<!-- vim-markdown-toc -->


[![CI](https://github.com/karel-brinda/tp-zpevnik/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/karel-brinda/tp-zpevnik/actions/workflows/ci.yml)



Repozitář obsahuje podklady pro sazbu TP zpěvníků a příbuzných variant. Jsou zde historické i novější edice,
například `TP2011`, `TP2012`, `TP2013`, `TP2015 (neoficiální)`, `TP2016`, `TP2017` a `TP2020`, plus pomocné
`Snakefile.*` konfigurace pro vlastní varianty. Vygenerovaný web je publikován na
[brinda.eu/tp-zpevnik](https://brinda.eu/tp-zpevnik).

Co tento systém umožňuje:
* Sestavit existující zpěvníky.
* Opravit chyby v písních nebo sazbě.
* Vytvořit si vlastní zpěvník na bázi TP zpěvníků.
* Transponovat jednotlivé písně do jiné tóniny.

## Jak je repozitář uspořádán

* `songs/` - texty a akordy písní rozdělené do 4 základních kategorií
* `Snakefile.*` - soubory definující jednotlivé zpěvníky
* `tpcb/` - společná sazební logika, LaTeX šablony a generování rejstříků
* `output/` - výstupní soubory

## Požadavky

### Prostředí

Preferované prostředí je Linux nebo macOS (build ale může fungovat i na Windows).


### Potřebný software

* Python 3 a `pip`
* [Snakemake](https://snakemake.readthedocs.io/)
* LuaLaTeX
* Git
* Česká locale pro správné řazení:
  * `cs_CZ.UTF-8`
  * případně systémový alias `czech`

Instalace pythonových závislostí:

```bash
python3 -m pip install -r requirements.txt
```

Poznámky:
* Rejstříky i pomocné generátory spoléhají na české řazení, takže bez české locale může být build chybný nebo skončí chybou.
* Pro webový výstup v `output/` jsou navíc potřeba `ghostscript` a `pdfcrop`.


## Jak sestavit zpěvníky

1. Naklonujte repozitář:

```bash
git clone https://github.com/karel-brinda/tp-zpevnik
cd tp-zpevnik
```

2. Nainstalujte Python závislosti:

```bash
python3 -m pip install -r requirements.txt
```

3. Ujistěte se, že máte aktivní českou locale, například:

```bash
export LANG=cs_CZ.UTF-8
export LC_ALL=cs_CZ.UTF-8
```

4. Sestavte požadovaný zpěvník:

```bash
snakemake -p -s Snakefile.TP2011 --cores all
```

Výstup vznikne v `output/`, například `output/TP_zpevnik_2011.pdf`.

### Sestavení více zpěvníků

Všechny `Snakefile.*` konfigurace lze spustit například jako:

```bash
make -j
```

Celá kompilace všech zpěvníků trvá na běžném notebooku zhruba 20s:
```
$ time ((make -j 2>&1) >/dev/null)

real	0m18.255s
user	1m28.758s
sys	0m16.914s
```


## Webový výstup

Webový výstup se generuje z PDF souborů v adresáři `output/`. Po sestavení zpěvníků stačí spustit:

```bash
make -C output
```

Tím vznikne:
* ořezaná PDF `*.tablet.pdf`
* `output/index.html`
* `output/Snakefile.sablona`


## Jak opravit chybu v písni

### Jednodušší varianta

Opravte soubor přímo přes webové rozhraní GitHubu a vytvořte pull request.

### Preferovaná varianta

1. Vytvořte si fork repozitáře [karel-brinda/tp-zpevnik](https://github.com/karel-brinda/tp-zpevnik).
2. Naklonujte svůj fork:

```bash
git clone https://github.com/<vase-username>/tp-zpevnik
cd tp-zpevnik
```

3. Opravte chyby.
4. Otestujte, že se příslušný zpěvník správně přeloží a že výsledek vypadá po vysázení správně.
5. Odešlete změny:

```bash
git add jmeno_upraveneho_souboru_1.tex jmeno_upraveneho_souboru_2.tex
git commit -m "Krátký popis změny"
git push
```

6. Otevřete pull request na GitHubu.

## Jak přidat novou píseň

Postupujte obdobně jako při opravě chyby. Dodržujte, prosím, logiku celého zpěvníku:

1. **Pojmenujte píseň**
      * Vzor: `Cele_Jmeno_Interpreta____Jmeno_pisne.tex`.
      * Jestliže se jiná píseň od interpreta ve zpěvníku už vyskytuje, ověřte, že je jeho jméno v přesně stejné formě.
      * V případě nejistoty si ověřte křestní jméno nebo pravopis na Google.
      * Jména písní by měla velké jen první písmeno a pak tam, kde patří podle jiných pravidel (vlastní jména, anglické dny v týdnu a mě
síce apod.)
      * Dodržujte přesně čtyři podtržítka mezi jménem interpreta a názvem písně.
3. **Vložte text**
      * České písně by měly mít texty psané jako celé věty včetně kompletní interpunkce, zalámané do veršů.
      ***** Písničky v angličtině a několika dalších jazycích mají velké písmeno na začátku každé řádky a interpunkce na jejich koncích (kromě té se speciálním významem), včetně tečky na konci věty, se ruší.
      ***** Zkontrolujte překlepy v textovém editoru nebo pomocí LLM.
      * "Sólo", "předehra" / "intro", "mezihra" a podobné nepotřebují text a vlastní `\zs ... \ks` (výjimkou je sloka nahrazená sólem beze zpívá
ní). Stačí v odpovídajícím místě napsat řadu akordů s prázdným textem.
4. **Vložte akordy**
      * Do jedné značky `<...>` vkládejte právě jeden akord (jinak program ohlásí neznámý formát akordové značky)
      * Ověřte správnost akordů a jejich umístění nad začátky slabik.
      * Pro všechny písně včetně anglických používejte české značení akordů (t.j., A#=B, A##=H, B# = H).
       * Mollové akordy zapisujte jako `Ami`, `Dmi7` apod.
5. **Zpěvník znovu přeložte** a **vizuálně zkontrolujte** výsledek
6. **Pokud píseň přetéká** na druhou stránku, postupujte následovně:
      * Pokud přetéká jen o několik řádků, zkuste ji zkrátit nebo přeskládat tak, aby se vešla na jednu A4 celá
      * Sekvenci akordů, které se v průběhu písně nebo v jejích částech opakuje v přesně stejném sledu, stačí napsat jen jednou.
      * Řádky od druhé sloky dále pospojovat po dvou nebo po celých slokách.
      * Zkrátit opakovaný text pomocí repetic `/: ... :/` nebo tří teček, refrény vynechat.
      * Vynechat od druhé sloky dále výplně jako u Zítra ráno v pět nebo u Milionáře od Nohavici.
      * Když se vtěsnat na jednu stránku nepovede, využijte dobře prostor obou stránek. Je možno i ponechat na výběr dvě verze (viz Veličenstvo Kat)



## Jak vytvořit vlastní zpěvník

Nejjednodušší je vyjít ze `Snakefile.test` nebo si nechat vygenerovat šablonu:

```bash
python3 vygeneruj_novy_zpevnik.py > Snakefile.muj
```

Minimální vlastní `Snakefile.muj` může vypadat takto:

```python
# -*-coding: utf-8 -*-

left_page_head = "Levá hlavička"
right_page_head = "Pravá hlavička"
chordbook = "muj_novy_zpevnik"

options = [
    "ONESIDE",
]

songs = [
    ("songs/03_zahranicni/Beatles____Let_it_be.tex", 5),
    "songs/03_zahranicni/Beatles____Love_me_do.tex",
]

include: "tpcb/include.smk"


rule all:
    input:
        run(),
```

Pak spusťte:

```bash
snakemake -p -s Snakefile.muj --cores all
```

Hlavní výstup bude v:

```text
output/muj_novy_zpevnik.pdf
```

### Jednotlivé písně jako samostatná PDF

Pokud chcete vygenerovat i jednotlivé písně zvlášť, přidejte do `options` položku `"SINGLES"`:

```python
options = [
    "SINGLES",
    "ONESIDE",
]
```

Pak vzniknou i soubory v adresáři:

```text
output/muj_novy_zpevnik_singles/
```


## Přehled značek

* `\zp{jméno písně}{autor písně nebo interpret}`: začátek písně
* `\kp`: konec písně
* `\zr`: začátek refrénu
* `\kr`: konec refrénu
* `\zs`: začátek sloky
* `\ks`: konec sloky
* `<Dmi>Text`: akord nad následujícím textem

## Poznámky

* Pořadí písní i rejstříků je citlivé na správně nastavenou českou locale.

## Podobné zpěvníky

* [VOC songbook](https://github.com/ababaian/VOCsongbook)
