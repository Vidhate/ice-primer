from ice.paper import Paper
from ice.paper import Paragraph
from ice.recipe import recipe
from ice.utils import map_async
import sys

sys.path.append("../qa/")
from qa import answer

def make_prompt(paragraph: Paragraph, question: str) -> str:
	return f"""
Here is a paragraph from a research paper: "{paragraph}"

Question: Does this paragraph answer the question '{question}'? Say Yes or No.
Answer:""".strip()

async def classify_paragraph(paragraph: Paragraph, question: str) -> float:

	choice_probs, _ = await recipe.agent().classify(prompt=make_prompt(paragraph, question), choices=(" Yes"," No"))
	return choice_probs.get(" Yes", 0.0)

async def get_relevant_paragraphs(paper: Paper, question: str, top_n: int = 3):
	probs = await map_async(
		paper.paragraphs, lambda par: classify_paragraph(par, question)
	)
	sorted_pairs = sorted(zip(probs, paper.paragraphs), key=lambda x : x[0], reverse=True)
	return [par for probs,par in sorted_pairs[:top_n]]

async def answer_for_paper(paper: Paper, question: str, top_n: int = 3):

	relevant_paragraphs = await get_relevant_paragraphs(paper, question)
	context = "\n\n".join(map(str, relevant_paragraphs))
	return await answer(context = context, question = question)

recipe.main(answer_for_paper)