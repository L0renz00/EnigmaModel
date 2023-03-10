from copy import deepcopy
from time import sleep


def cli():
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # original walzenverdrahtungen der Enigma-I
    walze_I = Walze("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
    walze_II = Walze("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
    walze_III = Walze("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "D")
    walze_IV = Walze("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "R")
    walze_V = Walze("V", "VZBRGITYUPSDNHLXAWMJQOFECK", "H")
    ukw_b = ["AY", "BR", "CU", "DH", "EQ", "FS", "GL", "IP", "JX", "KN", "MO", "ZT", "WV"]

    # ausgewählte Walzen hier auswählen, 
    # erste walze in liste ist links installierte in der Enigma, erste die mittlere etc.
    print("Herzlich Willkommen zu der Enigma-I!")
    print("Im ersten Schritt wählen Sie die drei Walzen aus, die in die Maschine eingesetzt werden sollen.")
    print("Sie können aus den Walzen I bis V auswählen, geben Sie diese bitte so formatiert ein: \nI II III")
    print("Die Reihenfolge der Eingabe bestimmt die Reihenfolge der Walzen in der Maschine, die zuerst eingegebene ist die linke Walze etc.")
    print("Wenn Sie sich für keine Walzen entscheiden möchten, wird die Standardeinstellung der Walzen I, II und III verwendet.")
    walzen = []

    while True:

        walzen_wahl = input("Geben Sie jetzt ihre Walzen ein und drücken Sie danach die Enter-Taste.\n")

        if len(walzen_wahl) == 0:
            walzen = [deepcopy(walze_I), deepcopy(walze_II), deepcopy(walze_III)]
            break

        if len(walzen_wahl.split()) != 3:
            print("Zu viele oder zu wenige walzen ausgewählt!")
            print(walzen_wahl.split())

            continue

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
                    print(f"{other} ist keine mögliche Walzenwahl.")
                    continue

        break

    steckerbrett = ["AB", "GH", "UJ", "ZW", "FL", "YX", "OP", "UN", "SQ", "MK"]
    # steckerbrett konfiguration hier eingeben:
    print("Im zweiten Schritt können Sie die durch das Steckerbrett zu vertauschenden Buchstaben auswählen.")
    print("Sie können entweder ihre Buchstaben eingeben oder eine Standardkonfiguration wählen, welche die folgenden Buchstaben austauscht: ")
    for i in steckerbrett:
        print(i, end=" ")
    print()
    print("Wenn Sie ihre eigenen Buchstaben eingeben möchten, formatieren Sie diese bitte so:\nAB CD EF GH IJ\n")
    print("Beachten Sie auch, dass Buchstaben sich nicht wiederholen sollten.")
    while True:
        steckerbrett_wahl = input("Geben Sie jetzt ihre zu vertauschenden Buchstaben ein und drücken Sie danach die Enter-Taste.\n")

        for i in steckerbrett_wahl.split():
            if len(i) != 2:
                print("Falsche Eingabe: ", i)
                continue
            if i[0] not in alphabet or i[1] not in alphabet:
                print("Falsche Eingabe", i)
                continue
        # verflachen der list von 2 dimensional zu eindimensional zur duplikatcheckung
        stecker = [x for y in steckerbrett_wahl for x in y]
        stecker = [x for x in stecker if x != " "]
        # set() entfernt duplikate, wenn set kürzer ist dann gibt es duplikate
        if len(stecker) > len(set(stecker)):
            print("Duplikate in der Steckerbrett-Eingabe.")
            print(stecker, " ", set(stecker))
            continue

        steckerbrett = steckerbrett_wahl.split()
        break

    umkehrwalze = ukw_b
    
    tagesschluessel = "IQB"
    print("Im dritten und letzten Schritt können Sie noch die Walzenrotation konfigurieren, indem Sie drei Buchstaben eingeben, welche die Walzenrotation bestimmen.")
    while True:
        tagesschluessel = input("gib die walzenstellung ein(so: XXX): ")
        if len(tagesschluessel) != 3:
            print("Falscher Tagesschluessel!")
            continue
        for i in tagesschluessel:
            if i not in alphabet:
                print("Falscher Charakter: ", i)
                continue
        break

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
                return i[0]

        return char


if __name__ == "__main__":
    cli()
