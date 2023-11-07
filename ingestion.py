import os
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone

from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

import pinecone
from consts import PINECONE_INDEX_NAME

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV_REGION"]
)


def ingest_chain(file) -> None:
    loader = TextLoader(file)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()

    # First, check if our index already exists. If it doesn't, we create it
    if PINECONE_INDEX_NAME not in pinecone.list_indexes():
        # we create a new index
        pinecone.create_index(name=PINECONE_INDEX_NAME, metric="cosine", dimension=1536)
    # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
    docsearch = Pinecone.from_documents(docs, embeddings, index_name=PINECONE_INDEX_NAME)
    print(docsearch)
    print(docs[0].page_content)
    print("*******Added to Pinecone Vector*******")


if __name__ == '__main__':
    ingest_chain("user/account.txt")

