# app/main.py
import os
import sys
# Gerekli klasörleri Python yoluna ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.input_handler import get_manual_project_data
from ai_agents.brief_notes_agent import brief_notes_agent

def main():
    print("NOT ÖZETİ ÇIKARMA SİSTEMİNE HOŞ GELDİNİZ")
    
    # 1. Kullanıcıdan toplantı notlarını al
    meeting_notes = get_manual_project_data()
    
    # 2. AI'dan özet üret
    ai_response = brief_notes_agent(meeting_notes)
    
    # 3. AI yanıtını işle
    if ai_response.startswith("API_HATA") or ai_response.startswith("HATA"):
        print(ai_response)
        return

    try:
        # LLM çıktısının beklenen formatta olduğu varsayılır
        if "**Toplantı Özeti**" in ai_response and "**Gerekçe**" in ai_response:
            # Özeti ve gerekçeyi ayır
            parts = ai_response.split("**Gerekçe**", 1)
            summary = parts[0].strip() if len(parts) > 1 else ai_response
            reasoning = parts[1].strip() if len(parts) > 1 else "Gerekçe sağlanamadı."

            print("📋 TOPLANTI ÖZETİ:")
            print("--------------------------------------------------")
            print(summary)
            print("--------------------------------------------------")
            print("GEREKÇE:")
            print(reasoning)
            print("--------------------------------------------------")
        else:
            raise ValueError("Yapay zeka çıktısı beklenen özet formatında değil.")

    except ValueError as ve:
        print(f"❌ HATA: {ve}")
        print(f"Ham AI Yanıtı:\n{ai_response}")
        print("--------------------------------------------------")
    except Exception as e:
        print(f"❌ Beklenmedik bir hata oluştu: {e}")
        print(f"Ham AI Yanıtı:\n{ai_response}")
        print("--------------------------------------------------")
if __name__ == "__main__":
    main()