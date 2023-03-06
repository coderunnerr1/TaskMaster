from TaskMaster import db

class Tarefas(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    tarefa = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    prazo = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name
    
class Usuarios(db.Model):
    nickname = db.Column(db.String(10),primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name