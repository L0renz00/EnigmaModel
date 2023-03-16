from copy import deepcopy
from enigma import Walze, EnigmaKonf, verschluesseln


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
    print("Geben sie die Walzenstellung wiefolgt formatiert ein: \nXXX\n")
    while True:
        tagesschluessel = input("Geben sie jetzt ihre Walzenstellung ein")
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


if __name__ == "__main__":
    cli()
