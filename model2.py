"""Versuch 2 die Verschlüsselung zu implementieren"""
from copy import deepcopy

#originalkonfigurationen
global alphabet, I, II, III, IV, V, UKW_B
alphabet =  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
I =         "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
II =        "AJDKSIRUXBLHWTMCQGZNPYFVOE"
III =       "BDFHJLCPRTXVZNYEIWGAKMUSQO"
IV =        "ESOVPZJAYQUIRHXLNFTGKDCMWB"
V =         "VZBRGITYUPSDNHLXAWMJQOFECK"
UKW_B =     "YRUHQSLDPXNGOKMIEBFZCWVJAT"

def char_zahl(char):
    return ord(char) - 65

def zahl_char(zahl):
    return alphabet[zahl]

def verschiebung(chiffre, zahl):
   #print("Chiffre vor Verschiebung:  " + chiffre)
    for i in range(zahl):
        char = chiffre[0]
        chiffre = chiffre[1:]
        chiffre += char
    
    #print("Chiffre nach Verschiebung: " + chiffre)
    
    return chiffre

#die walzenkonfiguration muss komplett reversed werden wenn man rückwärts durch die Maschine läuft
def walzen_konf_reverse(walze):
    rev_walze = []
    for i in range(26):
        rev_walze.append("")

    for i in walze:
        rev_walze[char_zahl(i)] = zahl_char(walze.index(i))

    return rev_walze

def verschluesseln(charakter, steckerbrett_konfiguration, charakter_route, walzen_drehung):
    
    _I = verschiebung(I, I.index(walzen_drehung[0]))
    _II = verschiebung(II, II.index(walzen_drehung[1]))
    _III = verschiebung(III, III.index(walzen_drehung[2]))

    #"""
    #erste steckerbrett permutation
    charakter = steckerbrett_konfiguration[char_zahl(charakter)]
    charakter_route.append(deepcopy(charakter))
    #"""

    #"""
    #Enigma ist konfiguriert mit den Walzen I, II und III
    #die Walzen werden von links nach rechts in die Enigma platziert
    #deshalb ist erste walze III
    charakter = _III[char_zahl(charakter)]
    charakter_route.append(deepcopy(charakter))
    charakter = _II[char_zahl(charakter)]
    charakter_route.append(deepcopy(charakter))
    #"""
    charakter = _I[char_zahl(charakter)]
    charakter_route.append(deepcopy(charakter))
    #"""

    #darauf folgt umkehrwalze
    charakter = UKW_B[char_zahl(charakter)]
    charakter_route.append(deepcopy(charakter))

    _I = walzen_konf_reverse(_I)
    _II = walzen_konf_reverse(_II)
    _III = walzen_konf_reverse(_III)

    #"""
    #dann walzen in umgekehrter reihenfolge
    charakter = _I[char_zahl(charakter)]
    charakter_route.append(deepcopy(charakter))
    #"""
    charakter = _II[char_zahl(charakter)]
    charakter_route.append(deepcopy(charakter))
    charakter = _III[char_zahl(charakter)]
    charakter_route.append(deepcopy(charakter))
    #"""

    #"""
    charakter = steckerbrett_konfiguration[char_zahl(charakter)]
    charakter_route.append(deepcopy(charakter))
    #"""

    return charakter


def main():
    #eigene konfiguration des steckerbretts, genommen aus Auszug
    #eines Kurzsignalhefts der Luftwaffe für jeden Tag, 
    #Steckerlage vom 31. Tag des Maschinenschlüssels Nr. 2744
    #                             ABCDEFGHIJKLMNOPQRSTUVWXYZ
    steckerbrett_konfiguration = "HIKLMFPABQCDENOGJVSWYRTXUZ"
    walzen_drehung = "AAA"

    charakter = input("Charakter zum Verschlüsseln: ")
    charakter_route = [deepcopy(charakter)]

    charakter = verschluesseln(charakter, steckerbrett_konfiguration, charakter_route, walzen_drehung)

    print(charakter)
    print(charakter_route)

    print("\n\nRückversuch\n\n")

    charakter2 = charakter
    charakter2_route = [deepcopy(charakter2)]
    print("Charakter zum Verschlüsseln: ", charakter2)

    charakter2 = verschluesseln(charakter2, steckerbrett_konfiguration, charakter2_route, walzen_drehung)

    print(charakter2)
    print(charakter2_route)


if __name__ == "__main__":
    main()
