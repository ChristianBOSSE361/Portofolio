#!/usr/bin/env python3
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader

# help(PyPDFLoader)

# Initialization
CV = "../data/CVs/CV_BOSSE_July_3_eng.pdf"

# Loading of the CV
cv_loader = PyPDFLoader(CV)
document = cv_loader.load()

# Loading the different part of the portofolio
portofolio_loader = DirectoryLoader("../data", glob="**/*.md", loader_cls=TextLoader)
document += portofolio_loader.load()

print("Number of document loaded :",len(document))
