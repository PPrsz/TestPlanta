"""
Sistema de Design Nova para PlantCare AI.
Inspirado na interface moderna da Assistente Virtual Nova:
Fundo Dark Obsidian (#0a0a0f), Tipografia Space Grotesk + Inter,
Gradientes Eletrizantes (Violeta, Ciano, Rosa), Avatar Animado com Orbs e Efeitos Futuristas.
"""

CUSTOM_CSS = """
<style>
/* ===== Fontes Modernas: Inter & Space Grotesk ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700;800&display=swap');

/* ===== Variáveis do Tema Nova (Contraste Aprimorado) ===== */
:root {
  --bg: #0a0a0f;
  --bg-elevated: #13131d;
  --bg-card: #171722;
  --border: rgba(255, 255, 255, 0.12);
  --border-glow: rgba(167, 139, 250, 0.4);
  --text: #ffffff;
  --text-muted: #cbd5e1; /* Contraste melhorado para legibilidade */
  --primary: #a78bfa;
  --primary-light: #c4b5fd;
  --secondary: #38bdf8;
  --accent: #f472b6;
  --success: #34d399;
  --gradient: linear-gradient(135deg, #a78bfa 0%, #38bdf8 50%, #f472b6 100%);
  --gradient-botanical: linear-gradient(135deg, #34d399 0%, #38bdf8 50%, #a78bfa 100%);
  --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.65);
  --radius: 22px;
  --radius-sm: 14px;
}

/* ===== Reset & Base da Aplicação ===== */
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
  line-height: 1.6;
}

/* Cabeçalhos em Space Grotesk */
h1, h2, h3, h4, h5, h6, .brand-font {
  font-family: 'Space Grotesk', sans-serif !important;
  letter-spacing: -0.025em;
  color: var(--text) !important;
}

/* Ocultar elementos padrão do Streamlit mantendo a usabilidade */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

header[data-testid="stHeader"] {
  background: transparent !important;
  pointer-events: none !important;
}

header[data-testid="stHeader"] [data-testid="stToolbar"],
header[data-testid="stHeader"] [data-testid="stDecoration"],
header[data-testid="stHeader"] [data-testid="stStatusWidget"] {
  display: none !important;
  visibility: hidden !important;
}

/* Botão Lateral para Recolher/Expandir Menu com Estilo Nova */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
header button {
  pointer-events: auto !important;
}

[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
  visibility: visible !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: fixed !important;
  top: 14px !important;
  left: 14px !important;
  z-index: 999999 !important;
  width: 44px !important;
  height: 44px !important;
  background: var(--bg-card) !important;
  color: var(--primary-light) !important;
  border: 1.5px solid var(--border-glow) !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 18px rgba(167, 139, 250, 0.3) !important;
  cursor: pointer !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

[data-testid="stSidebarCollapsedControl"]:hover,
[data-testid="collapsedControl"]:hover {
  background: var(--bg-elevated) !important;
  border-color: var(--primary) !important;
  transform: scale(1.08) !important;
  box-shadow: 0 8px 25px rgba(167, 139, 250, 0.5) !important;
}

/* ===== Barra Lateral Estilo Dark Obsidian ===== */
[data-testid="stSidebar"] {
  background-color: var(--bg) !important;
  background-image: linear-gradient(180deg, #0e0e17 0%, #0a0a0f 100%) !important;
  border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
  color: var(--text) !important;
}

[data-testid="stSidebar"] .stRadio label {
  font-size: 0.98rem;
  font-weight: 500;
  padding: 8px 14px;
  border-radius: 12px;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

[data-testid="stSidebar"] .stRadio label:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: var(--border);
}

/* ===== Gradiente de Texto Nova ===== */
.gradient-text {
  background: var(--gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.gradient-text-botanical {
  background: var(--gradient-botanical);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

/* ===== Badges Flutuantes ===== */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(167, 139, 250, 0.15);
  border: 1px solid rgba(167, 139, 250, 0.35);
  color: var(--primary-light);
  padding: 0.4rem 1.1rem;
  border-radius: 999px;
  font-size: 0.86rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.badge-dot {
  width: 8px;
  height: 8px;
  background: var(--success);
  border-radius: 50%;
  animation: pulse-dot 2s infinite;
  box-shadow: 0 0 10px var(--success);
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

/* ===== Hero Section Nova (Espaçamento Ajustado) ===== */
.nova-hero-container {
  position: relative;
  background: linear-gradient(135deg, rgba(23, 23, 34, 0.8) 0%, rgba(19, 19, 29, 0.92) 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2.5rem 2.5rem;
  margin-bottom: 2rem;
  overflow: hidden;
  box-shadow: var(--shadow);
  backdrop-filter: blur(25px);
}

.nova-hero-grid {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  align-items: center;
  gap: 2rem;
  position: relative;
  z-index: 2;
}

@media (max-width: 900px) {
  .nova-hero-grid {
    grid-template-columns: 1fr;
    text-align: center;
  }
}

.nova-hero-title {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: clamp(2rem, 3.8vw, 3rem) !important;
  font-weight: 800 !important;
  line-height: 1.2 !important;
  letter-spacing: -0.03em !important;
  margin: 0 0 1rem 0 !important;
}

.nova-hero-desc {
  color: var(--text-muted);
  font-size: 1.02rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  max-width: 540px;
}

/* Orbs Brilhantes em Background */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.4;
  animation: orb-float 9s ease-in-out infinite;
  pointer-events: none;
}

.orb-1 { width: 240px; height: 240px; background: #a78bfa; top: -10%; right: 15%; }
.orb-2 { width: 200px; height: 200px; background: #38bdf8; bottom: -15%; right: 5%; animation-delay: -3.5s; }
.orb-3 { width: 150px; height: 150px; background: #f472b6; top: 35%; right: 28%; animation-delay: -6s; }

@keyframes orb-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(20px, -20px) scale(1.05); }
  66% { transform: translate(-15px, 12px) scale(0.96); }
}

/* ===== Cartões Glassmorphic e Métricas ===== */
.modern-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.6rem;
  margin-bottom: 1.6rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.modern-card:hover {
  transform: translateY(-2px);
  border-color: var(--border-glow);
  box-shadow: 0 16px 40px rgba(167, 139, 250, 0.15);
}

.metric-box {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 1.2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.metric-box:hover {
  border-color: var(--border-glow);
  transform: translateY(-2px);
}

.metric-label {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 6px;
}

.metric-value {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text);
}
</style>
"""
