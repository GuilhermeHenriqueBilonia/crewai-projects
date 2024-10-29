from crewai_tools import BaseTool, SerperDevTool, tool
import chainlit as cl
from chainlit import run_sync
from humanlayer import HumanLayer
from dotenv import load_dotenv

load_dotenv()

hl = HumanLayer.cloud(verbose=True)

search_tool = SerperDevTool()

class HumanTool(BaseTool):
    name: str = "Human interact"
    description: str = (
        "Fazer perguntas ao usuário para coletar informações"
    )

    def _run(self, argument: str) -> str:
        # Implementation goes here
        human_response  = run_sync( 
                                   cl.AskUserMessage(content=f"{argument}",
                                        author="assistant"
                                    )
                                   .send()
                                )
        if human_response:
            return human_response["output"]
        
       
@tool
@hl.human_as_tool() 
def humanTool_v2(arguments) -> str:
    """ Implementation goes here """
    print('aqui')
    # human_response  = run_sync( 
    #                            cl.AskUserMessage(content=f"{argument}",
    #                                 author="assistant"
    #                             )
    #                            .send()
    #                         )
    # if human_response:
    #     return human_response["output"]

