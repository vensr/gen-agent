# pip install pypdf

# document loaders from langchain
from langchain.document_loaders import PyPDFLoader, TextLoader

# chunks splitter of document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# embeddings from openai
from langchain.embeddings.openai import OpenAIEmbeddings

# chroma vector store
from langchain.vectorstores import Chroma

# retrieval chain
from langchain.chains import RetrievalQAWithSourcesChain

# openai chat model
from langchain import OpenAI

import chainlit as cl
from chainlit.types import AskFileResponse

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, length_function = len, is_separator_regex = False)
embeddings = OpenAIEmbeddings()

welcome_message = """Welcome to the local document search demo! To get started:
1. Upload a PDF or text file
2. Ask any question you like, contained in the file
"""

# process the input file
# 1. Read the file
# 2. split the chunks and then label them as sources

def process_file(file: AskFileResponse):
    import tempfile

    if file.type == "text/plain":
        Loader = TextLoader
    elif file.type == "application/pdf":
        Loader = PyPDFLoader

    with tempfile.NamedTemporaryFile() as tempfile:
        tempfile.write(file.content)
        tempfile.read()
        loader = Loader(tempfile.name)
        documents = loader.load_and_split(text_splitter=text_splitter)        
        return documents

# perform similarity search
# 1. Process the uploaded file
# 2. embed the chunks and persist them to the vector db
# 3. return the search_doc

def get_doc_search(file: AskFileResponse):
    docs = process_file(file)
    print(docs)

    # Save data in the user session
    cl.user_session.set("docs", docs)

    # Create a unique namespace for the file

    search_doc = Chroma.from_documents(
        docs, embeddings
    )
    return search_doc


@cl.on_chat_start
async def start():
    
    # say hello message on the UI, ask for file upload
    await cl.Message(content="Hi, I am your Generative Agent. I can help you answer questions in your local docs.").send()
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content=welcome_message,
            accept=["text/plain", "application/pdf"],
            max_size_mb=20,
            timeout=180,
        ).send()

    print(files)
    file = files[0]

    msg = cl.Message(content=f"Processing `{file.name}`...")
    await msg.send()

    # process the document and persist it in the vector store
    search_doc = await cl.make_async(get_doc_search)(file)

    # use langchain to perform search on vector db
    # append results of search as context to chatgpt
    # return the results
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        OpenAI(temperature=1, streaming=True),
        chain_type="stuff",
        retriever=search_doc.as_retriever(max_tokens_limit=4037),
    )

    # Let the user know that the system is ready
    msg.content = f"`{file.name}` is now processed. I can answer your questions now!"
    await msg.update()

    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message):
    # fetch the chain
    chain = cl.user_session.get("chain")

    # call LLM to get back the response
    response = await chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # print(response)
    answer = response["answer"]
    await cl.Message(content=answer).send()

# chainlit run 05_local_file_bot.py -w
