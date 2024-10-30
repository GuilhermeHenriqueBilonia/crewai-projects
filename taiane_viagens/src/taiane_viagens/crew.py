from datetime import date
from textwrap import dedent
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import BuscarPassagemTool, HumanTool, search_tool
import streamlit as st

def callback_response(response):
	print(response.result)
	st.write(response.result)
	res = st.chat_input("")
	return res
	

@CrewBase
class TaianeViagensCrew():
	"""TaianeViagens crew"""

	@agent
	def analista_aeroportos(self) -> Agent:
		return Agent(
			config=self.agents_config['analista_aeroportos'],
			verbose=True,
   			tools=[search_tool]
			
		)
	
	@agent
	def buscador_passagem(self) -> Agent:
		return Agent(
			config=self.agents_config['buscador_passagem'],
			backstory=dedent(
          		f"TODO ANO DA DATA DE IDA E VOLTA DEVE SER APÓS A Data atual: {date.today()}"
            	f"{self.agents_config['buscador_passagem']['backstory']}"
			),
			verbose=True,
			
		)
  
	@agent
	def agente_viagem(self) -> Agent:
		return Agent(
			config=self.agents_config['agente_viagem'],
			verbose=True,
   			tools=[BuscarPassagemTool()]
			
		)


	# TASKS ------------------------------------------
	@task
	def atendente_task(self) -> Task:
		return Task(
			config=self.tasks_config['atendee_task'],
		)

	@task
	def correcao_task(self) -> Task:
		return Task(
			config=self.tasks_config['correction_task']
		)
  
	@task
	def buscador_passagem_task(self) -> Task:
		return Task(
			config=self.tasks_config['buscador_passagem_task']
		)
  
	@task
	def agente_viagem_task(self) -> Task:
		return Task(
			config=self.tasks_config['agente_viagem_task']
		)

	# CREW ------------------------------------------
	@crew
	def crew(self) -> Crew:
		"""Creates the TaianeViagens crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			language='pt-br',
			memory=True,
			
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
  
TaianeViagensCrew()