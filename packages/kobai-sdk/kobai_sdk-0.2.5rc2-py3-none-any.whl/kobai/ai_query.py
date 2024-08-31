from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatDatabricks
import json

MESSAGE_SYSTEM_TEMPLATE = """
    You are a data analyst tasked with answering questions based on a provided data set. Please answer the questions based on the provided context below. Make sure not to make any changes to the context, if possible, when preparing answers to provide accurate responses. If the answer cannot be found in context, just politely say that you do not know, do not try to make up an answer.
    """

MESSAGE_AI_TEMPLATE = """
    The table information is as follows:
    {table_data}
    """

MESSAGE_USER_CONTEXT_TEMPLATE = """
    The context being provided is from a table named: {table_name}
    """

MESSAGE_USER_QUESTION_TEMPLATE = """
    {question}
    """


def follow_up_question(question, data, data_label):


    chat_model = ChatDatabricks(
        endpoint="databricks-dbrx-instruct"
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(MESSAGE_SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template(MESSAGE_USER_CONTEXT_TEMPLATE),
            AIMessagePromptTemplate.from_template(MESSAGE_AI_TEMPLATE),
            HumanMessagePromptTemplate.from_template(MESSAGE_USER_QUESTION_TEMPLATE)
        ]
    )

    output_parser = StrOutputParser()

    chain = prompt | chat_model | output_parser

    response = chain.invoke(
        {
            "table_name": data_label,
            "table_data": json.dumps(data),
            "question": question
        }
    )

    return response