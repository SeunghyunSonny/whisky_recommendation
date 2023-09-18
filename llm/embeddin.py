from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader


class DocEmbedding:

    def __init__(self, directory_path='/data/docent', openai_api_key="YOUR_API_KEY", model_name="ada-002"):
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.documents = self.load_docs(directory_path)
        self.docs = self.split_docs()
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key, model_name=self.model_name)
        self.db = self.create_chroma_from_docs()

    def load_docs(self, directory):
        loader = DirectoryLoader(directory)
        documents = loader.load()
        return documents

    def split_docs(self, chunk_size=None, chunk_overlap=None):
        # 기본값 설정
        chunk_size = chunk_size or 500
        chunk_overlap = chunk_overlap or 40
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
        return Chroma.from_documents(documents=self.docs, embedding=self.embeddings,
                                     persist_directory=persist_directory)


# 사용 예시
doc_embed = DocEmbedding()
query_result = doc_embed.similarity_search("give information about {}")
print(query_result)