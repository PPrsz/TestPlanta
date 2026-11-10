import streamlit as st
from typing import Dict, Any, List, Optional
from PIL import Image

def render_hero(title: str = "PlantCare AI", subtitle: str = "Diagnóstico Botânico Inteligente com Teachable Machine e Google Gemini"):
    """Renderiza cabeçalho principal imersivo com identidade botânica."""
    st.markdown(f"""
    <div class="plant-hero-card">
        <h1 class="plant-hero-title">🌿 {title}</h1>
        <p class="plant-hero-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_quality_audit(audit: Dict[str, Any]):
    """Renderiza a avaliação de qualidade fotográfica antes da inferência."""
    rating = audit.get("quality_rating", "Desconhecida")
    is_ok = audit.get("is_acceptable", True)
    
    badge_class = "badge-healthy" if rating == "Excelente" else ("badge-warning" if rating == "Aceitável" else "badge-danger")
    icon = "✅" if is_ok else "⚠️"
    
    st.markdown(f"""
    <div style="background: #f8faf8; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px 16px; margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #1b4332; font-size: 0.95rem;">📸 Auditoria da Qualidade Fotográfica:</strong>
            <span class="badge-pill {badge_class}">{icon} {rating}</span>
        </div>
        <div style="font-size: 0.85rem; color: #4b5563; display: flex; gap: 15px; flex-wrap: wrap;">
            <span>📐 Resolução: <b>{audit.get('width')}x{audit.get('height')}px</b></span>
            <span>💡 Brilho Médio: <b>{audit.get('brightness')}/255</b></span>
            <span>🎯 Nitidez Estimada: <b>{audit.get('sharpness')}</b></span>
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
    """Renderiza o cartão de classificação especializada do Teachable Machine."""
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
            <span>🔬 Classificador Local: Google Teachable Machine</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div>
                <span style="font-size: 1.15rem; font-weight: 700; color: #1e293b;">{top_class}</span>
            </div>
            <span class="badge-pill {badge_type}">{status_icon} {conf_pct:.1f}% de Certeza Local</span>
        </div>
        <div style="font-size: 0.88rem; color: #475569; margin-bottom: 14px;">
            {tm_result.get('summary')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Exibição da distribuição de todas as classes
    with st.expander("📊 Ver distribuição de probabilidades do Teachable Machine", expanded=False):
        for class_name, score in tm_result.get("sorted_predictions", []):
            pct = score * 100
            st.write(f"**{class_name}**: {pct:.1f}%")
            st.progress(min(max(pct / 100.0, 0.0), 1.0))

def render_diagnosis_view(gemini_data: Dict[str, Any], tm_result: Optional[Dict[str, Any]] = None):
    """Renderiza a tela completa de diagnóstico estruturado com cartões especializados."""
    
    ident = gemini_data.get("identificacao", {})
    saude = gemini_data.get("estado_saude", {})
    sintomas = gemini_data.get("analise_sintomas", {})
    coerencia = gemini_data.get("coerencia_teachable_machine", {})
    tratamento = gemini_data.get("plano_tratamento", {})
    perguntas = gemini_data.get("perguntas_complementares", [])
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
                <span style="font-size: 1.4rem; font-weight: 800; color: #1b4332;">{ident.get('nome_popular', 'Espécie em análise')}</span>
                <br>
                <em style="color: #64748b; font-size: 1.05rem;">{ident.get('nome_cientifico', 'Classificação científica')}</em>
            </div>
            <p style="font-size: 0.92rem; color: #334155; margin-top: 10px; line-height: 1.5;">
                {ident.get('caracteristicas_gerais', '')}
            </p>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 8px;">
                Certeza da identificação taxonômica: <b>{ident.get('confianca_identificacao', 'Média')}</b>
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
                    <div class="metric-value" style="font-size: 1.1rem; color: #1b4332;">{saude.get('confianca_diagnostico', 'Média')}</div>
                </div>
            </div>
            <p style="font-size: 0.88rem; color: #475569; margin-top: 10px; margin-bottom: 0;">
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
        <div class="modern-card" style="border-left: 4px solid #52b788;">
            <div class="card-title">🤝 Cruzamento de IA: Teachable Machine + Gemini</div>
            <p style="font-size: 0.92rem; color: #1e293b; margin-bottom: 6px;">
                <strong>Consistência com Modelo Local:</strong> <span class="badge-pill badge-info">{conc}</span>
            </p>
            <p style="font-size: 0.9rem; color: #475569; margin: 0; line-height: 1.5;">
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
    Renderiza um widget de chat flutuante no canto inferior direito,
    atuando como assistente virtual botânico com Google Gemini.
    """
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou seu **Agrônomo Virtual**. 🌿\n\nComo posso ajudar suas plantas hoje? Pode me perguntar sobre frequência de rega, adubos, podas, sol ou dúvidas sobre o diagnóstico!"
            }
        ]

    # Popover flutuante posicionado no canto inferior direito
    with st.popover("💬 Assistente Virtual", help="Abra o chat para tirar dúvidas com a IA botânica"):
        # Cabeçalho do Chat
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #f0fdf4; padding-bottom: 10px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.6rem;">🌱</span>
                <div>
                    <strong style="color: #1b4332; font-size: 1.05rem; display: block; line-height: 1.2;">Agrônomo Virtual</strong>
                    <span style="font-size: 0.76rem; color: #15803d; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
                        <span style="display: inline-block; width: 7px; height: 7px; background: #22c55e; border-radius: 50%;"></span>
                        Online via Google Gemini
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
            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 6px 10px; font-size: 0.8rem; color: #166534; margin-bottom: 10px;">
                🌿 <b>Contexto ativo:</b> {p_name} ({p_health})
            </div>
            """, unsafe_allow_html=True)

        # Sugestões rápidas de perguntas quando o chat tem poucas mensagens
        if len(st.session_state.chat_messages) <= 2:
            st.markdown("<p style='font-size: 0.78rem; font-weight: 600; color: #64748b; margin-bottom: 6px;'>Perguntas frequentes:</p>", unsafe_allow_html=True)
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
                avatar = "🌿" if m["role"] == "assistant" else "👤"
                with st.chat_message(m["role"], avatar=avatar):
                    st.markdown(m["content"])

        # Formulário de Envio
        with st.form("chat_floating_input_form", clear_on_submit=True):
            col_in, col_btn = st.columns([4.2, 1])
            with col_in:
                user_query = st.text_input(
                    "Mensagem",
                    placeholder="Pergunte sobre regas, folhas, pragas...",
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
                        "content": "Conversa reiniciada! No que posso ajudar com suas plantas agora? 🌿"
                    }
                ]
                st.rerun()

def _send_chat_message(text: str, gemini_service, context: Optional[str] = None):
    """Envia a mensagem ao Gemini e anexa a resposta no histórico."""
    st.session_state.chat_messages.append({"role": "user", "content": text})
    
    # Garantir que o serviço esteja atualizado e possua o método chat
    if not hasattr(gemini_service, "chat"):
        from services.gemini_service import GeminiPlantDoctorService
        gemini_service = GeminiPlantDoctorService()

    try:
        answer = gemini_service.chat(
            user_message=text,
            chat_history=st.session_state.chat_messages,
            context=context
        )
    except Exception as e:
        answer = f"⚠️ Não foi possível obter resposta no momento: {str(e)}"

    st.session_state.chat_messages.append({"role": "assistant", "content": answer})
