import streamlit as st
import replicate
import os
#from langchain_community.llms import Ollama
#from langchain.prompts import PromptTemplate
#from langchain_core.output_parsers import StrOutputParser

def get_response_from_query(db, query, k=3):

    print(f"\nSearching: {query}")
    try:
        os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
        docs = db.similarity_search(query, k=k)
        docs_page_content = " / ".join([d.page_content for d in docs])

        prompt_temp = f"""You are a professional document analyst. You are tasked with reading the provided document and answering the specified question in detail.
        
        Question/Request: {query}
        
        Document Context: {docs_page_content}
        
        Instructions:
        - Get straight to the point/answer.
        - Do not invent facts.
        - Base your answer solely on the information provided in the document.
        - Do NOT add useless comments at the end such as: "I hope this response helped you / I hope I answered your question / if you have more questions..."
        - Neatly structure your response using Newline, bold text, and bullet points if necessary.
        """

        response = ""
        for event in replicate.stream(
            "meta/meta-llama-3-70b-instruct",
            input={
                "prompt": prompt_temp,
                "max_tokens": 1000,
                "temperature": 0.5,
                "top_p": 0.9,
                "top_k": 50,
                "presence_penalty": 1.15,
                "frequency_penalty": 0.2,
            },
        ):
            response += str(event)

        return response, docs_page_content

    except Exception as e:
        st.error(f"Error processing query: {query}")
        st.exception(e)
        return None, None


#local solution
"""
def get_response_from_query_local(db, query, k=3):
    print(f"\nSearching: {query}")
    try:
        docs = db.similarity_search(query ,k=k)
        docs_page_content = " / ".join([d.page_content for d in docs])
        llm = Ollama(model="llama3")

        prompt_template = PromptTemplate.from_template(#
            You are a professional document analyst. You are tasked with reading the provided document and answering the specified question in detail.
                                                       
            Question/Request: {question}
            Document: {docs}
            
            Instructions:
            - Get straight to the point/answer.
            - Do not invent facts.
            - Base your answer solely on the information provided in the document.
            - Do NOT add useless comments at the end such as: "I hope this response helped you / I hope I asnwered your question / if you have more questions..." 
            - Neatly structure your response using Newline, bold text, and bullet points if necessary.
            #
        )
        output_parser = StrOutputParser()

        chain = prompt_template | llm | output_parser

        response = chain.invoke({"question": query, "docs": docs_page_content})
        return response, docs_page_content
    except Exception as e:
        st.error(f"Error processing query: {query}")
        st.exception(e)
        return None, None
"""