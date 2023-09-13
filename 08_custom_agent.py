# pip install arxiv
from langchain import OpenAI
from langchain.agents import initialize_agent, AgentExecutor
from langchain.agents import initialize_agent, AgentType, Tool

import chainlit as cl

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def multiplier(a, b):
    return a * b

def parsing_multiplier(string):
    a, b = string.split(",")
    return multiplier(int(a), int(b))

@cl.on_chat_start
def start():
    llm = OpenAI(temperature=0.5, streaming=True)
    tools = [
        Tool(
            name="Multiplier",
            func=parsing_multiplier,
            description="useful for when you need to multiply two numbers together. The input to this tool should be a comma separated list of numbers of length two, representing the two numbers you want to multiply together. For example, `1,2` would be the input if you wanted to multiply 1 by 2.",
        )
    ]

    agent_chain = initialize_agent(
        tools,
        llm,
        max_iterations=3,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    cl.user_session.set("agent", agent_chain)


@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    await cl.make_async(agent.run)(message, callbacks=[cl.LangchainCallbackHandler()])

# chainlit run 08_custom_agent.py -w
