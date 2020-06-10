# JWT_confusion_attack

Progetto di sicurezza - Anno accademico 2019/2020

Componente software in grado simulare un attacco di tipo key confusion/algorithm substitution su Token JWT

## Creazione dell'environment per l'installazione del progetto

- Il primo step prevede l'installazione di [Anaconda](https://www.anaconda.com/products/individual) disponibile per i principali sistemi operativi. Anaconda permette di creare ambienti python virtuali senza alterare le installazioni presenti sul sistema operativo principale

- Una volta installato Anaconda si può procedere all'attivazione dell'ambiente e all'installazione delle componenti necessarie

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

cat pubkey.pem | xxd -p | tr -d "\\n" > myhmac.txt

openssl dgst -sha256 -hmac -hex -macopt hexkey:\$(cat myhmac.txt) -out hmac.txt /bin/ps

https://www.getpostman.com/collections/4c9cf3a2d70263317bd6
https://pypi.org/project/PyJWT/0.4.3/
