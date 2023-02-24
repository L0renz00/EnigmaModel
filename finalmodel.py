from copy import deepcopy

class Walze:
    def __init__(self, schema):
        self.verdrahtung_vor = list(schema)
        #die walzenkonfiguration muss komplett umgekehrt werden 
        #wenn der Strom rückwärts durch die Maschine läuft
        self.verdrahtung_rueck = []
        for i in range(26):
            self.verdrahtung_rueck.append("")
        for i in self.verdrahtung_vor:
            self.verdrahtung_rueck[char_zahl(i)] = zahl_char(self.verdrahtung_vor.index(i))

        #hier kommen später noch die optionen für die walzenrotation nach tastaturdruck rein

    #die walzenkonfiguration muss komplett umgekehrt werden 
    #wenn der Strom rückwärts durch die Maschine läuft
    @classmethod
    def walzen_konf_umkehr(self):
        rev_walze = []
        for i in range(26):
            rev_walze.append("")

        for i in self.walzen_schema:
            rev_walze[char_zahl(i)] = zahl_char(walzen_schema.index(i))

        return rev_walze

def zahl_char(zahl):
    return alphabet[zahl]

def char_zahl(char):
    return ord(char) - 65


alphabet =    list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  
#original walzenverdrahtungen der Enigma-I
walze_I =     Walze("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
walze_II =    Walze("AJDKSIRUXBLHWTMCQGZNPYFVOE")
walze_III =   Walze("BDFHJLCPRTXVZNYEIWGAKMUSQO")
walze_IV =    Walze("ESOVPZJAYQUIRHXLNFTGKDCMWB")
walze_V =     Walze("VZBRGITYUPSDNHLXAWMJQOFECK")

ukw_b =     ["AY", "BR", "CU", "DH", "EQ", "FS", "GL", "IP", "JX", "KN", "MO", "ZT", "WV"]


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

def zahl_char(zahl):
    return alphabet[zahl]

def char_zahl(char):
    return ord(char) - 65

def verschluesseln(char, enigma):
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

def main():
    #ausgewählte Walzen hier auswählen, 
    #erste walze in liste ist links installierte in der Enigma, erste die mittlere etc.
    walzen = [deepcopy(walze_I), deepcopy(walze_II), deepcopy(walze_III)]
    #steckerbrett konfiguration hier eingeben:
    steckerbrett = ["AB","GH", "UJ", "ZW", "FL", "YX", "OP", "UN", "SQ", "MK"]
    #umkehrwalze hier auswählen:
    umkehrwalze = deepcopy(ukw_b)

    enigma = EnigmaKonf(walzen, steckerbrett, umkehrwalze)
    char = input("Charakter zum Verschlüsseln: ")

    chffr_char = verschluesseln(char, enigma)

    print("\nVerschluesselter Charakter: ", chffr_char)

if __name__ == "__main__":
    main()
