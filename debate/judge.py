import sys
from ice.recipe import recipe

from debate import debate
from prompt import judge_prompt_background_qa

sys.path.append("../qa/")
from qa import answer


async def judge(question: str = "Is it better to be in a relationship than be alone?") -> str:

	background, qa_question = judge_prompt_background_qa(question)
	pre_judge = await answer(context=background, question=qa_question)

	debate_string = await debate(question)
	
	background, qa_question = judge_prompt_background_qa(question, debate_string)
	post_judge = await answer(context=background, question=qa_question)
	
	return pre_judge, post_judge


async def analyse_pre_post(question: str = "") -> str:

	questions_pool = await answer(context="", question="Give me 5 questions that will make for a good debate")
	questions_pool = questions_pool.split('\n')
	judge_match = []
	for question in questions_pool:

		print(f"Sending question : {question[3:]}")
		pre_judge, post_judge = await judge(question[3:])
		print(pre_judge, post_judge)
		judge_match.append(pre_judge==post_judge)

	return judge_match

# recipe.main(judge)
recipe.main(analyse_pre_post)