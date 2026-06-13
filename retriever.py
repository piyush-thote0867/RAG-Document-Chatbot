from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq
import streamlit as st



def get_ans(que , embeddings):
   
   
    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    docs = vectorstore.similarity_search(que , k=4) # find the top 4 closet chunks 
    
    context = "\n\n".join([doc.page_content for doc in docs])
    sources =[]
    for doc in docs :
        source = doc.metadata.get("source" , "unknown")
        page = doc.metadata.get("page" , 0)+1
        sources.append(f"{source} (Page {page})")
    sources = list(dict.fromkeys(sources))
    


    #sending hte data to grok
    client = Groq(api_key = "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")
    response = client.chat.completions.create(
       model = "llama-3.3-70b-versatile",
        messages=[
          {  
              "role" : "system"  ,
              "content": "Answer the Question using the context provided "
          } ,
          {
              "role" : "user",
               "content": f"Context:\n{context}\n\nQuestion: {que}"
                                  
          }
        ]
    )
    ans =  response.choices[0].message.content
    return ans, sources  