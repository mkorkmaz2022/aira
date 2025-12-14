import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

class PDFService:
    def __init__(self, output_folder="reports"):
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # --- TÜRKÇE FONT KAYDI ---
        # 'arial.ttf' dosyasının services klasöründe olduğunu varsayıyoruz.
        font_path = os.path.join(os.path.dirname(__file__), 'ARIAL.TTF') 
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('Arial', font_path))
            self.main_font = 'Arial'
        else:
            print("⚠️ UYARI: arial.ttf bulunamadı. Türkçe karakterler bozuk çıkabilir.")
            self.main_font = 'Helvetica' # Yedek font

        # --- STİL TANIMLARI ---
        styles = getSampleStyleSheet()
        
        # Şablondaki stilleri tanımlıyoruz
        self.header_style = ParagraphStyle(
            'Header', parent=styles['Normal'], fontName=self.main_font,
            fontSize=16, textColor=colors.HexColor('#3498db'), leading=20, spaceAfter=10
        )
        self.section_title_style = ParagraphStyle(
            'SectionTitle', parent=styles['Normal'], fontName=self.main_font,
            fontSize=13, textColor=colors.HexColor('#2c3e50'), leading=16, spaceBefore=15, spaceAfter=5,
            borderPadding=5, borderColor=colors.HexColor('#3498db'), borderWidth=0, borderBottomWidth=1
        )
        self.body_style = ParagraphStyle(
            'Body', parent=styles['Normal'], fontName=self.main_font,
            fontSize=10, leading=14, spaceAfter=5
        )
        self.bullet_style = ParagraphStyle(
            'Bullet', parent=styles['Normal'], fontName=self.main_font,
            fontSize=10, leading=14, spaceAfter=5, bulletIndent=10, leftIndent=25, bulletText='•'
        )

    def create_pdf(self, filename, project, persona, content):
        """
        AI raporunu müşteri şablonuna uygun PDF formatına dönüştürür.
        """
        file_path = os.path.join(self.output_folder, filename)
        doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        
        elements = []
        today_str = datetime.datetime.now().strftime("%d.%m.%Y")

        # --- 1. BAŞLIK ALANI (LOGO & TARİH & PROJE) ---
        
        # LOGO (Eğer varsa)
        # logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        # if os.path.exists(logo_path):
        #    im = Image(logo_path, width=4*cm, height=1.5*cm)
        #    im.hAlign = 'LEFT'
        #    elements.append(im)
        # else:
        elements.append(Paragraph("<b>AIRA AI ASİSTAN</b>", self.header_style)) # Logo yoksa metin

        elements.append(Spacer(1, 0.5*cm))

        # Üst Bilgi Tablosu (Proje, Rol, Tarih)
        data = [
            [f"PROJE: {project}", f"TARİH: {today_str}"],
            [f"ROL: {persona}", ""]
        ]
        t = Table(data, colWidths=[12*cm, 5*cm])
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), self.main_font),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('TEXTCOLOR', (0,0), (0,0), colors.HexColor('#2c3e50')),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'), # Tarihi sağa yasla
            ('LINEBELOW', (0,1), (-1,-1), 1, colors.HexColor('#bdc3c7')), # Alt çizgi
        ]))
        elements.append(t)
        elements.append(Spacer(1, 1*cm))

        # --- 2. İÇERİK İŞLEME ---
        
        # AI'dan gelen metni satır satır okuyup uygun stilleri uygulayacağız.
        # Şablondaki başlıkların (** ile başlayanlar) tespiti:
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line: continue

            if line.startswith("**") and line.endswith("**"):
                # Bölüm Başlığı (Örn: **📌 Toplantı Özeti**)
                title_text = line.replace("**", "").strip()
                # Şablondaki ikonları temizle (isteğe bağlı)
                title_text = title_text.replace("📌", "").replace("🔹", "").replace("✅", "").replace("🚀", "").strip()
                elements.append(Paragraph(f"<b>{title_text.upper()}</b>", self.section_title_style))
                
            elif line.startswith("* ") or line.startswith("- "):
                # Maddeli Liste (Örn: * Karar 1)
                bullet_text = line[2:].strip()
                # Metin içindeki kalın kısımları ReportLab etiketine çevir
                bullet_text = bullet_text.replace("**", "<b>", 1).replace("**", "</b>", 1)
                elements.append(Paragraph(bullet_text, self.bullet_style))
                
            elif line[0].isdigit() and line[1] == ".":
                 # Numaralı Liste (Örn: 1. Aksiyon)
                bullet_text = line[2:].strip()
                bullet_text = bullet_text.replace("**", "<b>", 1).replace("**", "</b>", 1)
                elements.append(Paragraph(f"{line[0]}. {bullet_text}", self.bullet_style))

            else:
                # Normal Paragraf
                # Metin içindeki kalın kısımları ReportLab etiketine çevir
                para_text = line.replace("**", "<b>", 1).replace("**", "</b>", 1)
                elements.append(Paragraph(para_text, self.body_style))
                
            elements.append(Spacer(1, 0.2*cm)) # Paragraflar arası boşluk

        # --- 3. PDF OLUŞTUR ---
        doc.build(elements)
        print(f"✅ PDF Oluşturuldu: {file_path}")
        return file_path