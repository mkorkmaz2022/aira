# ai/google_ai.py
import os
from dotenv import load_dotenv
from ai.base import AIClient
# google.generativeai kütüphanesinin kurulu olması gerekir (requirements.txt'te var)
import google.generativeai as genai 


load_dotenv()

class GoogleAIClient(AIClient):
    """Gemini (Google AI) ile iletişim kurmak için bir istemci."""
    def __init__(self, api_key: str = None):
        # API anahtarını ortam değişkeninden veya doğrudan gelen argümandan al.
        api_key_env = api_key or os.getenv("GOOGLE_AI_API_KEY")
        if not api_key_env:
            raise ValueError("GOOGLE_AI_API_KEY ortam değişkeni ayarlanmalıdır.")
            
        genai.configure(api_key=api_key_env)
        # İş gücü tahmini için hızlı ve yetenekli bir model.
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def send_message(self, message: str) -> str:
        """Mesajı Gemini'ye gönderir ve metin yanıtını döndürür."""
        try:
            # Yapılandırılmış (Structured) çıktı almak için kullanılabilir.
            # Şimdilik basit metin döndürelim.
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            # Hata durumunda boş döndürüp main.py'de yönetmek daha iyidir.
            print(f"❌ Gemini API Hatası: {e}")
            return f"API_ERROR: {e}"
