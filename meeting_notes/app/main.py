import os
import sys
import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Proje kök dizinini yola ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_agents.brief_notes_agent import generate_ai_report
from services.pdf_service import PDFService 

# --- API TANIMI ---
app = FastAPI(title="Aira PDF Backend")

# Mobil uygulamadan gelecek veri formatını tanımlıyoruz
class ReportRequest(BaseModel):
    persona: str
    project: str
    raw_notes: str
    action_items: str = "" # Opsiyonel

# --- ANA FONKSİYON (Değişmedi) ---
def process_meeting_logic(data: ReportRequest):
    """
    İş mantığını yürüten fonksiyon.
    """
    print(f"\n🔄 İstek Alındı: {data.project} ({data.persona})")
    
    # 1. AI Raporu
    print("🤖 AI Raporu Hazırlanıyor...")
    ai_report_text = generate_ai_report(
        notes=data.raw_notes,
        manual_actions=data.action_items,
        persona=data.persona,
        project_name=data.project
    )
    
    if "API_HATA" in ai_report_text:
        raise HTTPException(status_code=500, detail=ai_report_text)

    # 2. PDF Oluşturma
    print("📄 PDF'e Dönüştürülüyor...")
    pdf_service = PDFService()
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_project_name = data.project.replace(" ", "_")
    filename = f"{safe_project_name}_{timestamp}.pdf"
    
    pdf_path = pdf_service.create_pdf(
        filename=filename,
        project=data.project,
        persona=data.persona,
        content=ai_report_text
    )

    # 3. Sonuç (PDF Yolu veya URL'i)
    # Gerçek sunucuda burası "https://api.aira.com/reports/dosya.pdf" gibi bir URL döner.
    return {
        "status": "success",
        "message": "Rapor başarıyla oluşturuldu.",
        "pdf_url": pdf_path, # Mobil uygulama bu dosyayı indirecek
        "preview": ai_report_text[:200]
    }

# --- API ENDPOINT ---
# Mobil uygulama BURAYA istek atacak: POST http://sunucu-adresi/generate-report
@app.post("/generate-report")
async def generate_report_endpoint(request: ReportRequest):
    try:
        return process_meeting_logic(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ARTIK 'if main' YOK, UVICORN İLE ÇALIŞTIRILACAK ---