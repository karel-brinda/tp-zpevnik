# -*-coding: utf-8 -*-

import os

# import PyPDF2
import shutil
import platform
import filecmp

from chords import *
from index import *


def cache_dir():
    return os.path.join("cache", chordbook)


def cb_pdf():
    return os.path.join("output", "{}.pdf".format(chordbook))


def cb_tex():
    return os.path.join(cache_dir(), "{}.tex".format(chordbook))


def cb_idx():
    return os.path.join(cache_dir(), "{}.idx".format(chordbook))


def cb_ind():
    return os.path.join(cache_dir(), "{}.ind".format(chordbook))


def sc_tex(song):
    return os.path.join(cache_dir(), "{}.tex".format(song))


def sc_pdf(song):
    return os.path.join("output", chordbook + "_singles", "{}.pdf".format(song))


def prepare_outputs():
    return [
        cb_tex(),
        os.path.join(cache_dir(), "_list.tex"),
        os.path.join(cache_dir(), "template.tex"),
        os.path.join(cache_dir(), "songbook.sty"),
    ] + [sc_tex(x) for x in songs_dict.keys()]


def ind_pisne():
    return cb_ind() + "_pisne"


def ind_interpreti():
    return cb_ind() + "_interpreti"


def idx_pisne():
    return cb_idx() + "_pisne"


def idx_interpreti():
    return cb_idx() + "_interpreti"


def call_xelatex(xelatex_file):
    if platform.system() == "Windows":
        xelatex_command = """xelatex -interaction nonstopmode -include-directory "{dir}" -aux-directory "{dir}" -output-directory "{dir}" "{texfile}" """.format(
            dir=os.path.basedir(xelatex_file),
            texfile=xelatex_file,
        )
    else:
        xelatex_command = """
            cd "{dir}"
            xelatex -interaction nonstopmode "{texfile}"
            """.format(
            dir=os.path.dirname(xelatex_file),
            texfile=os.path.basename(xelatex_file),
        )
    shell(xelatex_command)


def run():
    outputs = [cb_pdf()]

    if "SINGLES" in options:
        outputs.extend([sc_pdf(x) for x in songs_dict.keys()])

    return outputs


def prepare_chordbook_run(output):
    try:
        shutil.copyfile(
            cover_front, os.path.join(cache_dir(), os.path.basename(cover_front))
        )
    except NameError:
        pass
    try:
        shutil.copyfile(
            cover_back, os.path.join(cache_dir(), os.path.basename(cover_back))
        )
    except NameError:
        pass

    shutil.copyfile(
        os.path.join("tpcb", "template.tex"), os.path.join(cache_dir(), "template.tex")
    )
    shutil.copyfile(
        os.path.join("tpcb", "songbook.sty"), os.path.join(cache_dir(), "songbook.sty")
    )

    with open(output[0], "w+", encoding="utf-8") as f:
        main_tex = "\\def\\thelist{_list.tex}\n"
        main_tex += os.linesep.join(["\\def\\{}{{}}".format(x) for x in options]) + "\n"
        try:
            main_tex += "\\def\\RHEAD{{{}}}\n".format(right_page_head)
        except NameError:
            pass
        try:
            main_tex += "\\def\\LHEAD{{{}}}\n".format(left_page_head)
        except NameError:
            pass
        try:
            main_tex += "\\def\\FRONTCOVER{{{}}}\n".format(
                os.path.basename(cover_front)
            )
        except NameError:
            pass
        try:
            main_tex += "\\def\\BACKCOVER{{{}}}\n".format(os.path.basename(cover_back))
        except NameError:
            pass
        main_tex += "\n\\input{template.tex}\n"
        f.write(main_tex)

    with open(output[1], "w+", encoding="utf-8") as f:
        list_tex = os.linesep.join(
            [
                "\\input {{{}}}".format(os.path.relpath(sc_tex(x), cache_dir()))
                for x in songs_dict.keys()
            ]
        )
        f.write(list_tex)

    for song_id, song_path in songs_dict.items():
        with open(song_path, "r", encoding="utf-8") as f:
            song = f.read()
            song2 = transposition_song(song, songs_dict_transp[song_id])
        with open(sc_tex(song_id), "w+", encoding="utf-8") as f:
            f.write(song2)


def main_pdf_run(input, output):
    # Výstup je nyní v adresáři output. Pokud existuje stará verze, smažeme
    # ji, aby nemátla.
    if os.path.isfile("_{}.pdf".format(chordbook)):
        os.remove("_{}.pdf".format(chordbook))

    if not os.path.isfile(ind_pisne()) or not os.path.isfile(ind_interpreti()):
        call_xelatex(input[0])
        udelejRejstrik(idx_pisne(), ind_pisne())
        udelejRejstrik(idx_interpreti(), ind_interpreti())

    call_xelatex(input[0])

    shutil.copyfile(ind_pisne(), ind_pisne() + ".old")
    udelejRejstrik(idx_pisne(), ind_pisne())
    udelejRejstrik(idx_interpreti(), ind_interpreti())

    if not filecmp.cmp(ind_pisne(), ind_pisne() + ".old"):
        call_xelatex(input[0])

    shutil.copyfile(output[1], output[0])


def song_pdf_run(input, output):
    with open(output[1], "w+", encoding="utf-8") as f:
        main_tex = "\\def\\thelist{{{}}}\n".format(os.path.basename(input[0]))
        main_tex += "\\def\\SINGLE{}\n\\input{template.tex}\n"
        f.write(main_tex)
    call_xelatex(output[1])
    shutil.copyfile(output[2], output[0])


#####
##### SETTING ALL PARAMS
#####

try:
    options = options
except NameError:
    options = []

songs_prop = []
for i, x in enumerate(songs):
    # no transposition
    if isinstance(x, str):
        songs_prop.append(
            (x, 0, os.path.basename(x).replace(".tex", ""), "s{:04d}".format(i))
        )
    # transposition ... must be a list
    else:
        songs_prop.append(
            (
                x[0],
                int(x[1]),
                os.path.basename(x[0]).replace(".tex", ""),
                "s{:04d}".format(i),
            )
        )

songs_dict = OrderedDict([(x[3], x[0]) for x in songs_prop])

songs_dict_transp = OrderedDict([(x[3], x[1]) for x in songs_prop])


# připravit celý chordbook cache adresář najednou
rule prepare_chordbook:
    input:
        workflow.snakefile,
        os.path.join("tpcb", "template.tex"),
        os.path.join("tpcb", "songbook.sty"),
    output:
        prepare_outputs(),
    run:
        prepare_chordbook_run(output)


# zpevnik.tex => zpevnik.pdf
rule main_pdf:
    output:
        cb_pdf(),
        temp(cb_tex().replace(".tex", ".pdf")),
        temp(cb_tex().replace(".tex", ".log")),
        temp(cb_tex().replace(".tex", ".out")),
        temp(idx_pisne()),
        temp(idx_interpreti()),
        ind_pisne(),
        ind_interpreti(),
        temp(ind_pisne() + ".old"),
    input:
        prepare_outputs(),
    run:
        main_pdf_run(input, output)


# cache/pisen.tex => cache/_single_pisen.pdf
rule song_pdf:
    input:
        sc_tex("{song}"),
        os.path.join(cache_dir(), "template.tex"),
        os.path.join(cache_dir(), "songbook.sty"),
    output:
        sc_pdf("{song}"),
        os.path.join(cache_dir(), "single_{song}.tex"),
        temp(os.path.join(cache_dir(), "single_{song}.pdf")),
        temp(os.path.join(cache_dir(), "single_{song}.log")),
        temp(os.path.join(cache_dir(), "single_{song}.out")),
        temp(os.path.join(cache_dir(), "single_{song}.aux")),
    run:
        song_pdf_run(input, output)
