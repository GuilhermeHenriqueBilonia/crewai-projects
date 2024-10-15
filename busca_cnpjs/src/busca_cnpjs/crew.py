from datetime import date
from textwrap import dedent
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import CalbackStep, CustomHandler, VerificarSqlQuery, search_tool, HumanTool, IntegrarCnpjTool,scrap_ibge, scrap_documentacao

# Uncomment the following line to use an example of a custom tool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

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
  
	@agent
	def atendente(self) -> Agent:
		return Agent(
			config=self.agents_config['atendente'],
   			backstoty=dedent(
				f"Data Atual: {str(date.today().strftime('%d/%m/%Y'))}"
    			f"{self.agents_config['atendente']['backstory']}"
    		),
      		# tools=[HumanTool()],
			step_callback=CalbackStep,
        	callbacks=[CustomHandler("supervisor")],
			verbose=True
		)
  
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
	def atendente_task(self) -> Task:
		return Task(
			config=self.tasks_config['atendente_task'],
			human_input=True,			
			callback=[CustomHandler("supervisor")]
		)

	@task
	def pesquisar(self) -> Task:
		return Task(
			config=self.tasks_config['pesquisador_task']
		)
  
	@task
	def transformar(self) -> Task:
		return Task(
			config=self.tasks_config['transformador_task'],
		)
  
	@task
	def integrar(self) -> Task:
		return Task(
			config=self.tasks_config['integrador_task']
		)
  
	@task
	def dba_task(self) -> Task:
		return Task(
			config=self.tasks_config['dba_task']
		)
  
	@task
	def consultor_task(self) -> Task:
		return Task(
			config=self.tasks_config['consultor_task']
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TaianeViagens crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			verbose=True,
			language='pt-br',
			memory=True,
			manager_agent=Agent(
				config=self.agents_config['supervisor'],
				backstoty=dedent(
					f"Data Atual: {str(date.today().strftime('%d/%m/%Y'))}"
					f"{self.agents_config['supervisor']['backstory']}"
				),
				# tools=[HumanTool()],
				step_callback=CalbackStep,
				callbacks=[CustomHandler("supervisor")],
				verbose=True,
				allow_delegation=True
			),
			manager_callbacks=[CustomHandler("supervisor")]
			
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
  
  
