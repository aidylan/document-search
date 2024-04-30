import streamlit as st

@st.cache_data
def display_result(search_results, pdf_files, context = False):

    for i, (key, value) in enumerate(search_results.items()):
        display_search_results(i, (key, value))

    try:
        display_download_buttons(i, pdf_files[i])
    except IndexError as e:
        print(f"Error: {str(e)}")

@st.cache_data
def display_search_results(i, results, context = False):
    query = results[0]
    result, result_context = results[1]
    result_display_box = st.empty()
    with result_display_box.container(border=True):
        if context:
            st.markdown(f"### {query}")
            st.markdown(result, unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("### Context")
            st.markdown(result_context)
        else:
            st.markdown(result, unsafe_allow_html=True)          

def display_download_buttons(file_num, pdf_file):
    placeholder_download = st.empty()
    pdf_data, pdf_name = pdf_file

    with placeholder_download.container():
        st.download_button(
            label=f"⬇️",
            data=pdf_data,
            file_name=pdf_name,
            mime="application/pdf",
            key=f"download_{file_num}"
        )

def display_newline():
    st.markdown(
        """
        <style>
        .stDownloadButton {
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )