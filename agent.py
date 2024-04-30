import os
import streamlit as st
import sys
from file_process import combine_files, generate_file
from embed_docs import load_faiss_index
from llm import get_response_from_query
from display import display_search_results, display_newline, display_download_buttons
import atexit

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def close_app():
    print("Closing the Streamlit app...")
    st.stop()
    os._exit(0)

def on_browser_close():
    print("Browser tab closed. Shutting down Streamlit...")
    st.stop()

def update_index():
    file_path = combine_files(st.session_state.uploaded_files)
    db = load_faiss_index(file_path)
    st.session_state.db = db

def main():
    st.set_page_config(page_title="Document Search Agent", page_icon=":mag_right:", layout="wide")
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "queries" not in st.session_state: 
        st.session_state.queries = ""
    if "export_pdf_files" not in st.session_state:
        st.session_state.export_pdf_files = []

    page = st.sidebar.radio("Mode", ["Search", "Context"])

    uploaded_files = st.sidebar.file_uploader("_", accept_multiple_files=True, key="file_uploader")

    st.sidebar.markdown("---")
    close_button = st.sidebar.button("Exit")

    if close_button:
        close_app()

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
    else:
        st.session_state.uploaded_files = []

    if uploaded_files is not None:
        uploaded_files = list(uploaded_files)

        if uploaded_files != st.session_state.uploaded_files:
            st.session_state.uploaded_files = uploaded_files

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files

    if page == "Search":
        st.title("Document Search Agent")
        msg_holder = st.empty()
        msg_holder.info("Upload documents using sidebar")

        if not st.session_state.uploaded_files:
            st.session_state.queries = ""
            if "search_results" in st.session_state:
                del st.session_state.search_results
            if "export_pdf_files" in st.session_state:
                del st.session_state.export_pdf_files

        if st.session_state.uploaded_files:
            msg_holder.empty()
            query = st.text_area("Enter your request/question (one per line):")  
            search_button = st.button("Search")

            if search_button:
                print("Search Button Clicked")
                msg_holder.warning("Getting ready to search...")

                update_index()
                db = st.session_state.db

                if query:
                    queries = query.split("\n")
                    queries = [q for q in queries if q.strip()]
                    print("Search Started.")
                    print("Working on following queries", queries)

                    search_results = {}
                    export_pdf_files = []

                    for i in range(0, len(queries)):

                        if queries[i].strip():
                            msg_holder.warning(f"Searching: {queries[i]}")
                            response, docs_page_content = get_response_from_query(db, queries[i])

                            if response:
                                search_results[queries[i]] = (response, docs_page_content)
                                pdf_data, pdf_name = generate_file(response, queries[i])
                                export_pdf_files.append((pdf_data, pdf_name))

                    st.session_state.export_pdf_files = export_pdf_files
                    st.session_state.search_results = search_results

                    if len(queries)==len(st.session_state.search_results) == len(st.session_state.export_pdf_files):
                        print("\n**ALL QUERIES PROCESSED - RESULTS AND PDF FILES GENERATED**\n")
                    else :
                        msg_holder.warning("Caution: Number of requests, results, pdf files not equal.")
                        print("\n**Caution: Number of queries, results, pdf files not equal.\n")
                        print("Queries:", len(queries), 
                              "Results:", len(st.session_state.search_results), 
                              "Files:", len(st.session_state.export_pdf_files))
                else:
                    msg_holder.warning("Please enter at least one query.")

        if "search_results" in st.session_state:
            print("Search Completed. Displaying the results.")
            msg_holder.success("Search Completed!")

            if st.session_state.search_results:
                for i, (key, value) in enumerate(st.session_state.search_results.items()):

                    try:
                        display_search_results(i, (key, value))
                        display_download_buttons(i, st.session_state.export_pdf_files[i])

                    except IndexError as e:
                        print(f"Error: {str(e)}")

                display_newline()
            else:
                st.info("No search results found.")
    




    elif page == "Context":

        if "search_results" in st.session_state:

            if st.session_state.search_results:
                for i, (key, value) in enumerate(st.session_state.search_results.items()):

                    try:
                        display_search_results(i, (key, value), True)
                        display_download_buttons(i, st.session_state.export_pdf_files[i])

                    except IndexError as e:
                        print(f"Error: {str(e)}")

                display_newline()
            else:
                st.info("No search results found.")
        else:
            st.info("No search results available. Please perform a search first.")

if __name__ == "__main__":
    main()
    atexit.register(on_browser_close)