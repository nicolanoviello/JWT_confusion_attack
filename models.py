from start import db

class UserModel(db.Model):
    __tablename__ = 'utenti'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    ruolo = db.Column(db.String(20),  default="studente",nullable = False)
    
    # Salvataggio su db
    def salva_sul_db(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def cerca_su_db(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def tutta_la_lista(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password,
                'role': x.ruolo
                 }
        return {'Utenti': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def svuota_db(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} utenti cancellati'.format(num_rows_deleted)}
        except:
            return {'message': 'OPS. Qualcosa è andato storto.'}