"""Versuch 3 :/ die Verschlüsselung zu implementieren"""

from copy import deepcopy

global I, II, III, IV, V, UKW_B
I =         list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
II =        list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
III =       list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
IV =        list("ESOVPZJAYQUIRHXLNFTGKDCMWB")
V =         list("VZBRGITYUPSDNHLXAWMJQOFECK")
UKW_B =     ["AY", "BR", "CU", "DH", "EQ", "FS", "GL", "IP", "JX", "KN", "MO", "ZT", "WV"]
UKW_B_str =     list("YRUHQSLDPXNGOKMIEBFZCWVJAT")

def zahl_char(zahl):
    alphabet =  list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return alphabet[zahl]

def char_zahl(char):
    return ord(char) - 65

#die walzenkonfiguration muss komplett reversed werden wenn man rückwärts durch die Maschine läuft
def walzen_konf_reverse(walze):
    rev_walze = []
    for i in range(26):
        rev_walze.append("")

    for i in walze:
        rev_walze[char_zahl(i)] = zahl_char(walze.index(i))

    return rev_walze

def enigma(charakter, steckerbrett, walzenkonfiguration):
    #verschlüsseln! 
    #steckerbrett
    charakter = rez_substitution(charakter, steckerbrett)
    
    #Walzen vorwärts durchlaufen:
    charakter = wal_substitution(charakter, walzenkonfiguration, "F")
    #umkehrwalze
    charakter = rez_substitution(charakter, deepcopy(UKW_B))
    #Walzen rückwärts durchlaufen:
    charakter = wal_substitution(charakter, walzenkonfiguration, "R")

    #steckerbrett
    charakter = rez_substitution(charakter, steckerbrett)

    return charakter

def main():
    steckerbrett = ["AB","GH", "UJ", "ZW", "FL", "YX", "OP", "UN", "SQ", "MK"]
    #Walzenkonfiguration ist I als linke, II als mittlere III als rechte
    walzenkonfiguration = [deepcopy(I), deepcopy(II), deepcopy(III)]

    charakter = input("Charakter zu verschlüsseln: ")

    charakter = enigma(charakter, steckerbrett, walzenkonfiguration)

    print("Verschlüsselter Charakter: " + charakter)

#funktion, die reziproke substitutionen durchführt
#bekommt paarliste z.B. ["AB", "GH",  UJ, ZW] und sucht nach char
#vertauscht dann mit jeweils anderem buchstaben falls gefunden
def rez_substitution(char, paarliste):
    for i in paarliste:
        if char in i:
            if i[0] == char:
                return i[1]
            else: #eigentlich unnötig aber für codeklarheit
                return i[0]
        else: #eigentlich unnötig aber für codeklarheit
            return char

#funktion, die die walzen substitutionen durchführt
#bekommt char, drei walzen in liste (erste ist ganz linke walze in maschine etc.)
#bekommt auch richtung (entweder "V" oder "R" und führt dann substitution 
#vorwärts oder rückwärts durch
#wenn rückwärts durchläuft dann muss 
def wal_substitution(char, walzen, richtung):    
    if richtung == "V":
        for i in walzen.reverse():
           char = i[char_zahl(char)] 
    
    else:
        for i in walzen:
            rev_walze = walzen_konf_reverse(i)
            char = rev_walze[char_zahl(char)]

    return char

if __name__ == "__main__":
    main()
