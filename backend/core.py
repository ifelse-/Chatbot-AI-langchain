import os
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


def run_llm(query: str):
    embeddings = OpenAIEmbeddings()
    docsearch = Pinecone.from_existing_index(
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME)
    chat = ChatOpenAI(verbose=True, temperature=0)
    qa = RetrievalQA.from_chain_type(
        llm=chat,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=False
    )
    return qa({"query" : query})


if __name__ == '__main__':
    print(run_llm(query="Is it a good idea to buy a TV $3000 this month with the money in a bank account?"))
