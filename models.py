from db import db

class Filme(db.Model):
    __tablename__ = 'filmes'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'ano': self.ano,
            'genero': self.genero,
            'descricao': self.descricao,
            'imagem': self.imagem
        }
