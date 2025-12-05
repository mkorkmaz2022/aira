# utils/input_handler.py

def get_manual_project_data() -> list: # Dönüş tipi artık list
    """
    Kullanıcıdan toplantı notlarını satır satır alır ve liste olarak döndürür.
    """
    print("--------------------------------------------------")
    print("📝 Toplantı Notlarını Girin (Her satır ayrı bir madde olsun).")
    print("Bitirmek için **###SON###** yazın:")
    print("--------------------------------------------------")
    
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip().upper() == "###SON###":
            print("✅ Not girişi tamamlandı.")
            break
        
        # Boş satırları listeye eklemeyelim
        if line.strip():
            lines.append(line.strip())
        
    if not lines:
        print("UYARI: Hiç not girilmedi.")
        return []

    print(f"✅ {len(lines)} adet madde alındı.")
    return lines # Artık string değil, liste dönüyor