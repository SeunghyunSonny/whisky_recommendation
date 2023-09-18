from langchain import (OpenAI,
from langchain.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from embeddin import DocEmbedding
import pandas as pd


class LangChainWhiskey:
    def __init__(self, api_key, directory="./docent"):
        self.llm = OpenAI(openai_api_key=api_key)  # OpenAI 객체 초기화
        self.doc_embed = DocEmbedding(directory=directory)  # DocEmbedding 객체 초기화
        self.df = self.whiskeydataframe()  # 데이터프레임 로드

        # 위스키에 대한 동적 컨텍스트 가져오기
        self.context = self.retrieve_context()

        # 데이터프레임을 사용하여 WHISKEY 템플릿 생성
        self.WHISKEY_template = self.create_template_from_df(
            "Given the context: {context}. Using korean language appropriately, Provide detailed information about the whiskey: {whiskey}.",
            use_last_column=False
        )

        # 데이터프레임을 사용해 DOCENT 템플릿 생성
        docent_text = self.create_template_from_df(
            """Given the context: {context}. 
            Using korean language appropriately, Re-write the whiskey given below like a whiskey sommelier of the whiskey bar:
            whiskey:
            {whiskey}
            """,
            use_last_column=True
        )
        self.DOCENT_template = PromptTemplate(
            input_variables=["whiskey", "context"],
            template=docent_text
        )

    # 데이터프레임 로드 함수
    def whiskeydataframe(self):
        df = pd.read_csv(r'./docent/whisky_preprocessing_done (1).csv', encoding='utf-8')
        return df

    # 데이터프레임을 바탕으로 동적 템플릿 생성 함수
    def create_template_from_df(self, base_template, use_last_column):
        # 데이터프레임에서 샘플 행 가져오기
        sample_row = self.df.sample(1).iloc[0]
        if use_last_column:
            example_text = sample_row.values[-1]
        else:
            example_text = ' '.join(sample_row.values[:-1].astype(str))
        return base_template.replace("{whiskey}", example_text)

    # 동적 컨텍스트 검색 함수
    def retrieve_context(self):
        context_results = self.doc_embed.similarity_search("context about whiskey")
        if isinstance(context_results, list) and context_results:
            return context_results[0]
        else:
            return context_results

    # 위스키 정보 검색 함수
    def get_whiskey_info(self, whiskey_name):
        WHISKEY_chain = LLMChain(
            llm=self.llm,
            prompt=self.WHISKEY_template,
            output_key="whiskey_info",
            verbose=True
        )
        return WHISKEY_chain.run(whiskey=whiskey_name, context=self.context)

    # 도슨트 설명 생성 함수
    def get_docent_description(self, whiskey_name):
        DOCENT_chain = LLMChain(
            llm=self.llm,
            prompt=self.DOCENT_template,
            output_key="docent_description",
            verbose=True
        )
        return DOCENT_chain.run(whiskey=whiskey_name, context=self.context)
