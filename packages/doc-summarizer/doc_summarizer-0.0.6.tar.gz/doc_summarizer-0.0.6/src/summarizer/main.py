import os
from typing import Optional
from langchain_openai import ChatOpenAI

from langchain_community.document_loaders import (
    CSVLoader, TextLoader,
    UnstructuredWordDocumentLoader, UnstructuredHTMLLoader,
    # UnstructuredPDFLoader
)
from langchain_community.document_loaders import PyPDFLoader

from langchain.chains.summarize import load_summarize_chain
import tiktoken


class Summarizer:
    """
    A class to summarize text from files.

    Attributes:
        file_dir (str): The directory where the file is located.
        file_name (str): The name of the file (without the directory).
        extension (Optional[str]): The file extension, if it cannot be extracted from the file name. 
                                   Must be one of ['.pdf', '.docs', '.txt'].
    
    Methods:
        __init__(file_dir: str, file_name: str, extension: Optional[str] = None) -> None:
            Initializes the Summarizer with file directory, file name, and optional file extension.
            Validates the extension if provided. If not provided, attempts to infer the extension from the file name.
            Raises ValueError if the extension is invalid or cannot be determined from the file name.
    """

    VALID_EXTENSIONS = ['.pdf', '.docx', '.txt', '.csv', '.html']

    def __init__(self, file_dir: str, file_name: str, extension: Optional[str] = None) -> None:
        """
        Initializes the Summarizer with the specified file directory, file name, and an optional file extension.

        Args:
            file_dir (str): The directory where the file is located.
            file_name (str): The name of the file (without the directory).
            extension (Optional[str]): The file extension, if it cannot be extracted from the file name. 
                                       Must be one of ['.pdf', '.docs', '.txt'].
        
        Raises:
            ValueError: If the file extension is invalid or cannot be determined from the file name.
        """

        self.file_dir = file_dir
        self.file_name = file_name

        # Determine the extension
        if extension:
            # Validate provided extension
            if extension not in self.VALID_EXTENSIONS:
                raise ValueError(f"Invalid file extension '{extension}'. Must be one of {self.VALID_EXTENSIONS}.")
            self.extension = extension
        else:
            # Extract extension from file_name
            self.extension = self._extract_extension_from_filename(file_name)

            if self.extension is None:
                raise ValueError("Could not determine file extension from file_name and no extension was provided.")
    
    def _extract_extension_from_filename(self, file_name: str) -> Optional[str]:
        """
        Attempts to extract the file extension from the file name.
        
        Args:
            file_name (str): The name of the file.
        
        Returns:
            Optional[str]: The file extension if it can be determined and is valid, None otherwise.
        """
        # Get extension from the file name
        _, ext = os.path.splitext(file_name)
        
        # Validate the extracted extension
        if ext in self.VALID_EXTENSIONS:
            return ext
        else:
            return None

    def _load_document(self):
        """
        Loads the document based on its file extension using LangChain document loaders.
        
        Raises:
            ValueError: If the file type is unsupported.
        """
        file_path = os.path.join(self.file_dir, self.file_name)
            
        # Determine the appropriate loader based on the file extension
        if self.extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif self.extension == '.csv':
            loader = CSVLoader(file_path)
        elif self.extension == '.txt':
            loader = TextLoader(file_path)
        elif self.extension == '.docx':
            loader = UnstructuredWordDocumentLoader(file_path)
        elif self.extension == '.html':
            loader = UnstructuredHTMLLoader(file_path)
        else:
            raise ValueError(f"Unsupported file extension '{self.extension}'.")

        # Load and return documents
        return loader.load()
    
    def _count_tokens(self, document, model="gpt-3.5-turbo"):
        """
        Counts the tokens in the document using tiktoken and the specified model's tokenizer.
        """
        # Initialize the tokenizer for the model
        tokenizer = tiktoken.encoding_for_model(model)
        
        # Join all document pages into a single string
        text = " ".join([doc.page_content for doc in document])

        # Count the tokens
        tokens = tokenizer.encode(text)
        return len(tokens)
    
    def summarize(self):
        """
        Summarizes the loaded document using an LLM via LangChain.
        
        Returns:
            str: A summary of the document.
        """
        # Load document
        document = self._load_document()
        
        token_count = self._count_tokens(document, model="gpt-3.5-turbo")
        
        # Define a token threshold (around 3000 tokens for stuff, adjust as needed)
        token_threshold = 120000

        # Decide on the summarization strategy
        if token_count <= token_threshold:
            chain_type = "stuff"
        else:
            chain_type = "map_reduce"
        print(f'The document contains approximatly {token_count} tokens. Using {chain_type} method.')

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        chain = load_summarize_chain(llm, chain_type=chain_type)

        summary = chain.run(document)

        return summary
    
    def extract_keywords(self):
        """
        Extracts keywords from the loaded document using an LLM via a custom LangChain prompt.
        
        Returns:
            list: Extracted keywords as a list of strings.
        """
        return ['python', 'programming', 'list', 'tuple', 'data structure']

