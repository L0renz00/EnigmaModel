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
