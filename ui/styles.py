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

/* ===== Variáveis do Tema Nova ===== */
:root {
  --bg: #0a0a0f;
  --bg-elevated: #12121a;
  --bg-card: #16161f;
  --border: rgba(255, 255, 255, 0.08);
  --border-glow: rgba(167, 139, 250, 0.3);
  --text: #f1f5f9;
  --text-muted: #94a3b8;
  --primary: #a78bfa;
  --primary-light: #c4b5fd;
  --secondary: #38bdf8;
  --accent: #f472b6;
  --success: #34d399;
  --gradient: linear-gradient(135deg, #a78bfa 0%, #38bdf8 50%, #f472b6 100%);
  --gradient-botanical: linear-gradient(135deg, #34d399 0%, #38bdf8 50%, #a78bfa 100%);
  --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
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

[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="collapsedControl"] svg {
  fill: var(--primary-light) !important;
  stroke: var(--primary-light) !important;
  width: 20px !important;
  height: 20px !important;
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
  background: rgba(255, 255, 255, 0.04);
  border-color: var(--border);
}

[data-testid="stSidebarCollapseButton"] {
  color: var(--text-muted) !important;
  background: rgba(255, 255, 255, 0.05) !important;
  border-radius: 8px !important;
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
  background: rgba(167, 139, 250, 0.12);
  border: 1px solid rgba(167, 139, 250, 0.3);
  color: var(--primary-light);
  padding: 0.4rem 1.1rem;
  border-radius: 999px;
  font-size: 0.86rem;
  font-weight: 500;
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

/* ===== Hero Section Nova ===== */
.nova-hero-container {
  position: relative;
  background: linear-gradient(135deg, rgba(22, 22, 31, 0.7) 0%, rgba(18, 18, 26, 0.85) 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 3rem 2.8rem;
  margin-bottom: 2.2rem;
  overflow: hidden;
  box-shadow: var(--shadow);
  backdrop-filter: blur(25px);
}

.nova-hero-grid {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  align-items: center;
  gap: 2.5rem;
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
  font-size: clamp(2.2rem, 4vw, 3.2rem) !important;
  font-weight: 800 !important;
  line-height: 1.15 !important;
  letter-spacing: -0.03em !important;
  margin: 0 0 1rem 0 !important;
}

.nova-hero-desc {
  color: var(--text-muted);
  font-size: 1.05rem;
  line-height: 1.6;
  margin-bottom: 1.8rem;
  max-width: 540px;
}

/* Orbs Brilhantes em Background */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.45;
  animation: orb-float 9s ease-in-out infinite;
  pointer-events: none;
}

.orb-1 {
  width: 260px;
  height: 260px;
  background: #a78bfa;
  top: -10%;
  right: 15%;
}

.orb-2 {
  width: 220px;
  height: 220px;
  background: #38bdf8;
  bottom: -15%;
  right: 5%;
  animation-delay: -3.5s;
}

.orb-3 {
  width: 170px;
  height: 170px;
  background: #f472b6;
  top: 35%;
  right: 28%;
  animation-delay: -6s;
}

@keyframes orb-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(25px, -25px) scale(1.06); }
  66% { transform: translate(-20px, 15px) scale(0.95); }
}

/* ===== Avatar Animado da Nova ===== */
.hero-avatar-area {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 280px;
}

.avatar-container {
  position: relative;
  z-index: 3;
}

.avatar-ring {
  position: absolute;
  inset: -18px;
  border: 2px solid rgba(167, 139, 250, 0.35);
  border-radius: 50%;
  animation: spin-slow 22s linear infinite;
}

.avatar-ring.ring-2 {
  inset: -34px;
  border-color: rgba(56, 189, 248, 0.25);
  animation-direction: reverse;
  animation-duration: 32s;
}

@keyframes spin-slow {
  to { transform: rotate(360deg); }
}

.pulse-ring {
  position: absolute;
  inset: -10px;
  border: 2px solid rgba(167, 139, 250, 0.4);
  border-radius: 50%;
  animation: pulse-expand 2.8s ease-out infinite;
}

@keyframes pulse-expand {
  0% { transform: scale(1); opacity: 0.6; }
  100% { transform: scale(1.35); opacity: 0; }
}

.avatar {
  width: 150px;
  height: 150px;
  background: linear-gradient(145deg, #181824, #242436);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 
    0 0 0 3px rgba(167, 139, 250, 0.25),
    0 20px 50px rgba(0, 0, 0, 0.6),
    inset 0 0 35px rgba(167, 139, 250, 0.15);
  animation: avatar-float 4s ease-in-out infinite;
}

@keyframes avatar-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.avatar-face {
  position: relative;
  width: 60%;
  height: 50%;
}

.eye {
  position: absolute;
  width: 15px;
  height: 15px;
  background: #f1f5f9;
  border-radius: 50%;
  top: 20%;
  animation: blink 4s infinite;
}

.eye.left { left: 16%; }
.eye.right { right: 16%; }

.eye::after {
  content: '';
  position: absolute;
  width: 7px;
  height: 7px;
  background: #181824;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

@keyframes blink {
  0%, 94%, 98%, 100% { transform: scaleY(1); }
  96% { transform: scaleY(0.1); }
}

.mouth {
  position: absolute;
  bottom: 8%;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 11px;
  border: 2.5px solid #f1f5f9;
  border-top: none;
  border-radius: 0 0 20px 20px;
}

/* ===== Cartões Glassmorphic ===== */
.modern-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.6rem;
  margin-bottom: 1.6rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.modern-card:hover {
  transform: translateY(-3px);
  border-color: var(--border-glow);
  box-shadow: 0 16px 40px rgba(167, 139, 250, 0.12);
}

.card-title {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 1.22rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 10px;
}

/* ===== Caixas de Métricas Rápidas ===== */
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
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 6px;
}

.metric-value {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 1.7rem;
  font-weight: 800;
  color: var(--text);
}

/* ===== Badges e Pílulas de Status ===== */
.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
}

.badge-healthy {
  background: rgba(52, 211, 153, 0.12);
  color: #34d399;
  border: 1px solid rgba(52, 211, 153, 0.35);
}

.badge-warning {
  background: rgba(251, 191, 36, 0.12);
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.35);
}

.badge-danger {
  background: rgba(244, 114, 182, 0.14);
  color: #f472b6;
  border: 1px solid rgba(244, 114, 182, 0.35);
}

.badge-info {
  background: rgba(56, 189, 248, 0.12);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.35);
}

.badge-neutral {
  background: rgba(255, 255, 255, 0.06);
  color: #cbd5e1;
  border: 1px solid var(--border);
}

/* Indicadores de Gravidade */
.severity-pill-nenhuma { background: rgba(52, 211, 153, 0.15); color: #34d399; padding: 4px 10px; border-radius: 8px; font-weight: 600; }
.severity-pill-baixa { background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 4px 10px; border-radius: 8px; font-weight: 600; }
.severity-pill-média { background: rgba(251, 191, 36, 0.15); color: #fbbf24; padding: 4px 10px; border-radius: 8px; font-weight: 600; }
.severity-pill-alta { background: rgba(249, 115, 22, 0.18); color: #fb923c; padding: 4px 10px; border-radius: 8px; font-weight: 600; }
.severity-pill-crítica { background: rgba(244, 114, 182, 0.18); color: #f472b6; padding: 4px 10px; border-radius: 8px; font-weight: 600; }

/* ===== Passos de Tratamento ===== */
.step-container {
  display: flex;
  gap: 16px;
  margin-bottom: 1rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 1.1rem;
  transition: all 0.2s ease;
}

.step-container:hover {
  border-color: var(--border-glow);
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 38px;
  height: 38px;
  background: var(--gradient);
  color: #ffffff;
  font-weight: 700;
  border-radius: 50%;
  font-size: 0.95rem;
  box-shadow: 0 4px 12px rgba(167, 139, 250, 0.35);
}

.step-content {
  flex: 1;
}

.step-title {
  font-weight: 700;
  color: var(--text);
  font-size: 1rem;
  margin-bottom: 4px;
}

.step-desc {
  color: var(--text-muted);
  font-size: 0.92rem;
  line-height: 1.5;
}

/* Callout de Transparência */
.transparency-callout {
  background: rgba(167, 139, 250, 0.08);
  border-left: 4px solid var(--primary);
  padding: 1rem 1.3rem;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font-size: 0.9rem;
  color: var(--primary-light);
  margin-top: 1.5rem;
}

/* ===== Botões Pill Estilo Nova ===== */
.stButton > button {
  border-radius: 999px !important;
  font-weight: 600 !important;
  font-size: 0.94rem !important;
  padding: 0.6rem 1.4rem !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  border: 1px solid var(--border) !important;
  background: rgba(255, 255, 255, 0.04) !important;
  color: var(--text) !important;
}

.stButton > button:hover {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: var(--border-glow) !important;
  transform: translateY(-2px) !important;
}

.stButton > button[kind="primary"] {
  background: var(--gradient) !important;
  border: none !important;
  color: #ffffff !important;
  box-shadow: 0 6px 20px rgba(167, 139, 250, 0.35) !important;
}

.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 10px 30px rgba(167, 139, 250, 0.55) !important;
  filter: brightness(1.08);
}

/* Inputs e Selectboxes Dark Mode */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
  background-color: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.25) !important;
}

/* Expanders Glassmorphic */
[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  overflow: hidden;
}

/* ===== Widget Flutuante de Chat no Canto Inferior Direito ===== */
div[data-testid="stPopover"] {
  position: fixed !important;
  bottom: 24px !important;
  right: 24px !important;
  z-index: 999990 !important;
}

div[data-testid="stPopover"] > button {
  background: var(--gradient) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 9999px !important;
  padding: 12px 24px !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.98rem !important;
  letter-spacing: 0.01em !important;
  box-shadow: 0 8px 30px rgba(167, 139, 250, 0.45) !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 10px !important;
  cursor: pointer !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

div[data-testid="stPopover"] > button:hover {
  transform: translateY(-3px) scale(1.05) !important;
  box-shadow: 0 12px 36px rgba(167, 139, 250, 0.65) !important;
  filter: brightness(1.1);
}

/* Janela do Popover (Corpo do Chat Dark Nova) */
div[data-testid="stPopoverBody"] {
  width: 410px !important;
  max-width: calc(100vw - 36px) !important;
  max-height: 610px !important;
  border-radius: 24px !important;
  border: 1.5px solid var(--border-glow) !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6) !important;
  padding: 18px !important;
  background: #12121a !important;
  overflow-y: auto !important;
  backdrop-filter: blur(20px) !important;
}

/* Mensagens de Chat Estilo Nova */
[data-testid="stChatMessage"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 18px !important;
  padding: 10px 14px !important;
  margin-bottom: 8px !important;
}

/* Chips de Sugestão */
.chat-suggestion-chip {
  background: rgba(167, 139, 250, 0.08);
  border: 1px solid rgba(167, 139, 250, 0.2);
  color: var(--primary-light);
  border-radius: 999px;
  padding: 4px 12px;
  font-size: 0.8rem;
  cursor: pointer;
  display: inline-block;
  margin: 3px;
  transition: all 0.2s ease;
}

.chat-suggestion-chip:hover {
  background: rgba(167, 139, 250, 0.18);
  border-color: var(--primary);
  transform: translateY(-1px);
}

/* Responsividade móvel */
@media (max-width: 640px) {
  div[data-testid="stPopover"] {
    bottom: 16px !important;
    right: 16px !important;
  }
  div[data-testid="stPopover"] > button {
    padding: 10px 18px !important;
    font-size: 0.9rem !important;
  }
  div[data-testid="stPopoverBody"] {
    width: calc(100vw - 32px) !important;
    right: 16px !important;
    max-height: 75vh !important;
  }
}
</style>
"""
