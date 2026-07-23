#!/usr/bin/env python3
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader

# help(PyPDFLoader)

# Initialization
CV = "../data/CVs/CV_BOSSE_July_3_eng.pdf"

# Loading of the CV
cv_loader = PyPDFLoader(CV)
document = cv_loader.load()

# Loading the different part of the portofolio
portofolio_loader = None

for file in os.listdir("../data"):
    if not os.path.isfile(file): continue
    portofolio_loader = TextLoader(file)
    document += portofolio_loader.load()

