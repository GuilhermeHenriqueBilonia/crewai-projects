#!/usr/bin/env python
import sys
from crew import ReceitaCrmCrew
import streamlit as st

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'filters': 'Olá'
    }
    ReceitaCrmCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        ReceitaCrmCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ReceitaCrmCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        ReceitaCrmCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


# Title
st.title("Consultas cnpjs da receita por filtros")


# Text Inputs

# st.write('Vamos montar uma apresentação? descreva o tema e pontos importantes para que eu consiga te ajudar')
st.chat_message('assistant').write("""Olá, eu sou a Diana, assistente virtual que vai te ajudar a obter informações sobre CNPJs.
    Para isso, basta informar os filtros que deseja utilizar para a busca.
    
    ## FILTROS DISPONIVEIS ##
    
    atividade_principal_id => Código CNAE
    atividade_secundaria_id => Código CNAE
    atividade_id => Código CNAE (pesquisa na atividade principal e secundária)
    natureza_juridica_id => Código da Natureza Jurídica
    razao_social => Razão Social
    nome_fantasia => Nome Fantasia
    pais_id => Código do País do BACEN
    estado_id => Código IBGE do estado
    cidade_id => Código IBGE da Cidade
    cep => CEP
    situacao_cadastral => Situação cadastral na Receita Federal
    data_situacao_cadastral_de => Data da Situação Cadastral (A partir dessa data) no formato YYYY-MM-DD
    data_situacao_cadastral_ate => Data da Situação Cadastral (Até essa data) no formato YYYY-MM-DD
    porte_id => Id do porte da empresa
    socio_nome => Nome do Sócio
    data_inicio_atividade_de => Data de Inicio de Atividade (A partir dessa data) no formato YYYY-MM-DD
    data_inicio_atividade_ate => Data de Inicio de Atividade Até (Até essa data) no formato YYYY-MM-DD
    
                                   """)

st.session_state.messages = []

st.session_state.status_text = 'Iniciando pesquisa...'

if inp := st.chat_input('Filtros desejados', key="principal_input"):
    st.session_state.status_text = 'Iniciando pesquisa...'
    st.session_state.messages.append({"role": "user", "content": inp})
    st.chat_message("user").markdown(inp)
    with st.spinner("Gerando resultado..."):
        result = ReceitaCrmCrew().crew().kickoff(inputs={"filters": inp})
        st.session_state.messages.append({"role": "user", "content":result })
        st.chat_message("assistant").markdown(result)

    
