"""
Estilos e Identidade Visual para PlantCare AI / Agrônomo Inteligente.
Paleta inspirada na natureza: Verde-Floresta, Verde-Sálvia, Branco e Tons Neutros.
"""

CUSTOM_CSS = """
<style>
/* Fonte e Reset Suave */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1f2937;
}

/* Esconder cabeçalho padrão Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Variáveis de Cores */
:root {
    --forest-dark: #1b4332;
    --forest-medium: #2d6a4f;
    --forest-light: #40916c;
    --sage-bright: #52b788;
    --sage-soft: #74c69d;
    --sage-pale: #b7e4c7;
    --sage-subtle: #d8f3dc;
    --mint-bg: #f4fbf7;
    --card-bg: #ffffff;
    --border-light: #e5e7eb;
    --text-primary: #111827;
    --text-secondary: #4b5563;
    --text-muted: #6b7280;
    --danger-red: #dc2626;
    --warning-orange: #d97706;
    --info-blue: #2563eb;
}

/* Barra lateral elegante */
[data-testid="stSidebar"] {
    background-color: #081c15 !important;
    background-image: linear-gradient(180deg, #081c15 0%, #1b4332 100%) !important;
}

[data-testid="stSidebar"] * {
    color: #f3f4f6 !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-size: 1.02rem;
    font-weight: 500;
    padding: 6px 12px;
    border-radius: 8px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255, 255, 255, 0.08);
}

/* Cabeçalho Principal */
.plant-hero-card {
    background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
    color: white;
    padding: 2.2rem 2.5rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px -5px rgba(27, 67, 50, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.plant-hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.02em;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 12px;
}

.plant-hero-subtitle {
    font-size: 1.05rem;
    font-weight: 400;
    color: #d8f3dc;
    margin-top: 0.5rem;
    margin-bottom: 0;
    line-height: 1.5;
}

/* Cartões Gerais */
.modern-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.modern-card:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1b4332;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 2px solid #f0fdf4;
    padding-bottom: 8px;
}

/* Badges e Pílulas de Status */
.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.88rem;
    font-weight: 600;
    letter-spacing: 0.01em;
}

.badge-healthy {
    background-color: #dcfce7;
    color: #15803d;
    border: 1px solid #86efac;
}

.badge-warning {
    background-color: #fef3c7;
    color: #b45309;
    border: 1px solid #fcd34d;
}

.badge-danger {
    background-color: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fca5a5;
}

.badge-info {
    background-color: #e0f2fe;
    color: #0369a1;
    border: 1px solid #7dd3fc;
}

.badge-neutral {
    background-color: #f3f4f6;
    color: #374151;
    border: 1px solid #d1d5db;
}

/* Barra de Progresso Customizada */
.custom-progress-bg {
    background-color: #e5e7eb;
    border-radius: 8px;
    height: 12px;
    overflow: hidden;
    margin: 8px 0;
}

.custom-progress-fill {
    background: linear-gradient(90deg, #52b788 0%, #2d6a4f 100%);
    height: 100%;
    border-radius: 8px;
    transition: width 0.4s ease;
}

/* Caixas de Métricas Rápidas */
.metric-box {
    background-color: #f8faf8;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.metric-label {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 4px;
}

.metric-value {
    font-size: 1.4rem;
    font-weight: 800;
    color: #1e293b;
}

/* Etapas do Tratamento */
.step-container {
    display: flex;
    gap: 16px;
    margin-bottom: 1rem;
    background: #fdfdfd;
    border: 1px solid #f1f5f9;
    border-radius: 12px;
    padding: 1rem;
}

.step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 38px;
    height: 38px;
    background-color: #2d6a4f;
    color: #ffffff;
    font-weight: 700;
    border-radius: 50%;
    font-size: 1rem;
}

.step-content {
    flex: 1;
}

.step-title {
    font-weight: 700;
    color: #1e293b;
    font-size: 1rem;
    margin-bottom: 4px;
}

.step-desc {
    color: #475569;
    font-size: 0.92rem;
    line-height: 1.5;
}

/* Alerta de Transparência */
.transparency-callout {
    background-color: #f0fdf4;
    border-left: 4px solid #2d6a4f;
    padding: 1rem 1.25rem;
    border-radius: 0 10px 10px 0;
    font-size: 0.9rem;
    color: #166534;
    margin-top: 1.5rem;
}

/* Indicador de Gravidade */
.severity-pill-nenhuma { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 6px; font-weight: 600; }
.severity-pill-baixa { background: #dbeafe; color: #1e40af; padding: 4px 10px; border-radius: 6px; font-weight: 600; }
.severity-pill-média { background: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 6px; font-weight: 600; }
.severity-pill-alta { background: #ffedd5; color: #c2410c; padding: 4px 10px; border-radius: 6px; font-weight: 600; }
.severity-pill-crítica { background: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 6px; font-weight: 600; }

/* Botões do Streamlit com tom natural */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button[kind="primary"] {
    background-color: #2d6a4f !important;
    border-color: #2d6a4f !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(45, 106, 79, 0.25) !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: #1b4332 !important;
    border-color: #1b4332 !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(27, 67, 50, 0.35) !important;
}
</style>
"""
