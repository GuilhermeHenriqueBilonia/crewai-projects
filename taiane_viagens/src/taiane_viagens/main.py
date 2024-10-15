#!/usr/bin/env python
from datetime import time
import sys
from taiane_viagens.crew import TaianeViagensCrew
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
        'topic': 'Ola'
    }
    TaianeViagensCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'topic': 'Ola'
    }
    try:
        TaianeViagensCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TaianeViagensCrew().crew().replay(task_id=sys.argv[1])

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
        TaianeViagensCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


run()
# st.set_page_config(
#     layout="wide"
# )

# # Title
# st.title("Taiane")


# # Text Inputs

# st.write('Olá, eu sou a taiane, sua assistente virtual de viagens. Como posso te ajudar hoje?')

# inp = st.chat_input('Digite o que deseja', key="principal_input")

# if inp:
#     result = TaianeViagensCrew().crew().kickoff(inputs={"topic": inp})
#     st.write(result)

#     st.markdown(result, unsafe_allow_html=True)
        

