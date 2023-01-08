from utils import *
from prompt import *
from ice.recipe import recipe
from ice.recipes.primer.debate.types import *

async def turn(debate_tracker: Debate, agent_name: Name, turns: int, debate_string: str):
	
	prompt = render_debate_prompt(agent_name, debate_tracker, turns)
	response = await recipe.agent().complete(prompt=prompt, stop='"')
	debate_tracker.append(Turn([agent_name,response]))
	debate_string+=f"{agent_name}: {response}\n"
	return debate_string, debate_tracker

async def debate(question: str = "Should we legalize all drugs?", turns: int = 5):

	debate_tracker = initialize_debate(question)
	debate_string = ""

	previous_answer = {'Alice':"", 'Bob':""}
	for i in range(turns):
		for name in ["Alice", "Bob"]:
			debate_string, debate_tracker = await turn(debate_tracker, name, turns-i, debate_string)
			# If AI repeats itself, kill the debate without caring about number of turns left
			if previous_answer.get(debate_tracker[-1][0], "") == debate_tracker[-1][1]:
				debate_tracker.pop()
				debate_string = '\n'.join(debate_string.split('\n')[:-2])
				return debate_string
			previous_answer[debate_tracker[-1][0]] = debate_tracker[-1][1]

	return debate_string

# recipe.main(debate)