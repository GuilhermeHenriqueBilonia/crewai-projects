from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import HumanTool, humanTool_v2
import streamlit as st

# Uncomment the following line to use an example of a custom tool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


# def step_callback(output):
# 	"""Example of a step callback function"""
# 	texts = {
# 		"gerar_requisitos": "REQUISITOS",
# 		"gerar_domain": "DOMAIN",
# 		"gerar_sql": "SCRIPT SQL",
# 		"gerar_configuration": "CONFIGURATION",
# 		"gerar_dto": "DTO",
# 		"gerar_service": "SERVICE",
# 		"gerar_commands": "COMMANDS",
# 	}
# 	with st.status(texts[output.name]):
# 		raw = f'{output.agent}: {output.raw}'
# 		st.session_state.messages.append({"role": "assistant", "content": raw})
# 		st.chat_message("assistant").markdown(raw)


@CrewBase
class BackendCrew():
	"""BackendCrew crew"""
 
  
	@agent
	def requisitos(self) -> Agent:
		return Agent(
			config=self.agents_config['requisitos'],
			tools=[humanTool_v2],
			verbose=True,
		)
  
	@agent
	def domain(self) -> Agent:
		return Agent(
			config=self.agents_config['domain'],
			verbose=True,
		)
  
	@agent
	def dba(self) -> Agent:
		return Agent(
			config=self.agents_config['dba'],
			verbose=True,
		)
	
	@agent
	def configuration(self) -> Agent:
		return Agent(
			config=self.agents_config['configuration'],
			verbose=True,
		)
  
	@agent
	def dto(self) -> Agent:
		return Agent(
			config=self.agents_config['dto'],
			verbose=True,
		)
	
	@agent
	def service(self) -> Agent:
		return Agent(
			config=self.agents_config['service'],
			verbose=True,
		)

	@agent
	def commands(self) -> Agent:
		return Agent(
			config=self.agents_config['commands'],
			verbose=True,
		)
  
	@task
	def gerar_requisitos(self) -> Task:
		return Task(
			config=self.tasks_config['requisitos_task'],
   			# callback=step_callback
		)
  
	@task
	def gerar_domain(self) -> Task:
		return Task(
			config=self.tasks_config['domain_task'],
   			# callback=step_callback
		)
  
	@task
	def gerar_sql(self) -> Task:
		return Task(
			config=self.tasks_config['sql_task'],
   			# callback=step_callback
		)
  
	@task
	def gerar_configuration(self) -> Task:
		return Task(
			config=self.tasks_config['configure_task'],
   			# callback=step_callback
		)
  
	@task
	def gerar_dto(self) -> Task:
		return Task(
			config=self.tasks_config['dto_task'],
   			# callback=step_callback
		)
  
	@task
	def gerar_service(self) -> Task:
		return Task(
			config=self.tasks_config['service_task'],
   			# callback=step_callback
		)
  
	@task
	def gerar_commands(self) -> Task:
		return Task(
			config=self.tasks_config['command_task'],
   			# callback=step_callback
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TaianeViagens crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			manager_agent=Agent(
				config=self.agents_config['supervisor'],
				verbose=True,
			),
			verbose=True,
			
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
  
    
