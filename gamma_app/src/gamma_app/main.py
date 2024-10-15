#!/usr/bin/env python
import sys
from crew import GammaAppCrew
import streamlit as st

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    topic = input("Sobre qual tópico você quer criar uma apresentação? \n")
    inputs = {
        'topic': topic
    }
    GammaAppCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        GammaAppCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        GammaAppCrew().crew().replay(task_id=sys.argv[1])

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
        GammaAppCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

# Title
st.title("Gerar apresentação")


# Text Inputs

# st.write('Vamos montar uma apresentação? descreva o tema e pontos importantes para que eu consiga te ajudar')
st.chat_message('assistant').write('Vamos montar uma apresentação? descreva o tema e pontos importantes para que eu consiga te ajudar')

st.session_state.messages = []

if inp := st.chat_input('Tema e informação importante', key="principal_input"):
    st.session_state.messages.append({"role": "user", "content": inp})
    st.chat_message("user").markdown(inp)
    with st.spinner("Gerando apresentação..."):
        result = GammaAppCrew().crew().kickoff(inputs={"topic": inp})
        st.session_state.messages.append({"role": "user", "content":result })
        st.chat_message("assistant").markdown(result)

    