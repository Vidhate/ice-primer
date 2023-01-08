from ice.recipes.primer.debate.utils import *


def render_debate_prompt(agent_name: str, debate: Debate, turns_left: int) -> str:
    prompt = f"""
You are {agent_name}. There are {turns_left} turns left in the debate. You are trying to win the debate using reason and evidence. Don't repeat yourself. No more than 1-2 sentences per turn.

{render_debate(debate, agent_name)}
You: "
""".strip()
    return prompt


def judge_prompt_background_qa(question: str, debate_string: str = "") -> str:

    if debate_string:
        background=f'For the question "{question}", a debate takes place between Alice and Bob. Alice is in favor of the question and Bob is against it. The debate proceeds as follows\n"{debate_string}"'
        judge_question="Who won this debate? Answer in a single word, Alice, Bob or None."
        return background, judge_question

    else:
        background=f'For the question "{question}", a debate takes place between Alice and Bob. Alice is in favor of the question and Bob is against it.'
        judge_question="Based on the question, who will likely win this debate? Answer in a single word, Alice, Bob or None."
        return background, judge_question