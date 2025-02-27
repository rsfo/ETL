import os
import logfire
from dotenv import load_dotenv
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Pessoas

# Carrega variáveis de ambiente
load_dotenv()

LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")

logfire.configure(token=LOGFIRE_TOKEN)

app = Flask(__name__)
logfire.instrument_flask(app)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Conexão com o banco de dados
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Inicializando o Flask
app = Flask(__name__)
logfire.instrument_flask(app)

# Função para criar a tabela
def criar_tabela():
    Base.metadata.create_all(engine)
    print("Tabela criada/verificada com sucesso!")

# Rotas CRUD
@app.route("/pessoas", methods=['GET'])
def listar_pessoas():
    session = Session()
    pessoas = session.query(Pessoas).all()
    return [{"id": p.id, "nome": p.nome, "idade": p.idade, "timestamp": p.timestamp} for p in pessoas], 200

@app.route("/pessoas", methods=['POST'])
def adicionar_pessoa():
    nova_pessoa = request.json
    pessoa = Pessoas(nome=nova_pessoa['nome'], idade=nova_pessoa['idade'])
    session = Session()
    session.add(pessoa)
    session.commit()
    return {"id": pessoa.id, "nome": pessoa.nome, "idade": pessoa.idade}, 201

@app.route("/pessoas/<int:id>", methods=['PUT'])
def atualizar_pessoa(id):
    session = Session()
    pessoa = session.query(Pessoas).filter(Pessoas.id == id).first()
    if pessoa:
        dados_atualizados = request.json
        pessoa.nome = dados_atualizados.get('nome', pessoa.nome)
        pessoa.idade = dados_atualizados.get('idade', pessoa.idade)
        session.commit()
        return {"id": pessoa.id, "nome": pessoa.nome, "idade": pessoa.idade}, 200
    return {"erro": "Pessoa não encontrada"}, 404

@app.route("/pessoas/<int:id>", methods=['DELETE'])
def remover_pessoa(id):
    session = Session()
    pessoa = session.query(Pessoas).filter(Pessoas.id == id).first()
    if pessoa:
        session.delete(pessoa)
        session.commit()
        return {"mensagem": "Pessoa removida com sucesso"}, 200
    return {"erro": "Pessoa não encontrada"}, 404

if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)