"""Versuch 2 die Verschlüsselung zu implementieren"""

#originalkonfigurationen
global alphabet, I, II, III, IV, V, UKW_B
alphabet =  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
I =         "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
II =        "AJDKSIRUXBLHWTMCQGZNPYFVOE"
III =       "BDFHJLCPRTXVZNYEIWGAKMUSQO"
IV =        "ESOVPZJAYQUIRHXLNFTGKDCMWB"
V =         "VZBRGITYUPSDNHLXAWMJQOFECK"
UKW_B =     "YRUHQSLDPXNGOKMIEBFZCWVJAT"

def char_zahl_transform(char):
    return ord(char) - 65

def main():
    #eigene konfiguration des steckerbretts, genommen aus Auszug
    #eines Kurzsignalhefts der Luftwaffe für jeden Tag, 
    #Steckerlage vom 31. Tag des Maschinenschlüssels Nr. 2744
    steckerbrett_konfiguration = "HIKLMFPABQCDENOGJVSWYRTXUZ"

    charakter = input("Charakter zum Verschlüsseln: ")

    #erste steckerbrett permutation
    charakter = steckerbrett_konfiguration[char_zahl_transform(charakter)]
    #Enigma ist konfiguriert mit den Walzen I, II und III
    #die Walzen werden von links nach rechts in die Enigma platziert
    #deshalb ist erste walze III
    charakter = III[char_zahl_transform(charakter)]
    charakter = II[char_zahl_transform(charakter)]
    charakter = I[char_zahl_transform(charakter)]

    #darauf folgt umkehrwalze
    charakter = UKW_B[char_zahl_transform(charakter)]

    #dann 

    print(charakter)

if __name__ == "__main__":
    main()
