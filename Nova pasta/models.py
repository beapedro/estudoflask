from jogoteca import db

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nome = db.Column(db.String(50), nullable = False)
    categoria = db.Column(db.String(40), nullable = False)
    console = db.Column(db.String(20), nullable = False)
    
    def __repr__(self):
        return '<Name %r>' % self.name 
    
class Usuarios(db.Model):
    nickname = db.Column(db.String(25), primary_key = True, nullable = False)
    nome = db.Column(db.String(500), nullable = False)
    senha = db.Column(db.String(100), nullable = False)    

    def __repr__(self):
        return '<Name %r>' % self.name

class Amigos(db.Model):
    amizadeid = db.Column(db.String(36), primary_key = True, nullable = False)
    amigo1 = db.Column(db.String(25), nullable = False)
    amigo2 = db.Column(db.String(25), nullable = False) 
    mensagem = db.Column(db.String(500))  
    confirmacao = db.Column(db.Boolean, nullable = False) 
    datainicio = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return f'<Amizade {self.amizadeid}>'