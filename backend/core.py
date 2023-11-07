import os
from typing import List, Dict, Any
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationSummaryBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from consts import PINECONE_INDEX_NAME
import pinecone

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV_REGION"]
)


def run_llm(query: str) -> Any:
    embeddings = OpenAIEmbeddings()
    docsearch = Pinecone.from_existing_index(
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key='question',
        output_key='answer',
        return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0),
        docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True
    )

    # chat = ChatOpenAI(verbose=True, temperature=0)
    # qa = RetrievalQA.from_chain_type(
    #     llm=chat,
    #     chain_type="stuff",
    #     retriever=docsearch.as_retriever(),
    #     return_source_documents=True
    # )
    result = qa({"question": query})
    return result

