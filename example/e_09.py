import os
import logfire
from dotenv import load_dotenv
from datetime import date

load_dotenv()

LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")

logfire.configure(token=LOGFIRE_TOKEN)

logfire.info('Olá, {name}!', name='Mundo')

# Capturar a entrada do usuário dentro do span
with logfire.span('Pergunte ao usuário sua data de nascimento.') as span:
    user_input = input('Qual é a sua data de nascimento [YYYY-mm-dd]? ')
    span.set_attribute("user_input", user_input)  # Adiciona a entrada do usuário no log do span

# Calcular a idade
dob = date.fromisoformat(user_input)
today = date.today()
age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# Registrar a idade nos logs
logfire.info('O usuário forneceu a data de nascimento: {dob}, idade calculada: {age}', dob=dob, age=age)

if __name__ == "__main__": 
    pass