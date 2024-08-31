__version__ = "0.1.0"
__author__ = "Bhavyahshree Navaneetha Krishnan"

from langchain_text_splitters import CharacterTextSplitter
import os
import chromadb
from chromadb.utils import embedding_functions
import ollama

import splitBioModels
import createVectorDB
import createDocuments
# Import functions from other modules
from splitBioModels import splitBioModels
from createVectorDB import createVectorDB
from createDocuments import createDocuments

# Define __all__ to specify which names are publicly accessible
__all__ = ['splitBioModels', 'createVectorDB', 'createDocuments']
