from flask import Blueprint, request, jsonify
from models import Filme, db
import logging
import os

# Criação do Blueprint
movie_bp = Blueprint('movies', __name__)

@movie_bp.route('/', methods=['GET'])
def listar_filmes():
    """Rota para listar todos os filmes."""
    try:
        filmes = Filme.query.all()
        return jsonify([filme.to_dict() for filme in filmes]), 200
    except Exception as e:
        logging.error("Erro ao listar filmes: %s", e)
        return jsonify({'error': str(e)}), 500

@movie_bp.route('/', methods=['POST'])
def adicionar_filme():
    """Rota para adicionar um novo filme."""
    content_type = request.content_type

    if 'application/json' in content_type:
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON format'}), 400

            novo_filme = Filme(**data)
            db.session.add(novo_filme)
            db.session.commit()
            return jsonify(novo_filme.to_dict()), 201
        except Exception as e:
            logging.error("Erro ao adicionar filme: %s", e, exc_info=True)
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    elif 'multipart/form-data' in content_type:
        try:
            data = {
                'titulo': request.form['titulo'],
                'ano': request.form['ano'],
                'genero': request.form['genero'],
                'descricao': request.form.get('descricao'),
                'imagem': None
            }

            if 'imagem' in request.files:
                imagem = request.files['imagem']
                imagem.save(os.path.join('static/uploads', imagem.filename))
                data['imagem'] = imagem.filename

            novo_filme = Filme(**data)
            db.session.add(novo_filme)
            db.session.commit()
            return jsonify(novo_filme.to_dict()), 201
        except Exception as e:
            logging.error("Erro ao adicionar filme: %s", e, exc_info=True)
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415

@movie_bp.route('/<int:id>', methods=['PUT'])
def editar_filme(id):
    """Rota para editar um filme existente."""
    try:
        filme = Filme.query.get(id)
        if not filme:
            return jsonify({'error': 'Filme não encontrado'}), 404

        data = request.json
        if 'titulo' in data:
            filme.titulo = data['titulo']
        if 'ano' in data:
            filme.ano = data['ano']
        if 'genero' in data:
            filme.genero = data['genero']
        if 'descricao' in data:
            filme.descricao = data['descricao']

        db.session.commit()
        return jsonify(filme.to_dict()), 200
    except Exception as e:
        logging.error("Erro ao editar filme: %s", e, exc_info=True)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@movie_bp.route('/<int:id>', methods=['DELETE'])
def deletar_filme(id):
    """Rota para deletar um filme existente."""
    try:
        filme = Filme.query.get(id)
        if not filme:
            return jsonify({'error': 'Filme não encontrado'}), 404

        db.session.delete(filme)
        db.session.commit()
        return jsonify({'message': 'Filme deletado com sucesso'}), 200
    except Exception as e:
        logging.error("Erro ao deletar filme: %s", e, exc_info=True)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Função para registrar as rotas
def register_routes(app):
    app.register_blueprint(movie_bp, url_prefix='/api/filmes')
