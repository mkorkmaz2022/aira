# # ai_agents/chromadb_agent.py
# import os
# from langchain_community.document_loaders import TextLoader # Doğru import
# from langchain_text_splitters import RecursiveCharacterTextSplitter # Doğru import
# from langchain_community.vectorstores import Chroma
# from langchain_google_genai import GoogleGenerativeAIEmbeddings # Doğru import
# from dotenv import load_dotenv
# from ai.google_ai import GoogleAIClient # Mevcut LLM istemciniz

# load_dotenv()

# # Sabitler
# CHROMA_DB_PATH = "./chroma_db"
# EMBEDDING_MODEL = "models/embedding-001" 

# def create_and_store_notes_db(meeting_notes: str) -> Chroma | str:
#     """
#     Toplantı notlarını alır, parçalara ayırır, vektörleştirir ve ChromaDB'ye kaydeder (SCUM-109).
#     """
#     if not meeting_notes or not meeting_notes.strip():
#         return "HATA: Vektörleştirilecek notlar boş."
    
#     # Geçici dosyaya yazma (LangChain loader için)
#     temp_file_path = "temp_notes.txt"
#     with open(temp_file_path, "w", encoding="utf-8") as f:
#         f.write(meeting_notes)

#     try:
#         # 1. Belge Yükleme ve Parçalama (Chunking)
#         loader = TextLoader(temp_file_path, encoding="utf-8")
#         documents = loader.load()

#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000,
#             chunk_overlap=200
#         )
#         docs = text_splitter.split_documents(documents)
        
#         # 2. Embeddings (Gömme) Modelini Hazırla ve API Anahtarını İlet
#         google_api_key = os.getenv("GOOGLE_AI_API_KEY") 
#         if not google_api_key:
#             return "API_HATA: GOOGLE_AI_API_KEY bulunamadı. Lütfen .env dosyasını kontrol edin."

#         # 🚨 KRİTİK DÜZELTME: LangChain'in aradığı anahtar adını (GOOGLE_API_KEY) ayarlayın
#         os.environ["GOOGLE_AI_API_KEY"] = google_api_key
            
#         embeddings = GoogleGenerativeAIEmbeddings(
#             model=EMBEDDING_MODEL,
#             api_key=google_api_key # Parametre olarak da iletilmeye devam et
#         )
        
#         # 3. ChromaDB'ye Ekleme ve İndeksleme
#         print(f"✅ Notlar parçalara ayrıldı ({len(docs)} chunk). ChromaDB'ye ekleniyor...")
        
#         vectordb = Chroma.from_documents(
#             documents=docs, 
#             embedding=embeddings, 
#             persist_directory=CHROMA_DB_PATH
#         )
        
#         # Kaydı tamamla ve dosyayı temizle
#         vectordb.persist()
#         os.remove(temp_file_path)
        
#         print(f"✅ ChromaDB oluşturuldu ve {CHROMA_DB_PATH} dizinine kaydedildi.")
#         return vectordb

#     except Exception as e:
#         if os.path.exists(temp_file_path):
#             os.remove(temp_file_path)
#         return f"API_HATA: ChromaDB oluşturulurken hata oluştu: {e}"

# def retrieve_and_summarize_notes(query: str, vectordb: Chroma) -> str:
#     """
#     Sorguya en yakın not parçalarını ChromaDB'den getirir ve bu bağlamla AI'dan özet ister (SCUM-110).
#     """
    
#     # 1. Anlamsal Arama (Retrieval)
#     retrieved_docs = vectordb.similarity_search(query, k=4)
    
#     # 2. Bağlamı (Context) Oluştur
#     context_text = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
    
#     # 3. RAG İstemi (Prompt) Oluştur
#     prompt = f"""
#     Sen bir Toplantı Özeti Uzmanısın. Sana sunulan "BAĞLAM" metinlerini kullanarak, aşağıdaki "SORGU"ya en uygun ve kısa özeti çıkar. Yanıtını kesinlikle sadece sunulan BAĞLAM'daki bilgilere dayanarak oluştur. Teknik jargon kullanma ve karar vericiye hitap et.

#     BAĞLAM (ChromaDB'den Gelen İlgili Not Parçaları):
#     ---
#     {context_text}
#     ---

#     SORGU: {query}
    
#     ÇIKTI FORMATI:
#     **Toplantı Özeti** (Kısa, net ve taranabilir özet - 2-4 cümle)
#     **Gerekçe**: (Yanıtını neden bu bağlama dayanarak verdiğini belirten 1 cümle)

#     Başla:
#     """
    
#     # 4. LLM'e Gönder (Generation)
#     try:
#         # GoogleAIClient, API key'i kendi içinde okur.
#         client = GoogleAIClient()
#         response = client.send_message(prompt) 
#         return response
#     except Exception as e:
#         return f"API_HATA: Mesaj gönderilirken hata oluştu: {e}"
# ai_agents/chromadb_agent.py
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from ai.google_ai import GoogleAIClient

load_dotenv()

CHROMA_DB_PATH = "./chroma_db"

# HuggingFace embedding modeli
HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def create_and_store_notes_db(meeting_notes: str) -> Chroma | str:

    if not meeting_notes or not meeting_notes.strip():
        return "HATA: Vektörleştirilecek notlar boş."
    
    temp_file_path = "temp_notes.txt"
    with open(temp_file_path, "w", encoding="utf-8") as f:
        f.write(meeting_notes)

    try:
        # 1. Belge Yükleme ve Chunking
        loader = TextLoader(temp_file_path, encoding="utf-8")
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(documents)

        # ---------------------------------------------
        # 🔥 HuggingFace Embeddings Kullanımı
        # ---------------------------------------------
        embeddings = HuggingFaceEmbeddings(
            model_name=HF_EMBEDDING_MODEL
        )
        # ---------------------------------------------

        print(f"✅ Notlar parçalara ayrıldı ({len(docs)} chunk). ChromaDB'ye ekleniyor...")

        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=CHROMA_DB_PATH
        )

        vectordb.persist()
        os.remove(temp_file_path)

        print(f"✅ ChromaDB oluşturuldu ve {CHROMA_DB_PATH} dizinine kaydedildi.")
        return vectordb

    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return f"API_HATA: ChromaDB oluşturulurken hata oluştu: {e}"
    
def retrieve_and_summarize_notes(query: str, vectordb: Chroma) -> str:
    """
    Sorguya en yakın not parçalarını ChromaDB'den getirir ve bu bağlamla AI'dan özet ister (SCUM-110).
    """
    
    # 1. Anlamsal Arama (Retrieval)
    retrieved_docs = vectordb.similarity_search(query, k=4)
    
    # 2. Bağlamı (Context) Oluştur
    context_text = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # 3. RAG İstemi (Prompt) Oluştur
    prompt = f"""
    Sen bir Toplantı Özeti Uzmanısın. Sana sunulan "BAĞLAM" metinlerini kullanarak, aşağıdaki "SORGU"ya en uygun ve kısa özeti çıkar. Yanıtını kesinlikle sadece sunulan BAĞLAM'daki bilgilere dayanarak oluştur. Teknik jargon kullanma ve karar vericiye hitap et.

    BAĞLAM (ChromaDB'den Gelen İlgili Not Parçaları):
    ---
    {context_text}
    ---

    SORGU: {query}
    
    ÇIKTI FORMATI:
    **Toplantı Özeti** (Kısa, net ve taranabilir özet - 2-4 cümle)
    **Gerekçe**: (Yanıtını neden bu bağlama dayanarak verdiğini belirten 1 cümle)

    Başla:
    """
    
    # 4. LLM'e Gönder (Generation)
    try:
        # GoogleAIClient, API key'i kendi içinde okur.
        client = GoogleAIClient()
        response = client.send_message(prompt) 
        return response
    except Exception as e:
        return f"API_HATA: Mesaj gönderilirken hata oluştu: {e}"
