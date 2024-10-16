from datetime import date
from textwrap import dedent
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import CalbackStep, CustomHandler, VerificarSqlQuery, search_tool, HumanTool, IntegrarCnpjTool,scrap_ibge, scrap_documentacao
import streamlit as st

# Uncomment the following line to use an example of a custom tool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

def step_callback(output):
	"""Example of a step callback function"""
	texts = {
		"pesquisador_task": "Pesquisando códigos IBGE...",
		"transformador_task": "Transformando dados...",
		"integrador_task": "buscando dados da receita...",
		"dba_task": "Buscando CNPJs da base de dados do cliente...",
		"consultor_task": "Gerando texto final..."
	}
	with st.status(texts[output.name]):
		raw = f'{output.agent}: {output.raw}'
		st.session_state.messages.append({"role": "assistant", "content": raw})
		st.chat_message("assistant").markdown(raw)


@CrewBase
class ReceitaCrmCrew():
	"""TaianeViagens crew"""
	
	# @agent
	# def supervisor(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['supervisor'],
   	# 		backstoty=dedent(
	# 			f"Data Atual: {str(date.today().strftime('%d/%m/%Y'))}"
    # 			f"{self.agents_config['supervisor']['backstory']}"
    # 		),
    #   		# tools=[HumanTool()],
    #     	callbacks=[CustomHandler("supervisor")],
	# 		verbose=True,
   	# 		allow_delegation=True
	# 	)
  
	# @agent
	# def atendente(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['atendente'],
   	# 		backstoty=dedent(
	# 			f"Data Atual: {str(date.today().strftime('%d/%m/%Y'))}"
    # 			f"{self.agents_config['atendente']['backstory']}"
    # 		),
    #   		# tools=[HumanTool()],
	# 		step_callback=CalbackStep,
    #     	callbacks=[CustomHandler("supervisor")],
	# 		verbose=True
	# 	)
  
	@agent
	def pesquisador(self) -> Agent:
		return Agent(
			config=self.agents_config['pesquisador'],
   			backstoty=dedent(
				f"Data atual: {date.today()}"
    			f"{self.agents_config['pesquisador']['backstory']}"
    		),
			tools=[scrap_ibge],
			verbose=True
		)

	@agent
	def transformador(self) -> Agent:
		return Agent(
			config=self.agents_config['transformador'],
			backstory=dedent(
				f"Data Atual: {str(date.today().strftime('%d/%m/%Y'))}"
    			f"{self.agents_config['transformador']['backstory']}"
    		),
			verbose=True,
			
		)
  
	@agent
	def integrador(self) -> Agent:
		return Agent(
			config=self.agents_config['integrador'],
			verbose=True,
			tools=[IntegrarCnpjTool()]
		)
  
	@agent
	def dba(self) -> Agent:
		return Agent(
			config=self.agents_config['dba'],
			verbose=True,
			tools=[VerificarSqlQuery()]
		)
  
	@agent
	def consultor(self) -> Agent:
		return Agent(
			config=self.agents_config['consultor'],
			verbose=True,

		)

	@task
	# def atendente_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['atendente_task'],
	# 		human_input=True,			
	# 		callback=[CustomHandler("supervisor")]
	# 	)

	@task
	def pesquisador_task(self) -> Task:
		return Task(
			config=self.tasks_config['pesquisador_task'],
   			callback=step_callback
		)
  
	@task
	def transformador_task(self) -> Task:
		return Task(
			config=self.tasks_config['transformador_task'],
   			callback=step_callback
		)
  
	@task
	def integrador_task(self) -> Task:
		return Task(
			config=self.tasks_config['integrador_task'],
   			callback=step_callback
		)
  
	@task
	def dba_task(self) -> Task:
		return Task(
			config=self.tasks_config['dba_task'],
   			callback=step_callback
		)
  
	@task
	def consultor_task(self) -> Task:
		return Task(
			config=self.tasks_config['consultor_task'],
   			callback=step_callback
		)

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
  
  
