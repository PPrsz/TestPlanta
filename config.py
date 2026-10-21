import os
from pathlib import Path
from dotenv import load_dotenv

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Carregar arquivo .env se existir
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
else:
    load_dotenv()

class Config:
    """Configurações centrais do PlantCare AI / Agrônomo Inteligente."""
    
    # Chave de API do Google Gemini (compatível com .env local e st.secrets do Streamlit Cloud)
    _api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not _api_key:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                _api_key = str(st.secrets["GEMINI_API_KEY"]).strip()
        except Exception:
            pass
    GEMINI_API_KEY = _api_key
    
    # Modelos Gemini preferenciais em ordem de fallback
    PRIMARY_GEMINI_MODEL = os.getenv("PRIMARY_GEMINI_MODEL", "gemini-3.8-flash")
    FALLBACK_MODELS = [
        m.strip() for m in os.getenv(
            "FALLBACK_GEMINI_MODELS", 
            "gemini-3.5-flash,gemini-3.5-flash-lite"
        ).split(",") if m.strip()
    ]
    
    # Modelo do Google Teachable Machine (SavedModel local)
    TM_MODEL_PATH = os.getenv("TEACHABLE_MACHINE_MODEL_PATH", str(BASE_DIR))
    TM_LABELS_FILE = os.getenv("TEACHABLE_MACHINE_LABELS_FILE", str(BASE_DIR / "labels.txt"))
    
    # Parâmetros de pré-processamento Teachable Machine
    TM_IMAGE_SIZE = (224, 224)
    TM_CONFIDENCE_THRESHOLD = float(os.getenv("TM_CONFIDENCE_THRESHOLD", "0.65"))  # 65% para alta certeza
    TM_AMBIGUITY_MARGIN = float(os.getenv("TM_AMBIGUITY_MARGIN", "0.15"))          # Margem de 15% entre topo 1 e 2
    
    # Parâmetros de validação de imagem
    MIN_IMAGE_RESOLUTION = (150, 150)
    MAX_IMAGE_DIMENSION = 1200 # Dimensão máxima para envio à API (economiza tokens e latência)
    JPEG_COMPRESSION_QUALITY = 85
    
    # Banco de dados local SQLite
    DATA_DIR = BASE_DIR / "data"
    DB_PATH = DATA_DIR / "plantcare.db"
    UPLOADS_DIR = DATA_DIR / "uploads"
    
    @classmethod
    def initialize_dirs(cls):
        """Garante que os diretórios necessários existam."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Inicializar diretórios
Config.initialize_dirs()
