# works_and_streamlit.py

from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class LangChainWhiskey:


    def __init__(self, api_key):
        self.llm = OpenAI(openai_api_key=api_key)

        # WHISKEY 템플릿
        self.WHISKEY_template = PromptTemplate(
            input_variables=["whiskey"],
            template="give me an detail information of whiskey that using following whiskey : {whiskey}",
        )

        # DOCENT 템플릿
        docent_text = """Re-write the whiskey given below like a whiskey sommelier of the whiskey bar:

        whiskey:
        {whiskey}
        """

        self.DOCENT_template = PromptTemplate(
            input_variables=['whiskey'],
            template=docent_text
        )

    def get_whiskey_info(self, whiskey_name):
        WHISKEY_chain = LLMChain(
            llm=self.llm,
            prompt=self.WHISKEY_template,
            output_key="whiskey_info",
            verbose=True
        )
        return WHISKEY_chain.run(whiskey=whiskey_name)

    def get_docent_description(self, whiskey_name):
        DOCENT_chain = LLMChain(
            llm=self.llm,
            prompt=self.DOCENT_template,
            output_key="docent_description",
            verbose=True
        )
        return DOCENT_chain.run(whiskey=whiskey_name)
