class Enigma:
    #              ABCDEFGHIJKLMNOPQRSTUVWXYZ  
    walze_I =     "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    walze_II =    "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    walze_III =   "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    walze_IV =    "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    walze_V =     "VZBRGITYUPSDNHLXAWMJQOFECK"
    umkehrwalze = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

    #steckerbrett konfiguration mit 10 "swaps" in pairs AD, BZ, CH, FK, IJ, MR, OP, TV, EY, UQ
    #               ABCDEFGHIJKLMNOPQRSTUVWXYZ
    steckerbrett = "DZHAYKGCJIFLRNPOUMSVQTWXEB" 

    #Die Enigma Konfiguration mit den konfigurationen der verschiedenen Walzen 
    #(l = links, r = rechts, m = mittel), dem steckerbrett und den verschiedenen schlüsseln
    #für den Tag und die Sitzung

    #für demo Steckerbrett, Tagesschlüssel und Sitzungsschlüssel ausgelassen
    def __init__(self, r_walze, m_walze, l_walze, umkehrwalze, steckerbrett):
        self.steckerbrett = steckerbrett
        self.r_walze = r_walze
        self.m_walze = m_walze
        self.l_walze = l_walze
        self.umkehrwalze = umkehrwalze
        #self.tagkey = tagkey
        #self.seshkey = seshkey

    def __str__(self):
        return f'Enigma(\nr_walze: {self.r_walze}, \nm_walze: {self.m_walze}, \nl_walze: {self.l_walze})'

def zahl_buchstabe(zahl):
    return alphabet[zahl]

#ordinalzahl für 'A' = 65, den Charakter bekommt man wenn man 
#einfach so abzieht
def buchstabe_zahl(char):
    return ord(char) - 65

def schluesseln(char, konfiguration):
    #zu verschlüsselnder charakter greift als zahl in list, wird so zu nächstem charakter verschlüsselt
    #zur demo bei jedem verschlüsselungsschritt einmal ausdrucken
    print("anfang: " + char)

    #steckerbrett
    char = konfiguration.steckerbrett[buchstabe_zahl(char)]
    print("nach steckerbrett: ", char)

    #drei walzen,  rechts nach links
    char = konfiguration.r_walze[buchstabe_zahl(char)]
    print("r_walze: " + char)
    char = konfiguration.m_walze[buchstabe_zahl(char)]
    print("m_walze: " + char)
    char = konfiguration.l_walze[buchstabe_zahl(char)]
    print("l_walze: " + char)

    #umkehrwalze 
    char = konfiguration.umkehrwalze[buchstabe_zahl(char)]
    print("umkehrwalze: ", char)

    #rueckkehr durch walzen, diesmal links nach rechts
    char = konfiguration.l_walze[buchstabe_zahl(char)]
    print("rueckehr I: ", char)
    char = konfiguration.m_walze[buchstabe_zahl(char)]
    print("rueckkehr II: ", char)
    char = konfiguration.r_walze[buchstabe_zahl(char)]
    print("rueckkehr III: ", char)

    #steckerbrett
    char = konfiguration.steckerbrett[buchstabe_zahl(char)]
    print("nach steckerbrett: ", char)

    return char


def main():
    global alphabet
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    enigma = Enigma(Enigma.walze_I, Enigma.walze_II, Enigma.walze_III, Enigma.umkehrwalze, Enigma.steckerbrett)

    charakter = str(input("Charakter zum Verschlüsseln: "))

    print(enigma)
    charakter = schluesseln(charakter, enigma)
    print(enigma)

    print("\n\nRückversuch\n\n");
    charakter2 = charakter

    print(enigma)
    charakter2 = schluesseln(charakter2, enigma)
    print(enigma)

if __name__ == "__main__":
    main()
