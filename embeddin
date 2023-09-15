import pandas as pd
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocEmbedding:

    def __init__(self, file_path='./docent/whiskey.txt', openai_api_key="YOUR_ACTUAL_OPENAI_API_KEY", model_name="ada-002"):
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.documents = self.load_data_from_txt(file_path)
        self.docs = self.split_docs()
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key, model_name=self.model_name)
        self.db = self.create_chroma_from_docs()

    def load_data_from_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            documents = file.readlines()
        return documents

    def split_docs(self, chunk_size=500, chunk_overlap=40):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_documents(self.documents)

    def create_chroma_from_docs(self):
        db = Chroma.from_documents(self.docs, self.embeddings)
        return db

    def similarity_search(self, query):
        return self.db.similarity_search(query)

    def similarity_search_with_score(self, query, k=1):
        return self.db.similarity_search_with_score(query, k=k)

    def persist_chroma(self, persist_directory="chroma_db"):
        return Chroma.from_documents(documents=self.docs, embedding=self.embeddings, persist_directory=persist_directory)

# Usage
doc_embed = DocEmbedding()
query_result = doc_embed.similarity_search("give information about {}")
print(query_result)

