"""
ORCA INTERIORES SAAS - Aplicação Principal
Sistema completo de orçamento para marcenaria
Versão: 2.0 - Com visualização individual de móveis
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List
import plotly.express as px
import plotly.graph_objects as go

# Importar módulos do sistema
from auth_manager import AuthManager
from file_analyzer import FileAnalyzer
from orcamento_engine import OrcamentoEngine
from config import Config

# Configuração da página
st.set_page_config(
    page_title="Orca Interiores SaaS",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para interface Apple-level
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .component-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #28a745;
    }
    
    .plan-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem;
    }
    
    .plan-popular {
        border: 2px solid #667eea;
        transform: scale(1.05);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
        margin: 1rem 0;
    }
    
    .mobile-view {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .visualization-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Função principal da aplicação"""
    
    # Inicializar componentes
    auth_manager = AuthManager()
    file_analyzer = FileAnalyzer()
    orcamento_engine = OrcamentoEngine()
    
    # Verificar autenticação
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = False
    
    if not st.session_state.usuario_logado:
        mostrar_tela_login(auth_manager)
    else:
        usuario = st.session_state.usuario_atual
        mostrar_aplicacao_principal(file_analyzer, orcamento_engine, usuario)

def mostrar_tela_login(auth_manager: AuthManager):
    """Tela de login e registro"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🏠 Orca Interiores SaaS</h1>
        <h3>Sistema Inteligente de Orçamento para Marcenaria</h3>
        <p>Transforme seus projetos 3D em orçamentos precisos em segundos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Informações dos planos
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="plan-card">
            <h4>💎 Gratuito</h4>
            <h2>R$ 0</h2>
            <p>3 projetos/mês</p>
            <ul style="text-align: left;">
                <li>Upload básico</li>
                <li>Orçamento simples</li>
                <li>Suporte email</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="plan-card">
            <h4>🚀 Básico</h4>
            <h2>R$ 49,90</h2>
            <p>50 projetos/mês</p>
            <ul style="text-align: left;">
                <li>Visualização 3D</li>
                <li>Preços atualizados</li>
                <li>Relatórios PDF</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="plan-card plan-popular">
            <h4>⭐ Profissional</h4>
            <h2>R$ 99,90</h2>
            <p>200 projetos/mês</p>
            <ul style="text-align: left;">
                <li>API integração</li>
                <li>White label</li>
                <li>Suporte prioritário</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="plan-card">
            <h4>🏢 Empresarial</h4>
            <h2>R$ 299,90</h2>
            <p>Projetos ilimitados</p>
            <ul style="text-align: left;">
                <li>Multi-usuários</li>
                <li>Dashboard avançado</li>
                <li>Consultoria inclusa</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Área de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Acesso ao Sistema")
        
        tab1, tab2 = st.tabs(["Login", "Registro"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("📧 Email")
                senha = st.text_input("🔒 Senha", type="password")
                submitted = st.form_submit_button("Entrar", use_container_width=True)
                
                if submitted:
                    usuario = auth_manager.fazer_login(email, senha)
                    if usuario:
                        st.session_state.usuario_logado = True
                        st.session_state.usuario_atual = usuario
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Email ou senha incorretos!")
        
        with tab2:
            with st.form("registro_form"):
                nome = st.text_input("👤 Nome completo")
                email = st.text_input("📧 Email")
                senha = st.text_input("🔒 Senha", type="password")
                plano = st.selectbox("📋 Plano", ["gratuito", "basico", "profissional", "empresarial"])
                submitted = st.form_submit_button("Criar Conta", use_container_width=True)
                
                if submitted:
                    if auth_manager.criar_usuario(nome, email, senha, plano):
                        st.success("Conta criada com sucesso! Faça login.")
                    else:
                        st.error("Erro ao criar conta. Email já existe.")
    
    # Contas demo
    st.markdown("---")
    st.markdown("### 🎯 Contas Demo para Teste")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Demo Básico**\n\n📧 demo@orcainteriores.com\n🔒 demo123")
    
    with col2:
        st.info("**Arquiteto**\n\n📧 arquiteto@teste.com\n🔒 arq123")
    
    with col3:
        st.info("**Marceneiro**\n\n📧 marceneiro@teste.com\n🔒 marc123")

def mostrar_aplicacao_principal(file_analyzer: FileAnalyzer, orcamento_engine: OrcamentoEngine, usuario: Dict):
    """Interface principal da aplicação"""
    
    # Sidebar com informações do usuário
    with st.sidebar:
        st.markdown(f"### 👤 {usuario['nome']}")
        st.markdown(f"**Plano:** {usuario['plano'].title()}")
        st.markdown(f"**Projetos este mês:** {usuario['projetos_mes']}")
        
        # Limites por plano
        limites = {
            'gratuito': 3,
            'basico': 50,
            'profissional': 200,
            'empresarial': 999999
        }
        
        limite = limites.get(usuario['plano'], 3)
        if limite < 999999:
            progresso = usuario['projetos_mes'] / limite
            st.progress(progresso)
            st.caption(f"{usuario['projetos_mes']}/{limite} projetos utilizados")
        
        st.markdown("---")
        
        # Configurações de orçamento
        st.markdown("### ⚙️ Configurações")
        
        material = st.selectbox(
            "Material",
            ["mdf_15mm", "mdf_18mm", "compensado_15mm", "compensado_18mm", "melamina_15mm", "melamina_18mm"],
            format_func=lambda x: {
                "mdf_15mm": "MDF 15mm - R$ 69,15/m²",
                "mdf_18mm": "MDF 18mm - R$ 79,50/m²",
                "compensado_15mm": "Compensado 15mm - R$ 64,00/m²",
                "compensado_18mm": "Compensado 18mm - R$ 72,80/m²",
                "melamina_15mm": "Melamina 15mm - R$ 89,50/m²",
                "melamina_18mm": "Melamina 18mm - R$ 98,20/m²"
            }[x]
        )
        
        qualidade_acessorios = st.selectbox(
            "Qualidade dos Acessórios",
            ["comum", "premium"],
            format_func=lambda x: "Comum" if x == "comum" else "Premium"
        )
        
        complexidade = st.selectbox(
            "Complexidade do Projeto",
            ["simples", "media", "complexa", "premium"],
            format_func=lambda x: {
                "simples": "Simples (1.0x)",
                "media": "Média (1.2x)",
                "complexa": "Complexa (1.5x)",
                "premium": "Premium (2.0x)"
            }[x]
        )
        
        margem_lucro = st.slider("Margem de Lucro (%)", 10, 50, 30)
        
        st.markdown("---")
        st.markdown("### 📊 Preços Léo Madeiras")
        st.caption("Atualizado em 30/06/2025")
        st.markdown("[🔗 Visitar site](https://www.leomadeiras.com.br/)")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.usuario_logado = False
            st.session_state.usuario_atual = None
            st.rerun()
    
    # Área principal
    st.markdown(f"# 🏠 Orca Interiores - {usuario['nome']}")
    
    # Upload de arquivo
    st.markdown("### 📁 Upload do Projeto 3D")
    
    uploaded_file = st.file_uploader(
        "Arraste seu arquivo 3D aqui ou clique para selecionar",
        type=['obj', 'dae', 'stl', 'ply'],
        help="Formatos suportados: OBJ, DAE, STL, PLY (até 500MB)"
    )
    
    if uploaded_file is not None:
        # Verificar limite de projetos
        limite = limites.get(usuario['plano'], 3)
        if usuario['projetos_mes'] >= limite and limite < 999999:
            st.error(f"Limite de {limite} projetos/mês atingido! Faça upgrade do seu plano.")
            return
        
        # Processar arquivo
        with st.spinner("Analisando arquivo 3D..."):
            analise = file_analyzer.analisar_arquivo_3d(uploaded_file)
            
            if analise:
                st.session_state.analise = analise
                st.success("Arquivo analisado com sucesso!")
                
                # Configurações do orçamento
                configuracoes = {
                    'material': material,
                    'qualidade_acessorios': qualidade_acessorios,
                    'complexidade': complexidade,
                    'margem_lucro': margem_lucro
                }
                
                # Calcular orçamento
                orcamento = orcamento_engine.calcular_orcamento_completo(analise, configuracoes)
                
                if orcamento:
                    st.session_state.orcamento = orcamento
                    mostrar_resultados(analise, orcamento, file_analyzer, orcamento_engine)
                else:
                    st.error("Erro ao calcular orçamento.")
            else:
                st.error("Erro ao analisar arquivo. Verifique o formato.")

def mostrar_resultados(analise: Dict, orcamento: Dict, file_analyzer: FileAnalyzer, orcamento_engine: OrcamentoEngine):
    """Mostra os resultados do orçamento"""
    
    # Tabs para organizar informações
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Resumo", "🔧 Componentes", "📈 Gráficos", "📋 Relatório", "🎯 Visualização 3D"])
    
    with tab1:
        mostrar_resumo(orcamento)
    
    with tab2:
        mostrar_componentes(orcamento, file_analyzer)
    
    with tab3:
        mostrar_graficos(orcamento, orcamento_engine)
    
    with tab4:
        mostrar_relatorio(orcamento, orcamento_engine)
    
    with tab5:
        mostrar_visualizacao_3d(analise, orcamento)

def mostrar_resumo(orcamento: Dict):
    """Mostra resumo do orçamento"""
    
    resumo = orcamento.get('resumo', {})
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Valor Final",
            f"R$ {resumo.get('valor_final', 0):,.2f}",
            delta=f"R$ {resumo.get('valor_lucro', 0):,.2f} lucro"
        )
    
    with col2:
        st.metric(
            "📐 Área Total",
            f"{resumo.get('area_total_m2', 0)} m²",
            delta=f"R$ {resumo.get('preco_por_m2', 0):,.2f}/m²"
        )
    
    with col3:
        st.metric(
            "🔧 Componentes",
            resumo.get('quantidade_componentes', 0),
            delta="peças identificadas"
        )
    
    with col4:
        st.metric(
            "📈 Margem",
            f"{resumo.get('margem_lucro_pct', 0)}%",
            delta=f"R$ {resumo.get('valor_lucro', 0):,.2f}"
        )
    
    # Breakdown de custos
    st.markdown("### 💸 Breakdown de Custos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📦 Material</h4>
            <h3>R$ {:.2f}</h3>
            <p>Custo das chapas e materiais</p>
        </div>
        """.format(resumo.get('custo_material', 0)), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h4>⚙️ Acessórios</h4>
            <h3>R$ {:.2f}</h3>
            <p>Dobradiças, puxadores, corrediças</p>
        </div>
        """.format(resumo.get('custo_acessorios', 0)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>✂️ Corte/Usinagem</h4>
            <h3>R$ {:.2f}</h3>
            <p>Mão de obra de corte e furação</p>
        </div>
        """.format(resumo.get('custo_corte', 0)), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h4>💰 Lucro</h4>
            <h3>R$ {:.2f}</h3>
            <p>Margem de {}%</p>
        </div>
        """.format(resumo.get('valor_lucro', 0), resumo.get('margem_lucro_pct', 0)), unsafe_allow_html=True)

def mostrar_componentes(orcamento: Dict, file_analyzer: FileAnalyzer):
    """Mostra detalhes dos componentes com visualização individual"""
    
    componentes = orcamento.get('componentes', [])
    
    st.markdown("### 🔧 Detalhamento por Componente")
    
    for i, comp in enumerate(componentes):
        with st.expander(f"📦 {comp.get('nome', f'Componente {i+1}')} - R$ {comp.get('custo_total', 0):,.2f}"):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Informações do componente
                st.markdown(f"""
                **Tipo:** {comp.get('tipo', 'N/A').title()}  
                **Área:** {comp.get('area_m2', 0)} m²  
                **Preço/m²:** R$ {comp.get('preco_por_m2', 0):,.2f}
                """)
                
                # Breakdown de custos
                st.markdown("**Breakdown de Custos:**")
                st.write(f"• Material: R$ {comp.get('custo_material', 0):,.2f}")
                st.write(f"• Acessórios: R$ {comp.get('custo_acessorios', 0):,.2f}")
                st.write(f"• Corte: R$ {comp.get('custo_corte', 0):,.2f}")
                st.write(f"• Multiplicador: {comp.get('multiplicador_complexidade', 1.0)}x")
                
                # Gráfico individual do componente
                custos_comp = [
                    comp.get('custo_material', 0),
                    comp.get('custo_acessorios', 0),
                    comp.get('custo_corte', 0)
                ]
                labels_comp = ['Material', 'Acessórios', 'Corte']
                
                fig_comp = px.pie(
                    values=custos_comp,
                    names=labels_comp,
                    title=f"Custos - {comp.get('nome', 'Componente')}",
                    color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
                )
                fig_comp.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_comp, use_container_width=True)
            
            with col2:
                # Visualização 3D individual do componente
                st.markdown("**Visualização 3D:**")
                
                # Gerar visualização 3D simplificada do componente
                try:
                    fig_3d = gerar_visualizacao_componente_individual(comp, i)
                    if fig_3d:
                        st.plotly_chart(fig_3d, use_container_width=True)
                    else:
                        st.info("Visualização 3D não disponível para este componente")
                except Exception as e:
                    st.warning("Erro ao gerar visualização 3D")

def gerar_visualizacao_componente_individual(componente: Dict, index: int) -> go.Figure:
    """Gera visualização 3D individual de um componente"""
    
    try:
        # Simular dados 3D baseados nas dimensões do componente
        area = componente.get('area_m2', 1.0)
        
        # Estimar dimensões baseadas na área (assumindo formato retangular)
        largura = (area ** 0.5) * 1.2
        altura = (area ** 0.5) * 0.8
        profundidade = 0.02  # 2cm de espessura padrão
        
        # Criar pontos do cubo/paralelepípedo
        x = [0, largura, largura, 0, 0, largura, largura, 0]
        y = [0, 0, altura, altura, 0, 0, altura, altura]
        z = [0, 0, 0, 0, profundidade, profundidade, profundidade, profundidade]
        
        # Definir as faces do cubo
        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
        
        # Cores baseadas no tipo de componente
        cores_tipo = {
            'armario': '#8B4513',    # Marrom
            'gaveta': '#CD853F',     # Peru
            'porta': '#A0522D',      # Sienna
            'prateleira': '#DEB887'  # BurlyWood
        }
        
        cor = cores_tipo.get(componente.get('tipo', 'armario'), '#8B4513')
        
        # Criar figura 3D
        fig = go.Figure(data=[
            go.Mesh3d(
                x=x, y=y, z=z,
                i=i, j=j, k=k,
                color=cor,
                opacity=0.8,
                name=componente.get('nome', f'Componente {index+1}')
            )
        ])
        
        # Configurar layout
        fig.update_layout(
            title=f"{componente.get('nome', f'Componente {index+1}')}",
            scene=dict(
                xaxis_title="Largura (m)",
                yaxis_title="Altura (m)",
                zaxis_title="Espessura (m)",
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            width=400,
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        return fig
        
    except Exception as e:
        return None

def mostrar_graficos(orcamento: Dict, orcamento_engine: OrcamentoEngine):
    """Mostra gráficos do orçamento"""
    
    graficos = orcamento_engine.gerar_graficos(orcamento)
    
    if graficos['pizza']:
        st.plotly_chart(graficos['pizza'], use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if graficos['barras']:
            st.plotly_chart(graficos['barras'], use_container_width=True)
    
    with col2:
        if graficos['area']:
            st.plotly_chart(graficos['area'], use_container_width=True)

def mostrar_relatorio(orcamento: Dict, orcamento_engine: OrcamentoEngine):
    """Mostra relatório detalhado"""
    
    st.markdown("### 📋 Relatório Detalhado")
    
    relatorio = orcamento_engine.gerar_relatorio_detalhado(
        orcamento, 
        "Cliente Demo", 
        "Ambiente Demo"
    )
    
    st.markdown(relatorio)
    
    # Botão para exportar JSON
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Exportar JSON", use_container_width=True):
            json_data = orcamento_engine.exportar_json(orcamento)
            st.download_button(
                label="💾 Baixar JSON",
                data=json_data,
                file_name=f"orcamento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col2:
        if st.button("📄 Gerar PDF", use_container_width=True):
            st.info("Funcionalidade de PDF será implementada em breve!")

def mostrar_visualizacao_3d(analise: Dict, orcamento: Dict):
    """Mostra visualização 3D completa do projeto"""
    
    st.markdown("### 🎯 Visualização 3D Completa")
    
    try:
        # Gerar visualização 3D de todos os componentes
        componentes = orcamento.get('componentes', [])
        
        if componentes:
            fig = go.Figure()
            
            cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
            
            for i, comp in enumerate(componentes):
                # Simular posição de cada componente
                offset_x = (i % 3) * 2
                offset_y = (i // 3) * 2
                
                area = comp.get('area_m2', 1.0)
                largura = (area ** 0.5) * 1.2
                altura = (area ** 0.5) * 0.8
                profundidade = 0.02
                
                # Pontos do componente com offset
                x = [offset_x, offset_x + largura, offset_x + largura, offset_x, 
                     offset_x, offset_x + largura, offset_x + largura, offset_x]
                y = [offset_y, offset_y, offset_y + altura, offset_y + altura,
                     offset_y, offset_y, offset_y + altura, offset_y + altura]
                z = [0, 0, 0, 0, profundidade, profundidade, profundidade, profundidade]
                
                # Faces do cubo
                i_faces = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
                j_faces = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
                k_faces = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
                
                fig.add_trace(go.Mesh3d(
                    x=x, y=y, z=z,
                    i=i_faces, j=j_faces, k=k_faces,
                    color=cores[i % len(cores)],
                    opacity=0.7,
                    name=comp.get('nome', f'Componente {i+1}'),
                    showlegend=True
                ))
            
            # Configurar layout
            fig.update_layout(
                title="Visualização 3D - Todos os Componentes",
                scene=dict(
                    xaxis_title="X (m)",
                    yaxis_title="Y (m)",
                    zaxis_title="Z (m)",
                    camera=dict(
                        eye=dict(x=2, y=2, z=1.5)
                    )
                ),
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Informações adicionais
            st.markdown("### 📊 Informações do Projeto")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Componentes", len(componentes))
            
            with col2:
                area_total = sum(comp.get('area_m2', 0) for comp in componentes)
                st.metric("Área Total", f"{area_total:.2f} m²")
            
            with col3:
                valor_total = orcamento.get('resumo', {}).get('valor_final', 0)
                st.metric("Valor Total", f"R$ {valor_total:,.2f}")
        
        else:
            st.warning("Nenhum componente encontrado para visualização.")
            
    except Exception as e:
        st.error(f"Erro ao gerar visualização 3D: {str(e)}")
        st.info("Tente fazer upload de um arquivo 3D válido.")

if __name__ == "__main__":
    main()

