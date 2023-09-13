# Add Streaming
# Add Generating Message
# Add Backend Context - understand what is running behind the scenes

# pip install langchain

import chainlit as cl
from dotenv import load_dotenv, find_dotenv
from langchain import PromptTemplate, OpenAI, LLMChain

load_dotenv(find_dotenv())

template = """Question: {question}
Answer: Let's think of the answer step by step."""

@cl.on_chat_start
def main():
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(
        prompt=prompt,
        llm=OpenAI(temperature=1, streaming=True),
        verbose=True
    )
    cl.user_session.set("llm_chain", llm_chain)
    
@cl.on_message
async def main(message: str):
    llm_chain = cl.user_session.get("llm_chain")
    response = await llm_chain.acall(message, callbacks = [cl.AsyncLangchainCallbackHandler()])
    await cl.Message(content=response["text"]).send()

#chainlit run 03_chainlit_langchain.py -w
