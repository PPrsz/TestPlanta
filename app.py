import os
import json
from pathlib import Path
from datetime import datetime, date
import streamlit as st
from PIL import Image

from config import Config
from services.image_quality_service import ImageQualityService
from services.teachable_machine_service import TeachableMachineService
from services.gemini_service import GeminiPlantDoctorService
from services.database_service import DatabaseService
from ui.styles import CUSTOM_CSS
from ui.components import (
    render_hero,
    render_quality_audit,
    render_teachable_machine_panel,
    render_diagnosis_view
)

# Configuração da Página Web
st.set_page_config(
    page_title="PlantCare AI - Diagnóstico e Saúde Vegetal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injetar Estilos Visuais Profissionais
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# Inicialização dos Serviços em Cache
# ==========================================
@st.cache_resource
def get_db():
    return DatabaseService()

@st.cache_resource
def get_tm_service():
    return TeachableMachineService()

@st.cache_resource
def get_gemini_service():
    return GeminiPlantDoctorService()

db = get_db()
tm_service = get_tm_service()
gemini_service = get_gemini_service()

# ==========================================
# Estado da Sessão (Session State)
# ==========================================
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "current_audit" not in st.session_state:
    st.session_state.current_audit = None
if "selected_plant_id" not in st.session_state:
    st.session_state.selected_plant_id = None

# ==========================================
# Barra Lateral de Navegação
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0 1rem 0;">
        <span style="font-size: 3rem;">🌿</span>
        <h2 style="margin: 0; color: #ffffff; font-weight: 800; font-size: 1.5rem;">PlantCare AI</h2>
        <p style="color: #a7f3d0; font-size: 0.85rem; margin: 4px 0 0 0;">Saúde Vegetal & Inteligência Artificial</p>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navegação",
        [
            "🏠 Início",
            "🔍 Nova Análise",
            "🌿 Meu Jardim & Acompanhamento",
            "🧪 Validação & Testes de IA",
            "⚙️ Configurações & API"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    
    # Status dos Modelos no Sidebar
    st.markdown("<p style='font-size: 0.8rem; font-weight: 700; color: #9ca3af; text-transform: uppercase;'>Status dos Sistemas</p>", unsafe_allow_html=True)
    
    tm_status_icon = "🟢" if tm_service.is_loaded else "🔴"
    tm_status_text = "Operacional" if tm_service.is_loaded else "Falha ao carregar"
    st.markdown(f"<span style='font-size: 0.85rem;'>{tm_status_icon} <b>Teachable Machine:</b> {tm_status_text}</span>", unsafe_allow_html=True)

    gemini_configured = gemini_service.is_configured()
    gem_icon = "🟢" if gemini_configured else "🟡"
    gem_text = f"Ativo ({Config.PRIMARY_GEMINI_MODEL})" if gemini_configured else "Chave pendente"
    st.markdown(f"<span style='font-size: 0.85rem;'>{gem_icon} <b>Google Gemini:</b> {gem_text}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("🌱 Desenvolvido com Google Gemini & Google Teachable Machine.")

# ==========================================
# PÁGINA 1: INÍCIO
# ==========================================
if page == "🏠 Início":
    render_hero(
        title="PlantCare AI: Saúde & Diagnóstico Vegetal",
        subtitle="Identificação de espécies, patologia botânica e recuperação orientada por IA."
    )

    # Métricas Rápidas do Jardim
    plants = db.get_all_plants()
    recent_diagnoses = db.get_recent_diagnoses(limit=5)
    
    total_plants = len(plants)
    healthy_count = sum(1 for p in plants if "saud" in (p.get("health_status") or "").lower())
    attention_count = total_plants - healthy_count

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Plantas Cadastradas</div>
            <div class="metric-value">{total_plants}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Aparentemente Saudáveis</div>
            <div class="metric-value" style="color: #15803d;">{healthy_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Sob Atenção / Tratamento</div>
            <div class="metric-value" style="color: #b45309;">{attention_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Diagnósticos Realizados</div>
            <div class="metric-value" style="color: #1b4332;">{len(recent_diagnoses)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    col_cta1, col_cta2 = st.columns([1.8, 1.2])
    with col_cta1:
        st.markdown("""
        <div class="modern-card">
            <div class="card-title">🔍 Como Funciona o Assistente Inteligente</div>
            <p style="color: #374151; font-size: 0.95rem; line-height: 1.6;">
                O <b>PlantCare AI</b> combina duas camadas complementares de inteligência artificial para maximizar a precisão:
            </p>
            <ul style="color: #4b5563; font-size: 0.92rem; line-height: 1.7;">
                <li><b>1. Classificador Local (Google Teachable Machine):</b> Avalia padrões visuais aprendidos localmente em frações de segundo, identificando sinais de alerta.</li>
                <li><b>2. Raciocínio Botânico (Google Gemini):</b> Analisa a foto em alta definição, interpreta o modelo local, identifica a espécie botânica, investiga causas subjacentes e formula um tratamento seguro passo a passo.</li>
                <li><b>3. Diferenciação Científica:</b> Separa sintomas observados (como folhas amarelas) de causas reais (como rega incorreta ou fungos), sem suposições precipitadas.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_cta2:
        st.markdown("""
        <div class="modern-card" style="background: #f0fdf4; border-color: #bbf7d0;">
            <div class="card-title" style="color: #166534;">💡 Dicas de Cuidados Botânicos</div>
            <p style="font-size: 0.88rem; color: #15803d; line-height: 1.5;">
                • <b>Drenagem é vida:</b> Mais plantas morrem por excesso de rega (asfixia radicular) do que por sede.<br><br>
                • <b>Observe a luz:</b> Luz indireta brilhante é o ambiente ideal para a maioria das folhagens domésticas.<br><br>
                • <b>Poda profilática:</b> Remova folhas doentes com tesoura esterilizada para não infectar galhos sadios.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Últimos Diagnósticos Registrados
    if recent_diagnoses:
        st.subheader("📋 Últimas Análises Realizadas")
        for diag in recent_diagnoses[:3]:
            dt = diag.get("created_at", "")[:10]
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 10px; padding: 12px 18px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>Planta:</strong> {diag.get('plant_name') or 'Análise Avulsa'} &nbsp;|&nbsp; 
                    <span style="color: #64748b;">Data: {dt}</span>
                </div>
                <span class="badge-pill badge-healthy">{diag.get('gemini_status') or diag.get('tm_top_class')}</span>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# PÁGINA 2: NOVA ANÁLISE
# ==========================================
elif page == "🔍 Nova Análise":
    render_hero(
        title="Diagnóstico de Saúde Vegetal",
        subtitle="Fotografe a folha ou planta para análise integrada entre Teachable Machine e Google Gemini."
    )

    col_up1, col_up2 = st.columns([1.1, 0.9])
    
    with col_up1:
        st.markdown("##### 1. Capturar ou Enviar Imagem")
        input_method = st.radio(
            "Método de entrada",
            ["📤 Upload de Arquivo (JPG/PNG)", "📷 Usar Câmera", "🌱 Usar Imagem de Exemplo (plantas_1.jpg)"],
            horizontal=True
        )

        image_to_process = None

        if input_method == "📤 Upload de Arquivo (JPG/PNG)":
            uploaded_file = st.file_uploader("Selecione uma imagem de folha ou planta:", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                image_to_process = Image.open(uploaded_file).convert("RGB")

        elif input_method == "📷 Usar Câmera":
            camera_file = st.camera_input("Tire uma foto nítida da planta ou do sintoma:")
            if camera_file:
                image_to_process = Image.open(camera_file).convert("RGB")

        elif input_method == "🌱 Usar Imagem de Exemplo (plantas_1.jpg)":
            sample_path = Path("plantas_1.jpg")
            if sample_path.exists():
                image_to_process = Image.open(sample_path).convert("RGB")
                st.caption("Imagem de exemplo carregada da pasta do projeto.")
            else:
                st.warning("Arquivo 'plantas_1.jpg' não encontrado.")

        # Auditoria da Qualidade se imagem estiver disponível
        if image_to_process:
            st.session_state.current_image = image_to_process
            audit = ImageQualityService.inspect_and_validate(image_to_process)
            st.session_state.current_audit = audit
            render_quality_audit(audit)
            st.image(image_to_process, caption="Fotografia selecionada para análise", use_container_width=True)

    with col_up2:
        st.markdown("##### 2. Informações de Contexto (Opcional, melhora o diagnóstico)")
        with st.expander("📝 Responder perguntas para refinar o diagnóstico", expanded=True):
            st.caption("Estas respostas ajudam a IA a diferenciar carências nutricionais de problemas de rega ou pragas.")
            
            c_loc = st.selectbox("Onde a planta fica?", ["Não informado", "Interior (dentro de casa / apartamento)", "Exterior (varanda / quintal aberto)"])
            c_luz = st.selectbox("Qual é a iluminação diária?", ["Não informado", "Luz solar direta constante", "Luz solar indireta brilhante", "Meia-sombra / luz fraca", "Ambiente escuro"])
            c_rega = st.selectbox("Com que frequência costuma regar?", ["Não informado", "Diariamente", "2 a 3 vezes por semana", "1 vez por semana", "Apenas quando o solo seca completamente", "Raras vezes"])
            c_tempo = st.selectbox("Quando os sintomas começaram?", ["Não informado", "Há poucos dias (recente)", "Há 1 a 2 semanas", "Há mais de um mês"])
            c_distrib = st.selectbox("Onde os sintomas aparecem?", ["Não informado", "Apenas em uma folha isolada", "Nas folhas mais velhas da base", "Nas folhas novas brotando no topo", "Na planta inteira"])
            c_vaso = st.checkbox("Houve transplante, troca de vaso ou solo recentemente?")

            user_context = {
                "Localização": c_loc if c_loc != "Não informado" else None,
                "Iluminação": c_luz if c_luz != "Não informado" else None,
                "Frequência de Rega": c_rega if c_rega != "Não informado" else None,
                "Início dos Sintomas": c_tempo if c_tempo != "Não informado" else None,
                "Distribuição dos Sintomas": c_distrib if c_distrib != "Não informado" else None,
                "Transplante recente": "Sim" if c_vaso else "Não"
            }

        # Botão de Ação
        st.write("")
        start_btn = st.button("🔬 Iniciar Diagnóstico Completo com IA", type="primary", use_container_width=True)

    # Execução do Processamento
    if start_btn:
        if not st.session_state.current_image:
            st.error("Por favor, selecione ou envie uma imagem antes de iniciar o diagnóstico.")
        elif not gemini_service.is_configured():
            st.error("A chave da API do Google Gemini não está configurada! Vá na aba '⚙️ Configurações & API' para configurar.")
        else:
            img = st.session_state.current_image
            
            # Stepper Visual com Feedback Real
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Etapa 1: Otimização da Imagem
            status_text.info("📸 Etapa 1/4: Preparando e otimizando a fotografia...")
            progress_bar.progress(25)
            optimized_img = ImageQualityService.prepare_for_ai(img)

            # Etapa 2: Classificação Local Teachable Machine
            status_text.info("🔬 Etapa 2/4: Classificando padrões visuais no Google Teachable Machine local...")
            progress_bar.progress(50)
            tm_result = tm_service.predict(img)

            # Etapa 3: Consulta ao Agrônomo Virtual Gemini
            status_text.info("🌿 Etapa 3/4: Raciocínio botânico aprofundado com Google Gemini...")
            progress_bar.progress(75)
            gemini_res = gemini_service.analyze_plant(
                image=optimized_img,
                tm_result=tm_result,
                user_context=user_context
            )

            # Etapa 4: Consolidação dos Resultados
            status_text.info("📋 Etapa 4/4: Consolidando relatório fitossanitário...")
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()

            if gemini_res.get("success"):
                st.session_state.current_analysis = {
                    "tm_result": tm_result,
                    "gemini_data": gemini_res.get("data"),
                    "model_used": gemini_res.get("model_used"),
                    "timestamp": datetime.now().isoformat()
                }
                st.success(f"Diagnóstico concluído com sucesso via {gemini_res.get('model_used')}!")
            else:
                st.error(f"Erro no diagnóstico: {gemini_res.get('error_message')}")

    # Exibição dos Resultados Existentes na Sessão
    if st.session_state.current_analysis:
        analysis = st.session_state.current_analysis
        tm_res = analysis.get("tm_result")
        gem_data = analysis.get("gemini_data")

        st.markdown("---")
        st.subheader("📋 Relatório Fitossanitário Inteligente")

        # Exibir painel do Teachable Machine
        render_teachable_machine_panel(tm_res)

        # Exibir visão detalhada do Gemini
        render_diagnosis_view(gem_data, tm_res)

        # Ações pós-análise: Salvar no Jardim ou Exportar
        st.markdown("---")
        col_act1, col_act2, col_act3 = st.columns(3)

        with col_act1:
            with st.expander("💾 Salvar Diagnóstico no Meu Jardim", expanded=True):
                all_plants = db.get_all_plants()
                plant_options = {"Criar Nova Planta com este Diagnóstico": None}
                for p in all_plants:
                    plant_options[f"#{p['id']} - {p['name']} ({p.get('species') or 'Sem espécie'})"] = p['id']
                
                selected_choice = st.selectbox("Vincular a qual planta?", list(plant_options.keys()))
                target_plant_id = plant_options[selected_choice]

                new_plant_name = ""
                if target_plant_id is None:
                    suggested_name = gem_data.get("identificacao", {}).get("nome_popular", "Minha Planta")
                    new_plant_name = st.text_input("Nome da nova planta:", value=suggested_name)

                save_notes = st.text_area("Observações pessoais (opcional):", placeholder="Ex: Manchas surgiram após a chuva...")

                if st.button("Confirmar e Salvar", type="primary"):
                    # Salvar imagem no disco
                    saved_img_path = db.save_image_to_disk(st.session_state.current_image, prefix="diag")
                    
                    if target_plant_id is None:
                        target_plant_id = db.create_plant(
                            name=new_plant_name or "Minha Planta",
                            species=gem_data.get("identificacao", {}).get("nome_popular", ""),
                            scientific_name=gem_data.get("identificacao", {}).get("nome_cientifico", ""),
                            image_path=saved_img_path,
                            health_status=gem_data.get("estado_saude", {}).get("status", "")
                        )

                    diag_id = db.save_diagnosis(
                        image_path=saved_img_path,
                        plant_id=target_plant_id,
                        tm_top_class=tm_res.get("top_class", ""),
                        tm_confidence=tm_res.get("top_confidence", 0.0),
                        tm_predictions=tm_res.get("predictions", {}),
                        gemini_status=gem_data.get("estado_saude", {}).get("status", ""),
                        gemini_severity=gem_data.get("estado_saude", {}).get("gravidade_estimada", ""),
                        gemini_data=gem_data,
                        notes=save_notes
                    )
                    st.success(f"Diagnóstico #{diag_id} salvo com sucesso no seu Jardim!")

        with col_act2:
            st.markdown("##### 📄 Exportar Relatório")
            report_text = f"""# Relatório Fitossanitário - PlantCare AI
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Espécie: {gem_data.get('identificacao', {}).get('nome_popular')} ({gem_data.get('identificacao', {}).get('nome_cientifico')})
Estado de Saúde: {gem_data.get('estado_saude', {}).get('status')}
Gravidade: {gem_data.get('estado_saude', {}).get('gravidade_estimada')}

## Sintomas Observados
{chr(10).join(['- ' + s for s in gem_data.get('analise_sintomas', {}).get('sintomas_visiveis', [])])}

## Causas Prováveis
{chr(10).join(['- ' + c.get('causa') + ': ' + c.get('explicacao') for c in gem_data.get('analise_sintomas', {}).get('causas_provaveis', [])])}

## Plano de Tratamento
{chr(10).join(['- ' + p.get('titulo') + ': ' + p.get('descricao') for p in gem_data.get('plano_tratamento', {}).get('passo_a_passo', [])])}

## Prevenção
{chr(10).join(['- ' + pr for pr in gem_data.get('plano_tratamento', {}).get('prevencao', [])])}
"""
            st.download_button(
                label="📥 Baixar Relatório em Markdown",
                data=report_text,
                file_name=f"diagnostico_planta_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col_act3:
            st.markdown("##### 🔄 Nova Consulta")
            if st.button("Limpar e Analisar Outra Imagem", use_container_width=True):
                st.session_state.current_analysis = None
                st.session_state.current_image = None
                st.session_state.current_audit = None
                st.rerun()

# ==========================================
# PÁGINA 3: MEU JARDIM & ACOMPANHAMENTO
# ==========================================
elif page == "🌿 Meu Jardim & Acompanhamento":
    render_hero(
        title="Meu Jardim & Acompanhamento de Saúde",
        subtitle="Monitore a evolução das suas plantas ao longo do tempo e compare antes x depois da recuperação."
    )

    all_plants = db.get_all_plants()

    col_j1, col_j2 = st.columns([1, 2])

    with col_j1:
        st.subheader("🌱 Suas Plantas")
        
        # Botão para adicionar nova planta manualmente
        with st.expander("➕ Adicionar Nova Planta ao Jardim"):
            np_name = st.text_input("Nome da Planta (ex: Samambaia da Sala)")
            np_spec = st.text_input("Espécie / Nome Popular")
            np_scie = st.text_input("Nome Científico (se souber)")
            np_days = st.number_input("Regar a cada quantos dias?", min_value=1, max_value=30, value=3)
            np_notes = st.text_area("Notas iniciais")
            
            if st.button("Cadastrar Planta"):
                if np_name:
                    new_id = db.create_plant(name=np_name, species=np_spec, scientific_name=np_scie, notes=np_notes, watering_days=np_days)
                    st.success(f"Planta #{new_id} cadastrada!")
                    st.rerun()
                else:
                    st.error("Informe o nome da planta.")

        if not all_plants:
            st.info("Você ainda não tem plantas cadastradas. Faça uma análise ou adicione uma planta acima!")
        else:
            for plant in all_plants:
                p_id = plant["id"]
                is_selected = (st.session_state.selected_plant_id == p_id)
                btn_type = "primary" if is_selected else "secondary"
                
                status_icon = "🟢" if "saud" in (plant.get("health_status") or "").lower() else "🟡"
                if st.button(f"{status_icon} #{p_id} - {plant['name']}", key=f"plant_btn_{p_id}", type=btn_type, use_container_width=True):
                    st.session_state.selected_plant_id = p_id
                    st.rerun()

    with col_j2:
        if st.session_state.selected_plant_id:
            plant = db.get_plant_by_id(st.session_state.selected_plant_id)
            if plant:
                p_id = plant["id"]
                st.markdown(f"""
                <div class="modern-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h2 style="margin: 0; color: #1b4332;">{plant['name']}</h2>
                        <span class="badge-pill badge-healthy">{plant.get('health_status')}</span>
                    </div>
                    <p style="color: #64748b; margin: 4px 0 12px 0;">
                        <b>Espécie:</b> {plant.get('species') or 'Não informada'} | 
                        <em>{plant.get('scientific_name') or ''}</em>
                    </p>
                    <div style="display: flex; gap: 12px; font-size: 0.88rem; color: #4b5563;">
                        <span>💧 Rega: a cada <b>{plant.get('watering_frequency_days', 3)} dias</b></span>
                        <span>📅 Última Rega: <b>{plant.get('last_watered_date') or 'Sem registro'}</b></span>
                        <span>🌱 Cadastrada em: <b>{plant['created_at'][:10]}</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Ações Rápidas de Cuidados (1 clique)
                col_care1, col_care2, col_care3 = st.columns(3)
                with col_care1:
                    if st.button("💧 Reguei Hoje", key=f"care_water_{p_id}", use_container_width=True):
                        db.log_care(p_id, "Rega", "Rega rotineira realizada")
                        st.toast("Rega registrada!")
                        st.rerun()
                with col_care2:
                    if st.button("🍃 Adubei Hoje", key=f"care_fert_{p_id}", use_container_width=True):
                        db.log_care(p_id, "Adubação", "Adubação aplicada")
                        st.toast("Adubação registrada!")
                        st.rerun()
                with col_care3:
                    if st.button("✂️ Fiz Poda Sanitária", key=f"care_prune_{p_id}", use_container_width=True):
                        db.log_care(p_id, "Poda", "Folhas secas ou lesadas removidas")
                        st.toast("Poda registrada!")
                        st.rerun()

                # Abas: Histórico de Diagnósticos, Comparador Antes x Depois, Diário de Cuidados
                tab_hist, tab_comp, tab_diary = st.tabs(["📋 Histórico de Diagnósticos", "🔄 Comparador Antes x Depois", "📖 Diário de Cuidados"])

                with tab_hist:
                    diagnoses = db.get_diagnoses_for_plant(p_id)
                    if not diagnoses:
                        st.info("Nenhum diagnóstico registrado para esta planta ainda.")
                    else:
                        for d in diagnoses:
                            with st.expander(f"Diagnóstico #{d['id']} - {d['created_at'][:10]} ({d.get('gemini_status')})"):
                                col_dh1, col_dh2 = st.columns([1, 2])
                                with col_dh1:
                                    if os.path.exists(d.get("image_path", "")):
                                        st.image(d["image_path"], caption=f"Foto em {d['created_at'][:10]}", use_container_width=True)
                                with col_dh2:
                                    st.write(f"**Status:** {d.get('gemini_status')}")
                                    st.write(f"**Gravidade:** {d.get('gemini_severity')}")
                                    st.write(f"**Teachable Machine:** {d.get('tm_top_class')} ({d.get('tm_confidence', 0)*100:.1f}%)")
                                    if d.get("notes"):
                                        st.write(f"**Notas:** {d.get('notes')}")

                with tab_comp:
                    st.markdown("##### Comparação Visual de Evolução (Antes x Depois)")
                    diagnoses = db.get_diagnoses_for_plant(p_id)
                    if len(diagnoses) < 2:
                        st.warning("É necessário ter pelo menos 2 diagnósticos registrados para comparar a recuperação.")
                    else:
                        diag_opts = {f"#{d['id']} - {d['created_at'][:10]} ({d.get('gemini_status')})": d for d in diagnoses}
                        
                        col_c1, col_c2 = st.columns(2)
                        with col_c1:
                            sel_before_key = st.selectbox("Foto Anterior (Antes):", list(diag_opts.keys()), index=len(diag_opts)-1)
                            diag_before = diag_opts[sel_before_key]
                            if os.path.exists(diag_before.get("image_path", "")):
                                st.image(diag_before["image_path"], caption=f"Antes: {diag_before['created_at'][:10]}", use_container_width=True)
                        
                        with col_c2:
                            sel_after_key = st.selectbox("Foto Recente (Depois):", list(diag_opts.keys()), index=0)
                            diag_after = diag_opts[sel_after_key]
                            if os.path.exists(diag_after.get("image_path", "")):
                                st.image(diag_after["image_path"], caption=f"Depois: {diag_after['created_at'][:10]}", use_container_width=True)

                        # Registrar parecer de recuperação
                        st.markdown("##### Avaliação da Recuperação:")
                        col_ev1, col_ev2 = st.columns([1.5, 1])
                        with col_ev1:
                            comp_notes = st.text_input("Observação sobre a mudança:", placeholder="Ex: Manchas secaram e não surgiram novas lesões...")
                        with col_ev2:
                            status_ev = st.selectbox("Status de Evolução:", ["Melhorando / Recuperando", "Estável / Sem alteração", "Piorando / Sintomas avançaram", "Inconclusivo"])
                        
                        if st.button("Salvar Comparação no Histórico"):
                            db.record_comparison(
                                plant_id=p_id,
                                before_diag_id=diag_before["id"],
                                after_diag_id=diag_after["id"],
                                evolution_status=status_ev,
                                notes=comp_notes
                            )
                            st.success("Comparação registrada com sucesso!")

                with tab_diary:
                    st.markdown("##### Registro de Intervenções e Cuidados")
                    logs = db.get_care_logs(p_id)
                    if not logs:
                        st.info("Nenhum registro no diário de cuidados ainda.")
                    else:
                        for l in logs:
                            st.write(f"• **{l['timestamp'][:16].replace('T', ' ')}** - `{l['care_type']}`: {l.get('notes') or 'Sem observações'}")

        else:
            st.info("👈 Selecione uma planta na lista ao lado para ver sua ficha completa ou cadastre uma nova.")

# ==========================================
# PÁGINA 4: VALIDAÇÃO & TESTES DE IA
# ==========================================
elif page == "🧪 Validação & Testes de IA":
    render_hero(
        title="Validação & Testes dos Modelos de IA",
        subtitle="Auditoria de métricas, testes de estresse, matriz de confusão e verificação de redundância."
    )

    tab_t1, tab_t2, tab_t3 = st.tabs(["🔬 Teste do Teachable Machine Local", "🌐 Teste de Redundância do Gemini", "📊 Avaliação de Desempenho"])

    with tab_t1:
        st.markdown("##### Teste Rápido do Classificador Teachable Machine")
        st.write(f"**Caminho do Modelo:** `{Config.TM_MODEL_PATH}`")
        st.write(f"**Arquivo de Labels:** `{Config.TM_LABELS_FILE}`")
        st.write(f"**Classes Identificadas ({len(tm_service.labels)}):** `{', '.join(tm_service.labels)}`")

        sample_img_path = Path("plantas_1.jpg")
        if sample_img_path.exists():
            test_img = Image.open(sample_img_path)
            col_tt1, col_tt2 = st.columns([1, 1.5])
            with col_tt1:
                st.image(test_img, caption="Amostra de Teste (plantas_1.jpg)", use_container_width=True)
            with col_tt2:
                if st.button("Executar Inferência de Teste no Teachable Machine", type="primary"):
                    import time
                    t0 = time.time()
                    t_res = tm_service.predict(test_img)
                    latency_ms = (time.time() - t0) * 1000
                    
                    st.success(f"Inferência executada em {latency_ms:.1f}ms!")
                    st.json(t_res)

    with tab_t2:
        st.markdown("##### Teste de Conectividade e Latência com Modelos Gemini")
        st.caption("Verifica quais modelos estão ativos na sua conta da API e o tempo de resposta de cada um.")
        
        models_to_test = [Config.PRIMARY_GEMINI_MODEL] + Config.FALLBACK_MODELS
        
        if st.button("Testar Todos os Modelos Candidatos"):
            if not gemini_service.is_configured():
                st.error("Chave da API não configurada.")
            else:
                for mod in models_to_test:
                    with st.spinner(f"Testando {mod}..."):
                        import time
                        t0 = time.time()
                        try:
                            resp = gemini_service.client.models.generate_content(
                                model=mod,
                                contents="Responda em uma palavra: 'OK'"
                            )
                            lat = time.time() - t0
                            st.success(f"✅ **{mod}**: Operacional ({lat:.2f}s) - Resposta: '{resp.text.strip()}'")
                        except Exception as e:
                            st.error(f"❌ **{mod}**: Indisponível ou Erro: {e}")

    with tab_t3:
        st.markdown("##### Matriz de Consistência e Limitações Metodológicas")
        st.markdown("""
        <div class="transparency-callout" style="margin-top: 0;">
            <b>Critérios de Confiabilidade Fitossanitária:</b><br>
            • Um modelo de Teachable Machine treinado apenas em fotos de laboratório pode apresentar perda de acurácia em condições reais de iluminação ou com câmeras de smartphones.<br>
            • O PlantCare AI utiliza o Google Gemini como árbitro botânico: quando a confiança do Teachable Machine estiver abaixo do limiar (65%) ou houver ambiguidade entre classes, o Gemini é instruído a não assumir a hipótese local como verdade.
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("**Limiares de Incerteza Configuráveis no Sistema:**")
        st.write(f"- Limiar Mínimo de Confiança Local: `{Config.TM_CONFIDENCE_THRESHOLD * 100}%`")
        st.write(f"- Margem Mínima entre Top 1 e Top 2: `{Config.TM_AMBIGUITY_MARGIN * 100}%`")

# ==========================================
# PÁGINA 5: CONFIGURAÇÕES & API
# ==========================================
elif page == "⚙️ Configurações & API":
    render_hero(
        title="Configurações & Integrações",
        subtitle="Gerenciamento de credenciais da API Gemini, diretórios de modelos e parâmetros do sistema."
    )

    st.markdown("##### 1. Chave de API do Google Gemini")
    st.caption("A chave deve ser mantida em segredo. Ela é carregada automaticamente a partir do arquivo `.env`.")

    current_key_display = Config.GEMINI_API_KEY[:8] + "..." + Config.GEMINI_API_KEY[-4:] if len(Config.GEMINI_API_KEY) > 12 else ("Configurada" if Config.GEMINI_API_KEY else "Não configurada")
    st.info(f"🔑 Chave atual ativa no backend: **{current_key_display}**")

    new_api_key = st.text_input("Atualizar Chave da API Gemini:", type="password", placeholder="Cole sua nova API Key aqui")
    if st.button("Salvar Nova Chave de API"):
        if new_api_key:
            gemini_service.set_api_key(new_api_key)
            st.success("Chave atualizada na sessão atual!")
            st.rerun()

    st.markdown("---")
    st.markdown("##### 2. Seleção de Modelos Gemini")
    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        st.write(f"**Modelo Primário Ativo:** `{Config.PRIMARY_GEMINI_MODEL}`")
    with col_cfg2:
        st.write(f"**Modelos de Redundância (Fallback):** `{', '.join(Config.FALLBACK_MODELS)}`")

    st.markdown("---")
    st.markdown("##### 3. Modelo do Google Teachable Machine")
    st.write(f"**Diretório de Carga:** `{os.path.abspath(Config.TM_MODEL_PATH)}`")
    if st.button("🔄 Recarregar Modelo Teachable Machine"):
        tm_service.load_model()
        if tm_service.is_loaded:
            st.success(f"Modelo recarregado com sucesso! Classes: {', '.join(tm_service.labels)}")
        else:
            st.error(f"Erro ao carregar modelo: {tm_service.load_error}")
