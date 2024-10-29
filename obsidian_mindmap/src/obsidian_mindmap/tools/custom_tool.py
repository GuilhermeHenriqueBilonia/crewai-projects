from crewai_tools import BaseTool, SerperDevTool

search_tool = SerperDevTool()

class HumanTool(BaseTool):
    name: str = "Human interact"
    description: str = (
        "Fazer perguntas ao usuário para coletar informações"
    )

    def _run(self, argument: str) -> str:
        # Implementation goes here
        print(argument)
        res = input(f"{argument} \n")
        return res


