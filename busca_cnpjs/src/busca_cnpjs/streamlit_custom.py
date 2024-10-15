import asyncio
from textwrap import dedent
import streamlit as st
from busca_cnpjs.src.busca_cnpjs.tools.custom_tool import TrackableAssistantAgent
from crew import ReceitaCrmCrew
from autogen import ConversableAgent
from mem0 import MemoryClient
from dotenv import load_dotenv
import uuid


load_dotenv()

llm_config = {"config_list": [{"model": "gpt-4o-mini", "temperature": 0.4}]}
# Let's first define the assistant agent that suggests tool calls.
atendente_instruct = dedent("""
                          Você é um atendente de uma empresa de pesquisa de CNPJs. Sua função é obter informações do usuário e criar um resumo das informações passadas.
Você é conhecido por sua habilidade de obter informações precisas e relevantes dos usuários de forma humanizada.
Mostre, de uma só vez, TODOS os filtros disponíveis, NUNCA pergunta de um em um.
Após o usuário passar os filtros, pergunte se é só isso. Se sim, siga o fluxo. Se não, pergunte o que ele deseja mudar, depois siga o mesmo fluxo dito.
não é obrigatório ao usuário passar todos os filtros, apenas os que o usuário desejar. Se ele passar todos, não precisa perguntar nada.
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

Você não deve perguntar pro usuário código ibge, id do porte. o usuário responderá sempre com textos. Não se preocupe com isso, um próximo agente fará esse trabalho de ajuste

Quando o usuario mandar os dados, confirme se ele já indicou os filtros que ele deseja e se pode seguir adiante. 
Se sim, responda educadamente com o resumo dos filtros de forna enumerada e, no final, o texto 'FINALIZADO'. 
Se não, pergunte o que ele deseja mudar, depois siga o mesmo fluxo dito.
"""
    )

      # Streamlit UI setup
st.title("💬 Buscar cnpjs") 
# Initialize the message log in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display existing messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input():
    #chat with user
    # create an AssistantAgent instance named "assistant"
    
    assistant = TrackableAssistantAgent(
        name="assistant", llm_config=llm_config, system_message=atendente_instruct, human_input_mode="NEVER",
        
        is_termination_msg=lambda msg: "FINALIZADO" in msg["content"]
        )

    # create a UserProxyAgent instance named "user"
    user_proxy = TrackableAssistantAgent(
        name="user", human_input_mode="ALWAYS", 
        llm_config=False, code_execution_config=False,
        system_message="Se o usuário indicar que já informou os filtros ou que deseja finalizar a conversa, diga 'FINALIZADO'.",
        is_termination_msg=lambda msg: "FINALIZADO" in msg["content"])
    
    # Create an event loop
    result = user_proxy.initiate_chat(
            assistant,
            message=prompt,
        )

    # Run the asynchronous function within the event loop
    final = ReceitaCrmCrew().crew().kickoff(inputs={'filters': result})
    # Display the final result
    result = f"## Here is the Final Result \n\n {final}"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)
    
