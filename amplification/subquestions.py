from ice.recipe import recipe
from ice.utils import map_async
import sys
sys.path.append("../qa/")
from qa import answer as qa_answer
from qa_simple import answer as simple_answer

from typing import List


def make_subquestion_prompt(question: str) -> str:
    return f"""Decompose the following question into 2-5 subquestions that would help you answer the question. Make the questions stand alone, so that they can be answered without the context of the original question.

Question: "{question}"
Subquestions:
-""".strip()

def create_context_from_subs(subs) -> str:

    s = """Here is relevant background information:
"""
    subs_context = "\n".join(f"Q:{question}\nA:{answer}" for question, answer in subs)
    return s+subs_context


async def ask_subquestions(
    question: str = "What is the effect of creatine on cognition?",
):
    prompt = make_subquestion_prompt(question)
    subquestions_text = await recipe.agent().complete(prompt=prompt)
    subquestions = [line.strip("- ") for line in subquestions_text.split("\n")]
    return subquestions

async def answer_subquestions(question: str = "What is the effect of creatine on cognition?", depth: int = 1) -> str:

    subquestions = await ask_subquestions(question)
    subanswers = await map_async(subquestions, lambda x : answer_amplified(x, depth))
    return zip(subquestions, subanswers)

async def answer_amplified(question: str = "What is the effect of creatine on cognition?", depth: int = 2) -> str:

    subs = await answer_subquestions(question, depth-1) if depth>0 else []
    result = await qa_answer(create_context_from_subs(subs), question)
    return result

recipe.main(answer_amplified)