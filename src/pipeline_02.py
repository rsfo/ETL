import os
import time
import requests
import logging
import logfire
from datetime import datetime
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuração do Logfire
logfire.configure()
logging.basicConfig(handlers=[logfire.LogfireLoggingHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Banco de Dados
from database import Base, BitcoinPreco

load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def criar_tabela():
    Base.metadata.create_all(engine)
    logger.info("Tabela criada/verificada com sucesso!")

def extrair_dados_bitcoin():
    url = 'https://api.coinbase.com/v2/prices/spot'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        logger.error(f"Erro na API: {resposta.status_code}")
        return None

def tratar_dados_bitcoin(dados_json):
    valor = float(dados_json['data']['amount'])
    criptomoeda = dados_json['data']['base']
    moeda = dados_json['data']['currency']
    timestamp = datetime.now()

    return {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }

def salvar_dados_postgres(dados):
    session = Session()
    try:
        novo_registro = BitcoinPreco(**dados)
        session.add(novo_registro)
        session.commit()
        logger.info(f"[{dados['timestamp']}] Dados salvos no PostgreSQL!")
    except Exception as ex:
        logger.error(f"Erro ao inserir dados no PostgreSQL: {ex}")
        session.rollback()
    finally:
        session.close()

# Servidor Web
app = Flask(__name__)

@app.route("/")
def home():
    return "Bitcoin ETL rodando no Render!"

if __name__ == "__main__":
    criar_tabela()
    logger.info("Iniciando ETL com atualização a cada 15 segundos...")

    # Definir a porta correta para Render
    port = int(os.environ.get("PORT", 10000))

    # Executar ETL em um loop separado
    from threading import Thread
    
    def run_etl():
        while True:
            try:
                dados_json = extrair_dados_bitcoin()
                if dados_json:
                    dados_tratados = tratar_dados_bitcoin(dados_json)
                    logger.info(f"Dados Tratados: {dados_tratados}")
                    salvar_dados_postgres(dados_tratados)
                time.sleep(15)
            except KeyboardInterrupt:
                logger.info("Processo interrompido pelo usuário. Finalizando...")
                break
            except Exception as e:
                logger.error(f"Erro durante a execução: {e}")
                time.sleep(15)
    
    etl_thread = Thread(target=run_etl)
    etl_thread.start()

    # Iniciar servidor Flask
    app.run(host="0.0.0.0", port=port)