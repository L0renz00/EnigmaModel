# EnigmaModel
An accurate model of the Enigma encryption machine, written in Python and deployed to a webserver.  
This model was created for the Fünfte Prüfungskomponente of the german Abiturexam. 

## Design Ethics
- Clean, more functional than oop-oriented implementation
- to more easily facilitate change-over of web deployment
- simple, concise implementations

## Design Plan
- A class containing the specific states of the different enigma-components  
- Instance of that class created at start of app, to be passed around the application  
- Application begins with letter to be encrypted, which is then passed around the application with the enigma-object  
- Encryption-parts of the machine are "represented" with pure functions that execute the encryption steps of the different enigma-components
- Instance of enigma and letter passed through these functions until encrypted letter emerges at end of "function chain"
