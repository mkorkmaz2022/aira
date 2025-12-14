import os
import sys
import datetime

# Proje kök dizinini yola ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# DÜZELTME 1: Doğru fonksiyonu import ediyoruz
from ai_agents.brief_notes_agent import generate_ai_report
from services.pdf_service import PDFService 

def process_meeting_request(request_data: dict):
    """
    Backend'den gelen isteği işler ve PDF üretir.
    Girdi: { "persona": "...", "project": "...", "raw_notes": "..." }
    Çıktı: { "status": "success", "pdf_path": "reports/rapor_123.pdf" }
    """
    print(f"\n🔄 İstek Alındı: {request_data['project']} ({request_data['persona']})")
    
    # 1. AI ile Rapor Metnini Oluştur
    print("🤖 AI Raporu Hazırlanıyor...")
    
    # DÜZELTME 2: Yeni fonksiyona uygun parametreleri gönderiyoruz
    ai_report_text = generate_ai_report(
        notes=request_data['raw_notes'],
        manual_actions="", # Eğer frontend'den gelirse buraya eklenir
        persona=request_data['persona'],
        project_name=request_data['project']
    )
    
    if "API_HATA" in ai_report_text:
        return {"status": "error", "message": ai_report_text}

    # 2. PDF Oluştur
    print("📄 PDF'e Dönüştürülüyor...")
    pdf_service = PDFService()
    
    # Dosya adını benzersiz yapalım (Tarih + Proje)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_project_name = request_data['project'].replace(" ", "_")
    filename = f"{safe_project_name}_{timestamp}.pdf"
    
    pdf_path = pdf_service.create_pdf(
        filename=filename,
        project=request_data['project'],
        persona=request_data['persona'],
        content=ai_report_text
    )

    # 3. Sonuç Dön (PDF Dosya Yolu)
    return {
        "status": "success",
        "message": "Rapor başarıyla oluşturuldu.",
        "pdf_path": pdf_path,
        "ai_summary_preview": ai_report_text[:100] + "..." # Önizleme için
    }

# --- TEST SİMÜLASYONU ---
if __name__ == "__main__":
    print("🚀 BACKEND TEST BAŞLATILIYOR...")
    
    # Sanki backend'den gelmiş gibi bir veri paketi
    mock_incoming_data = {
        "persona": "Yönetici",
        "project": "Atlas Logistics",
        "raw_notes": """
        - Lojistik firmalarıyla görüşüldü, fiyatlar %10 artmış.
        - Yeni tırların plakaları haftaya çıkıyor.
        - Muhasebe ile bütçe revizyonu lazım.
        - Ali bey operasyon sorumlusu oldu.
        """
    }
    
    try:
        result = process_meeting_request(mock_incoming_data)
        print("\n✅ İŞLEM SONUCU:")
        print(result)
    except Exception as e:
        print(f"\n❌ BEKLENMEDİK HATA: {e}")