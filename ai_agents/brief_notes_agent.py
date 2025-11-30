# ai_agents/effort_estimator_agent.py
import os
from ai.google_ai import GoogleAIClient
from dotenv import load_dotenv

load_dotenv()

def brief_notes_agent(project_data: str) -> str:
    """
    Toplantı notlarını özetlemek için Google AI'dan yardım ister.

    Args:
        project_data (str): Kullanıcıdan alınan ham toplantı notları.

    Returns:
        str: AI'dan gelen ham özet metni (Toplantı Özeti şablonunda).
    """
    # 1. AI İstemcisini Hazırla
    try:
        client = GoogleAIClient()
    except ValueError as e:
        return f"API_HATA: {e}. Lütfen .env dosyasını kontrol edin."

    # 2. Giriş Verisini Kontrol Et
    if not isinstance(project_data, str) or not project_data.strip():
        return "HATA: Toplantı notları geçersiz veya boş."

    meeting_notes = project_data.strip()

    # 3. Toplantı Notları İçin İstemi Oluştur
    prompt = f"""
Sen bir Toplantı Özeti Uzmanısın. Görev: Aşağıdaki toplantı notlarını oku, yalnızca ana tartışma noktalarını, alınan kararları ve eylem maddelerini çıkararak kısa, net ve taranabilir bir özet üret. Her madde 1-2 cümle olsun, gereksiz detayları atla. EK KURALLAR: Risk veya engel belirtilmişse, özetin sonuna bir cümlelik uyarı ekle; eylem maddelerine sorumlu kişi ve (varsa) son tarih ekle. ÇIKTI FORMATI (KESİNLİKLE UY):

**Toplantı Özeti**  
- **Ana Tartışmalar**: (madde işaretli, 2-4 madde)  
- **Kararlar**: (kalın yaz, 1-3 madde)  
- **Eylem Maddeleri**: (numaralandırılmış, 1-3 madde)  

**Gerekçe**: 2-3 cümle, teknik jargon kullanma, karar vericilere hitap et.

Toplantı Notları:{meeting_notes}

Başla:
    """

    # 4. Mesajı Gönder ve Yanıtı Döndür
    try:
        response = client.send_message(prompt)
        return response
    except Exception as e:
        return f"API_HATA: Mesaj gönderilirken hata oluştu: {e}"

# Proje anahtar kelimeleri (gelecekteki genişletmeler için)
PROJECT_INPUT_KEYS = ["toplanti_notlari"]