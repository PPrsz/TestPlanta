# 🌿 PlantCare AI — Diagnóstico e Saúde Vegetal com IA

Aplicativo moderno e inteligente para identificação botânica, diagnóstico patológico e acompanhamento terapêutico de plantas. Combina **Google Teachable Machine** (classificação visual local com TensorFlow) e a API oficial do **Google Gemini** (raciocínio agronômico e botânico com visão computacional multimodal).

---

## 🌟 Principais Recursos

1. **Combinação de IA Híbrida (Teachable Machine + Gemini):**
   - **Camada 1 (Teachable Machine):** Classifica padrões visuais aprendidos localmente em frações de segundo (`SavedModel`), computando probabilidades e detectando ambiguidades ou margens estreitas.
   - **Camada 2 (Google Gemini Multimodal):** Interpreta a fotografia em alta definição, cruza com a predição local, identifica a espécie (nome popular e científico), investiga causas fundamentadas e formula recomendações personalizadas.
2. **Auditoria de Qualidade Fotográfica:**
   - Avalia resolução mínima, iluminação (subexposição/superexposição) e nitidez/foco antes do processamento, instruindo o usuário caso a foto precise de ajuste.
3. **Diagnóstico Estruturado e Científico:**
   - Diferencia claramente **sintomas visíveis** de **causas inferidas**.
   - Aponta hipóteses alternativas e diagnóstico diferencial para doenças com sintomas parecidos (ex: amarelecimento por rega vs. deficiência de nitrogênio).
   - Avalia gravidade estimada (Nenhuma, Baixa, Média, Alta, Crítica) e grau de confiança.
4. **Plano Terapêutico e de Recuperação:**
   - Ações imediatas (24-48 horas) para conter danos.
   - Passo a passo prático com prioridades.
   - Prevenção contra reinfecções.
   - Sinais de melhora e sinais de piora.
   - Alertas de segurança fitossanitária (evita receitas caseiras arriscadas e produtos químicos desnecessários).
5. **Meu Jardim & Acompanhamento Temporal:**
   - Cadastro e gerenciamento de plantas.
   - Histórico cronológico de diagnósticos e fotografias.
   - **Comparador Visual de Evolução (Antes x Depois):** Visualize lado a lado a recuperação da planta e registre se os sintomas estão regredindo.
   - Diário de cuidados com registro rápido (Rega, Adubação, Poda Sanitária).
6. **Segurança e Privacidade:**
   - Chave de API protegida em `.env` no backend, nunca exposta no frontend.
   - Fallback inteligente entre modelos Gemini (`gemini-3.8-flash`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`).
   - Persistência relacional em banco de dados SQLite local (`data/plantcare.db`).

---

## 🏗️ Arquitetura do Projeto

```
AntiGravity Stuff/
│
├── .env                          # Variáveis de ambiente com chave de API (ignorado em commits)
├── .env.example                  # Modelo de configuração sem dados sensíveis
├── config.py                     # Configurações globais e limiares do sistema
├── app.py                        # Interface principal Streamlit e controlador
├── requirements.txt              # Dependências Python
├── saved_model.pb                # Arquivo do modelo SavedModel (Teachable Machine)
├── variables/                    # Pesos do modelo Teachable Machine
├── assets/                       # Metadados do modelo
├── labels.txt                    # Classes do classificador local
├── plantas_1.jpg                 # Amostra de teste
│
├── services/
│   ├── teachable_machine_service.py # Inferência local TensorFlow, probabilidades e ambiguidade
│   ├── gemini_service.py            # Integração oficial Google GenAI, fallback e JSON estruturado
│   ├── image_quality_service.py     # Inspeção de iluminação, nitidez e compressão inteligente
│   └── database_service.py          # Persistência relacional SQLite (plantas, diagnósticos, histórico)
│
├── ui/
│   ├── styles.py                    # Tema CSS botânico (Verde-Floresta, Sálvia, Neutros)
│   └── components.py                # Cartões de diagnóstico, stepper, badges e comparadores
│
├── data/                            # Banco de dados e uploads
│   ├── plantcare.db                 # Banco SQLite local
│   └── uploads/                     # Fotos salvas no histórico
│
└── tests/
    └── test_pipeline.py             # Testes unitários e de integração
```

---

## 🚀 Instalação e Execução

### 1. Pré-requisitos
- Python 3.10 ou superior.

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar a Chave da API do Google Gemini
Crie ou edite o arquivo `.env` na raiz do projeto:
```env
GEMINI_API_KEY=sua_chave_aqui
PRIMARY_GEMINI_MODEL=gemini-3.8-flash
FALLBACK_GEMINI_MODELS=gemini-3.5-flash,gemini-3.5-flash-lite
TEACHABLE_MACHINE_MODEL_PATH=.
TEACHABLE_MACHINE_LABELS_FILE=labels.txt
```
> Obtenha sua chave gratuita em [Google AI Studio](https://aistudio.google.com/).

### 4. Iniciar o Aplicativo
```bash
streamlit run app.py
```
O navegador abrirá automaticamente em `http://localhost:8501`.

---

## 🔬 Como Exportar e Atualizar o Teachable Machine

Caso treine um novo modelo no [Google Teachable Machine](https://teachablemachine.withgoogle.com/):
1. No projeto do Teachable Machine, clique em **Export Model** (Exportar Modelo).
2. Selecione a aba **TensorFlow** e escolha o formato **SavedModel**.
3. Baixe o arquivo `.zip` gerado.
4. Extraia o conteúdo diretamente na pasta do projeto (substituindo `saved_model.pb`, a pasta `variables/` e o arquivo `labels.txt`).
5. No aplicativo, acesse **⚙️ Configurações & API** e clique em **🔄 Recarregar Modelo Teachable Machine**.

---

## 🧪 Execução de Testes Automatizados

Para rodar a bateria de testes unitários do pipeline:
```bash
python tests/test_pipeline.py
```
Os testes cobrem:
- Validação e auditoria de qualidade fotográfica (resolução, brilho, foco).
- Carga e inferência do modelo TensorFlow local com classes reais.
- Persistência e integridade do banco de dados SQLite.
