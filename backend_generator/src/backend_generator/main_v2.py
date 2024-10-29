#!/usr/bin/env python
import sys
from crew_2 import BackendCrew
import streamlit as st

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    topic = input("Especifique o nome da tabela e os campos que você precisa, incluindo os tipos de dados. \n")
    inputs = {
        'topic': topic
    }
    BackendCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        BackendCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        BackendCrew().crew().replay(task_id=sys.argv[1])

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
        BackendCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    result = BackendCrew().crew().kickoff(inputs={'topic': message.content})

    # Send a response back to the user
    await cl.Message(
        content=f"{result}",
        author="assistant"
    ).send()