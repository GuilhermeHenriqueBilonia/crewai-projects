import streamlit as st

from busca_cnpjs.src.busca_cnpjs.crew import ReceitaCrmCrew


st.session_state.messages = []


# Inicializa o estado da sessão se ainda não estiver definido
if "status_text" not in st.session_state:
    st.session_state["status_text"] = "Iniciando a tarefa..."


def step_callback(output):
	"""Example of a step callback function"""
	texts = {
		"pesquisador_task": "Pesquisando códigos IBGE...",
		"transformador_task": "Transformando dados...",
		"integrador_task": "buscando dados da receita...",
		"dba_task": "Buscando CNPJs da base de dados do cliente...",
		"consultor_task": "Gerando texto final..."
	}
	st.session_state["status_text"] = texts[output.name]
	# with st.status(texts[output.name]):
	# 	raw = f'{output.agent}: {output.raw}'
	# 	st.session_state.messages.append({"role": "assistant", "content": raw})
	# 	st.chat_message("assistant").markdown(raw)



if inp := st.chat_input('Filtros desejados', key="principal_input"):
    st.session_state.status_text = 'Iniciando pesquisa...'
    st.session_state.messages.append({"role": "user", "content": inp})
    st.chat_message("user").markdown(inp)
    with st.spinner(st.session_state["status_text"]):
        result = ReceitaCrmCrew().crew().kickoff(inputs={"filters": inp})
        st.session_state.messages.append({"role": "user", "content":result })
        st.chat_message("assistant").markdown(result)

    