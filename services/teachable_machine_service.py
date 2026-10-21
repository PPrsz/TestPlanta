import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
from config import Config

class TeachableMachineService:
    """
    Serviço de inferência local com modelo treinado no Google Teachable Machine.
    Suporta modelos no formato SavedModel (saved_model.pb + variables).
    """

    def __init__(self, model_path: str = None, labels_file: str = None):
        self.model_path = model_path or Config.TM_MODEL_PATH
        self.labels_file = labels_file or Config.TM_LABELS_FILE
        self.infer_fn = None
        self.labels: List[str] = []
        self.is_loaded = False
        self.load_error: str = None
        
        self.load_model()

    def load_model(self) -> bool:
        """Carrega o modelo SavedModel e as classes do arquivo de labels."""
        try:
            abs_model_path = os.path.abspath(self.model_path)
            abs_labels_path = os.path.abspath(self.labels_file)

            if not os.path.exists(abs_labels_path):
                self.load_error = f"Arquivo de rótulos não encontrado em: {abs_labels_path}"
                self.is_loaded = False
                return False

            with open(abs_labels_path, "r", encoding="utf-8") as f:
                raw_labels = [line.strip() for line in f.readlines() if line.strip()]
            
            # Limpar índices como "0 Plantas Saudáveis" -> "Plantas Saudáveis"
            cleaned_labels = []
            for label in raw_labels:
                parts = label.split(" ", 1)
                if len(parts) > 1 and parts[0].isdigit():
                    cleaned_labels.append(parts[1])
                else:
                    cleaned_labels.append(label)
            self.labels = cleaned_labels

            # Carregar o SavedModel
            imported = tf.saved_model.load(abs_model_path)
            if "serving_default" in imported.signatures:
                self.infer_fn = imported.signatures["serving_default"]
            else:
                first_sig = list(imported.signatures.keys())[0]
                self.infer_fn = imported.signatures[first_sig]

            self.is_loaded = True
            self.load_error = None
            return True

        except Exception as e:
            self.is_loaded = False
            self.load_error = f"Falha ao inicializar modelo Teachable Machine: {str(e)}"
            return False

    def preprocess_image(self, pil_image: Image.Image) -> np.ndarray:
        """
        Pré-processamento padronizado para Teachable Machine:
        - Ajuste para 224x224 (LANCZOS)
        - Normalização de [0, 255] para [-1, 1]
        - Expansão de dimensão batch [1, 224, 224, 3]
        """
        img_rgb = pil_image.convert("RGB")
        resized_img = ImageOps.fit(img_rgb, Config.TM_IMAGE_SIZE, Image.Resampling.LANCZOS)
        img_array = np.asarray(resized_img, dtype=np.float32)
        
        # Normalização [-1, 1] padrão do Teachable Machine (MobileNet)
        normalized_array = (img_array / 127.5) - 1.0
        batch_array = np.expand_dims(normalized_array, axis=0)
        return batch_array

    def predict(self, pil_image: Image.Image) -> Dict[str, Any]:
        """
        Executa inferência na imagem e retorna distribuição de probabilidades,
        classe líder, confiança e diagnóstico de ambiguidade.
        """
        if not self.is_loaded:
            return {
                "success": False,
                "error": self.load_error or "Modelo não carregado.",
                "predictions": {},
                "top_class": "Indisponível",
                "top_confidence": 0.0,
                "is_ambiguous": True,
                "summary": "Modelo local indisponível."
            }

        try:
            batch_data = self.preprocess_image(pil_image)
            input_tensor = tf.convert_to_tensor(batch_data)
            raw_predictions = self.infer_fn(input_tensor)
            
            output_key = list(raw_predictions.keys())[0]
            scores = raw_predictions[output_key].numpy()[0]
            
            # Mapear scores para cada classe
            predictions_map = {}
            for i, label in enumerate(self.labels):
                score = float(scores[i]) if i < len(scores) else 0.0
                predictions_map[label] = round(score, 4)

            # Ordenar por probabilidade decrescente
            sorted_classes = sorted(predictions_map.items(), key=lambda x: x[1], reverse=True)
            top_class, top_confidence = sorted_classes[0]
            second_confidence = sorted_classes[1][1] if len(sorted_classes) > 1 else 0.0

            # Detecção de ambiguidade e incerteza
            margin = top_confidence - second_confidence
            is_low_confidence = top_confidence < Config.TM_CONFIDENCE_THRESHOLD
            is_close_margin = (len(sorted_classes) > 1) and (margin < Config.TM_AMBIGUITY_MARGIN)
            is_ambiguous = is_low_confidence or is_close_margin

            if is_ambiguous:
                summary = (
                    f"Classificação ambígua pelo Teachable Machine: {top_class} ({top_confidence*100:.1f}%), "
                    f"porém com margem estreita para {sorted_classes[1][0]} ({second_confidence*100:.1f}%). "
                    "Necessária validação aprofundada com visão do Gemini."
                )
            else:
                summary = f"Padrão visual classificado como '{top_class}' com {top_confidence*100:.1f}% de certeza local."

            return {
                "success": True,
                "error": None,
                "predictions": predictions_map,
                "sorted_predictions": sorted_classes,
                "top_class": top_class,
                "top_confidence": top_confidence,
                "confidence_percent": round(top_confidence * 100, 2),
                "margin": round(margin, 4),
                "is_ambiguous": is_ambiguous,
                "summary": summary
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Erro durante a predição: {str(e)}",
                "predictions": {},
                "top_class": "Erro",
                "top_confidence": 0.0,
                "is_ambiguous": True,
                "summary": "Falha na execução do modelo local."
            }
