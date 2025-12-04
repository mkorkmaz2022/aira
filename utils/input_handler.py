# utils/input_handler.py
def get_manual_project_data() -> str:
    """
    Kullanıcıdan çok satırlı toplantı notlarını alır.
    """
    print("--------------------------------------------------")
    print("📝 Toplantı Notlarını Girin (Bitirmek için **###SON###** yazın):")
    print("--------------------------------------------------")
    
    lines = []
    # Çok satırlı girişi okumaya başla
    while True:
        try:
            line = input()
        except EOFError:
            # Ctrl+D (EOF) basılırsa döngüden çık
            break

        if line.strip().upper() == "###SON###":
            print("Toplantı notları girişi tamamlandı.")
            break
        lines.append(line)
        
    meeting_notes = "\n".join(lines).strip()
    
    if not meeting_notes:
        print("UYARI: Toplantı notları boş, None olarak işlenecek.")
        return None

    print("--------------------------------------------------")
    print(f"✅ Toplantı Notları Hazırlandı: {meeting_notes[:50]}..." if len(meeting_notes) > 50 else f"✅ Toplantı Notları Hazırlandı: {meeting_notes}")
    return meeting_notes