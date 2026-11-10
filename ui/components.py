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
  grid-template-columns:1.4fr 1fr;
  align-items:center;
  gap:2.5rem;
  padding:2rem 2.4rem 2rem;
  position:relative;
  background:linear-gradient(135deg,rgba(22,22,31,0.75) 0%,rgba(18,18,26,0.9) 100%);
  border:1px solid var(--border);
  border-radius:22px;
  backdrop-filter:blur(25px);
  box-shadow:0 25px 50px -12px rgba(0,0,0,0.5);
  overflow:hidden;
}}
/* gradient text */
.gradient-text{{
  background:var(--gradient);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;display:inline;
}}
/* badge */
.badge{{
  display:inline-flex;align-items:center;gap:.45rem;
  background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.28);
  color:var(--primary-light);padding:.35rem 1rem;border-radius:999px;
  font-size:.83rem;font-weight:500;margin-bottom:1.1rem;
}}
.badge-dot{{
  width:7px;height:7px;background:var(--success);border-radius:50%;
  box-shadow:0 0 8px var(--success);
  animation:pulse-dot 2s infinite;
}}
@keyframes pulse-dot{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.55;transform:scale(1.35)}}}}
/* title */
h1{{
  font-family:'Space Grotesk',sans-serif;
  font-size:clamp(1.75rem,3.5vw,2.8rem);
  font-weight:800;line-height:1.15;letter-spacing:-.03em;
  margin-bottom:.9rem;color:var(--text);
}}
p.desc{{color:var(--text-muted);font-size:1rem;line-height:1.65;max-width:480px}}

/* ── hero visual ── */
.hero-visual{{
  position:relative;display:flex;align-items:center;justify-content:center;
  height:280px;
}}
/* orbs */
.orb{{position:absolute;border-radius:50%;filter:blur(55px);opacity:.5;animation:orb-float 8s ease-in-out infinite;pointer-events:none}}
.orb-1{{width:220px;height:220px;background:#a78bfa;top:5%;left:10%}}
.orb-2{{width:160px;height:160px;background:#38bdf8;bottom:10%;right:8%;animation-delay:-3s}}
.orb-3{{width:130px;height:130px;background:#f472b6;top:38%;right:25%;animation-delay:-5s}}
@keyframes orb-float{{
  0%,100%{{transform:translate(0,0) scale(1)}}
  33%{{transform:translate(18px,-25px) scale(1.06)}}
  66%{{transform:translate(-12px,18px) scale(.94)}}
}}
/* avatar */
.avatar-container{{position:relative;z-index:2}}
.avatar-ring{{
  position:absolute;inset:-20px;
  border:2px solid rgba(167,139,250,.3);border-radius:50%;
  animation:spin-slow 20s linear infinite;
}}
.avatar-ring.ring-2{{
  inset:-40px;border-color:rgba(56,189,248,.2);
  animation-direction:reverse;animation-duration:30s;
}}
@keyframes spin-slow{{to{{transform:rotate(360deg)}}}}
.avatar{{
  width:160px;height:160px;
  background:linear-gradient(145deg,#1e1e2e,#2a2a3d);
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  box-shadow:0 0 0 4px rgba(167,139,250,.2),0 20px 60px rgba(0,0,0,.4),inset 0 0 40px rgba(167,139,250,.12);
  animation:avatar-float 6s ease-in-out infinite;
}}
@keyframes avatar-float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
.avatar.speaking{{animation:speak-bounce .6s ease infinite,avatar-float 6s ease-in-out infinite}}
@keyframes speak-bounce{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.04)}}}}
/* face */
.avatar-face{{position:relative;width:60%;height:50%}}
.eye{{
  position:absolute;width:16px;height:16px;background:#e2e8f0;
  border-radius:50%;top:20%;box-shadow:inset 0 -2px 0 rgba(0,0,0,.15);transition:transform .15s ease;
}}
.eye.left{{left:12%}}.eye.right{{right:12%}}
.eye::after{{
  content:'';position:absolute;width:7px;height:7px;background:#1e1e2e;
  border-radius:50%;top:50%;left:50%;transform:translate(-50%,-50%);
}}
.mouth{{
  position:absolute;bottom:8%;left:50%;transform:translateX(-50%);
  width:26px;height:11px;border:2.5px solid #e2e8f0;border-top:none;
  border-radius:0 0 18px 18px;transition:all .3s ease;
}}
.avatar.happy .mouth{{width:30px;height:14px;border-radius:0 0 28px 28px}}
.avatar.speaking .mouth{{animation:mouth-talk .35s ease infinite alternate}}
@keyframes mouth-talk{{from{{height:7px;width:22px}}to{{height:15px;width:28px;border-radius:0 0 36px 36px}}}}
/* pulse ring */
.pulse-ring{{
  position:absolute;inset:-10px;
  border:2px solid rgba(167,139,250,.4);border-radius:50%;
  animation:pulse-expand 2.5s ease-out infinite;
}}
@keyframes pulse-expand{{0%{{transform:scale(1);opacity:.6}}100%{{transform:scale(1.45);opacity:0}}}}
/* particles */
.particles{{position:absolute;inset:0;pointer-events:none;overflow:hidden;border-radius:22px}}
.particle{{
  position:absolute;border-radius:50%;opacity:.35;
  animation:float-particle 14s infinite linear;
}}
@keyframes float-particle{{
  0%{{transform:translateY(100%) scale(0);opacity:0}}
  10%{{opacity:.4}}90%{{opacity:.15}}
  100%{{transform:translateY(-80px) scale(1);opacity:0}}
}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(24px)}}to{{opacity:1;transform:translateY(0)}}}}
.hero-content{{animation:fadeUp .7s ease both}}
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
// Particles
(function(){{
  const c=document.getElementById('particles');
  if(!c)return;
  const colors=['#a78bfa','#38bdf8','#f472b6','#c4b5fd'];
  for(let i=0;i<28;i++){{
    const p=document.createElement('div');
    p.className='particle';
    p.style.left=Math.random()*100+'%';
    p.style.animationDelay=Math.random()*14+'s';
    p.style.animationDuration=(10+Math.random()*10)+'s';
    const sz=1.5+Math.random()*3+'px';
    p.style.width=sz;p.style.height=sz;
    p.style.background=colors[Math.floor(Math.random()*4)];
    c.appendChild(p);
  }}
}})();

// Blink eyes
function blinkEyes(){{
  document.querySelectorAll('.eye').forEach(e=>e.style.transform='scaleY(0.08)');
  setTimeout(()=>document.querySelectorAll('.eye').forEach(e=>e.style.transform=''),140);
}}
setInterval(blinkEyes, 3200+Math.random()*1800);

// Idle avatar expression cycle
const av=document.getElementById('heroAvatar');
if(av){{
  setInterval(()=>{{
    av.classList.add('happy');
    setTimeout(()=>av.classList.remove('happy'),1200);
  }}, 7000);
}}
</script>
</body>
</html>"""

    height = 240 if show_avatar else 160
    components.html(hero_html, height=height, scrolling=False)

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
