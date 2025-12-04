import chromadb
import uuid
from datetime import datetime

class ChromaDBService:
    def __init__(self, collection_name="meeting_notes_db", db_path="./chroma_data"):
        # Verileri diske kaydetmek için PersistentClient kullanıyoruz
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        print(f"✅ Chroma DB Bağlandı: '{collection_name}' ({db_path})")

    def save_note(self, raw_notes: str, summary: str, tags: str = "Genel"):
        """
        Ham notu ve yapay zeka özetini veritabanına kaydeder.
        Biz burada 'Özet'i (summary) vektörleştiriyoruz, çünkü aramaları genelde
        özet bilgi üzerinden yapmak daha verimlidir. Ham notu metadata'da saklarız.
        """
        doc_id = str(uuid.uuid4()) # Benzersiz ID oluştur
        
        # Meta veriler (Filtreleme ve ham veriye ulaşmak için)
        metadata = {
            "date": datetime.now().isoformat(),
            "raw_notes": raw_notes[:5000], # Çok uzunsa kırpabiliriz veya chunklara bölebiliriz
            "type": "meeting_summary",
            "tags": tags
        }

        self.collection.add(
            documents=[summary], # Vektör araması bu metin üzerinden yapılacak
            metadatas=[metadata],
            ids=[doc_id]
        )
        print(f"💾 Not ve Özet VDB'ye kaydedildi. ID: {doc_id}")
        return doc_id

    def query_notes(self, query_text: str, n_results=3):
        """Vektör veritabanında anlamsal arama yapar."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        return results