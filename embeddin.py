from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 간단한 Document 클래스 정의
class Document:
    def __init__(self, content):
        self.page_content = content
        self.metadata = {}

class DocEmbedding:

    def __init__(self, txt_file_path=r'.\txt', openai_api_key="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", model_name="ada-002"):
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.documents = self.load_data_from_txt(txt_file_path)
        self.docs = self.split_docs()
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key, model_name=self.model_name)
        self.db = self.create_chroma_from_docs()

    # txt 파일을 읽는 메서드
    def load_data_from_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            documents = [Document(line.strip()) for line in file.readlines()]
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

# 사용 예시
doc_embed = DocEmbedding()
query_result = doc_embed.similarity_search("give information about {}")
print(query_result)
