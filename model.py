class Walze:
    def __init__(self, chiffre, umkehrchar):
        self.chiffre = chiffre
        self.umkehrchar = umkehrchar
        self.start_position = chiffre[0]
        self.counter = 0

    def drehen(self):
        #enimga walzen drehen sich so, dass eine umdrehung einer permutation vom ersten charkter zum zweiten entspricht
        #auch wichtig ist dass erst die drehung geschieht, und dann die Verschlüsselung
        self.chiffre = self.chiffre + self.chiffre[0]
        self.chiffre = self.chiffre[1 : len(self.chiffre) + 1]
        self.counter += 1

class Enigma:
    #                    ABCDEFGHIJKLMNOPQRSTUVWXYZ  
    walze_I =     Walze("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
    walze_II =    Walze("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
    walze_III =   Walze("BDFHJLCPRTXVZNYEIWGAKMUSQO", "D")
    walze_IV =    Walze("ESOVPZJAYQUIRHXLNFTGKDCMWB", "R")
    walze_V =     Walze("VZBRGITYUPSDNHLXAWMJQOFECK", "H")
    umkehrwalze =       "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    #umkehrwalze kein "Walze", weil keinerlei Umkehr, verwendete chiffre ist von UKW-B

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

def zahl_buchstabe(zahl):
    return alphabet[zahl]

#ordinalzahl für 'A' = 65, den Charakter bekommt man wenn man 
#einfach so abzieht
def buchstabe_zahl(char):
    return ord(char) - 65

def schluesseln(char, konfiguration):
    #erster Verschlüsselungsschritt ist walzen zu drehen!
    
    if konfiguration.m_walze.chiffre[0] == konfiguration.m_walze.umkehrchar:
    #doppelte umkehr hier implementiert, wenn mittlere walze an der umkehrposition ist, dann wird die linke walze einmal gedreht
    #aber wegen der doppelten umkehr die mittlere walze auch
        konfiguration.m_walze.drehen()
        konfiguration.l_walze.drehen()
    if konfiguration.r_walze.chiffre[0] == konfiguration.r_walze.umkehrchar:
        konfiguration.m_walze.drehen()

    konfiguration.r_walze.drehen()


    #zu verschlüsselnder charakter greift als zahl in list, wird so zu nächstem charakter verschlüsselt
    #zur demo bei jedem verschlüsselungsschritt einmal ausdrucken
    print("anfang: " + char)

    #steckerbrett
    char = konfiguration.steckerbrett[buchstabe_zahl(char)]
    print("nach steckerbrett: ", char)

    #drei walzen,  rechts nach links
    char = konfiguration.r_walze.chiffre[buchstabe_zahl(char)]
    print("r_walze: " + char)
    char = konfiguration.m_walze.chiffre[buchstabe_zahl(char)]
    print("m_walze: " + char)
    char = konfiguration.l_walze.chiffre[buchstabe_zahl(char)]
    print("l_walze: " + char)

    #umkehrwalze 
    char = konfiguration.umkehrwalze[buchstabe_zahl(char)]
    print("umkehrwalze: ", char)

    #rueckkehr durch walzen, diesmal links nach rechts
    char = konfiguration.l_walze.chiffre[buchstabe_zahl(char)]
    print("rueckehr I: ", char)
    char = konfiguration.m_walze.chiffre[buchstabe_zahl(char)]
    print("rueckkehr II: ", char)
    char = konfiguration.r_walze.chiffre[buchstabe_zahl(char)]
    print("rueckkehr III: ", char)

    #steckerbrett
    char = konfiguration.steckerbrett[buchstabe_zahl(char)]
    print("nach steckerbrett: ", char)

    return char


def main():
    global alphabet
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    enigma = Enigma(Enigma.walze_I, Enigma.walze_II, Enigma.walze_III, Enigma.umkehrwalze, Enigma.steckerbrett)

    charakter = str(input("Charakter zum verschlüsseln: "))

    charakter = schluesseln(charakter, enigma)

    print("Verschlüsselt zu: " + charakter)

    print("\n\nRückversuch\n\n");
    
    charakter2 = charakter

    #zurücksetzen der enigma
    enigma = Enigma(Enigma.walze_I, Enigma.walze_II, Enigma.walze_III, Enigma.umkehrwalze, Enigma.steckerbrett)
    charakter2 = schluesseln(charakter2, enigma)

if __name__ == "__main__":
    main()
