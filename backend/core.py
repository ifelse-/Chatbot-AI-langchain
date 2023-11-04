import os
from typing import List, Dict, Any
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
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
    chat = ChatOpenAI(verbose=True, temperature=0)

    qa = RetrievalQA.from_chain_type(
        llm=chat,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True
    )

    return qa({"query": query})


if __name__ == '__main__':
    print(run_llm(query=""))
