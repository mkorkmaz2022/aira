# ai/base.py
from abc import ABC, abstractmethod

class AIClient(ABC):
    """
    Tüm yapay zeka istemcileri için temel soyut sınıf.
    Projemizi belirli bir LLM sağlayıcısına bağlamamak için kullanılır.
    """
    @abstractmethod
    def send_message(self, message: str) -> str:
        """Belirtilen mesajı LLM'e gönderir ve yanıtı döndürür."""
        pass
