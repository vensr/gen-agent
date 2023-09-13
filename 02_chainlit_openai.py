# pip install chainlit
# pip install openai
# pip install dotenv

import chainlit as cl
import openai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

@cl.on_message
async def main(message: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role":"assistant","content": "you are a helpful assistant"},
            {"role":"user","content": message}
        ],
        temperature=1
    )
    print(response)
    await cl.Message(content=str(response["choices"][0]["message"]["content"])).send()

#chainlit run 02_chainlit_openai.py -w
