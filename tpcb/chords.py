# -*-coding: utf-8 -*-

import re

tone_normalization={
    "Cb" : "H",
    "C"  : "C",
    "C#" : "C#",
    "Db" : "C#",
    "D"  : "D",
    "D#" : "D#",
    "Eb" : "D#",
    "E"  : "E",
    "Fb" : "E",
    "E#" : "F",
    "F"  : "F",
    "F#" : "F#",
    "Gb" : "F#",
    "G"  : "G",
    "G#" : "G#",
    "Ab" : "G#",
    "A"  : "A",
    "A#" : "B",
    "Bb" : "B",
    "B"  : "B",
    "B#" : "C",
    "Hb" : "B",
    "H"  : "H",
    "H#" : "C",
}

# from chords import *
# transposition_tone("Hb",3)
# transposition_chord("Hb",3)
def transposition_tone(tone,shift):
    semitones=["C","C#","D","D#","E","F","F#","G","G#","A","B","H"]
    dict_shifts=dict(
        [ [semitones[i],semitones[(i+shift) % len(semitones)]] for i in range(len(semitones)) ] +
        [ ["",""] ]
    )
    normalized_tone=tone_normalization[tone]
    return dict_shifts[normalized_tone]

def transposition_chord(chord,shift):
    semitones=tone_normalization.keys()

    if chord.find(" ")!=-1:
        raise(NotImplementedError("Unimplemented format of the chord '{}'. Chords cannot contain any spaces.".format(chord)))

    #bass tone
    if len(chord)>2 and chord[-2]=="/":
        bass_semitone=chord[-1:]
        chord=chord[:-2]
    elif len(chord)>3 and  chord[-3]=="/":
        bass_semitone=chord[-2:]
        chord=chord[:-3]
    else:
        bass_semitone=""

    if chord[:2] in semitones:
        main_semitone = chord[:2]
        middle = chord[2:]
    elif chord[:1] in semitones:
        main_semitone = chord[:1]
        middle = chord[1:]
    else:
        raise(NotImplementedError("Unimplemented format of the chord '{}'".format(chord)))

    new_chord = transposition_tone(main_semitone,shift) + middle
    if bass_semitone != "":
        new_chord += "/"+transposition_tone(bass_semitone,shift)

    return new_chord

# transposition_song("""\Ch{Cmi}{Někdy} se \Ch{Fmi}{zajikáme} \Ch{Cmi}{štěstím,}""",3)
def transposition_song(text,shift):
    lines = text.split("\n")
    for i in range(0, len(lines)):
        parts = lines[i].split("<")
        for j in range(1, len(parts)):
            right_index = parts[j].find(">")
            if right_index == -1: continue
            chord = parts[j][0:right_index]
            # Pokud je těsně za akordem mezera, ukončit jej hned, aby "visel
            # ve vzduchu" a nepřekrýval se s následujícími slovy. Toto je
            # konzistentní s akordem umístěným na konec řádky.
            if parts[j].find(" ", right_index+1) == right_index+1:
                end_index = right_index+1
                star = False
            else:
                # Pokud je v řetězci některý ze speciálních znaků \, } nebo &
                # (typicky třeba kvůli uvozovkám), ukončíme text akordu před
                # nimi.  Také mezery na konci pustíme ven.
                end_match = re.search(r"}|\\|&", parts[j])
                if end_match == None:
                    end_index = re.search("\s*$", parts[j]).start()
                    # Detekuje přerušení uprostřed slova
                    star = (end_index == len(parts[j]) and j < len(parts)-1)
                else:
                    end_index = re.search("\s*$", parts[j][:end_match.start()]).start()
                    star = False
            if end_index != -1:
                parts[j] = ("\Ch*" if star else "\Ch") + "{" + chord + "}{" + \
                    parts[j][right_index+1:end_index] + "}" + parts[j][end_index:]
            else:
                parts[j] = ("\Ch*" if star else "\Ch") + "{" + chord + "}{" + \
                    parts[j][right_index+1:] + "}"
        lines[i] = "".join(parts)
    text = "\n".join(lines)

    parts = text.split("\Ch")
    for i in range(1,len(parts)):
        #print("part", parts[i])
        mod_part=parts[i].lstrip()
        #assert parts[i][0]=="{"
        star=(parts[i][0]=="*")
        left_index=mod_part.find("{")
        right_index=mod_part.find("}")
        original_chord=mod_part[left_index+1:right_index].strip()
        #print("original chord", original_chord)
        assert original_chord.find("\\")==-1,"Chord '{}' contains forbidden character '\\''".format(original_chord)
        new_chord=transposition_chord(original_chord,shift)
        parts[i]=("*{" if star else "{")+new_chord+mod_part[right_index:]

    return "\Ch".join(parts)
