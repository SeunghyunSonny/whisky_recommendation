from langchain import OpenAI, create_pandas_dataframe_agent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from embeddin import DocEmbedding
import pandas as pd


class LangChainWhiskey:
    def __init__(self, api_key, directory="./docent"):
        self.llm = OpenAI(openai_api_key=api_key)
        self.doc_embed = DocEmbedding(directory=directory)
        self.df = self.whiskeydataframe()

        # Dynamically get the context based on whiskey
        self.context = self.retrieve_context()

        # WHISKEY template with context using dataframe
        self.WHISKEY_template = self.create_template_from_df(
            "Given the context: {context}. Provide detailed information about the whiskey: {whiskey}."
        )

        # DOCENT template with context using dataframe
        docent_text = self.create_template_from_df(
            """Given the context: {context}. 
            Re-write the whiskey given below like a whiskey sommelier of the whiskey bar:
            whiskey:
            {whiskey}
            """
        )
        self.DOCENT_template = PromptTemplate(
            input_variables=["whiskey", "context"],
            template=docent_text
        )

    def whiskeydataframe(self):
        df = pd.read_csv(r'./docent/whisky_preprocessing_done (1).csv', encoding='utf-8')
        return df

    def create_template_from_df(self, base_template):
        # Sample a random row from dataframe for example
        sample_row = self.df.sample(1).iloc[0]
        example_text = ' '.join(sample_row.values.astype(str))
        return base_template.replace("{whiskey}", example_text)

    def retrieve_context(self):
        # This function uses DocEmbedding to retrieve dynamic context
        context_results = self.doc_embed.similarity_search("context about whiskey")

        # Assuming context_results is a list and we want the most relevant one
        if isinstance(context_results, list) and context_results:
            return context_results[0]
        else:
            return context_results  # if it's already a string or other format

    def get_whiskey_info(self, whiskey_name):
        WHISKEY_chain = LLMChain(
            llm=self.llm,
            prompt=self.WHISKEY_template,
            output_key="whiskey_info",
            verbose=True
        )
        return WHISKEY_chain.run(whiskey=whiskey_name, context=self.context)

    def get_docent_description(self, whiskey_name):
        DOCENT_chain = LLMChain(
            llm=self.llm,
            prompt=self.DOCENT_template,
            output_key="docent_description",
            verbose=True
        )
        return DOCENT_chain.run(whiskey=whiskey_name, context=self.context)
