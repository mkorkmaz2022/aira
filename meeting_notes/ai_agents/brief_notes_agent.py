import os
from ai.google_ai import GoogleAIClient
from dotenv import load_dotenv

load_dotenv()

# Persona Tanımları (UI'daki butonlara karşılık gelen roller)
PERSONA_PROMPTS = {
    "Yönetici": "Sen sonuç odaklı, stratejik düşünen bir Yöneticisin. Bütçe, riskler, zaman çizelgesi ve büyük resme odaklan.",
    "Yazılımcı": "Sen teknik detaylara hakim bir Yazılımcısın (Tech Lead). Kod kalitesi, API değişiklikleri, buglar ve teknik borçlara odaklan.",
    "Satış/Pazarlama": "Sen müşteri odaklı bir Satışçısın. Gelir fırsatları, müşteri memnuniyeti ve ürünün pazarlanabilir özelliklerine odaklan.",
    "Tasarımcı": "Sen kullanıcı deneyimi (UX/UI) odaklı bir Tasarımcısın. Görsel tutarlılık, kullanıcı akışları ve arayüz kararlarına odaklan."
}

def generate_ai_report(notes: str, manual_actions: str, persona: str, project_name: str) -> str:
    """
    Mobil ekrandan gelen verileri (Persona, Proje, Notlar, Aksiyonlar) alıp
    kişiselleştirilmiş bir rapor üretir.
    """
    try:
        client = GoogleAIClient()
    except ValueError as e:
        return f"API_HATA: {e}"

    # Persona'ya uygun rolü seç, yoksa varsayılan davran
    role_description = PERSONA_PROMPTS.get(persona, "Sen uzman bir Asistansın.")

    prompt = f"""
    {role_description}
    
    Şu an üzerinde çalıştığımız proje: **{project_name}**
    
    GÖREVİN:
    Aşağıda girilen "Ham Toplantı Notları" ve kullanıcının eklediği "Manuel Aksiyon Maddeleri"ni kullanarak,
    benim bakış açıma ({persona}) uygun profesyonel bir rapor oluştur.

    GİRDİLER:
    ---
    📝 Ham Notlar:
    {notes}
    
    ⚡ Girilen Aksiyonlar:
    {manual_actions}
    ---

    KURALLAR:
    1. Benim personama ({persona}) uygun bir dil kullan. (Örn: Yazılımcıysam teknik konuş, Yöneticiysem özet geç).
    2. Manuel girilen aksiyonları, notlardan çıkardığın diğer aksiyonlarla birleştir ve "Aksiyonlar" başlığı altında topla.
    3. Çıktı formatını kesinlikle bozma.

    İSTENEN ÇIKTI FORMATI:
    
    **📌 {project_name} - {persona} Raporu**
    (Persona bakış açısıyla yazılmış 2-3 cümlelik yönetici özeti.)

    **🔹 Kritik Başlıklar**
    * (Madde 1)
    * (Madde 2)

    **✅ Alınan Kararlar**
    * (Karar 1)
    * (Karar 2)

    **🚀 Aksiyon Planı**
    1. (Manuel girilen aksiyonlar buraya entegre edilecek)
    2. (Notlardan çıkarılan yeni görevler)
    
    Başla:
    """

    try:
        response = client.send_message(prompt)
        return response
    except Exception as e:
        return f"API_HATA: {e}"