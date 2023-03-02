from copy import deepcopy

def main():
    #original walzenverdrahtungen der Enigma-I
    walze_I =     Walze("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
    walze_II =    Walze("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
    walze_III =   Walze("BDFHJLCPRTXVZNYEIWGAKMUSQO", "D")
    walze_IV =    Walze("ESOVPZJAYQUIRHXLNFTGKDCMWB", "R")
    walze_V =     Walze("VZBRGITYUPSDNHLXAWMJQOFECK", "H")
    ukw_b =     ["AY", "BR", "CU", "DH", "EQ", "FS", "GL", "IP", "JX", "KN", "MO", "ZT", "WV"]

    #ausgewählte Walzen hier auswählen, 
    #erste walze in liste ist links installierte in der Enigma, erste die mittlere etc.
    walzen = [deepcopy(walze_I), deepcopy(walze_II), deepcopy(walze_III)]
    #steckerbrett konfiguration hier eingeben:
    steckerbrett = ["AB","GH", "UJ", "ZW", "FL", "YX", "OP", "UN", "SQ", "MK"]
    #umkehrwalze hier auswählen:
    umkehrwalze = deepcopy(ukw_b)


    enigma = EnigmaKonf(walzen, steckerbrett, umkehrwalze)

    #test für walzenstellungen nach drehung:
    for i in (["A"] * (26*26)):
        verschluesseln(i, enigma)
        print(f"{enigma.walzen[0].verdrahtung_vor[0]}{enigma.walzen[1].verdrahtung_vor[0]}{enigma.walzen[2].verdrahtung_vor[0]}")


def verschluesseln(char, enigma):
    #vor dem verschluesseln die walzen drehen:
    #doppelte umdrehung:
    #wenn mittlere walze umkehr erreicht dann wird rechte gedreht, allerdings 
    #auch die mittlere, so-gennantes "double stepping"
    if enigma.walzen[1].verdrahtung_vor[0] == enigma.walzen[1].umkehrchar:
        enigma.walzen[1].drehen()
        enigma.walzen[0].drehen()
    #wenn rechte walze umkehr charakter erreicht wird walze links davon gedreht
    if enigma.walzen[2].verdrahtung_vor[0] == enigma.walzen[2].umkehrchar:
        enigma.walzen[1].drehen()

    enigma.walzen[2].drehen()

    #verschluesseln:

    #steckerbrett:
    char = enigma.steckerbrett.rez_substitution(char)

    #walzen von rechts nach links:
    char = enigma.walzen[2].verdrahtung_vor[char_zahl(char)]
    char = enigma.walzen[1].verdrahtung_vor[char_zahl(char)]
    char = enigma.walzen[0].verdrahtung_vor[char_zahl(char)]

    #umkehrwalze:
    char = enigma.umkehrwalze.rez_substitution(char)

    #rueckwaerts und von links nach rechts durch walzen:
    char = enigma.walzen[0].verdrahtung_rueck[char_zahl(char)]
    char = enigma.walzen[1].verdrahtung_rueck[char_zahl(char)]
    char = enigma.walzen[2].verdrahtung_rueck[char_zahl(char)]

    #erneut durch das steckerbrett:
    char = enigma.steckerbrett.rez_substitution(char)

    return char


def zahl_char(zahl):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  
    return alphabet[zahl]

def char_zahl(char):
    return ord(char) - 65

#klasse um alle Enigma Konfigurationsoptionen zu speichern
class EnigmaKonf:
    #alle Konfigurationsoptionen die von dem Nutzer eingestellt werden
    #werden hier eingespeist
    #walzen_konf sind die drei vom nutzer sichtbaren Buchstaben die 
    #durch die rotation der walzen eingestellt werden, analog zum
    #Tagesschlüssel bzw. Nachrichtenschlüssel der vom Nutzer eingestellt wird
    def __init__(self, walzen, steckerbrett, umkehrwalze):
        self.walzen = walzen
        self.steckerbrett = Substitution(steckerbrett)
        self.umkehrwalze = Substitution(umkehrwalze)


class Walze:
    def __init__(self, schema, umkehrchar):
        self.verdrahtung_vor = list(schema)
        #die walzenkonfiguration muss komplett umgekehrt werden 
        #wenn der Strom rückwärts durch die Maschine läuft
        self.verdrahtung_rueck = []
        for i in range(26):
            self.verdrahtung_rueck.append("")
        for i in self.verdrahtung_vor:
            self.verdrahtung_rueck[char_zahl(i)] = zahl_char(self.verdrahtung_vor.index(i))

        #charakter der angiebt wann die walze die nächste walze umdreht
        self.umkehrchar = umkehrchar
        #counter für rotationsschritte der walze
        self.umdrehungen = 0

    def drehen(self):
        #enimga walzen drehen sich so, dass eine umdrehung einer permutation vom ersten charkter zum zweiten entspricht
        #auch wichtig ist dass erst die drehung geschieht, und dann die Verschlüsselung
        self.verdrahtung_vor.append(self.verdrahtung_vor[0])
        self.verdrahtung_vor.pop(0)
        self.umdrehungen += 1

        #update rueck verschluesselung
        for i in range(26):
            self.verdrahtung_rueck.append("")
        for i in self.verdrahtung_vor:
            self.verdrahtung_rueck[char_zahl(i)] = zahl_char(self.verdrahtung_vor.index(i))

class Substitution:
    def __init__(self, paarliste):
        self.paarliste = paarliste
    
    #funktion, die reziproke substitutionen durchführt
    #bekommt paarliste z.B. ["AB", "GH",  UJ, ZW] und sucht nach char
    #vertauscht dann mit jeweils anderem buchstaben falls gefunden
    def rez_substitution(self, char):
        for i in self.paarliste:
            if char in i:
                if i[0] == char:
                    return i[1]
                else: #eigentlich unnötig aber für codeklarheit
                    return i[0]
        return char


if __name__ == "__main__":
    main()
