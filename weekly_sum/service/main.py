# app/main.py
import os
import sys
# Gerekli klasörleri Python yoluna ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_agents.effort_estimator_agent import estimate_effort_agent
from utils.input_handler import get_manual_project_data

import time 

def main():
    print("✨ İş Gücü Tahmin Uygulaması Başlatılıyor...")

    # 1. Girdileri Kullanıcıdan Al (Elle Giriş)
    project_data = get_manual_project_data()
    print("\n✅ Proje Verileri Hazırlandı:", project_data)
    time.sleep(1) # Kullanıcıya bilgi vermek için kısa bir duraklama

    # 2. AI Agent'ı Çağır (Tahmini Başlat)
    print("\n⏳ Yapay Zeka Uzmanından Tahmin İsteniyor...")
    
    # LLM'den gelen yanıt (Tahmin Sayısı + Gerekçe Metni)
    ai_response = estimate_effort_agent(project_data)

    # 3. Yanıtı Ayrıştır ve Göster
    print("\n--------------------------------------------------")
    
    if ai_response.startswith("API_HATA"):
        print(ai_response)
        return

    try:
        # LLM çıktısının ilk satırının tahmin sayısı olması beklenir.
        lines = ai_response.split('\n', 1)
        estimated_effort = int(lines[0].strip())
        reasoning = lines[1].strip() if len(lines) > 1 else "Gerekçe sağlanamadı."
        
        print(f"💰 TOPLAM TAHMİNİ İŞ GÜCÜ (Man-Day): {estimated_effort}")
        print("--------------------------------------------------")
        print("GEREKÇE ve ANALİZ:")
        print(reasoning)
        print("--------------------------------------------------")
        
        # 4. (Opsiyonel) Sonucu Mail Gönderme
        # if estimated_effort > 150:
        #     send_email(...)
            
    except ValueError:
        print("❌ HATA: Yapay zeka çıktısı beklenen formatta değil veya bir sayı içermiyor.")
        print(f"Ham AI Yanıtı:\n{ai_response}")
        print("--------------------------------------------------")
    except Exception as e:
        print(f"❌ Beklenmedik bir hata oluştu: {e}")


if __name__ == "__main__":
	# AI Agent'ların doğru çalışması için API anahtarınızın ayarlandığından emin olun.
	# Buraya bir .env dosyası ve 'GOOGLE_AI_API_KEY' eklemeyi unutmayın.
	main()
