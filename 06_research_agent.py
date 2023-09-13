# pip install arxiv
from langchain import OpenAI
from langchain.agents import initialize_agent, AgentExecutor
from langchain.agents import load_tools, initialize_agent, AgentType

import chainlit as cl

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

@cl.on_chat_start
def start():
    llm = OpenAI(temperature=0.5, streaming=True)
    tools = load_tools(
        ["arxiv"]
    )

    agent_chain = initialize_agent(
        tools,
        llm,
        max_iterations=3,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,  ### IMPORTANT
    )

    cl.user_session.set("agent", agent_chain)


@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    await cl.make_async(agent.run)(message, callbacks=[cl.LangchainCallbackHandler()])

# chainlit run 06_research_agent.py -w