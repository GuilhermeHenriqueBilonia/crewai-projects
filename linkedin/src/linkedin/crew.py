from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from linkedin.tools.custom_tool import search_tool

# Uncomment the following line to use an example of a custom tool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class LinkedinCrew():
	"""TaianeViagens crew"""

	@agent
	def pesquisador(self) -> Agent:
		return Agent(
			config=self.agents_config['pesquisador'],
			tools=[search_tool], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def resumidor(self) -> Agent:
		return Agent(
			config=self.agents_config['resumidor'],
			verbose=True,
			
		)

	@task
	def pesquisar(self) -> Task:
		return Task(
			config=self.tasks_config['pesquisador_task'],
		)

	@task
	def resumir(self) -> Task:
		return Task(
			config=self.tasks_config['resumidor_task'],
			output_file='linkedin.md'
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