import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, Any, List, Optional
from PIL import Image


def render_hero(
    title: str = "Conheça o <span class=\"gradient-text\">PlantCare AI</span>",
    subtitle: str = "Sua assistente inteligente especializada no diagnóstico e recuperação da saúde vegetal com IA multimodal e Teachable Machine.",
    show_avatar: bool = True,
    badge_text: str = "Assistente Virtual & Saúde Botânica",
):
    """
    Renderiza o hero futurista estilo Nova usando st.components.v1.html,
    garantindo que todas as animações CSS/JS funcionem (orbs, anéis giratórios,
    olhos piscando, boca animada, partículas) exatamente como no HTML original.
    """
    avatar_section = ""
    if show_avatar:
        avatar_section = """
        <div class="hero-visual">
          <div class="orb orb-1"></div>
          <div class="orb orb-2"></div>
          <div class="orb orb-3"></div>
          <div class="avatar-container">
            <div class="avatar-ring"></div>
            <div class="avatar-ring ring-2"></div>
            <div class="avatar" id="heroAvatar">
              <div class="avatar-face">
                <div class="eye left"></div>
                <div class="eye right"></div>
                <div class="mouth"></div>
              </div>
            </div>
            <div class="pulse-ring"></div>
          </div>
        </div>
        """

    # ── enhanced avatar glow rings ─────────────────────────────────────────
    extra_rings = ""
    if show_avatar:
        extra_rings = """
        <div class="avatar-ring ring-3"></div>
        <div class="pulse-ring pulse-ring-2"></div>
        """

    hero_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700;800&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --bg:#0a0a0f;--bg-card:#16161f;
  --text:#f1f5f9;--text-muted:#94a3b8;
  --primary:#a78bfa;--primary-light:#c4b5fd;
  --secondary:#38bdf8;--accent:#f472b6;--success:#34d399;
  --gradient:linear-gradient(135deg,#a78bfa 0%,#38bdf8 50%,#f472b6 100%);
  --border:rgba(255,255,255,0.08);--border-glow:rgba(167,139,250,0.3);
}}
html,body{{background:transparent;color:var(--text);font-family:'Inter',sans-serif;overflow:hidden}}
.hero{{
  display:grid;
  grid-template-columns:1.35fr 1fr;
  align-items:center;
  gap:2rem;
  padding:2.2rem 2.6rem 2.2rem;
  position:relative;
  background:linear-gradient(135deg,rgba(22,22,31,0.8) 0%,rgba(14,14,22,0.92) 100%);
  border:1px solid rgba(167,139,250,0.15);
  border-radius:24px;
  backdrop-filter:blur(28px);
  box-shadow:0 30px 60px -15px rgba(0,0,0,0.6),inset 0 1px 0 rgba(255,255,255,0.05);
  overflow:hidden;
}}
/* shimmer border */
.hero::before{{
  content:'';position:absolute;inset:0;border-radius:24px;
  background:linear-gradient(135deg,rgba(167,139,250,.18) 0%,rgba(56,189,248,.1) 50%,rgba(244,114,182,.12) 100%);
  mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;
  padding:1px;pointer-events:none;
}}
.gradient-text{{
  background:var(--gradient);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;display:inline;
}}
.badge{{
  display:inline-flex;align-items:center;gap:.45rem;
  background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.25);
  color:var(--primary-light);padding:.38rem 1.05rem;border-radius:999px;
  font-size:.82rem;font-weight:500;margin-bottom:1.2rem;letter-spacing:.01em;
}}
.badge-dot{{
  width:7px;height:7px;background:var(--success);border-radius:50%;
  box-shadow:0 0 10px var(--success);
  animation:pulse-dot 2s infinite;
}}
@keyframes pulse-dot{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.5;transform:scale(1.4)}}}}
h1{{
  font-family:'Space Grotesk',sans-serif;
  font-size:clamp(1.8rem,3.8vw,2.9rem);
  font-weight:800;line-height:1.13;letter-spacing:-.035em;
  margin-bottom:.95rem;color:var(--text);
}}
p.desc{{color:var(--text-muted);font-size:1.02rem;line-height:1.68;max-width:460px}}

/* ── hero visual ── */
.hero-visual{{
  position:relative;display:flex;align-items:center;justify-content:center;
  height:290px;
}}
.orb{{position:absolute;border-radius:50%;filter:blur(60px);opacity:.45;animation:orb-float 9s ease-in-out infinite;pointer-events:none}}
.orb-1{{width:230px;height:230px;background:#a78bfa;top:0%;left:5%}}
.orb-2{{width:170px;height:170px;background:#38bdf8;bottom:5%;right:5%;animation-delay:-3.5s}}
.orb-3{{width:140px;height:140px;background:#f472b6;top:35%;right:22%;animation-delay:-6s;opacity:.35}}
@keyframes orb-float{{
  0%,100%{{transform:translate(0,0) scale(1)}}
  33%{{transform:translate(16px,-28px) scale(1.07)}}
  66%{{transform:translate(-14px,16px) scale(.93)}}
}}
/* avatar container */
.avatar-container{{position:relative;z-index:2}}
/* three rings */
.avatar-ring{{
  position:absolute;border-radius:50%;animation:spin-slow 20s linear infinite;
}}
.avatar-ring:nth-child(1){{
  inset:-18px;border:1.5px solid rgba(167,139,250,.35);
}}
.avatar-ring.ring-2{{
  inset:-36px;border:1.5px solid rgba(56,189,248,.22);
  animation-direction:reverse;animation-duration:28s;
}}
.avatar-ring.ring-3{{
  inset:-56px;border:1px dashed rgba(244,114,182,.15);
  animation-duration:45s;
}}
@keyframes spin-slow{{to{{transform:rotate(360deg)}}}}
/* avatar body */
.avatar{{
  width:168px;height:168px;
  background:radial-gradient(circle at 35% 30%,#2d2042,#1a1a2e 60%,#0d0d18);
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  position:relative;
  box-shadow:
    0 0 0 3px rgba(167,139,250,.25),
    0 0 30px rgba(167,139,250,.2),
    0 24px 60px rgba(0,0,0,.5),
    inset 0 0 50px rgba(167,139,250,.08);
  animation:avatar-float 6s ease-in-out infinite;
}}
/* glow halo behind avatar */
.avatar::before{{
  content:'';position:absolute;inset:-8px;border-radius:50%;
  background:radial-gradient(circle,rgba(167,139,250,.18) 0%,transparent 70%);
  animation:glow-pulse 3s ease-in-out infinite;
}}
@keyframes glow-pulse{{0%,100%{{opacity:.6}}50%{{opacity:1}}}}
@keyframes avatar-float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-12px)}}}}
.avatar.speaking{{box-shadow:0 0 0 3px rgba(167,139,250,.5),0 0 40px rgba(167,139,250,.35),0 24px 60px rgba(0,0,0,.5),inset 0 0 50px rgba(167,139,250,.12)}}
/* face */
.avatar-face{{position:relative;width:58%;height:48%}}
.eye{{
  position:absolute;width:17px;height:17px;background:#e8f0ff;
  border-radius:50%;top:18%;
  box-shadow:0 0 8px rgba(167,139,250,.5),inset 0 -2px 0 rgba(0,0,0,.2);
  transition:transform .12s ease;
}}
.eye.left{{left:11%}}.eye.right{{right:11%}}
.eye::after{{
  content:'';position:absolute;width:8px;height:8px;background:#1a1a2e;
  border-radius:50%;top:50%;left:50%;transform:translate(-50%,-50%);
  box-shadow:1px 1px 0 rgba(255,255,255,.15);
}}
.mouth{{
  position:absolute;bottom:6%;left:50%;transform:translateX(-50%);
  width:27px;height:12px;border:2.5px solid #e8f0ff;border-top:none;
  border-radius:0 0 20px 20px;transition:all .3s ease;
  box-shadow:0 2px 8px rgba(167,139,250,.3);
}}
.avatar.happy .mouth{{width:32px;height:15px;border-radius:0 0 30px 30px}}
.avatar.speaking .mouth{{animation:mouth-talk .35s ease infinite alternate}}
@keyframes mouth-talk{{from{{height:7px;width:22px}}to{{height:16px;width:30px;border-radius:0 0 38px 38px}}}}
/* pulse rings */
.pulse-ring{{
  position:absolute;border-radius:50%;border:2px solid rgba(167,139,250,.45);
  animation:pulse-expand 2.8s ease-out infinite;
}}
.pulse-ring:nth-of-type(1){{inset:-8px}}
.pulse-ring-2{{inset:-8px;animation-delay:1.4s;border-color:rgba(56,189,248,.3)}}
@keyframes pulse-expand{{0%{{transform:scale(1);opacity:.65}}100%{{transform:scale(1.5);opacity:0}}}}
/* particles */
.particles{{position:absolute;inset:0;pointer-events:none;overflow:hidden;border-radius:24px}}
.particle{{position:absolute;border-radius:50%;animation:float-particle 15s infinite linear}}
@keyframes float-particle{{
  0%{{transform:translateY(110%) scale(0);opacity:0}}
  8%{{opacity:.5}}88%{{opacity:.12}}
  100%{{transform:translateY(-90px) scale(1);opacity:0}}
}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(28px)}}to{{opacity:1;transform:translateY(0)}}}}
.hero-content{{animation:fadeUp .75s ease both}}
</style>
</head>
<body>
<div class="hero">
  <div class="particles" id="particles"></div>
  <div class="hero-content">
    <div class="badge">
      <span class="badge-dot"></span>
      {badge_text}
    </div>
    <h1>{title}</h1>
    <p class="desc">{subtitle}</p>
  </div>
  {avatar_section}
</div>
<script>
(function(){{
  const c=document.getElementById('particles');
  if(!c)return;
  const colors=['#a78bfa','#38bdf8','#f472b6','#c4b5fd','#34d399'];
  for(let i=0;i<32;i++){{
    const p=document.createElement('div');
    p.className='particle';
    p.style.left=Math.random()*100+'%';
    p.style.animationDelay=Math.random()*15+'s';
    p.style.animationDuration=(9+Math.random()*12)+'s';
    const sz=1+Math.random()*3.5+'px';
    p.style.width=sz;p.style.height=sz;
    p.style.background=colors[Math.floor(Math.random()*colors.length)];
    p.style.opacity=.2+Math.random()*.3;
    c.appendChild(p);
  }}
}})();
function blinkEyes(){{
  document.querySelectorAll('.eye').forEach(e=>e.style.transform='scaleY(0.07)');
  setTimeout(()=>document.querySelectorAll('.eye').forEach(e=>e.style.transform=''),130);
}}
setInterval(blinkEyes,2800+Math.random()*2200);
const av=document.getElementById('heroAvatar');
if(av){{
  setInterval(()=>{{
    av.classList.add('happy');
    setTimeout(()=>av.classList.remove('happy'),1400);
  }},6500);
  setInterval(()=>{{
    av.classList.add('speaking');
    setTimeout(()=>av.classList.remove('speaking'),900+Math.random()*600);
  }},11000);
}}
</script>
</body>
</html>"""

    height = 268 if show_avatar else 168
    components.html(hero_html, height=height, scrolling=False)

def render_metric_cards(
    total_plants: int,
    healthy_count: int,
    attention_count: int,
    diagnoses_count: int,
):
    """
    Renderiza os 4 cards de métricas com ícones SVG, fade-in staggerado,
    hover com elevação e glow — via components.v1.html para animações reais.
    """
    is_empty = total_plants == 0

    # valores e cores
    metrics = [
        {
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>',
            "label": "Plantas Cadastradas",
            "value": str(total_plants),
            "color": "#c4b5fd",
            "glow": "rgba(167,139,250,0.3)",
            "bg": "rgba(167,139,250,0.08)",
        },
        {
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 21.593c-5.63-5.539-11-10.297-11-14.402C1 3.335 4.248 1 7.5 1c1.998 0 4.049.986 5.5 2.717C14.451 1.986 16.502 1 18.5 1 21.752 1 25 3.335 25 7.19c0 4.106-5.37 8.863-11 14.402"/></svg>',
            "label": "Aparentemente Saudáveis",
            "value": str(healthy_count),
            "color": "#34d399",
            "glow": "rgba(52,211,153,0.3)",
            "bg": "rgba(52,211,153,0.08)",
        },
        {
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></svg>',
            "label": "Sob Atenção / Tratamento",
            "value": str(attention_count),
            "color": "#f59e0b",
            "glow": "rgba(245,158,11,0.3)",
            "bg": "rgba(245,158,11,0.08)",
        },
        {
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 17V13M12 17V9M15 17v-4"/></svg>',
            "label": "Diagnósticos Realizados",
            "value": str(diagnoses_count),
            "color": "#38bdf8",
            "glow": "rgba(56,189,248,0.3)",
            "bg": "rgba(56,189,248,0.08)",
        },
    ]

    cards_html = ""
    for i, m in enumerate(metrics):
        empty_note = ""
        if is_empty and i == 0:
            empty_note = "<p class='empty-hint'>Faça sua primeira análise ✨</p>"
        cards_html += f"""
        <div class="metric-card" style="--delay:{i*0.1}s;--color:{m['color']};--glow:{m['glow']};--bg:{m['bg']};">
          <div class="metric-icon">{m['icon']}</div>
          <div class="metric-value{'  zero' if m['value'] == '0' else ''}">{m['value']}</div>
          <div class="metric-label">{m['label']}</div>
          {empty_note}
        </div>"""

    empty_state_html = ""
    if is_empty:
        empty_state_html = """
        <div class="empty-state">
          <div class="empty-icon">🌱</div>
          <h3>Bem-vindo ao PlantCare AI!</h3>
          <p>Seu jardim ainda está vazio. Faça a primeira análise para começar a acompanhar a saúde das suas plantas.</p>
        </div>"""

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@700;800&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{
  font-family:'Inter',sans-serif;
  background:transparent;
  padding:4px 2px 8px;
}}
.grid{{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:14px;
}}
.metric-card{{
  background:linear-gradient(145deg,#12121a,#0e0e17);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:18px;
  padding:1.3rem 1.1rem 1.1rem;
  text-align:center;
  cursor:default;
  position:relative;
  overflow:hidden;
  opacity:0;
  transform:translateY(20px);
  animation:fadeUp .55s ease var(--delay) forwards;
  transition:transform .3s cubic-bezier(.4,0,.2,1),
             box-shadow .3s ease,
             border-color .3s ease;
}}
.metric-card::before{{
  content:'';position:absolute;inset:0;border-radius:18px;
  background:var(--bg);
  opacity:0;transition:opacity .3s ease;
}}
.metric-card:hover{{
  transform:translateY(-6px) scale(1.015);
  border-color:var(--color);
  box-shadow:0 16px 40px var(--glow),0 4px 12px rgba(0,0,0,.3);
}}
.metric-card:hover::before{{opacity:1}}
.metric-icon{{
  display:flex;align-items:center;justify-content:center;
  width:44px;height:44px;margin:0 auto 10px;
  background:var(--bg);border-radius:12px;
  border:1px solid var(--color);
  color:var(--color);
  transition:transform .3s ease,box-shadow .3s ease;
}}
.metric-card:hover .metric-icon{{
  transform:scale(1.12);
  box-shadow:0 0 16px var(--glow);
}}
.metric-icon svg{{width:22px;height:22px;stroke:var(--color)}}
.metric-value{{
  font-family:'Space Grotesk',sans-serif;
  font-size:2.2rem;font-weight:800;
  color:var(--color);line-height:1;
  margin-bottom:5px;
  position:relative;z-index:1;
  transition:transform .3s ease;
}}
.metric-card:hover .metric-value{{transform:scale(1.05)}}
.metric-value.zero{{color:rgba(148,163,184,.4)}}
.metric-label{{
  font-size:.72rem;font-weight:600;
  text-transform:uppercase;letter-spacing:.06em;
  color:#64748b;position:relative;z-index:1;
}}
.empty-hint{{
  font-size:.72rem;color:var(--color);opacity:.7;
  margin-top:5px;position:relative;z-index:1;
  animation:pulse-hint 2s ease-in-out infinite;
}}
@keyframes pulse-hint{{0%,100%{{opacity:.5}}50%{{opacity:.9}}}}
/* empty state */
.empty-state{{
  margin-top:16px;
  background:linear-gradient(135deg,rgba(167,139,250,.06) 0%,rgba(56,189,248,.04) 100%);
  border:1px dashed rgba(167,139,250,.25);
  border-radius:18px;padding:1.8rem 1.5rem;
  text-align:center;
  animation:fadeUp .6s ease .45s both;
}}
.empty-icon{{font-size:2.5rem;margin-bottom:.7rem;animation:bounce 2.5s ease-in-out infinite}}
@keyframes bounce{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
.empty-state h3{{
  font-family:'Space Grotesk',sans-serif;font-size:1.1rem;font-weight:700;
  color:#c4b5fd;margin-bottom:.5rem;
}}
.empty-state p{{font-size:.85rem;color:#64748b;line-height:1.55;max-width:380px;margin:0 auto}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
</style>
</head>
<body>
  <div class="grid">{cards_html}</div>
  {empty_state_html}
</body>
</html>"""

    height = 290 if is_empty else 148
    components.html(full_html, height=height, scrolling=False)


def render_home_info_cards():
    """
    Renderiza os dois cards informativos da home ('Como Funciona' + 'Dicas')
    com fade-in e hover animados via components.v1.html.
    """
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Inter',sans-serif;background:transparent;padding:4px 2px 6px}}
.grid{{display:grid;grid-template-columns:1.6fr 1fr;gap:16px;align-items:start}}
.card{{
  background:#16161f;
  border:1px solid rgba(255,255,255,0.07);
  border-radius:20px;padding:1.5rem 1.6rem;
  opacity:0;transform:translateY(18px);
  animation:fadeUp .55s ease var(--d,0s) forwards;
  transition:transform .3s ease,border-color .3s ease,box-shadow .3s ease;
  position:relative;overflow:hidden;
}}
.card::after{{
  content:'';position:absolute;inset:0;border-radius:20px;
  background:var(--accent-bg,rgba(167,139,250,.04));
  opacity:0;transition:opacity .3s;
}}
.card:hover{{transform:translateY(-5px);border-color:var(--accent,rgba(167,139,250,.35));box-shadow:0 14px 36px var(--glow,rgba(167,139,250,.12))}}
.card:hover::after{{opacity:1}}
.card-title{{
  font-family:'Space Grotesk',sans-serif;font-size:1.05rem;font-weight:700;
  color:#f1f5f9;margin-bottom:.9rem;padding-bottom:.7rem;
  border-bottom:1px solid rgba(255,255,255,.07);
  display:flex;align-items:center;gap:.5rem;
}}
.card-title .icon{{font-size:1.15rem}}
p{{color:#64748b;font-size:.88rem;line-height:1.65;position:relative;z-index:1}}
ul{{color:#64748b;font-size:.87rem;line-height:1.75;padding-left:0;list-style:none;position:relative;z-index:1}}
ul li{{padding-left:1rem;position:relative;margin-bottom:.25rem}}
ul li::before{{content:'›';position:absolute;left:0;color:#a78bfa;font-weight:700}}
ul li b{{color:#c4b5fd}}
.tip{{margin-bottom:.6rem;position:relative;z-index:1;display:flex;gap:.5rem;font-size:.87rem;color:#64748b;line-height:1.5}}
.tip b{{color:#38bdf8}}
.tip-icon{{flex-shrink:0;font-size:1rem}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
</style>
</head>
<body>
<div class="grid">
  <div class="card" style="--d:0s;--accent:rgba(167,139,250,.4);--glow:rgba(167,139,250,.12)">
    <div class="card-title"><span class="icon">🔍</span> Como Funciona a Assistente Inteligente</div>
    <p style="margin-bottom:.8rem">O <b style="color:#c4b5fd">PlantCare AI</b> combina duas camadas de IA para máxima precisão diagnóstica:</p>
    <ul>
      <li><b>Classificador Local (Teachable Machine):</b> Avalia padrões visuais em milissegundos, identificando sinais de alerta imediatamente.</li>
      <li><b>Raciocínio Botânico (Google Gemini):</b> Analisa a foto em alta definição, identifica a espécie, investiga causas e gera o plano de tratamento.</li>
      <li><b>Diferenciação Científica:</b> Separa sintomas de causas reais sem suposições precipitadas — diagnóstico responsável.</li>
    </ul>
  </div>
  <div class="card" style="--d:.12s;--accent:rgba(56,189,248,.4);--glow:rgba(56,189,248,.1);--accent-bg:rgba(56,189,248,.03)">
    <div class="card-title" style="color:#38bdf8"><span class="icon">💡</span> Dicas Botânicas</div>
    <div class="tip"><span class="tip-icon">💧</span><span><b>Drenagem é vida:</b> Mais plantas morrem por excesso de rega do que por sede. Cheque o solo antes de regar.</span></div>
    <div class="tip"><span class="tip-icon">☀️</span><span><b>Observe a luz:</b> Luz indireta brilhante é ideal para a maioria das folhagens domésticas.</span></div>
    <div class="tip"><span class="tip-icon">✂️</span><span><b>Poda profilática:</b> Remova folhas doentes com tesoura esterilizada para proteger os galhos sadios.</span></div>
  </div>
</div>
</body>
</html>"""
    components.html(html, height=240, scrolling=False)


def render_quality_audit(audit: Dict[str, Any]):
    """Renderiza a avaliação de qualidade fotográfica antes da inferência."""
    rating = audit.get("quality_rating", "Desconhecida")
    is_ok = audit.get("is_acceptable", True)
    
    badge_class = "badge-healthy" if rating == "Excelente" else ("badge-warning" if rating == "Aceitável" else "badge-danger")
    icon = "✅" if is_ok else "⚠️"
    
    st.markdown(f"""
    <div style="background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 14px; padding: 14px 18px; margin: 12px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: var(--text); font-size: 0.95rem;">📸 Auditoria da Qualidade Fotográfica:</strong>
            <span class="badge-pill {badge_class}">{icon} {rating}</span>
        </div>
        <div style="font-size: 0.86rem; color: var(--text-muted); display: flex; gap: 16px; flex-wrap: wrap;">
            <span>📐 Resolução: <b style="color: var(--text);">{audit.get('width')}x{audit.get('height')}px</b></span>
            <span>💡 Brilho Médio: <b style="color: var(--text);">{audit.get('brightness')}/255</b></span>
            <span>🎯 Nitidez Estimada: <b style="color: var(--text);">{audit.get('sharpness')}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if audit.get("issues"):
        with st.expander("🔍 Dicas para otimizar sua fotografia", expanded=not is_ok):
            for issue in audit.get("issues", []):
                st.write(f"• **Alerta:** {issue}")
            for rec in audit.get("recommendations", []):
                st.info(f"💡 **Recomendação:** {rec}")

def render_teachable_machine_panel(tm_result: Dict[str, Any]):
    """Renderiza o cartão de classificação especializada do Teachable Machine com estilo Nova."""
    if not tm_result.get("success"):
        st.warning(f"⚠️ Teachable Machine: {tm_result.get('error') or tm_result.get('summary')}")
        return

    top_class = tm_result.get("top_class", "Indefinido")
    conf_pct = tm_result.get("confidence_percent", 0.0)
    is_ambiguous = tm_result.get("is_ambiguous", False)
    
    badge_type = "badge-warning" if is_ambiguous else ("badge-healthy" if "saud" in top_class.lower() else "badge-danger")
    status_icon = "⚠️" if is_ambiguous else ("🌱" if "saud" in top_class.lower() else "🔬")

    st.markdown(f"""
    <div class="modern-card">
        <div class="card-title">
            <span>🔬 Classificador Visual Local: Google Teachable Machine</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
            <div>
                <span style="font-size: 1.25rem; font-weight: 700; color: var(--text);">{top_class}</span>
            </div>
            <span class="badge-pill {badge_type}">{status_icon} {conf_pct:.1f}% de Certeza Local</span>
        </div>
        <div style="font-size: 0.92rem; color: var(--text-muted); margin-bottom: 14px;">
            {tm_result.get('summary')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Exibição da distribuição de todas as classes
    with st.expander("📊 Ver distribuição de probabilidades do modelo local", expanded=False):
        for class_name, score in tm_result.get("sorted_predictions", []):
            pct = score * 100
            st.write(f"**{class_name}**: {pct:.1f}%")
            st.progress(min(max(pct / 100.0, 0.0), 1.0))

def render_diagnosis_view(gemini_data: Dict[str, Any], tm_result: Optional[Dict[str, Any]] = None):
    """Renderiza a tela completa de diagnóstico estruturado com tema futurista Nova."""
    
    ident = gemini_data.get("identificacao", {})
    saude = gemini_data.get("estado_saude", {})
    sintomas = gemini_data.get("analise_sintomas", {})
    coerencia = gemini_data.get("coerencia_teachable_machine", {})
    tratamento = gemini_data.get("plano_tratamento", {})
    transparencia = gemini_data.get("limitacoes_e_transparencia", "")

    status = saude.get("status", "Em Avaliação")
    gravidade = saude.get("gravidade_estimada", "Nenhuma").lower()
    
    # Mapeamento de badge para o estado de saúde
    if "saudável" in status.lower():
        status_badge_class = "badge-healthy"
        status_icon = "🟢"
    elif "doença" in status.lower() or "praga" in status.lower():
        status_badge_class = "badge-danger"
        status_icon = "🔴"
    elif "deficiência" in status.lower() or "estresse" in status.lower():
        status_badge_class = "badge-warning"
        status_icon = "🟡"
    else:
        status_badge_class = "badge-neutral"
        status_icon = "⚪"

    # Card 1: Identificação Botânica e Estado de Saúde
    col_id1, col_id2 = st.columns([1.2, 1])
    
    with col_id1:
        st.markdown(f"""
        <div class="modern-card">
            <div class="card-title">🌿 Identificação Botânica</div>
            <div style="margin-bottom: 8px;">
                <span style="font-size: 1.45rem; font-weight: 800; color: var(--primary-light);">{ident.get('nome_popular', 'Espécie em análise')}</span>
                <br>
                <em style="color: var(--secondary); font-size: 1rem;">{ident.get('nome_cientifico', 'Classificação científica')}</em>
            </div>
            <p style="font-size: 0.92rem; color: var(--text-muted); margin-top: 10px; line-height: 1.5;">
                {ident.get('caracteristicas_gerais', '')}
            </p>
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 8px;">
                Certeza da identificação taxonômica: <b style="color: var(--text);">{ident.get('confianca_identificacao', 'Média')}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_id2:
        st.markdown(f"""
        <div class="modern-card">
            <div class="card-title">🩺 Veredito Fitossanitário</div>
            <div style="margin-bottom: 12px;">
                <span class="badge-pill {status_badge_class}" style="font-size: 0.95rem;">
                    {status_icon} {status}
                </span>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 12px;">
                <div class="metric-box" style="flex: 1;">
                    <div class="metric-label">Gravidade</div>
                    <span class="severity-pill-{gravidade}">{gravidade.upper()}</span>
                </div>
                <div class="metric-box" style="flex: 1;">
                    <div class="metric-label">Convicção</div>
                    <div class="metric-value" style="font-size: 1.15rem; color: var(--primary-light);">{saude.get('confianca_diagnostico', 'Média')}</div>
                </div>
            </div>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 10px; margin-bottom: 0;">
                {saude.get('resumo_geral', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Card 2: Análise dos Sintomas vs Causas Inferidas
    st.markdown("""
    <div class="modern-card">
        <div class="card-title">🔬 Investigação de Sintomas & Etiologia</div>
    """, unsafe_allow_html=True)

    col_sint1, col_sint2 = st.columns(2)
    with col_sint1:
        st.markdown("**Sintomas Anatômicos Detectados:**")
        for s in sintomas.get("sintomas_visiveis", []):
            st.markdown(f"• 👁️ {s}")
        if sintomas.get("partes_afetadas"):
            st.markdown(f"*Regiões afetadas:* `{'`, `'.join(sintomas.get('partes_afetadas'))}`")

    with col_sint2:
        st.markdown("**Prováveis Causas Investigadas:**")
        for c in sintomas.get("causas_provaveis", []):
            st.markdown(f"• **{c.get('causa')}** ({c.get('probabilidade', 'Possível')}): {c.get('explicacao')}")

    if sintomas.get("diferenciacao_sintoma_causa"):
        st.info(f"💡 **Diferenciação Crítica (Sintoma vs Causa):** {sintomas.get('diferenciacao_sintoma_causa')}")

    if sintomas.get("doencas_com_sintomas_semelhantes"):
        with st.expander("⚖️ Diagnóstico Diferencial: Doenças com Sintomas Parecidos"):
            st.write(sintomas.get("doencas_com_sintomas_semelhantes"))

    st.markdown("</div>", unsafe_allow_html=True)

    # Card 3: Coerência com Teachable Machine
    if coerencia:
        conc = coerencia.get("concordancia", "Complementa")
        st.markdown(f"""
        <div class="modern-card" style="border-left: 4px solid var(--secondary);">
            <div class="card-title">🤝 Cruzamento de IA: Teachable Machine + Gemini</div>
            <p style="font-size: 0.92rem; color: var(--text); margin-bottom: 6px;">
                <strong>Consistência com Modelo Local:</strong> <span class="badge-pill badge-info">{conc}</span>
            </p>
            <p style="font-size: 0.9rem; color: var(--text-muted); margin: 0; line-height: 1.5;">
                {coerencia.get('explicacao', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Card 4: Plano de Tratamento e Cuidados Personalizados
    st.markdown("""
    <div class="modern-card">
        <div class="card-title">🌱 Plano Terapêutico e de Recuperação</div>
    """, unsafe_allow_html=True)

    if tratamento.get("resumo"):
        st.markdown(f"**Diretriz Geral:** {tratamento.get('resumo')}")

    if tratamento.get("cuidados_imediatos"):
        st.markdown("##### ⚡ Ações Imediatas (Primeiras 24-48 horas)")
        for act in tratamento.get("cuidados_imediatos", []):
            st.markdown(f"🚨 {act}")

    if tratamento.get("passo_a_passo"):
        st.markdown("##### 📋 Passo a Passo Recomendado")
        for step in tratamento.get("passo_a_passo", []):
            prio = step.get("prioridade", "Média")
            prio_badge = "badge-danger" if prio == "Alta" else ("badge-warning" if prio == "Média" else "badge-healthy")
            st.markdown(f"""
            <div class="step-container">
                <div class="step-number">{step.get('etapa', '•')}</div>
                <div class="step-content">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="step-title">{step.get('titulo')}</span>
                        <span class="badge-pill {prio_badge}" style="font-size: 0.75rem; padding: 2px 8px;">{prio}</span>
                    </div>
                    <div class="step-desc">{step.get('descricao')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    col_mon1, col_mon2 = st.columns(2)
    with col_mon1:
        st.markdown("##### 📈 Sinais de Melhora")
        for sm in tratamento.get("sinais_de_melhora", []):
            st.markdown(f"🌿 {sm}")
    with col_mon2:
        st.markdown("##### ⚠️ Sinais de Piora")
        for sp in tratamento.get("sinais_de_piora", []):
            st.markdown(f"🔻 {sp}")

    if tratamento.get("prevencao"):
        st.markdown("##### 🛡️ Como Prevenir a Recorrência")
        for prev in tratamento.get("prevencao", []):
            st.markdown(f"• {prev}")

    if tratamento.get("tempo_acompanhamento"):
        st.success(f"⏱️ **Janela de Acompanhamento Recomendada:** {tratamento.get('tempo_acompanhamento')}")

    if tratamento.get("cuidados_com_quimicos_e_receitas"):
        st.warning(f"⚠️ **Atenção com Químicos & Receitas:** {tratamento.get('cuidados_com_quimicos_e_receitas')}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Transparência
    if transparencia:
        st.markdown(f"""
        <div class="transparency-callout">
            <strong>🛡️ Transparência e Responsabilidade Fitossanitária:</strong><br>
            {transparencia}
        </div>
        """, unsafe_allow_html=True)

def render_floating_chat(gemini_service, current_analysis: Optional[Dict[str, Any]] = None):
    """
    Renderiza o widget flutuante de chat com a identidade visual da Assistente Nova,
    no canto inferior direito, com avatar animado e inteligência Gemini.
    """
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Olá! Eu sou a **Nova**, sua assistente botânica com IA. ✨🌿\n\nComo posso ajudar você e suas plantas hoje? Pode me perguntar sobre regas, sintomas, iluminação ou tirar dúvidas sobre o seu diagnóstico!"
            }
        ]

    # Popover flutuante posicionado no canto inferior direito
    with st.popover("✨ Conversar com a Nova", help="Abra o chat para tirar dúvidas botânicas em tempo real"):
        # Cabeçalho do Chat estilo Nova
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 38px; height: 38px; background: linear-gradient(145deg, #181824, #242436); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.4);">
                    <div style="position: relative; width: 55%; height: 45%;">
                        <div style="position: absolute; width: 6px; height: 6px; background: #f1f5f9; border-radius: 50%; top: 20%; left: 16%;"></div>
                        <div style="position: absolute; width: 6px; height: 6px; background: #f1f5f9; border-radius: 50%; top: 20%; right: 16%;"></div>
                        <div style="position: absolute; bottom: 5%; left: 50%; transform: translateX(-50%); width: 10px; height: 5px; border: 1.5px solid #f1f5f9; border-top: none; border-radius: 0 0 10px 10px;"></div>
                    </div>
                </div>
                <div>
                    <strong style="color: var(--text); font-size: 1.05rem; display: block; font-family: 'Space Grotesk', sans-serif;">Nova · Assistente IA</strong>
                    <span style="font-size: 0.76rem; color: var(--success); font-weight: 500; display: inline-flex; align-items: center; gap: 4px;">
                        <span style="display: inline-block; width: 7px; height: 7px; background: var(--success); border-radius: 50%; box-shadow: 0 0 8px var(--success);"></span>
                        Online agora via Gemini
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Contexto ativo se houver diagnóstico em tela
        context_desc = None
        if current_analysis:
            g_data = current_analysis.get("gemini_data", {})
            p_name = g_data.get("identificacao", {}).get("nome_popular", "Planta")
            p_health = g_data.get("estado_saude", {}).get("status", "Em avaliação")
            context_desc = f"Planta: {p_name} | Diagnóstico: {p_health}"
            st.markdown(f"""
            <div style="background: rgba(167, 139, 250, 0.08); border: 1px solid rgba(167, 139, 250, 0.25); border-radius: 10px; padding: 6px 12px; font-size: 0.8rem; color: var(--primary-light); margin-bottom: 10px;">
                ✨ <b>Contexto ativo:</b> {p_name} ({p_health})
            </div>
            """, unsafe_allow_html=True)

        # Sugestões rápidas de perguntas quando o chat tem poucas mensagens
        if len(st.session_state.chat_messages) <= 2:
            st.markdown("<p style='font-size: 0.78rem; font-weight: 600; color: var(--text-muted); margin-bottom: 6px;'>Sugestões rápidas:</p>", unsafe_allow_html=True)
            col_chip1, col_chip2 = st.columns(2)
            with col_chip1:
                if st.button("💧 Como regar certo?", key="btn_chip_rega", use_container_width=True):
                    _send_chat_message(
                        "Como saber se estou regando minha planta na quantidade certa ou em excesso?",
                        gemini_service,
                        context_desc
                    )
                    st.rerun()
            with col_chip2:
                if st.button("🍂 Folhas amarelas?", key="btn_chip_amarela", use_container_width=True):
                    _send_chat_message(
                        "O que geralmente faz as folhas de uma planta ficarem amarelas?",
                        gemini_service,
                        context_desc
                    )
                    st.rerun()

        # Janela de histórico de mensagens com rolagem interna
        chat_box = st.container(height=290)
        with chat_box:
            for m in st.session_state.chat_messages:
                avatar = "✨" if m["role"] == "assistant" else "👤"
                with st.chat_message(m["role"], avatar=avatar):
                    st.markdown(m["content"])

        # Formulário de Envio
        with st.form("chat_floating_input_form", clear_on_submit=True):
            col_in, col_btn = st.columns([4.2, 1])
            with col_in:
                user_query = st.text_input(
                    "Mensagem",
                    placeholder="Digite sua dúvida sobre plantas...",
                    label_visibility="collapsed"
                )
            with col_btn:
                sent = st.form_submit_button("➤", type="primary", use_container_width=True)

            if sent and user_query.strip():
                _send_chat_message(user_query.strip(), gemini_service, context_desc)
                st.rerun()

        # Botão para reiniciar o chat
        if len(st.session_state.chat_messages) > 1:
            if st.button("🧹 Limpar conversa", key="btn_limpar_historico_chat", use_container_width=True):
                st.session_state.chat_messages = [
                    {
                        "role": "assistant",
                        "content": "Conversa reiniciada! Como posso ajudar você agora? ✨🌿"
                    }
                ]
                st.rerun()

def _send_chat_message(text: str, gemini_service=None, context: Optional[str] = None):
    """Envia a mensagem ao Gemini e anexa a resposta no histórico com tolerância máxima a falhas."""
    st.session_state.chat_messages.append({"role": "user", "content": text})
    
    # Garantir que o serviço exista e possua o método chat
    if gemini_service is None or not hasattr(gemini_service, "chat"):
        try:
            from services.gemini_service import GeminiPlantDoctorService
            gemini_service = GeminiPlantDoctorService()
        except Exception as e:
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": f"⚠️ Não foi possível inicializar o assistente: {str(e)}"
            })
            return

    try:
        answer = gemini_service.chat(
            user_message=text,
            chat_history=st.session_state.chat_messages,
            context=context
        )
    except Exception as e:
        answer = f"⚠️ Não foi possível obter resposta no momento: {str(e)}"

    st.session_state.chat_messages.append({"role": "assistant", "content": answer})
