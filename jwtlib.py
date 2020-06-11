from functools import wraps
from flask import request, Response
import json
import jwt

private_key = open('mykey.pem').read()
public_key = open('pubkey.pem').read()
algo='RS256'
def encode_auth_token(utenteloggato):
    try:
        if  utenteloggato.ruolo == 'abcde':
            payload = {
            'username': utenteloggato.username,
            'role': 'abcde'
            }
        elif utenteloggato.ruolo == 'root':
            payload = {
            'username': utenteloggato.username,
            'role': 'root'
            }
        else:
            payload = {
                'username': utenteloggato.username
            }
        # jwt_encoded = jwt.encode(payload, private_key, algorithm='RS256')
        jwt_encoded = jwt.encode(payload, private_key,algorithm=algo)
        return jwt_encoded.decode('utf-8')
    except Exception as e:
        return e

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = False
        if not auth_token:
            auth_token = request.headers.get('capstoneAuth')
        if not auth_token:
            auth_token = request.headers.get('Authorization')
        if not auth_token:
            auth_token = request.cookies.get('capstoneAuth')
        if not auth_token:  # Authtoken no present so send 401
            return Response('Token mancante!\n' 'Mancano le autorizzazioni per effettuare la chiamata', 401,
                            {'WWW-Authenticate': 'Basic realm="Login Required"'})
        else:
            return f(*args, **kwargs)
    return decorated

def decode_auth_token(token):
    try:
        token = token.replace("Bearer ",'')
        # Integrazione fix
        header = jwt.utils.base64url_decode(token[:token.index(".")]).decode("utf-8")
        json_header = json.loads(header)['alg']
        if json_header == algo:
            message_received = jwt.decode(token, public_key)
            return(message_received)
    except Exception as e:
        return e