import os
import re
import tempfile
import subprocess
import streamlit as st
import sys
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader, CSVLoader

def combine_files(uploaded_files):
    print("combine_files")
    #print(f"Number of uploaded files: {len(uploaded_files)}")

    combined_file_path = ".all_files.txt"
    combined_file_path = os.path.abspath(combined_file_path)  # Get the absolute path

    try:
        with open(combined_file_path, "w") as combined_file:
            for uploaded_file in uploaded_files:
                file_extension = os.path.splitext(uploaded_file.name)[-1].lower()
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                        temp_file.write(uploaded_file.getvalue())
                        temp_file_path = temp_file.name

                    if file_extension == ".txt":
                        with open(temp_file_path, "r") as file:
                            file_content = file.read()
                        combined_file.write(file_content + "\n")

                    elif file_extension == ".csv":
                        file_loader = CSVLoader(file_path=temp_file_path)
                        document = file_loader.load()
                        document_string = " ".join(doc.page_content.replace("\n", " ") for doc in document)
                        combined_file.write(document_string)

                    elif file_extension in [".docx", ".doc"]:
                        file_loader = Docx2txtLoader(file_path=temp_file_path)
                        document = file_loader.load()
                        document_string = " ".join(doc.page_content.replace("\n", " ") for doc in document)
                        combined_file.write(document_string)

                    elif file_extension == ".pdf":
                        file_loader = PyMuPDFLoader(file_path=temp_file_path)
                        document = file_loader.load()
                        document_string = " ".join(doc.page_content.replace("\n", " ") for doc in document)
                        combined_file.write(document_string)

                    else:
                        st.warning(f"Skipping file '{uploaded_file.name}' due to unsupported file format.")

                    os.remove(temp_file_path)
                except Exception as e:
                    st.warning(f"Skipping file '{uploaded_file.name}' due to the following error: {str(e)}")
                    continue

        print(f"Combined file created at: {combined_file_path}")
        return combined_file_path

    except Exception as e:
        st.error(f"Error creating combined file: {str(e)}")
        return None
    
def generate_file(content, file_name):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    file_name = re.sub(r'[\s<>:"/\\|?*]', '_', file_name)
    pdf_file_path = f"{os.path.splitext(temp_file_path)[0]}_{file_name}.pdf"

    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.run(['mdpdf', '-o', pdf_file_path, temp_file_path], check=True, stdout=devnull, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error occurred while generating PDF: {str(e)}")

    with open(pdf_file_path, 'rb') as file:
        pdf_data = file.read()

    os.remove(temp_file_path)
    os.remove(pdf_file_path)
    print("Completed.\n")

    return pdf_data, f"{file_name}.pdf"