import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Yeni fonksiyon isimlerini import ediyoruz
from ai_agents.brief_notes_agent import generate_ai_report
from services.chroma_service import ChromaDBService

def get_multiline_input(prompt_text):
    print(prompt_text)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() == "###SON###":
            break
        lines.append(line)
    return "\n".join(lines).strip()

def main():
    print("📱 MOBİL UYGULAMA SİMÜLASYONU")
    print("--------------------------------")
    db = ChromaDBService()

    while True:
        print("\n=== ANA MENÜ ===")
        print("1. ➕ Hızlı Toplantı Notu Oluştur (Mobil Ekran)")
        print("2. 🔍 Proje Bazlı Arama Yap")
        print("3. ❌ Çıkış")
        
        secim = input("Seçim: ").strip()

        if secim == "1":
            # --- 1. PERSONA SEÇİMİ (UI'daki Buttonlar) ---
            print("\n👤 Persona Seçiniz:")
            print("   [1] Yönetici")
            print("   [2] Yazılımcı")
            print("   [3] Tasarımcı")
            p_secim = input("   Seçim (1-3): ")
            persona_map = {"1": "Yönetici", "2": "Yazılımcı", "3": "Tasarımcı"}
            persona = persona_map.get(p_secim, "Yönetici")

            # --- 2. PROJE SEÇİMİ (UI'daki Buttonlar) ---
            print(f"\n📂 Proje Seçiniz ({persona} olarak):")
            print("   [1] Aurora CRM")
            print("   [2] Atlas Logistics")
            print("   [3] Nimbus ERP")
            prj_secim = input("   Seçim (1-3): ")
            project_map = {"1": "Aurora CRM", "2": "Atlas Logistics", "3": "Nimbus ERP"}
            project = project_map.get(prj_secim, "Genel Proje")

            # --- 3. NOTLAR (UI'daki Text Area 1) ---
            notes = get_multiline_input(f"\n📝 [{project}] İçin Toplantı Notları (Bitince ###SON### yaz):")
            
            # --- 4. AKSİYONLAR (UI'daki Text Area 2) ---
            actions = get_multiline_input(f"\n⚡ [{project}] İçin Aksiyon Maddeleri (Opsiyonel - Bitince ###SON### yaz):")

            if not notes and not actions:
                print("❌ Veri girilmedi, iptal ediliyor.")
                continue

            # --- AI RAPOR ÜRETİMİ ---
            print(f"\n🤖 {persona} modunda AI raporu hazırlanıyor...")
            ai_report = generate_ai_report(notes, actions, persona, project)
            
            print("\n" + "="*30)
            print(ai_report)
            print("="*30)

            # --- KAYIT ---
            if input("\n💾 Kaydedilsin mi? (e/h): ").lower() == 'e':
                db.save_report(
                    raw_notes=notes,
                    action_items=actions,
                    ai_summary=ai_report,
                    project=project,
                    persona=persona
                )

        elif secim == "2":
            # --- FİLTRELİ ARAMA ---
            target_project = input("Hangi projede arayalım? (Örn: Atlas Logistics): ")
            query = input("Ne arıyorsunuz? (Örn: 'Veritabanı sorunu'): ")
            
            # Chroma'nın 'where' özelliğini kullanıyoruz!
            results = db.query_notes(
                query_text=query, 
                n_results=3,
                where_filter={"project": target_project} if target_project else None
            )
            
            print(f"\n--- Sonuçlar ({target_project or 'Tümü'}) ---")
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    meta = results['metadatas'][0][i]
                    print(f"\n📄 [{meta['type'].upper()}] - {meta['persona']}")
                    print(f"İçerik: {doc[:200]}...")
            else:
                print("Sonuç bulunamadı.")

        elif secim == "3":
            break

if __name__ == "__main__":
    main()