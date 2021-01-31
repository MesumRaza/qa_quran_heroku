from haystack import Finder
from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.reader.farm import FARMReader
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
import streamlit as st

#max_width_str = f"max-width: 1600px;"
#st.markdown(f"""<style> .reportview-container .main .block-container{{{max_width_str}}}</style>""", True)

st.markdown("<center> <h1> 📜 Questions And Answering Using Quran's English Translation </h1> </center>", True)

@st.cache
def read_corpus():
    document_store = InMemoryDocumentStore()
    doc_dir = "Quran"
    dicts = convert_files_to_dicts(dir_path=doc_dir, split_paragraphs=True)
    document_store.write_documents(dicts)
    return document_store

@st.cache
def retriever():
    document_store = read_corpus()
    retriever = TfidfRetriever(document_store=document_store)
    return retriever

question = st.text_input('Input your question here:')

if st.button('Ask'):
    with st.spinner('Reading all the translations from all over Quran'):
        retriever = retriever()
        reader = FARMReader(model_name_or_path="deepset/minilm-uncased-squad2", use_gpu=False)
        finder = Finder(reader, retriever)
        prediction = finder.get_answers(question=question, top_k_retriever=10, top_k_reader=5)
        st.info(prediction['answers'][0]['answer'])

