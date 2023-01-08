from ice.recipe import recipe

# DEFAULT_CONTEXT = "We're running a hackathon on 9/9/2022 to decompose complex reasoning tasks into subtasks that are easier to automate & evaluate with language models. Our team is currently breaking down reasoning about the quality of evidence in randomized controlled trials into smaller tasks e.g. placebo, intervention adherence rate, blinding procedure, etc."
DEFAULT_CONTEXT = "It is difficult to answer who won since both had equally good arguments. It might be said that Alice had a certain edge since her answers were moer open-minded."

# DEFAULT_QUESTION = "What is happening on 9/9/2022?"
DEFAULT_QUESTION = "Did Alice win or not, answer in Yes, No, Maybe?"

NUM_STEPS = 10


def make_qa_prompt(context: str = "", question: str = "") -> str:
    
    if not question:
        print("No Question found")
        raise Exception

    if context:

        return f"""
Background text: {context}

Answer the following question about the background text above:

Question: "{question}"
Answer: "
""".strip()

    else:
        return f"""
Answer the following question:

Question: "{question}"
Answer: "
""".strip()


def improve_answer_prompt(context: str, answer_prev:str, question: str) -> str:
    return f"""
Background text: "{context}"

Improve the answer to the following question about the background text above, over the previous answer:

Question: "{question}"
Previous answer: "{answer_prev}"
Answer: "
""".strip()


async def answer(
    context: str = DEFAULT_CONTEXT, question: str = DEFAULT_QUESTION, improve: bool = False
) -> str:

    prompt = make_qa_prompt(context, question)
    answer = await recipe.agent().complete(prompt=prompt, stop='"')
    if not improve:
        return answer

    final_answer = f"Let's think step by step."
    # print(answer)

    i=0
    while i<NUM_STEPS:
        prompt = improve_answer_prompt(context, answer, question)
        current_answer = await recipe.agent().complete(prompt=prompt, stop='"')
        # print(current_answer)
        if current_answer==answer:
            final_answer+=f"\n{answer}"
            return final_answer

        answer=current_answer
        
        i+=1

    # print(answer)

    final_answer+=f"\n{answer}"
    return final_answer

# recipe.main(answer)