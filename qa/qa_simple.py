from ice.recipe import recipe


def make_qa_prompt(question: str) -> str:
    return f"""Answer the following question:

Question: "{question}"
Answer: "
""".strip()


async def answer(question: str = "Tell me 5 best places to visit in the US."):
    prompt = make_qa_prompt(question)
    answer = await recipe.agent().complete(prompt=prompt, stop='"')
    return answer


recipe.main(answer)