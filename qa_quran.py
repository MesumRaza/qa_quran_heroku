from haystack import Finder
from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.reader.farm import FARMReader
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
import streamlit as st
from os import path
import pandas as pd

#max_width_str = f"max-width: 1600px;"
#st.markdown(f"""<style> .reportview-container .main .block-container{{{max_width_str}}}</style>""", True)

st.markdown("<center> <h1> 📜 Questions And Answering Using Quran's English Translation </h1> </center>", True)


def read_corpus():
    document_store = InMemoryDocumentStore()
    doc_dir = "Quran"
    dicts = convert_files_to_dicts(dir_path=doc_dir, split_paragraphs=True)
    document_store.write_documents(dicts)
    return document_store


def retriever():
    document_store = read_corpus()
    retriever = TfidfRetriever(document_store=document_store)
    return retriever

question = st.text_input('Input your question here:')

if st.button('Ask'):
    with st.spinner('Reading all the translations from all over Quran'):
        retriever = retriever()
        
        if not(path.exists('data/mlm-temp')):
            reader = FARMReader(model_name_or_path="deepset/minilm-uncased-squad2", use_gpu=False)
            reader.save(directory='data/mlm-temp)
        else:
            reader = FARMReader(model_name_or_path="data/mlm-temp", use_gpu=False)
        
        finder = Finder(reader, retriever)
        
        prediction = finder.get_answers(question=question, top_k_retriever=10, top_k_reader=5)

        keys=['answer','context','meta','probability','score']
        print(list( map(prediction.get, ['query'])))
        print("\n")
        answer_frame=pd.DataFrame.from_records([list( map(i.get, keys)) for i in prediction['answers']])
        answer_frame.columns=['answer','reference','Surah','confidence','score']
        answer_frame['Surah']=answer_frame['Surah']
        st.table(answer_frame.T)
