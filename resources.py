from flask_restful import Resource, reqparse
from models import UserModel
from flask import jsonify
#import jwt
import flask
from flask import request, Response
from jwtlib import encode_auth_token, decode_auth_token, requires_auth

# flask_restful ha una libreria integrata per il parsing
# possiamo usarla per effettuare verifiche sui campi obbligatori
# ad esempio questi sono quelli necessari alla login
parser = reqparse.RequestParser()
parser.add_argument('username', help = 'Questo campo non può essere vuoto', required = True)
parser.add_argument('password', help = 'Questo campo non può essere vuoto', required = True)
parser.add_argument('ruolo', help = 'Questo campo non può essere vuoto', required = False)


# qui è definita la lista di tutti gli endpoint da provare
class Registration(Resource):
    def post(self):
        data = parser.parse_args()
        # Acquisisco i dati da JSON
        nuovo_utente = UserModel(
            username = data['username'],
            password = data['password'],
            ruolo = data['ruolo']
        )
        # Controllo se l'utente è già presente su db
        if UserModel.cerca_su_db(data['username']):
          return {'message': '{} è già presente sul DB'. format(data['username'])}

        try:
            # Provo a creare un nuovo utente con i dati inviati nella post
            nuovo_utente.salva_sul_db()
        except:
            # Restituisco un errore 500
            return {'message': 'OPS. Qualcosa è andato storto.'}, 500
        return data


class Login(Resource):
    def post(self):
        data = parser.parse_args()
        # Memorizzo i dati dell'utente in una variabile
        utente_loggato = UserModel.cerca_su_db(data['username'])
        # Controllo se l'utente è presente sul DB
        if not utente_loggato:
            return {'message': '{} non esiste'.format(data['username'])}
        
        if data['password'] == utente_loggato.password:
            
            #payload = {'username':utente_loggato.username, 'role':utente_loggato.ruolo}
            encode_jwt = encode_auth_token(utente_loggato)
            return {
                'message': 'Hai effettuato l\'accesso come {}'.format(utente_loggato.username),
                'auth_token':encode_jwt
                }
        else:
            return {'message': 'Credenziali sbagliate'}
      
      
class ListaUtenti(Resource):
    def get(self):
        return UserModel.tutta_la_lista()

    def delete(self):
        UserModel.svuota_db()
        return {'message': 'Ripulisco il db cancellando tutti gli utenti'}
      
      
class CheckJWT(Resource):
    @requires_auth
    def get(self):
        auth_token = request.headers.get('Authorization')
        print(auth_token)
        message_received = decode_auth_token(auth_token)
        if not message_received.get('role'):
            return {'message': 'Benvenuto studente!'},200
        if message_received.get('role') == 'abcde':
            return {'message': 'Sei ufficialmente root'},200
        elif message_received.get('role') == 'root':
            return {'message': 'Mi dispiace per te ma sei un fake root'},200
