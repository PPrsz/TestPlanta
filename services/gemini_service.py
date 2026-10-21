import json
import re
from typing import Dict, Any, Optional, List
from PIL import Image
from google import genai
from google.genai import types
from google.genai.errors import APIError, ClientError, ServerError
from config import Config

class GeminiPlantDoctorService:
    """
    Serviço botânico avançado integrado à API oficial do Google Gemini.
    Processa imagens, contextualiza predições do Teachable Machine,
    avalia sintomas, infere causas e gera planos de tratamento estruturados.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.client = None
        self._init_client()

    def _init_client(self):
        """Inicializa o cliente oficial da biblioteca google-genai com segurança."""
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                self.client = None

    def is_configured(self) -> bool:
        """Verifica se a API Key do Gemini está presente."""
        return bool(self.api_key and self.client is not None)

    def set_api_key(self, new_key: str):
        """Permite atualizar a chave dinamicamente pela interface de usuário."""
        self.api_key = new_key.strip()
        self._init_client()

    def analyze_plant(
        self,
        image: Image.Image,
        tm_result: Optional[Dict[str, Any]] = None,
        user_context: Optional[Dict[str, Any]] = None,
        preferred_model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executa a análise botânica completa e estruturada da planta.
        Implementa redundância/fallback automático entre modelos Gemini caso haja
        alta demanda (503), quota ou indisponibilidade temporária.
        """
        if not self.is_configured():
            return {
                "success": False,
                "error_type": "NO_API_KEY",
                "error_message": (
                    "A chave da API do Google Gemini não está configurada. "
                    "Configure a variável de ambiente GEMINI_API_KEY no arquivo .env "
                    "ou insira sua chave na aba de Configurações."
                )
            }

        # Modelos candidatos em ordem de prioridade
        primary = preferred_model or Config.PRIMARY_GEMINI_MODEL
        candidates = [primary] + [m for m in Config.FALLBACK_MODELS if m != primary]

        # Contexto do Teachable Machine formatado
        tm_info = "Modelo Teachable Machine local não utilizado ou indisponível."
        if tm_result and tm_result.get("success"):
            predictions_str = ", ".join([f"{k}: {v*100:.1f}%" for k, v in tm_result.get("predictions", {}).items()])
            tm_info = (
                f"- Classe mais provável detectada: '{tm_result.get('top_class')}' ({tm_result.get('confidence_percent')}%% de confiança).\n"
                f"- Distribuição completa: {predictions_str}.\n"
                f"- Diagnóstico de ambiguidade: {'Sim (margem estreita / baixa certeza)' if tm_result.get('is_ambiguous') else 'Não (alta convicção visual local)'}."
            )

        # Contexto do usuário formatado
        user_info = "Nenhum histórico adicional fornecido pelo usuário."
        if user_context:
            ctx_lines = []
            for k, v in user_context.items():
                if v:
                    ctx_lines.append(f"- {k}: {v}")
            if ctx_lines:
                user_info = "\n".join(ctx_lines)

        prompt = f"""
Você é um Agrônomo e Botânico especialista de alto nível, com vasta experiência em patologia vegetal, fisiologia vegetal e jardinagem doméstica.
Analise a fotografia da planta em conjunto com os sinais do modelo classificador local e o histórico fornecido pelo usuário.

=== DADOS DO MODELO LOCAL (TEACHABLE MACHINE) ===
{tm_info}

=== HISTÓRICO E CONTEXTO DO USUÁRIO ===
{user_info}

=== DIRETRIZES FUNDAMENTAIS DE DIAGNÓSTICO E SEGURANÇA ===
1. Precisão e Transparência: Nunca afirme um diagnóstico como certeza absoluta se as evidências visuais forem limitadas. Diferencie claramente "sintomas observados" de "causas inferidas".
2. Discernimento de Sintomas Semelhantes: Amarelecimento pode ser excesso de água, falta de nitrogênio, raiz apodrecida ou senescência natural. Aponte essa distinção didaticamente.
3. Tratamento Seguro e Sustentável: Priorize intervenções mecânicas, ambientais e culturais (rega, drenagem, luz solar, ventilação, poda de folhas danificadas). Não recomende indiscriminadamente defensivos químicos perigosos ou receitas caseiras agressivas.
4. Coerência com o Teachable Machine: Analise criticamente se a predição do modelo local faz sentido perante a imagem real ou se é um falso positivo/falso negativo.

Responda OBRIGATORIAMENTE em formato JSON com EXATAMENTE a seguinte estrutura:

{{
  "identificacao": {{
    "nome_popular": "Nome popular da planta ou 'Não identificada com certeza'",
    "nome_cientifico": "Nome científico ou 'Inconclusivo'",
    "familia_ou_genero": "Família ou gênero botânico",
    "confianca_identificacao": "Alta" | "Média" | "Baixa",
    "caracteristicas_gerais": "Breve resumo dos hábitos da espécie (luz, umidade ideal)"
  }},
  "estado_saude": {{
    "status": "Aparentemente saudável" | "Possíveis sinais de doença" | "Possível infestação de pragas" | "Possível deficiência nutricional" | "Possível estresse ambiental" | "Resultado inconclusivo",
    "confianca_diagnostico": "Alta" | "Média" | "Baixa",
    "gravidade_estimada": "Nenhuma" | "Baixa" | "Média" | "Alta" | "Crítica",
    "resumo_geral": "Síntese em uma ou duas frases sobre o estado da planta"
  }},
  "analise_sintomas": {{
    "sintomas_visiveis": ["Lista de sintomas anatômicos visíveis na imagem"],
    "partes_afetadas": ["Folhas novas", "Folhas velhas", "Caules", "Bordas", etc],
    "diferenciacao_sintoma_causa": "Explicação que separa o sinal visual (ex: manchas necróticas) do agente causador provável",
    "causas_provaveis": [
      {{
        "causa": "Nome da provável causa ou patógeno",
        "probabilidade": "Provável" | "Possível" | "Secundária",
        "explicacao": "Por que esta causa se adequa ao quadro visível"
      }}
    ],
    "hipoteses_alternativas": ["Outras possibilidades caso a causa principal seja descartada"],
    "doencas_com_sintomas_semelhantes": "Comparativo curto entre doenças ou estresses que causam sintomas parecidos"
  }},
  "coerencia_teachable_machine": {{
    "concordancia": "Concorda" | "Diverge" | "Complementa" | "Inconclusivo",
    "explicacao": "Como a análise visual profunda do Gemini valida ou refina a classificação do modelo local"
  }},
  "perguntas_complementares": [
    "Perguntas pontuais caso o usuário deseje refinar o diagnóstico (máximo 3 perguntas curtas)"
  ],
  "plano_tratamento": {{
    "resumo": "Visão geral da conduta recomendada",
    "cuidados_imediatos": ["Ações rápidas para conter o dano nas próximas 24-48 horas"],
    "passo_a_passo": [
      {{
        "etapa": 1,
        "titulo": "Título da ação",
        "descricao": "Como executar a ação passo a passo",
        "prioridade": "Alta" | "Média" | "Preventiva"
      }}
    ],
    "prevencao": ["Como evitar que o problema retorne"],
    "tempo_acompanhamento": "Ex: Verificar evolução em 5 a 7 dias",
    "sinais_de_melhora": ["O que indica que a planta está se recuperando"],
    "sinais_de_piora": ["Sinais de alerta que demandam poda drástica ou ajuda agronômica especializada"],
    "cuidados_com_quimicos_e_receitas": "Orientações de segurança sobre fertilizantes ou tratamentos fitossanitários"
  }},
  "limitacoes_e_transparencia": "Aviso sobre as limitações do diagnóstico digital por fotografia"
}}
"""

        last_error = None
        for model_name in candidates:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=[image, prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2, # Baixa temperatura para diagnósticos mais precisos e consistentes
                    )
                )

                if response and response.text:
                    parsed_json = self._extract_json(response.text)
                    if parsed_json:
                        return {
                            "success": True,
                            "model_used": model_name,
                            "data": parsed_json,
                            "raw_text": response.text
                        }
                    else:
                        last_error = f"Resposta do modelo {model_name} não pôde ser convertida para JSON estruturado."

            except ClientError as ce:
                # 404 model not found ou 400 Bad Request -> tentar próximo modelo
                last_error = f"Erro de cliente no modelo {model_name}: {str(ce)}"
                continue
            except ServerError as se:
                # 503 temporariamente indisponível -> tentar modelo alternativo
                last_error = f"Modelo {model_name} em alta demanda (503): {str(se)}"
                continue
            except APIError as ae:
                last_error = f"Erro da API Google Gemini ({model_name}): {str(ae)}"
                continue
            except Exception as e:
                last_error = f"Falha inesperada com {model_name}: {str(e)}"
                continue

        return {
            "success": False,
            "error_type": "API_CALL_FAILED",
            "error_message": f"Não foi possível obter diagnóstico do Gemini. Detalhes: {last_error}"
        }

    def _extract_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """Extrai e decodifica o JSON retornado pelo modelo de forma resiliente."""
        text = raw_text.strip()
        
        # Tentar decodificação direta
        try:
            return json.loads(text)
        except Exception:
            pass

        # Remover blocos Markdown tipo ```json ... ``` se existirem
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass

        # Buscar qualquer bloco entre primeira '{' e última '}'
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except Exception:
                pass

        return None
