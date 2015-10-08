# Jestli řádek končí neuzavřenou {, schováme si ho a přidáme před zpracováním k dalšímu řádku.
# Znak konce řádku zůstane zachovaný. Pak se skript resetuje a načte další řádku.
/{[^}]*/H
/{[^}]*/d
# Jestli jsme došli sem, jsme balancovaní. I nová řádka se přidá k bufferu...
H
# ...a celý buffer vezmeme za vstup.
g
# Hlavní náhrada \Ch{a}{b} -> [a]b
s/\\Ch\s*{\([^}]*\)}\s*{\([^}]*\)}/<\1>\2/g
s/\\Ch\s*{\([^}]*\)}/<\1>/g
# Několik mezer -> jedna mezera
s/ \{2,\}/ /g
# Odstraníme případný znak konce řádku na jeho začátku a vypíšeme.
s/^\n//
p
# Buffer vyprázdníme. Tohle způsobí, že před další načtenou řádkou bude řádka 
# prázdná, ale o to je postaráno o dva příkazy výš.
s/.*//g
h
# Všechno smazat a hurá zpátky na začátek.
d
