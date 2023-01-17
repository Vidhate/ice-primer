from ice.recipe import recipe

def make_verification_prompt(question: str, answer: str) -> str:

	prompt = f"""Consider the question: {question}
Potential answer: "{answer}"

Is the potential answer above correct? Say "A: Yes" or "A: No".
A:"""
	return prompt


async def verify_answer(question: str, answer: str) -> str:

	prompt = make_verification_prompt(question, answer)
	probs, _ = await recipe.agent().classify(prompt=prompt, choices=(" Yes", " No"))
	return probs.get(" Yes", 0.0)

recipe.main(verify_answer)