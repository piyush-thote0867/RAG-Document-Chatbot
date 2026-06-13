import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from retriever import get_ans
import os 
import time
@st.cache_resource
def load_embeddings():
    return  HuggingFaceEmbeddings(
            model_name = "sentence-transformers/all-MiniLM-L6-v2"
        )
st.title("RAG Chatbot ")

uploaded_file = st.file_uploader("Upload a PDF", type = ["pdf", "txt","docx"])

if uploaded_file :
    ext = uploaded_file.name.split(".")[-1]  #extension finder
    temp_path = f"temp.{ext}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    from ingest import ingest
    with st.spinner("Processing document..."):
        ingest(temp_path)

    os.remove(temp_path)
    st.session_state.processed = True
    
    msg = st.success("PDF processed Sucessfully! Ask Your Questions please:)")

    time.sleep(3)
    msg.empty()



#history 
if "messages" not in st.session_state:
    st.session_state.messages=[]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])



que = st.chat_input("Ask a question")
if que : 
    if not os.path.exists("faiss_index"): #mean no fiel inserted 
        st.warning("please upload a pdf first")
   
    else :
        if not uploaded_file:  # only show if no new file uploaded
            st.success("Previous data loaded! Ask questions or add a new document.")
        #else thi will go 
        st.chat_message("user").write(que)
        try :
            with st.spinner("Thinking..."):
                embeddings = load_embeddings()
                ans ,sources = get_ans(que ,  embeddings)
         
        except Exception as e:
            ans = f"Error: {e}"
            sources = []
        st.chat_message("assistant").write(ans)
        if sources :
             st.caption("src : "+"|".join(sources))
        st.session_state.messages.append({"role":"user" , "content" : que})
        st.session_state.messages.append({"role":"assistant" , "content" : ans})

