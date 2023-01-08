from ice.recipe import recipe


def make_qa_prompt(question: str) -> str:
    return f"""Answer the following question:

Question: "{question}"
Answer: "
""".strip()


async def answer(question: str = "Generate 5 questions that would make for a good debate"):
    prompt = make_qa_prompt(question)
    answer = await recipe.agent().complete(prompt=prompt, stop='"')
    return answer


recipe.main(answer)