import os
import logfire
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")

logfire.configure(token=LOGFIRE_TOKEN)

app = Flask(__name__)
logfire.instrument_flask(app)

pessoas = [ 
    {"id":1, "nome": "Pedro", "idade": 30},
    {"id":2, "nome": "Paulo", "idade": 25},
    {"id":3, "nome": "Maria", "idade": 48},
    {"id":4, "nome": "Sandra", "idade": 17},
    {"id":5, "nome": "Renato", "idade": 29}
]

# GET
@app.route("/pessoas", methods=['GET'])
def listar_pessoas():
    return pessoas, 200

# POST
@app.route("/pessoas", methods=['POST'])
def adicionar_pessoa():
    nova_pessoa = request.json
    nova_pessoa['id'] = len(pessoas) + 1
    pessoas.append(nova_pessoa)
    return nova_pessoa, 201

# PUT
@app.route("/pessoas/<int:id>", methods=['PUT'])
def atualizar_pessoa(id):
    pessoa = next((p for p in pessoas if p['id'] == id), None)
    if pessoa:
        dados_atualizados = request.json
        pessoa.update(dados_atualizados)
        return pessoa, 200
    return {"erro":"Pessoa nao encontrada"}, 404

# DELETE
@app.route("/pessoas/<int:id>", methods=['DELETE'])
def remover_pessoa(id):
    global pessoas  # Declare 'pessoas' como uma variável global
    pessoa = next((p for p in pessoas if p['id'] == id), None)
    if pessoa:
        pessoas = [p for p in pessoas if p['id'] != id]
        return {"mensagem": "Pessoa removida com sucesso"}, 200
    return {"erro": "Pessoa não encontrada"}, 404

if __name__ == "__main__":
    app.run(debug=True)