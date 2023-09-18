from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


class LangChainWhiskey:
    def __init__(self, api_key):
        self.llm = OpenAI(openai_api_key=api_key)

    def get_info_and_description(self, whisky):
        # 위스키 정보에 대한 템플릿
        WHISKEY_template = PromptTemplate(
            input_variables=["whiskey"],
            template="give me detailed information about whiskey that uses the following whiskey.: {whiskey}")
        
        # 위스키 정보에 대한 체인
        WHISKEY_chain = LLMChain(
            llm=self.llm,
            prompt=WHISKEY_template,
            output_key="whiskey_info",
            verbose=True
        )
        
        # 위를 통해 얻은 위스키 정보를 소믈리에가 설명해주는 것처럼 바꿔주는 템플릿 샘플 텍스트
        docent_text = """
        You are a whiskey sommelier at a whiskey bar. Your job is to write a docent for that whiskey in Korean.
        whiskey: {whiskey_info}
        Docent for the above whiskey:
        """

        # 위 샘플 텍스트를 템플릿으로
        DOCENT_template = PromptTemplate(
            input_variables=['whiskey_info'],
            template=docent_text,
            validate_template=False
        )

        # 도슨트에 대한 체인
        DOCENT_chain = LLMChain(
            llm=self.llm,
            prompt=DOCENT_template,
            output_key="docent_description",
            verbose=True
        )

        # 위스키 체인과 도슨트 체인을 연결 및 아웃풋 설정
        overall_chain = SequentialChain(
            chains=[WHISKEY_chain, DOCENT_chain],
            input_variables=["whiskey"],
            output_variables=["whiskey_info", "docent_description"],
            verbose=True
        )

        # 인풋 설정 - 사용자의 위스키 이름
        # 아웃풋: 딕셔너리 형식, 예{'whiskey': 사용자의 위스키 이름, 'whiskey_info': 위스키 설명, 'docent_description': 도슨트 설명}
        results = overall_chain({"whiskey": whisky})
        return results
