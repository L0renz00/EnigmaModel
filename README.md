# EnigmaModel
Ein genaues Modell der Verschlüsselungsmaschine Enigma I (von 1932 - 1945 von der deutschen Wehrmacht benutzt), 
geschrieben in Python und bereitgestellt auf einem Webserver.  
Dieses Modell wurde für die Fünfte Prüfungskomponente des Abiturexamens erstellt. 

## Design-Ethik
- Saubere, funktionalere als OOP-orientierte Implementierung
- leichtere Umstellung des Webeinsatzes
- einfache, prägnante Implementierungen

## Entwurfsplan
- Eine Klasse, die die spezifischen Zustände der verschiedenen enigma-Komponenten enthält  
- Eine Instanz dieser Klasse wird beim Start der Anwendung erstellt und durch die Anwendung gereicht  
- Die Anwendung beginnt mit einem zu verschlüsselnden Brief, der dann mit dem Enigma-Objekt durch die Anwendung gereicht wird  
- Die Verschlüsselungsteile der Maschine werden durch reine Funktionen "repräsentiert", die die Verschlüsselungsschritte der verschiedenen Enigma-Komponenten ausführen
- Enigma-Instanz und Buchstabe werden durch diese Funktionen geleitet, bis am Ende der "Funktionskette" ein verschlüsselter Brief entsteht
