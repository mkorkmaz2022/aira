# ai_agents/effort_estimator_agent.py
import os
from ai.google_ai import GoogleAIClient
from dotenv import load_dotenv

load_dotenv()

def estimate_effort_agent(project_data: dict) -> str:
    """
    Parametrik tahmin girdilerini kullanarak Google AI'dan iş gücü tahmini ister.

    Args:
        project_data (dict): Elle girilmiş proje özelliklerini içerir. 
                             Örn: {"Fonksiyon_Sayisi": 10, "Karmasiklik": "Orta", ...}

    Returns:
        str: AI'dan gelen ham tahmin metni (Tahmin + Gerekçe).
    """

    # 1. AI İstemcisini Hazırla (Google AI'ı varsayıyoruz)
    # API Anahtarı .env dosyasından otomatik olarak okunacaktır.
    try:
        client = GoogleAIClient()
    except ValueError as e:
        return f"API_HATA: {e}. Lütfen .env dosyasını kontrol edin."

    # 2. Parametrik Tahmin için Prompt'u Oluştur
    # LLM'i bir uzman rolüne sokmak ve çıktıyı kesinleştirmek kritik.
    prompt = f"""
        Sen kıdemli bir Proje Yöneticisi ve Parametrik İş Gücü Tahmin Uzmanısın. 
        Mantıklı varsayımlar yaparak, belirsiz girdileri tamamla ve tutarlı bir tahmin üret.

        Görev: Aşağıdaki proje özelliklerini ve tahmini büyüklük verilerini kullanarak, 
        bu yazılım projesinin (mobil app, web sayfası veya benzeri) tamamlanması için gereken toplam İŞ GÜCÜNÜ (MAN-DAY) parametrik yöntemle tahmin et. 
        Tahminini adım adım hesapla: Önce temel man-day'i fonksiyon sayısı ve karmaşıklığa göre belirle, 
        sonra entegrasyon, ekip tecrübesi ve risk faktörlerini uygula.

        GEÇMİŞ METRİK İPUCU (ZORUNLU KULLANIM): 
        Bu metrikleri temel al ve ortalama değerleri kullan (örneğin, düşük için 6.5, orta için 11.5, yüksek için 20).
        - Düşük Karmaşıklık: Ortalama 5-8 Man-Day / Fonksiyon
        - Orta Karmaşıklık: Ortalama 8-15 Man-Day / Fonksiyon
        - Yüksek Karmaşıklık: Ortalama 15-25 Man-Day / Fonksiyon

        EK FAKTÖR KURALLARI (TAHMİNİ ETKİLEMEK İÇİN KULLAN):
        - Entegrasyon Sayısı: Her entegrasyon için ekstra 5-10 Man-Day ekle (ortalama 7.5 kullan).
        - Ekip Tecrübesi: 
        - Yüksek: Toplamı %90'a indir (verimli ekip).
        - Orta: Değişiklik yok.
        - Düşük: Toplamı %120'ye çıkar (ek eğitim ihtiyacı).
        - Risk Payı: Belirtilen gün sayısını doğrudan toplam man-day'e ekle.

        PROJE ÖZELLİKLERİ (ELLE GİRİLEN GİRDİLER):
        - Fonksiyon Sayısı: {project_data.get("Fonksiyon_Sayisi", 'Belirtilmemiş')}
        - Karmaşıklık Derecesi: {project_data.get("Karmasiklik_Derecesi", 'Belirtilmemiş')}
        - Entegrasyon Sayısı: {project_data.get("Entegrasyon_Sayisi", 0)}
        - Ekip Tecrübesi (Proje için): {project_data.get("Ekip_Tecrubesi", 'Orta')}
        - Risk Payı (Gün): {project_data.get("Risk_Payi_Gun", 0)}

        ÇIKTI FORMATI (KESİNLİKLE UY):
        1. İlk satır: Sadece rakam (tam sayı)
        2. Sonra: 3-4 cümleyle kısa, net gerekçe. Teknik jargon yok. Karar vericiye hitap et.

        Başla:
    """

    # 3. Mesajı Gönder ve Yanıtı Döndür
    response = client.send_message(prompt)
    return response

# Proje anahtar kelimeleri ve varsayılan değerleri tanımlayalım.
PROJECT_INPUT_KEYS = [
    "Fonksiyon_Sayisi", "Karmasiklik_Derecesi", "Entegrasyon_Sayisi", 
    "Ekip_Tecrubesi", "Risk_Payi_Gun"
]
