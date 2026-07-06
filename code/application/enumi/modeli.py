from enum import Enum



# Enum Modeli
class Modeli(Enum):
    COVJEK = (None, 'Čovjek')
    CHAT_GPT = (1, 'ChatGPT')
    CLAUDE = (2, 'Claude')
    GEMINI = (3, 'Gemini')

    def __init__(self, model_id, naziv):
        self.model_id = model_id
        self.naziv = naziv
