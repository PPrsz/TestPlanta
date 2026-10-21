import io
import numpy as np
from PIL import Image, ImageOps, ImageStat

class ImageQualityService:
    """
    Serviço especializado na validação, auditoria de qualidade e otimização
    de imagens fotográficas de plantas para análise botânica e patológica.
    """

    @staticmethod
    def inspect_and_validate(pil_image: Image.Image) -> dict:
        """
        Analisa resolução, iluminação, contraste e nitidez da imagem.
        Retorna dicionário com diagnóstico de qualidade e recomendações.
        """
        width, height = pil_image.size
        rgb_image = pil_image.convert("RGB")
        grayscale = rgb_image.convert("L")
        
        # 1. Estatísticas de Iluminação e Contraste
        stat = ImageStat.Stat(grayscale)
        mean_brightness = stat.mean[0]   # 0 (preto) a 255 (branco)
        contrast_std = stat.stddev[0]     # desvio padrão do brilho
        
        # 2. Estimativa de Nitidez (Gradiente / Variância Laplaciana simplificada com NumPy)
        gray_arr = np.array(grayscale, dtype=np.float32)
        # Diferenças de primeira ordem horizontal e vertical
        grad_y = np.diff(gray_arr, axis=0)
        grad_x = np.diff(gray_arr, axis=1)
        sharpness_score = float(np.var(grad_x) + np.var(grad_y))
        
        issues = []
        recommendations = []
        quality_rating = "Excelente"
        
        # Validação de Resolução
        if width < 200 or height < 200:
            issues.append(f"Resolução muito baixa ({width}x{height}px).")
            recommendations.append("Tire uma foto mais próxima ou com maior resolução.")
            quality_rating = "Inadequada"
        elif width < 400 or height < 400:
            issues.append(f"Resolução modesta ({width}x{height}px).")
            recommendations.append("Fotos mais nítidas facilitam a identificação de pequenas pragas.")
            if quality_rating != "Inadequada":
                quality_rating = "Aceitável"

        # Validação de Iluminação
        if mean_brightness < 45:
            issues.append("Imagem excessivamente escura / subexposta.")
            recommendations.append("Fotografe em local mais iluminado ou com luz solar indireta.")
            quality_rating = "Baixa"
        elif mean_brightness > 225:
            issues.append("Imagem excessivamente clara / superexposta (ofuscada).")
            recommendations.append("Evite luz solar direta intensa provocando reflexos nas folhas.")
            quality_rating = "Baixa"

        # Validação de Contraste
        if contrast_std < 22:
            issues.append("Baixo contraste entre a folha e o fundo.")
            recommendations.append("Posicione a planta contra um fundo neutro ou com melhor contraste.")
            if quality_rating not in ["Inadequada", "Baixa"]:
                quality_rating = "Aceitável"

        # Validação de Nitidez / Foco
        if sharpness_score < 40.0:
            issues.append("Possível desfoque ou perda de nitidez.")
            recommendations.append("Mantenha a câmera estável e foque exatamente na lesão ou sintoma da folha.")
            if quality_rating != "Inadequada":
                quality_rating = "Baixa"

        is_acceptable = quality_rating not in ["Inadequada"]

        return {
            "is_acceptable": is_acceptable,
            "quality_rating": quality_rating,
            "width": width,
            "height": height,
            "brightness": round(mean_brightness, 1),
            "contrast": round(contrast_std, 1),
            "sharpness": round(sharpness_score, 1),
            "issues": issues,
            "recommendations": recommendations,
        }

    @staticmethod
    def prepare_for_ai(pil_image: Image.Image, max_dimension: int = 1200, quality: int = 85) -> Image.Image:
        """
        Otimiza, corrige orientação EXIF e redimensiona a imagem para consumo da API do Gemini,
        economizando dados e latência sem perder detalhes botânicos vitais.
        """
        # Tratar orientação EXIF (muito comum em fotos tiradas por smartphones)
        transposed_img = ImageOps.exif_transpose(pil_image)
        if transposed_img is None:
            transposed_img = pil_image
            
        img = transposed_img.convert("RGB")
        w, h = img.size
        
        if max(w, h) > max_dimension:
            scale = max_dimension / float(max(w, h))
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
        # Comprimir em buffer JPEG para normalização de formato
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        buffer.seek(0)
        return Image.open(buffer)
