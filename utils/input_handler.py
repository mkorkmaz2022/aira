# utils/input_handler.py
from ai_agents.effort_estimator_agent import PROJECT_INPUT_KEYS

def get_manual_project_data() -> dict:
    """
    Kullanıcıdan manuel olarak proje özelliklerini alır.
    (Geliştirmenin ilk aşamasında LLM'e girdi sağlamak için kullanılır.)
    """
    print("--------------------------------------------------")
    print("Proje İş Gücü Tahmini için Girdileri Girin:")
    print("--------------------------------------------------")

    project_data = {}
    
    # Varsayılan değerler
    # Kullanıcının daha sonra elle değiştireceği varsayılır.
    project_data["Fonksiyon_Sayisi"] = int(input("1. Tahmini Fonksiyon Sayısı (Örn: 10): ") or 10)
    
    while True:
        complexity = input("2. Karmaşıklık Derecesi (Düşük/Orta/Yuksek): ") or "Orta"
        if complexity in ["Düşük", "Orta", "Yuksek"]:
            project_data["Karmasiklik_Derecesi"] = complexity
            break
        print("Geçersiz giriş. Lütfen 'Düşük', 'Orta' veya 'Yuksek' girin.")

    project_data["Entegrasyon_Sayisi"] = int(input("3. Harici Entegrasyon Sayısı (Örn: 2): ") or 2)
    project_data["Ekip_Tecrubesi"] = input("4. Ekip Tecrübesi (Yeni/Orta/Tecrübeli): ") or "Orta"
    project_data["Risk_Payi_Gun"] = int(input("5. Risk Payı (Man-Day cinsinden, Örn: 10): ") or 10)

    print("--------------------------------------------------")
    return project_data
