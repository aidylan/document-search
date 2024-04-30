from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st


def get_response_from_query(db, query, k=3):
    print(f"\nSearching: {query}")
    try:
        docs = db.similarity_search(query ,k=k)
        docs_page_content = " / ".join([d.page_content for d in docs])
        llm = Ollama(model="llama3")

        prompt_template = PromptTemplate.from_template("""
            You are a professional document analyst. You are tasked with reading the provided document and answering the specified question in detail.
                                                       
            Question/Request: {question}
            Document: {docs}
            
            Instructions:
            - Get straight to the point/answer.
            - Do not invent facts.
            - Base your answer solely on the information provided in the document.
            - Do NOT add useless comments at the end such as: "I hope this response helped you / I hope I asnwered your question / if you have more questions..." 
            - Neatly structure your response using Newline, bold text, and bullet points if necessary.
            """
        )
        output_parser = StrOutputParser()

        chain = prompt_template | llm | output_parser

        response = chain.invoke({"question": query, "docs": docs_page_content})
        return response, docs_page_content
    except Exception as e:
        st.error(f"Error processing query: {query}")
        st.exception(e)
        return None, None