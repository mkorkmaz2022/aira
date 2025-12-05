import chromadb
import uuid
from datetime import datetime

class ChromaDBService:
    def __init__(self, collection_name="meeting_notes_db", db_path="./chroma_data"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        print(f"✅ Chroma DB Bağlandı: '{collection_name}'")

    def save_report(self, raw_notes: str, action_items: str, ai_summary: str, project: str, persona: str):
        """
        Mobil ekrandaki tüm verileri kaydeder.
        """
        current_time = datetime.now().isoformat()
        summary_id = str(uuid.uuid4())
        
        # 1. AI Raporunu Ana Kayıt Olarak Ekle
        # Metadata kısmına PROJE ve PERSONA ekledik!
        self.collection.add(
            documents=[ai_summary],
            metadatas=[{
                "date": current_time,
                "type": "report",
                "project": project,  # <-- Yeni
                "persona": persona,  # <-- Yeni
                "raw_notes_backup": raw_notes[:1000] # Yedek olarak ham notun başı
            }],
            ids=[summary_id]
        )
        
        # 2. Ham Notları da ayrıca ekleyelim (Parçalı arama için)
        # Notları satırlara bölüyoruz
        note_lines = [line for line in raw_notes.split('\n') if line.strip()]
        
        for i, line in enumerate(note_lines):
            self.collection.add(
                documents=[line],
                metadatas=[{
                    "date": current_time,
                    "type": "raw_note",
                    "project": project, # <-- Bu sayede sadece bu projede arama yapabiliriz
                    "persona": persona,
                    "parent_id": summary_id
                }],
                ids=[f"{summary_id}_note_{i}"]
            )

        print(f"💾 Rapor ve {len(note_lines)} not maddesi '{project}' projesi altına kaydedildi.")
        return summary_id

    def query_notes(self, query_text: str, n_results=5, where_filter=None):
        """
        where_filter: Örn: {"project": "Atlas Logistics"} gönderilirse sadece o projede arar.
        """
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_filter, # <-- Filtreleme özelliği
            include=['documents', 'metadatas', 'distances']
        )