# pip install chainlit

import chainlit as cl

@cl.on_message
async def main(message: str):
    await cl.Message(content=message).send()

#chainlit run 01_chainlit_demo.py -w
