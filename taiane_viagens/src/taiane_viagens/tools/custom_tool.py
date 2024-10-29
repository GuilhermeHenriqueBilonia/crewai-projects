from pydantic import Field
import json
from typing import Callable, Optional
from crewai_tools import BaseTool, SerperDevTool, ScrapeWebsiteTool
import requests
import streamlit as st

test = ScrapeWebsiteTool(website_url='https://google.com')
search_tool = SerperDevTool()

def _print_func(argument: str) -> None:
    print(argument)

class HumanTool(BaseTool):
    name: str = "Human interact"
    description: str = (
        "Fazer perguntas ao usuário para coletar informações"
    )

    def _run(
        self,
        query: str
    ) -> str:
        """Use the Human input tool."""
        res = input(query)
        return res
    
   

 
class BuscarPassagemTool(BaseTool):
    name: str = "Buscar Passagem"
    description: str = (
        "Buscar passagem aérea"
    )

    def _run(self, argument: str) -> str:
        search = requests.post(
                            url='https://apistart.buscamilhas.com/login',
                            json={"login":"projetotaiane@gmail.com","senha":"Xkypvjhi"}
                          )
        jsn = search.json()
        token = jsn['token']
        jsonToSend = json.loads(argument);
        if 'argument' in argument:
            jtonToSend = argument['argument']
        search = requests.post(url='https://apistart.buscamilhas.com/busca',
                            headers={
                                'Authorization': f'Bearer {token}'
                            },
                            json=jsonToSend
                            )
        results = search.json()
        # rawData = pd.read_csv(io.StringIO(results.decode('utf-8')))
        # Itera sobre os voos
        resultados = []
        print('results', results)
        for voo_id, voo_info in results["Voos"].items():
            formatted_data = {}
            sentido = voo_info["Sentido"].lower()
            
            # Extraindo informações necessárias
            partida_data, partida_hora = voo_info["Embarque"].split()  # "15/10/2024 23:35"
            chegada_data, chegada_hora = voo_info["Desembarque"].split()
        
            # Calculando o valor total
            total_value = voo_info["Valor"]["Adulto"] + voo_info["Valor"]["Crianca"] + voo_info["Valor"]["TaxaEmbarque"]
            
            formatted_data = {
                "Sentido": sentido,
                "companhia": voo_info["Companhia"],
                "origem": voo_info["Origem"],
                "destino": voo_info["Destino"],
                "data_de_partida": partida_data,
                "horario_de_partida": partida_hora,
                "data_de_chegada": chegada_data,
                "horario_de_chegada": chegada_hora,
                "conexoes": voo_info["NumeroConexoes"],
                "Valor total": total_value
            }
            resultados.append(formatted_data)

        return resultados


