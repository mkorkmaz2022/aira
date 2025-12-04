import os
import sys

# Proje kök dizinini yola ekle (importlar çalışsın diye)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.input_handler import get_manual_project_data
from ai_agents.brief_notes_agent import brief_notes_agent
# Yeni servisimizi import ediyoruz
from services.chroma_service import ChromaDBService

def main():
    print("--------------------------------------------------")
    print("🚀 NOT ÖZETLEME VE VEKTÖR KAYIT SİSTEMİ")
    print("--------------------------------------------------")

    # 1. Chroma Servisini Başlat
    db_service = ChromaDBService()

    while True:
        print("\nNe yapmak istersiniz?")
        print("1. Yeni Not Ekle ve Özetle")
        print("2. Eski Notlarda Arama Yap")
        print("3. Çıkış")
        choice = input("Seçiminiz (1/2/3): ").strip()

        if choice == "1":
            # --- MEVCUT AKIŞINIZ ---
            meeting_notes = get_manual_project_data()
            if not meeting_notes:
                continue

            print("⏳ Yapay Zeka özeti hazırlıyor...")
            ai_response = brief_notes_agent(meeting_notes)

            # Hata kontrolü (Mevcut kodunuzdan alındı)
            if ai_response.startswith("API_HATA") or ai_response.startswith("HATA"):
                print(f"❌ {ai_response}")
                continue

            # --- YENİ EKLENEN KISIM: VDB KAYIT ---
            try:
                # Yapay zeka çıktısını temiz bir şekilde gösterme
                print("\n📋 AI ÖZETİ:")
                print(ai_response)
                
                # Kullanıcıya kaydetmek isteyip istemediğini sorabiliriz (Opsiyonel)
                save_confirm = input("\n💾 Bu özet veritabanına kaydedilsin mi? (E/H): ").lower()
                if save_confirm == 'e':
                    # Notu ve özeti Chroma'ya gönderiyoruz
                    db_service.save_note(
                        raw_notes=meeting_notes, 
                        summary=ai_response,
                        tags="Toplantı"
                    )
            except Exception as e:
                print(f"❌ Veritabanı kayıt hatası: {e}")

        elif choice == "2":
            # --- YENİ ÖZELLİK: ARAMA ---
            query = input("🔍 Ne aramak istiyorsunuz? (Örn: 'Veritabanı kararları'): ")
            results = db_service.query_notes(query_text=query, n_results=2)
            
            print(f"\n--- '{query}' için Sonuçlar ---")
            # Sonuçları listeleme
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i]
                    print(f"\n📄 SONUÇ {i+1}:")
                    print(f"Özet İçeriği: {doc[:200]}...") # Sadece başını göster
                    print(f"Tarih: {metadata.get('date')}")
                    print(f"Orijinal Not (Kısmi): {metadata.get('raw_notes')[:100]}...")
            else:
                print("Sonuç bulunamadı.")

        elif choice == "3":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()