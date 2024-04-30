# Document Search Agent

Document Search Agent is a powerful tool that allows you to search and analyze documents using natural language queries. It provides an intuitive interface for uploading documents, performing searches, and generating PDF reports based on the search results.

## Features

- Supports multiple file formats: TXT, CSV, DOCX, DOC, PDF
- Performs similarity search on documents using advanced embedding techniques
- Generates detailed responses to user queries based on the document content
- Provides context for each search result, highlighting relevant document snippets
- Allows downloading of search results as PDF files


## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/document-search-agent.git
```
Install the required dependencies:
```bash
pip install streamlit langchain-community huggingface-hub pymupdf python-docx
```
Run the Streamlit app:
```bash
streamlit run agent.py
```

## Usage
1. Open the Document Search Agent app in your web browser.
2. Upload one or more documents using the sidebar file uploader. Supported file formats include TXT, CSV, DOCX, DOC, and PDF.
3. Once the documents are uploaded, enter your search queries in the text area provided. You can enter multiple queries, one per line.
4. Click the "Search" button to initiate the search process. The app will process each query and generate search results based on the uploaded documents.
5. The search results will be displayed in the main panel. Each search result includes the original query, the generated response, and relevant context from the documents.
6. You can download individual search results as PDF files by clicking the download button next to each result.
7. To view the context for each search result, navigate to the "Context" tab in the sidebar. The context will be displayed alongside the search results, providing additional insights into the relevant document snippets.

## Configuration

- The app uses the `BAAI/bge-small-en-v1.5` embedding model by default. You can modify the `embeddings` variable in the `load_faiss_index` function to use a different embedding model.
- The search results are generated using the `Ollama` language model with the `llama3` configuration. You can customize the model and configuration in the `get_response_from_query` function.
- The prompt template used for generating search results can be modified in the `prompt_template` variable within the `get_response_from_query` function.

## Contributing

Contributions to Document Search Agent are welcome! If you find any bugs, have feature requests, or want to contribute improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the MIT License.

## Acknowledgements

Document Search Agent makes use of the following libraries and resources:

- **Streamlit** - Web app framework
- **Langchain** - Building blocks for LLM applications
- **FAISS** - Similarity search library
- **PyMuPDF** - PDF processing library
- **python-docx** - Microsoft Word document processing library

## Contact

For any questions or inquiries, please contact the project maintainer at `dylan.agentdev@gmail.com`.




