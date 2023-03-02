from copy import deepcopy


def cli():
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # original walzenverdrahtungen der Enigma-I
    walze_I =     Walze("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
    walze_II =    Walze("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
    walze_III =   Walze("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "D")
    walze_IV =    Walze("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "R")
    walze_V =     Walze("V", "VZBRGITYUPSDNHLXAWMJQOFECK", "H")
    ukw_b =     ["AY", "BR", "CU", "DH", "EQ", "FS", "GL", "IP", "JX", "KN", "MO", "ZT", "WV"]

    # ausgewählte Walzen hier auswählen, 
    # erste walze in liste ist links installierte in der Enigma, erste die mittlere etc.
    walzen_wahl = input("gib als string die walzen ein die verwendet werden sollen, in der richtigen Reihenfolge, erste eingegebene walze ist linke in der maschine etc.(so: I II IV): \n")
    walzen = []
    if len(walzen_wahl.split()) != 3:
        print("zu viele oder zu wenige walzen ausgewählt!")
        exit()
    for i in walzen_wahl.split():
        match i:
            case "I":
                walzen.append(deepcopy(walze_I))
            case "II":
                walzen.append(deepcopy(walze_II))
            case "III":
                walzen.append(deepcopy(walze_III))
            case "IV":
                walzen.append(deepcopy(walze_IV))
            case "V":
                walzen.append(deepcopy(walze_V))
            case other:
                print(f"{other} ist keine richtige walzenwahl")
                exit()

    # steckerbrett konfiguration hier eingeben:
    steckerbrett_wahl = input("gib die zu vertauschenden buchstaben ein(so: AB DC etc...): \n")
    for i in steckerbrett_wahl.split():
        if len(i) != 2:
            print("falsche vertausch input: ", i)
            exit()
        if i[0] not in alphabet or i[1] not in alphabet:
            print("falsche charaktere eingegeben: ", i)
            exit()
    # verflachen der list von 2 dimensional zu eindimensional zur duplikatcheckung
    stecker = [x for y in steckerbrett_wahl for x in y]
    # set() entfernt duplikate, wenn set kürzer ist dann gibt es duplikate
    if len(stecker) > len(set(stecker)):
        print("duplikate in der steckerbrett-eingabe!")
        exit()

    steckerbrett = steckerbrett_wahl.split()

    # umkehrwalze hier auswählen:
    print("Umkehrwalze ist UKW_B")
    umkehrwalze = deepcopy(ukw_b)

    # tagesschluessel = "AAA"
    tagesschluessel = input("gib die walzenstellung ein(so: XXX): ")
    if len(tagesschluessel) != 3:
        print("Falscher Tagesschluessel!")
        exit()
    for i in tagesschluessel:
        if i not in alphabet:
            print("Falscher Charakter in Tagesschluessel!")
            exit()

    enigma = EnigmaKonf(walzen, steckerbrett, umkehrwalze, tagesschluessel)

    # einstellung der walzenstellung, macht hier beim beispiel A zu jedem chiff
    # re-anfangsbuchstaben der walzen
    enigma.walzen_stellen(tagesschluessel)

    klar_text = input("Gib den zu verschluesselnden Text ein: \n")
    chiffre_text = ""

    for i in klar_text:
        chiffre_text += verschluesseln(i, enigma)

    print(chiffre_text)


def verschluesseln(char, enigma):
    # vor dem verschluesseln die walzen drehen:
    # doppelte umdrehung:
    # wenn mittlere walze umkehr erreicht dann wird rechte gedreht, allerdings
    # auch die mittlere, so-gennantes "double stepping"
    if enigma.walzen[1].verdrahtung_vor[0] == enigma.walzen[1].umkehrchar:
        enigma.walzen[1].drehen()
        enigma.walzen[0].drehen()
    # wenn rechte walze umkehr charakter erreicht wird walze links davon gedreht
    if enigma.walzen[2].verdrahtung_vor[0] == enigma.walzen[2].umkehrchar:
        enigma.walzen[1].drehen()

    enigma.walzen[2].drehen()

    # verschluesseln:

    # steckerbrett:
    char = enigma.steckerbrett.rez_substitution(char)

    # walzen von rechts nach links:
    char = enigma.walzen[2].verdrahtung_vor[char_zahl(char)]
    char = enigma.walzen[1].verdrahtung_vor[char_zahl(char)]
    char = enigma.walzen[0].verdrahtung_vor[char_zahl(char)]

    # umkehrwalze:
    char = enigma.umkehrwalze.rez_substitution(char)

    # rueckwaerts und von links nach rechts durch walzen:
    char = enigma.walzen[0].verdrahtung_rueck[char_zahl(char)]
    char = enigma.walzen[1].verdrahtung_rueck[char_zahl(char)]
    char = enigma.walzen[2].verdrahtung_rueck[char_zahl(char)]

    # erneut durch das steckerbrett:
    char = enigma.steckerbrett.rez_substitution(char)

    return char


def zahl_char(zahl):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return alphabet[zahl]


def char_zahl(char):
    return ord(char) - 65

# klasse um alle Enigma Konfigurationsoptionen zu speichern
class EnigmaKonf:
    # alle Konfigurationsoptionen die von dem Nutzer eingestellt werden
    # werden hier eingespeist
    # walzen_konf sind die drei vom nutzer sichtbaren Buchstaben die 
    # durch die rotation der walzen eingestellt werden, analog zum
    # Tagesschlüssel bzw. Nachrichtenschlüssel der vom Nutzer eingestellt wird
    def __init__(self, walzen, steckerbrett, umkehrwalze, tagesschluessel):
        self.walzen = walzen
        self.steckerbrett = Substitution(steckerbrett)
        self.umkehrwalze = Substitution(umkehrwalze)
        self.tagesschluessel = tagesschluessel

    def walzen_stellen(self, stellung):
        for i in range(3):
            while self.walzen[i].verdrahtung_vor[0] != stellung[i]:
                self.walzen[i].drehen()


class Walze:
    def __init__(self, name, schema, umkehrchar):
        self.name = name
        self.verdrahtung_vor = list(schema)
        # die walzenkonfiguration muss komplett umgekehrt werden
        # wenn der Strom rückwärts durch die Maschine läuft
        self.verdrahtung_rueck = []
        for i in range(26):
            self.verdrahtung_rueck.append("")
        for i in self.verdrahtung_vor:
            self.verdrahtung_rueck[char_zahl(i)] = zahl_char(self.verdrahtung_vor.index(i))

        # charakter der angiebt wann die walze die nächste walze umdreht
        self.umkehrchar = umkehrchar
        # counter für rotationsschritte der walze
        self.umdrehungen = 0

    def drehen(self):
        # enigma walzen drehen sich so, dass eine umdrehung einer permutation vom ersten charkter zum zweiten entspricht
        # auch wichtig ist dass erst die drehung geschieht, und dann die Verschlüsselung
        self.verdrahtung_vor.append(self.verdrahtung_vor[0])
        self.verdrahtung_vor.pop(0)
        self.umdrehungen += 1

        # update rueck verschluesselung
        for i in range(26):
            self.verdrahtung_rueck.append("")
        for i in self.verdrahtung_vor:
            self.verdrahtung_rueck[char_zahl(i)] = zahl_char(self.verdrahtung_vor.index(i))


class Substitution:
    def __init__(self, paarliste):
        self.paarliste = paarliste

    # funktion, die reziproke substitutionen durchführt
    # bekommt paarliste z.B. ["AB", "GH",  UJ, ZW] und sucht nach char
    # vertauscht dann mit jeweils anderem buchstaben falls gefunden
    def rez_substitution(self, char):
        for i in self.paarliste:
            if char in i:
                if i[0] == char:
                    return i[1]
                else:  # eigentlich unnötig aber für codeklarheit
                    return i[0]
        return char


if __name__ == "__main__":
    cli()
