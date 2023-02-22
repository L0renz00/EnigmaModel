"""Versuch 3 :/ die Verschlüsselung zu implementieren"""

global I, II, III, IV, V, UKW_B
I =         list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
II =        list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
III =       list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
IV =        list("ESOVPZJAYQUIRHXLNFTGKDCMWB")
V =         list("VZBRGITYUPSDNHLXAWMJQOFECK")
UKW_B =     list("YRUHQSLDPXNGOKMIEBFZCWVJAT")


def zahl_char(zahl):
    alphabet =  list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return alphabet[zahl]

def char_zahl(char):
    return ord(char) - 65

#funktion, die reziproke substitutionen durchführt
#bekommt paarliste z.B. ["AB", "GH",  UJ, ZW] und sucht nach char
#vertauscht dann mit jeweils anderem buchstaben falls gefunden
def rez_substitution(char, paarliste):
    for i in paarliste:
        if char in i:
            if i[0] = char:
                return i[1]
            else: #eigentlich unnötig aber für codeklarheit
                return i[0]
        else: #eigentlich unnötig aber für codeklarheit
            return char

#funktion, die die walzen substitutionen durchführt
#bekommt char, drei walzen in liste (erste ist ganz linke walze in maschine etc.)
#bekommt auch richtung (entweder "V" oder "R" und führt dann substitution 
#vorwärts oder rückwärts durch
def wal_substitution(char, walzen, richtung):    
    if richtung == "V":
        for i in walzen.reverse():
           char = i[char_zahl(char)] 
    
    elif richtung == "R":
        for i in walzen:
            char = i[]

