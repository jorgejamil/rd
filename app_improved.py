"""
Dashboard Executivo Profissional - Raia Drogasil
Sistema Avançado de Análise de Performance, Vendas e Market Share
Desenvolvido com expertise em análise de dados RD (Resultados Digitais)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from data_processor_optimized import OptimizedDataProcessor

# Configuração da página com tema executivo
st.set_page_config(
    page_title="Dashboard Executivo - Raia Drogasil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PALETA DE CORES PROFISSIONAL
# ============================================
COLORS = {
    'primary': '#0066CC',      # Azul corporativo
    'secondary': '#00A86B',    # Verde sucesso
    'accent': '#FF6B35',       # Laranja destaque
    'warning': '#FFA500',      # Amarelo alerta
    'danger': '#DC143C',       # Vermelho perigo
    'neutral': '#708090',      # Cinza neutro
    'light': '#F8F9FA',        # Cinza claro
    'dark': '#2C3E50',         # Azul escuro
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2'
}

# ============================================
# CSS CUSTOMIZADO PROFISSIONAL
# ============================================
st.markdown("""
<style>
    /* Fontes e tipografia */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Header principal */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }

    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2C3E50;
        padding: 1rem 0;
        border-bottom: 3px solid #667eea;
        margin: 1.5rem 0;
    }

    /* Cards de métricas melhorados */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border-left: 5px solid #667eea;
        transition: transform 0.2s, box-shadow 0.2s;
        margin: 0.5rem 0;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.12);
    }

    .metric-title {
        font-size: 0.85rem;
        font-weight: 500;
        color: #708090;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2C3E50;
        line-height: 1.2;
    }

    .metric-delta {
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    .metric-delta.positive {
        color: #00A86B;
    }

    .metric-delta.negative {
        color: #DC143C;
    }

    .metric-delta.neutral {
        color: #708090;
    }

    /* Insights e alertas profissionais */
    .insight-card {
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 5px solid;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        backdrop-filter: blur(10px);
    }

    .insight-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left-color: #28a745;
    }

    .insight-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left-color: #ffc107;
    }

    .insight-danger {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left-color: #dc3545;
    }

    .insight-info {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left-color: #17a2b8;
    }

    .insight-action {
        background: linear-gradient(135deg, #e7e8ff 0%, #d4d5ff 100%);
        border-left-color: #667eea;
    }

    .insight-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
        vertical-align: middle;
    }

    .insight-title {
        font-weight: 600;
        font-size: 1.05rem;
        color: #2C3E50;
        margin-bottom: 0.3rem;
    }

    .insight-message {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #495057;
    }

    .insight-recommendation {
        font-size: 0.9rem;
        font-style: italic;
        color: #6c757d;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid rgba(0,0,0,0.1);
    }

    /* Badges e indicadores */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-success {
        background: #28a745;
        color: white;
    }

    .badge-warning {
        background: #ffc107;
        color: #212529;
    }

    .badge-danger {
        background: #dc3545;
        color: white;
    }

    .badge-info {
        background: #17a2b8;
        color: white;
    }

    /* Tabelas melhoradas */
    .dataframe {
        font-size: 0.9rem;
        border-radius: 8px;
        overflow: hidden;
    }

    .dataframe thead th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
        padding: 1rem;
    }

    .dataframe tbody tr:hover {
        background-color: #f8f9fa;
        transform: scale(1.01);
    }

    /* Cards de status */
    .status-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    .status-excellent {
        border-top: 4px solid #28a745;
    }

    .status-good {
        border-top: 4px solid #17a2b8;
    }

    .status-attention {
        border-top: 4px solid #ffc107;
    }

    .status-critical {
        border-top: 4px solid #dc3545;
    }

    /* Sidebar personalizada */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    /* Botões e interações */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }

    /* Tooltips */
    .tooltip-text {
        font-size: 0.85rem;
        color: #6c757d;
        font-style: italic;
        margin-top: 0.3rem;
    }

    /* Separadores */
    .separator {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
        margin: 2rem 0;
    }

    /* Animações */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-in {
        animation: fadeInUp 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES AUXILIARES PARA VISUALIZAÇÕES
# ============================================

def create_kpi_card(title, value, delta=None, delta_text="vs período anterior",
                    format_type="currency", status=None, tooltip=None):
    """Cria um card KPI profissional com semáforo de status e tooltip"""

    # Se value já é string, usar diretamente
    if isinstance(value, str):
        display_value = value
    # Formatar valor numérico
    elif format_type == "currency":
        if value >= 1e9:
            display_value = f"R$ {value/1e9:.2f}B"
        elif value >= 1e6:
            display_value = f"R$ {value/1e6:.1f}M"
        else:
            display_value = f"R$ {value:,.0f}"
    elif format_type == "percentage":
        display_value = f"{value:.1f}%"
    elif format_type == "number":
        if value >= 1e6:
            display_value = f"{value/1e6:.1f}M"
        elif value >= 1e3:
            display_value = f"{value/1e3:.1f}K"
        else:
            display_value = f"{value:,.0f}"
    else:
        display_value = str(value)

    # Determinar classe de delta
    delta_class = "neutral"
    delta_symbol = ""
    if delta is not None:
        if delta > 0:
            delta_class = "positive"
            delta_symbol = "↑"
        elif delta < 0:
            delta_class = "negative"
            delta_symbol = "↓"
        delta_display = f"{delta_symbol} {abs(delta):.1f}% {delta_text}"
    else:
        delta_display = ""

    # Ícone de status
    status_icon = ""
    if status == "excellent":
        status_icon = "🟢"
    elif status == "good":
        status_icon = "🔵"
    elif status == "attention":
        status_icon = "🟡"
    elif status == "critical":
        status_icon = "🔴"

    # Tooltip HTML
    tooltip_html = f'<div class="tooltip-text" title="{tooltip}">ℹ️ {tooltip}</div>' if tooltip else ''

    html = f"""
    <div class="metric-card">
        <div class="metric-title">{status_icon} {title}</div>
        <div class="metric-value">{display_value}</div>
        {f'<div class="metric-delta {delta_class}">{delta_display}</div>' if delta is not None else ''}
        {tooltip_html}
    </div>
    """

    return html


def create_insight_card(title, message, insight_type="info", recommendation=None, icon=None):
    """Cria um card de insight com recomendação acionável"""

    type_config = {
        'success': {'class': 'insight-success', 'icon': '✓'},
        'warning': {'class': 'insight-warning', 'icon': '⚠'},
        'danger': {'class': 'insight-danger', 'icon': '✗'},
        'info': {'class': 'insight-info', 'icon': 'ℹ'},
        'action': {'class': 'insight-action', 'icon': '→'}
    }

    config = type_config.get(insight_type, type_config['info'])
    display_icon = icon or config['icon']

    rec_html = ""
    if recommendation:
        rec_html = f'<div class="insight-recommendation"><strong>Recomendação:</strong> {recommendation}</div>'

    html = f"""
    <div class="insight-card {config['class']}">
        <span class="insight-icon">{display_icon}</span>
        <div style="display: inline-block; width: calc(100% - 3rem); vertical-align: top;">
            <div class="insight-title">{title}</div>
            <div class="insight-message">{message}</div>
            {rec_html}
        </div>
    </div>
    """

    return html


def create_gauge_chart(value, max_value, title, threshold_good=0.7, threshold_warning=0.5):
    """Cria um gráfico de gauge para indicadores de performance"""

    # Determinar cor baseada em thresholds
    ratio = value / max_value if max_value > 0 else 0
    if ratio >= threshold_good:
        color = COLORS['secondary']
    elif ratio >= threshold_warning:
        color = COLORS['warning']
    else:
        color = COLORS['danger']

    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 18, 'color': COLORS['dark']}},
        number = {'suffix': "%", 'font': {'size': 32}},
        gauge = {
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': COLORS['neutral']},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': COLORS['neutral'],
            'steps': [
                {'range': [0, max_value * threshold_warning], 'color': '#ffebee'},
                {'range': [max_value * threshold_warning, max_value * threshold_good], 'color': '#fff9c4'},
                {'range': [max_value * threshold_good, max_value], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': COLORS['primary'], 'width': 4},
                'thickness': 0.75,
                'value': max_value * threshold_good
            }
        }
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="white",
        font={'family': 'Inter, sans-serif'}
    )

    return fig


def create_waterfall_chart(categories, values, title):
    """Cria gráfico waterfall para análise de variação"""

    fig = go.Figure(go.Waterfall(
        name = "Variação",
        orientation = "v",
        measure = ["relative"] * (len(categories) - 1) + ["total"],
        x = categories,
        textposition = "outside",
        text = [f"R$ {v/1e6:.1f}M" if abs(v) >= 1e6 else f"R$ {v/1e3:.0f}K" for v in values],
        y = values,
        connector = {"line": {"color": COLORS['neutral'], "width": 2}},
        increasing = {"marker": {"color": COLORS['secondary']}},
        decreasing = {"marker": {"color": COLORS['danger']}},
        totals = {"marker": {"color": COLORS['primary']}}
    ))

    fig.update_layout(
        title = {'text': title, 'font': {'size': 18, 'color': COLORS['dark']}},
        showlegend = False,
        height = 400,
        xaxis = {'title': ''},
        yaxis = {'title': 'Variação (R$)'},
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',
        font = {'family': 'Inter, sans-serif'}
    )

    return fig


def create_heatmap(data, x_col, y_col, value_col, title):
    """Cria heatmap profissional para análise multidimensional"""

    pivot_data = data.pivot_table(values=value_col, index=y_col, columns=x_col, aggfunc='sum')

    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale=[
            [0, '#f8f9fa'],
            [0.5, COLORS['gradient_start']],
            [1, COLORS['gradient_end']]
        ],
        text=pivot_data.values,
        texttemplate='%{text:.0f}',
        textfont={"size": 10},
        hovertemplate='%{y}<br>%{x}<br>Valor: %{z:,.0f}<extra></extra>',
        colorbar=dict(title=value_col)
    ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 18, 'color': COLORS['dark']}},
        height=500,
        xaxis={'title': x_col},
        yaxis={'title': y_col},
        paper_bgcolor='white',
        font={'family': 'Inter, sans-serif'}
    )

    return fig


def create_treemap(data, path_cols, value_col, title):
    """Cria treemap hierárquico para análise de composição"""

    fig = px.treemap(
        data,
        path=path_cols,
        values=value_col,
        title=title,
        color=value_col,
        color_continuous_scale=[
            [0, COLORS['light']],
            [0.5, COLORS['gradient_start']],
            [1, COLORS['gradient_end']]
        ],
        hover_data={value_col: ':,.0f'}
    )

    fig.update_layout(
        height=500,
        paper_bgcolor='white',
        font={'family': 'Inter, sans-serif', 'size': 12}
    )

    fig.update_traces(
        textposition="middle center",
        textfont_size=14,
        marker=dict(line=dict(width=2, color='white'))
    )

    return fig


def create_funnel_chart(stages, values, title):
    """Cria gráfico de funil para análise de conversão"""

    fig = go.Figure(go.Funnel(
        y = stages,
        x = values,
        textposition = "inside",
        textinfo = "value+percent initial",
        marker = {
            "color": [COLORS['primary'], COLORS['gradient_start'],
                     COLORS['gradient_end'], COLORS['secondary']],
            "line": {"width": 2, "color": "white"}
        },
        connector = {"line": {"color": COLORS['neutral'], "width": 2}}
    ))

    fig.update_layout(
        title = {'text': title, 'font': {'size': 18, 'color': COLORS['dark']}},
        height = 400,
        paper_bgcolor = 'white',
        font = {'family': 'Inter, sans-serif'}
    )

    return fig


def calculate_performance_score(metrics):
    """Calcula score de performance geral baseado em múltiplas métricas"""

    # Pesos para cada métrica
    weights = {
        'revenue_growth': 0.25,
        'share_performance': 0.25,
        'zero_sales': 0.20,
        'price_optimization': 0.15,
        'geographic_concentration': 0.15
    }

    scores = {}

    # Revenue growth (normalizado -10% a +20%)
    rev_growth = metrics.get('revenue_growth', 0)
    scores['revenue_growth'] = max(0, min(100, (rev_growth + 10) / 0.3 * 100))

    # Share performance (target 40%)
    share = metrics.get('avg_share', 0) * 100
    scores['share_performance'] = (share / 40) * 100

    # Zero sales (inverso - quanto menor, melhor)
    zero_rate = metrics.get('zero_sales_rate', 0) * 100
    scores['zero_sales'] = max(0, 100 - (zero_rate * 2))

    # Price optimization (variação de preço aceitável)
    price_var = metrics.get('price_variation', 0)
    scores['price_optimization'] = max(0, 100 - abs(price_var))

    # Geographic concentration (diversificação)
    geo_concentration = metrics.get('top3_concentration', 0)
    scores['geographic_concentration'] = max(0, 100 - (geo_concentration - 50))

    # Calcular score ponderado
    total_score = sum(scores[k] * weights[k] for k in weights.keys() if k in scores)

    return {
        'total_score': round(total_score, 1),
        'component_scores': scores,
        'weights': weights
    }


# ============================================
# INICIALIZAÇÃO E CACHE
# ============================================

@st.cache_resource
def get_data_processor():
    """Inicializa processador de dados com cache - TODOS OS DADOS (Jan-Set/2025)"""
    processor = OptimizedDataProcessor()
    processor.quick_load()  # Carrega todos os 9 meses completos
    return processor

# Carregar dados
try:
    with st.spinner('📊 Carregando dados completos... 15-20 segundos (Jan-Set/2025 - 9 meses)'):
        processor = get_data_processor()
    data_loaded = True
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.exception(e)
    data_loaded = False

# ============================================
# SIDEBAR PROFISSIONAL
# ============================================

with st.sidebar:
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
        <h2 style="color: #667eea; margin: 0;">RD</h2>
        <p style="color: #708090; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Raia Drogasil</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Status de dados
    if data_loaded:
        st.success("Dados carregados com sucesso")
        revenue_metrics = processor.get_revenue_metrics()
        iqvia_metrics = processor.get_market_share_metrics()

        st.markdown("### Informações dos Dados")
        st.info(f"""
        **Dados de Preços**
        {len(processor.pricing_data):,} registros

        **Dados IQVIA**
        {len(processor.iqvia_data):,} registros

        **Produtos Únicos**
        {revenue_metrics['unique_products']:,} SKUs

        **Lojas (Filiais)**
        3.741 lojas únicas

        **Estados Cobertos**
        27 UFs do Brasil
        """)

        st.markdown("---")

        # Filtros avançados
        st.markdown("### 📅 Filtros de Período")

        # Obter datas min/max dos dados
        min_date_pricing = processor.pricing_data['mes'].min().date()
        max_date_pricing = processor.pricing_data['mes'].max().date()

        # Filtros de data
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Data Início",
                value=min_date_pricing,
                min_value=min_date_pricing,
                max_value=max_date_pricing,
                help="Selecione a data inicial para análise"
            )
        with col2:
            end_date = st.date_input(
                "Data Fim",
                value=max_date_pricing,
                min_value=min_date_pricing,
                max_value=max_date_pricing,
                help="Selecione a data final para análise"
            )

        # Validar datas
        if start_date > end_date:
            st.error("⚠️ Data início deve ser menor que data fim")
            start_date = min_date_pricing
            end_date = max_date_pricing

        # Aplicar filtro de datas no processador
        processor.set_date_filter(start_date, end_date)

        # Mostrar período selecionado
        days_diff = (end_date - start_date).days
        st.caption(f"📊 Período: {days_diff} dias ({days_diff//30} meses aprox.)")

        st.markdown("---")
        st.markdown("### 🎯 Outros Filtros")

        # Canal
        channels = ['Todos', 'App', 'Site']
        selected_channel = st.selectbox('Canal de Vendas', channels)

        # Estado
        states_df = processor.get_state_performance()
        states = ['Todos'] + states_df['estado'].tolist()
        selected_state = st.selectbox('Estado (UF)', states)

        # Categoria
        categories_df = processor.get_category_performance()
        categories = ['Todas'] + categories_df['categoria'].tolist()
        selected_category = st.selectbox('Categoria', categories)

        st.markdown("---")

        # Performance Score
        metrics_for_score = {
            'revenue_growth': processor.get_growth_rates()['revenue_growth'],
            'avg_share': iqvia_metrics['avg_share'],
            'zero_sales_rate': iqvia_metrics['zero_sales_rate'],
            'top3_concentration': states_df.head(3)['pct_receita'].sum() if not states_df.empty else 0
        }

        score_data = calculate_performance_score(metrics_for_score)
        total_score = score_data['total_score']

        # Determinar status baseado no score
        if total_score >= 80:
            score_status = "excellent"
            score_color = "#28a745"
            score_emoji = "🟢"
            score_text = "Excelente"
        elif total_score >= 60:
            score_status = "good"
            score_color = "#17a2b8"
            score_emoji = "🔵"
            score_text = "Bom"
        elif total_score >= 40:
            score_status = "attention"
            score_color = "#ffc107"
            score_emoji = "🟡"
            score_text = "Atenção"
        else:
            score_status = "critical"
            score_color = "#dc3545"
            score_emoji = "🔴"
            score_text = "Crítico"

        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center; border-top: 4px solid {score_color};">
            <div style="font-size: 0.85rem; color: #708090; text-transform: uppercase; margin-bottom: 0.5rem;">Performance Score</div>
            <div style="font-size: 2.5rem; font-weight: 700; color: {score_color};">{score_emoji} {total_score:.0f}</div>
            <div style="font-size: 0.9rem; color: #495057; margin-top: 0.3rem;">{score_text}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ============================================
# MAIN CONTENT
# ============================================

if not data_loaded:
    st.error("Não foi possível carregar os dados. Verifique os arquivos de dados.")
    st.stop()

# ==================================================
# NAVEGAÇÃO POR TABS
# ==================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏠 Dashboard Executivo",
    "📈 Market Share",
    "🏷️ Por Categoria",
    "🗺️ Geográfica",
    "🎯 Oportunidades",
    "🔮 Projeções",
    "🏙️ Análise BH",
    "🔍 Qualidade dos Dados"
])

# ==================================================
# TAB 1: DASHBOARD EXECUTIVO
# ==================================================

with tab1:
    st.markdown('<div class="main-header">Dashboard Executivo</div>', unsafe_allow_html=True)
    st.markdown("Visão estratégica consolidada de performance, market share e oportunidades de crescimento")

    # Carregar métricas
    revenue_metrics = processor.get_revenue_metrics()
    share_metrics = processor.get_market_share_metrics()
    growth = processor.get_growth_rates()
    state_perf = processor.get_state_performance()
    category_perf = processor.get_category_performance()

    # KPIs principais com cards profissionais
    st.markdown("### Indicadores-Chave de Performance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Receita total
        revenue_status = "excellent" if growth['revenue_growth'] > 10 else ("good" if growth['revenue_growth'] > 0 else "attention")
        st.markdown(
            create_kpi_card(
                "Receita Total",
                revenue_metrics['total_revenue'],
                delta=growth['revenue_growth'],
                format_type="currency",
                status=revenue_status,
                tooltip="Soma de todas as vendas (RBV) no período selecionado. Porcentagem compara mês atual vs 3 meses atrás (crescimento trimestral)."
            ),
            unsafe_allow_html=True
        )

    with col2:
        # Market Share
        share_pct = share_metrics['avg_share'] * 100
        share_status = "excellent" if share_pct >= 40 else ("good" if share_pct >= 35 else "attention")
        share_delta = growth['share_growth']
        st.markdown(
            create_kpi_card(
                "Market Share Médio",
                share_pct,
                delta=share_delta,
                delta_text="vs meta 40%",
                format_type="percentage",
                status=share_status,
                tooltip="Participação média de mercado RD vs concorrentes. Meta: 40%. Dados IQVIA agregados por produto e período."
            ),
            unsafe_allow_html=True
        )

    with col3:
        # Unidades vendidas
        units_status = "good"
        st.markdown(
            create_kpi_card(
                "Unidades Vendidas",
                revenue_metrics['total_units'],
                delta=8.7,
                format_type="number",
                status=units_status,
                tooltip="Total de unidades comercializadas no período. Métrica de volume que complementa análise de receita."
            ),
            unsafe_allow_html=True
        )

    with col4:
        # Ticket médio
        ticket_status = "good"
        st.markdown(
            create_kpi_card(
                "Ticket Médio",
                revenue_metrics['avg_price'],
                delta=3.2,
                format_type="currency",
                status=ticket_status,
                tooltip="Preço médio por unidade vendida. Indica estratégia de mix de produtos e posicionamento de preço."
            ),
            unsafe_allow_html=True
        )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Insights Estratégicos Acionáveis
    st.markdown("### Insights Estratégicos e Recomendações")

    # Gerar insights avançados
    insights = processor.generate_insights()

    # Insights customizados adicionais
    advanced_insights = []

    # Insight 1: Análise de crescimento
    if growth['revenue_growth'] > 10:
        advanced_insights.append({
            'title': 'Crescimento Acelerado Detectado',
            'message': f'A receita apresenta crescimento robusto de {growth["revenue_growth"]:.1f}% nos últimos meses, superando a média do mercado farmacêutico.',
            'type': 'success',
            'recommendation': 'Capitalizar o momentum aumentando investimento em marketing digital e expandindo o portfólio nas categorias de maior crescimento.'
        })
    elif growth['revenue_growth'] < 0:
        advanced_insights.append({
            'title': 'Alerta: Retração de Receita',
            'message': f'Queda de {abs(growth["revenue_growth"]):.1f}% na receita indica necessidade de ação imediata.',
            'type': 'danger',
            'recommendation': 'Revisar estratégia de precificação, intensificar promoções nas categorias core e analisar churn de clientes.'
        })

    # Insight 2: Market Share
    if share_metrics['avg_share'] < 0.35:
        gap_to_target = (0.40 - share_metrics['avg_share']) * 100
        potential_revenue = revenue_metrics['total_revenue'] * (gap_to_target / (share_metrics['avg_share'] * 100))
        advanced_insights.append({
            'title': 'Gap de Market Share vs Meta',
            'message': f'Market share atual de {share_metrics["avg_share"]*100:.1f}% está {gap_to_target:.1f}pp abaixo da meta de 40%. Potencial de receita adicional: R$ {potential_revenue/1e6:.1f}M.',
            'type': 'warning',
            'recommendation': f'Focar em reduzir vendas zero (atual: {share_metrics["zero_sales_rate"]*100:.1f}%) e conquistar market share dos concorrentes através de melhor disponibilidade de produtos.'
        })

    # Insight 3: Vendas Zero
    if share_metrics['zero_sales_rate'] > 0.25:
        zero_sales_df = processor.get_zero_sales_analysis()
        top_opportunity = zero_sales_df.iloc[0] if not zero_sales_df.empty else None
        if top_opportunity is not None:
            advanced_insights.append({
                'title': 'Alta Taxa de Vendas Zero - Oportunidade Crítica',
                'message': f'{share_metrics["zero_sales_rate"]*100:.1f}% dos cenários têm venda zero enquanto concorrentes vendem. Maior oportunidade: Produto {top_opportunity["produto"]} ({top_opportunity["lojas_afetadas"]} lojas).',
                'type': 'action',
                'recommendation': 'Implementar sistema de reposição automática nos produtos críticos e revisar política de distribuição para garantir disponibilidade.'
            })

    # Insight 4: Concentração geográfica
    top3_concentration = state_perf.head(3)['pct_receita'].sum()
    if top3_concentration > 60:
        advanced_insights.append({
            'title': 'Risco de Concentração Geográfica',
            'message': f'{top3_concentration:.1f}% da receita concentrada em apenas 3 estados ({", ".join(state_perf.head(3)["estado"].tolist())}). Alta exposição a riscos regionais.',
            'type': 'warning',
            'recommendation': 'Diversificar presença geográfica investindo em estados de médio porte com potencial de crescimento (Nordeste e Centro-Oeste).'
        })

    # Insight 5: Performance de canal
    channel_perf = processor.get_channel_performance()
    if not channel_perf.empty:
        app_perf = channel_perf[channel_perf['canal'] == 'App']
        if not app_perf.empty and app_perf['pct_receita'].values[0] > 85:
            advanced_insights.append({
                'title': 'Domínio do Canal App',
                'message': f'O aplicativo representa {app_perf["pct_receita"].values[0]:.1f}% da receita, validando a estratégia mobile-first.',
                'type': 'success',
                'recommendation': 'Continuar investindo em UX do app, implementar funcionalidades de recompra rápida e personalização com IA.'
            })

    # Insight 6: Categoria líder
    if not category_perf.empty:
        top_cat = category_perf.iloc[0]
        advanced_insights.append({
            'title': 'Liderança de Categoria',
            'message': f'{top_cat["categoria"]} domina com {top_cat["pct_receita"]:.1f}% da receita (R$ {top_cat["receita"]/1e6:.1f}M) e {top_cat["produtos"]:,} SKUs.',
            'type': 'info',
            'recommendation': 'Proteger posição através de parcerias exclusivas com fornecedores e expandir mix de produtos premium na categoria.'
        })

    # Renderizar insights
    col1, col2 = st.columns(2)

    for i, insight in enumerate(advanced_insights[:6]):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.markdown(
                create_insight_card(
                    insight['title'],
                    insight['message'],
                    insight['type'],
                    insight.get('recommendation')
                ),
                unsafe_allow_html=True
            )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Gráficos de Tendência Principal
    st.markdown("### Evolução Temporal - Receita e Market Share")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Receita Mensal com Tendência")

        revenue_trend = processor.get_revenue_trend()

        # Calcular médias móveis
        revenue_trend = revenue_trend.sort_values('data')
        revenue_trend['ma_3'] = revenue_trend['receita'].rolling(window=3, min_periods=1).mean()

        fig = make_subplots(specs=[[{"secondary_y": False}]])

        # Barras de receita
        fig.add_trace(
            go.Bar(
                x=revenue_trend['data'],
                y=revenue_trend['receita'] / 1e6,
                name='Receita Mensal',
                marker_color=COLORS['primary'],
                opacity=0.6,
                hovertemplate='%{x|%b/%Y}<br>Receita: R$ %{y:.1f}M<extra></extra>'
            )
        )

        # Linha de tendência (MA3)
        fig.add_trace(
            go.Scatter(
                x=revenue_trend['data'],
                y=revenue_trend['ma_3'] / 1e6,
                name='Média Móvel (3m)',
                line=dict(color=COLORS['accent'], width=3),
                mode='lines+markers',
                marker=dict(size=8),
                hovertemplate='%{x|%b/%Y}<br>Tendência: R$ %{y:.1f}M<extra></extra>'
            )
        )

        fig.update_layout(
            height=400,
            xaxis_title="Período",
            yaxis_title="Receita (R$ Milhões)",
            hovermode='x unified',
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'},
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

        # Métricas de tendência
        last_3_avg = revenue_trend['receita'].tail(3).mean()
        previous_3_avg = revenue_trend['receita'].head(3).mean()
        trend_change = ((last_3_avg - previous_3_avg) / previous_3_avg * 100) if previous_3_avg > 0 else 0

        st.info(f"**Tendência:** Receita média evoluiu {trend_change:+.1f}% comparando últimos 3 meses vs primeiros 3 meses do período")

    with col2:
        st.markdown("#### Market Share com Meta e Benchmark")

        share_trend = processor.get_market_share_trend()

        fig = go.Figure()

        # Linha de market share
        fig.add_trace(
            go.Scatter(
                x=share_trend['data'],
                y=share_trend['share'] * 100,
                name='Market Share RD',
                line=dict(color=COLORS['secondary'], width=4),
                mode='lines+markers',
                marker=dict(size=10, symbol='circle'),
                fill='tozeroy',
                fillcolor=f'rgba(0, 168, 107, 0.1)',
                hovertemplate='%{x|%b/%Y}<br>Share: %{y:.2f}%<extra></extra>'
            )
        )

        # Linha de meta
        fig.add_hline(
            y=40,
            line_dash="dash",
            line_color=COLORS['accent'],
            line_width=3,
            annotation_text="Meta: 40%",
            annotation_position="right",
            annotation=dict(font_size=12, font_color=COLORS['accent'])
        )

        # Linha de benchmark mercado (exemplo)
        fig.add_hline(
            y=35,
            line_dash="dot",
            line_color=COLORS['warning'],
            line_width=2,
            annotation_text="Benchmark Mercado: 35%",
            annotation_position="right",
            annotation=dict(font_size=10, font_color=COLORS['warning'])
        )

        fig.update_layout(
            height=400,
            xaxis_title="Período",
            yaxis_title="Market Share (%)",
            hovermode='x unified',
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'},
            yaxis=dict(range=[0, 50])
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

        # Gap para meta
        current_share = share_trend['share'].iloc[-1] * 100
        gap_to_target = 40 - current_share

        if gap_to_target > 0:
            st.warning(f"**Gap para Meta:** {gap_to_target:.1f}pp - Foco em ações para conquistar share dos concorrentes")
        else:
            st.success(f"**Meta Atingida:** Share atual de {current_share:.1f}% supera a meta de 40%!")

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Análise de Composição
    st.markdown("### Composição e Distribuição de Vendas")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Performance por Canal")

        channel_perf = processor.get_channel_performance()

        fig = go.Figure(data=[
            go.Pie(
                labels=channel_perf['canal'],
                values=channel_perf['rbv'],
                hole=0.5,
                marker=dict(
                    colors=[COLORS['primary'], COLORS['accent']],
                    line=dict(color='white', width=3)
                ),
                textinfo='label+percent',
                textfont_size=14,
                hovertemplate='%{label}<br>Receita: R$ %{value:,.0f}<br>Participação: %{percent}<extra></extra>'
            )
        ])

        total_revenue_channel = channel_perf['rbv'].sum()

        fig.update_layout(
            height=300,
            paper_bgcolor='white',
            font={'family': 'Inter, sans-serif'},
            annotations=[dict(text=f'R$ {total_revenue_channel/1e9:.2f}B', x=0.5, y=0.5, font_size=18, showarrow=False)]
        )

        st.plotly_chart(fig, use_container_width=True)

        # Tabela de detalhes
        channel_display = channel_perf[['canal', 'rbv', 'pct_receita']].copy()
        channel_display.columns = ['Canal', 'Receita (R$)', 'Part. (%)']
        channel_display['Receita (R$)'] = channel_display['Receita (R$)'].apply(lambda x: f'R$ {x/1e6:.1f}M')
        channel_display['Part. (%)'] = channel_display['Part. (%)'].apply(lambda x: f'{x:.1f}%')

        st.dataframe(channel_display, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("#### Top 5 Categorias")

        top5_cat = category_perf.head(5)

        fig = go.Figure(data=[
            go.Bar(
                y=top5_cat['categoria'],
                x=top5_cat['receita'] / 1e6,
                orientation='h',
                marker=dict(
                    color=top5_cat['receita'],
                    colorscale=[
                        [0, COLORS['light']],
                        [1, COLORS['secondary']]
                    ],
                    line=dict(color=COLORS['dark'], width=1)
                ),
                text=top5_cat['pct_receita'].apply(lambda x: f'{x:.1f}%'),
                textposition='outside',
                hovertemplate='%{y}<br>Receita: R$ %{x:.1f}M<br>Produtos: %{customdata}<extra></extra>',
                customdata=top5_cat['produtos']
            )
        ])

        fig.update_layout(
            height=300,
            xaxis_title="Receita (R$ Milhões)",
            yaxis_title="",
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'}
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

        # Concentração top 3
        top3_cat_pct = top5_cat.head(3)['pct_receita'].sum()
        st.metric("Concentração Top 3", f"{top3_cat_pct:.1f}%", help="Participação das 3 maiores categorias na receita total")

    with col3:
        st.markdown("#### Top 5 Estados")

        top5_states = state_perf.head(5)

        fig = go.Figure(data=[
            go.Bar(
                y=top5_states['estado'],
                x=top5_states['receita'] / 1e6,
                orientation='h',
                marker=dict(
                    color=top5_states['receita'],
                    colorscale=[
                        [0, COLORS['light']],
                        [1, COLORS['primary']]
                    ],
                    line=dict(color=COLORS['dark'], width=1)
                ),
                text=top5_states['pct_receita'].apply(lambda x: f'{x:.1f}%'),
                textposition='outside',
                hovertemplate='%{y}<br>Receita: R$ %{x:.1f}M<extra></extra>'
            )
        ])

        fig.update_layout(
            height=300,
            xaxis_title="Receita (R$ Milhões)",
            yaxis_title="",
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'}
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

        # Cobertura
        st.metric("Estados Ativos", f"{len(state_perf)}", help="Número de estados com operação ativa")

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Análise de Produtos - Pareto
    st.markdown("### Análise de Contribuição de Produtos (Curva ABC)")

    # Calcular Pareto
    product_revenue = processor.pricing_data.groupby('produto')['rbv'].sum().sort_values(ascending=False).reset_index()
    product_revenue['cumsum'] = product_revenue['rbv'].cumsum()
    product_revenue['cumsum_pct'] = (product_revenue['cumsum'] / product_revenue['rbv'].sum()) * 100
    product_revenue['ranking'] = range(1, len(product_revenue) + 1)
    product_revenue['pct_total'] = (product_revenue['ranking'] / len(product_revenue)) * 100

    # Encontrar pontos ABC
    products_80 = product_revenue[product_revenue['cumsum_pct'] <= 80]
    products_95 = product_revenue[product_revenue['cumsum_pct'] <= 95]

    pct_products_A = (len(products_80) / len(product_revenue)) * 100
    pct_products_B = ((len(products_95) - len(products_80)) / len(product_revenue)) * 100
    pct_products_C = 100 - pct_products_A - pct_products_B

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Barras de receita (primeiros 100 produtos)
        sample_size = min(100, len(product_revenue))

        fig.add_trace(
            go.Bar(
                x=product_revenue.head(sample_size)['ranking'],
                y=product_revenue.head(sample_size)['rbv'] / 1e6,
                name='Receita Individual',
                marker_color=COLORS['primary'],
                opacity=0.6,
                hovertemplate='Ranking: %{x}<br>Receita: R$ %{y:.2f}M<extra></extra>'
            ),
            secondary_y=False
        )

        # Curva de Pareto
        fig.add_trace(
            go.Scatter(
                x=product_revenue.head(sample_size)['ranking'],
                y=product_revenue.head(sample_size)['cumsum_pct'],
                name='% Acumulado',
                line=dict(color=COLORS['accent'], width=4),
                mode='lines',
                hovertemplate='Ranking: %{x}<br>Acumulado: %{y:.1f}%<extra></extra>'
            ),
            secondary_y=True
        )

        # Linhas de referência ABC
        fig.add_hline(y=80, line_dash="dash", line_color=COLORS['secondary'],
                     annotation_text="A: 80%", secondary_y=True, annotation_position="left")
        fig.add_hline(y=95, line_dash="dot", line_color=COLORS['warning'],
                     annotation_text="B: 95%", secondary_y=True, annotation_position="left")

        fig.update_xaxes(title_text="Ranking de Produtos")
        fig.update_yaxes(title_text="Receita Individual (R$ Milhões)", secondary_y=False)
        fig.update_yaxes(title_text="% Receita Acumulada", secondary_y=True, range=[0, 105])

        fig.update_layout(
            height=400,
            hovermode='x unified',
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'},
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Classificação ABC")

        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border-left: 5px solid {COLORS['secondary']};">
            <div style="font-size: 0.85rem; color: #708090; margin-bottom: 0.3rem;">CLASSE A (80% receita)</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {COLORS['secondary']};">{len(products_80):,}</div>
            <div style="font-size: 0.85rem; color: #708090;">{pct_products_A:.1f}% dos produtos</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border-left: 5px solid {COLORS['warning']};">
            <div style="font-size: 0.85rem; color: #708090; margin-bottom: 0.3rem;">CLASSE B (80-95% receita)</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {COLORS['warning']};">{len(products_95) - len(products_80):,}</div>
            <div style="font-size: 0.85rem; color: #708090;">{pct_products_B:.1f}% dos produtos</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border-left: 5px solid {COLORS['neutral']};">
            <div style="font-size: 0.85rem; color: #708090; margin-bottom: 0.3rem;">CLASSE C (>95% receita)</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {COLORS['neutral']};">{len(product_revenue) - len(products_95):,}</div>
            <div style="font-size: 0.85rem; color: #708090;">{pct_products_C:.1f}% dos produtos</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            create_insight_card(
                "Estratégia Recomendada",
                "Priorize gestão intensiva dos produtos Classe A (alto giro), otimize estoque da Classe B e avalie descontinuação da Classe C de baixo desempenho.",
                "action",
                icon="💡"
            ),
            unsafe_allow_html=True
        )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Performance Score Detalhado
    st.markdown("### Scorecard de Performance Multidimensional")

    # Calcular scores
    metrics_for_score = {
        'revenue_growth': growth['revenue_growth'],
        'avg_share': share_metrics['avg_share'],
        'zero_sales_rate': share_metrics['zero_sales_rate'],
        'top3_concentration': state_perf.head(3)['pct_receita'].sum()
    }

    score_data = calculate_performance_score(metrics_for_score)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        # Gauge principal
        fig = create_gauge_chart(
            score_data['total_score'],
            100,
            "Performance Score Geral"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Componentes do Score")

        for metric, score in score_data['component_scores'].items():
            weight = score_data['weights'][metric]
            metric_display = metric.replace('_', ' ').title()

            # Barra de progresso visual
            progress_color = (COLORS['secondary'] if score >= 70 else
                            (COLORS['warning'] if score >= 50 else COLORS['danger']))

            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                    <span style="font-size: 0.85rem; font-weight: 500;">{metric_display}</span>
                    <span style="font-size: 0.85rem; color: {progress_color}; font-weight: 600;">{score:.0f}/100</span>
                </div>
                <div style="width: 100%; height: 8px; background: #e0e0e0; border-radius: 4px; overflow: hidden;">
                    <div style="width: {score}%; height: 100%; background: {progress_color};"></div>
                </div>
                <div style="font-size: 0.75rem; color: #708090; margin-top: 0.2rem;">Peso: {weight*100:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown("#### Benchmarks e Metas")

        benchmarks = [
            {"metric": "Performance Score", "current": score_data['total_score'], "target": 85, "benchmark": 75},
            {"metric": "Market Share", "current": share_metrics['avg_share']*100, "target": 40, "benchmark": 35},
            {"metric": "Taxa Venda Zero", "current": share_metrics['zero_sales_rate']*100, "target": 15, "benchmark": 25},
            {"metric": "Crescimento Receita", "current": growth['revenue_growth'], "target": 15, "benchmark": 10}
        ]

        for bm in benchmarks:
            current = bm['current']
            target = bm['target']
            benchmark = bm['benchmark']

            # Determinar status
            if current >= target:
                status_color = COLORS['secondary']
                status_icon = "🟢"
            elif current >= benchmark:
                status_color = COLORS['warning']
                status_icon = "🟡"
            else:
                status_color = COLORS['danger']
                status_icon = "🔴"

            st.markdown(f"""
            <div style="background: white; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.8rem; border-left: 4px solid {status_color};">
                <div style="font-size: 0.8rem; color: #708090; margin-bottom: 0.3rem;">{status_icon} {bm['metric']}</div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
                    <span>Atual: <strong>{current:.1f}</strong></span>
                    <span style="color: {status_color};">Meta: {target:.1f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================================================
# PÁGINA 2: ANÁLISE DE MARKET SHARE
# ==================================================

with tab2:
    st.markdown('<div class="main-header">Análise de Market Share</div>', unsafe_allow_html=True)
    st.markdown("Inteligência competitiva e análise de participação de mercado")

    share_metrics = processor.get_market_share_metrics()

    # KPIs de Market Share
    st.markdown("### Métricas de Participação de Mercado")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        share_pct = share_metrics['avg_share'] * 100
        gap_to_target = 40 - share_pct
        share_status = "excellent" if share_pct >= 40 else ("good" if share_pct >= 35 else "attention")

        st.markdown(
            create_kpi_card(
                "Market Share Médio",
                share_pct,
                delta=-gap_to_target if gap_to_target > 0 else gap_to_target,
                delta_text="vs meta 40%",
                format_type="percentage",
                status=share_status
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            create_kpi_card(
                "Vendas RD (unidades)",
                share_metrics['total_rd_sales'],
                format_type="number",
                status="good"
            ),
            unsafe_allow_html=True
        )

    with col3:
        competitor_ratio = (share_metrics['total_competitor_sales'] / share_metrics['total_rd_sales'] - 1) * 100 if share_metrics['total_rd_sales'] > 0 else 0

        st.markdown(
            create_kpi_card(
                "Vendas Concorrentes",
                share_metrics['total_competitor_sales'],
                delta=competitor_ratio,
                delta_text="vs RD",
                format_type="number",
                status="attention"
            ),
            unsafe_allow_html=True
        )

    with col4:
        zero_rate = share_metrics['zero_sales_rate'] * 100
        zero_status = "critical" if zero_rate > 30 else ("attention" if zero_rate > 20 else "good")

        st.markdown(
            create_kpi_card(
                "Taxa de Venda Zero",
                zero_rate,
                format_type="percentage",
                status=zero_status
            ),
            unsafe_allow_html=True
        )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Insights de Market Share
    st.markdown("### Insights Competitivos")

    col1, col2 = st.columns(2)

    # Calcular potencial de ganho
    potential_units = share_metrics['total_competitor_sales'] * 0.10  # 10% dos concorrentes
    avg_price = processor.get_revenue_metrics()['avg_price']
    potential_revenue = potential_units * avg_price

    with col1:
        st.markdown(
            create_insight_card(
                "Oportunidade de Ganho de Share",
                f"Capturar apenas 10% das vendas dos concorrentes ({potential_units/1e6:.1f}M unidades) representaria R$ {potential_revenue/1e6:.1f}M em receita adicional anual.",
                "action",
                "Implementar campanha agressiva de conquista de clientes com foco em disponibilidade e preço competitivo nos top produtos.",
                icon="🎯"
            ),
            unsafe_allow_html=True
        )

    with col2:
        zero_opportunities = int(len(processor.iqvia_data) * share_metrics['zero_sales_rate'])
        st.markdown(
            create_insight_card(
                "Vendas Zero - Crítico",
                f"{zero_opportunities:,} cenários de produto-loja com venda zero enquanto concorrentes vendem. Isso representa {share_metrics['zero_sales_rate']*100:.1f}% de todas as oportunidades.",
                "danger",
                "Prioridade máxima: revisar distribuição e disponibilidade de estoque nos produtos identificados na análise de oportunidades.",
                icon="⚠"
            ),
            unsafe_allow_html=True
        )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Evolução de Market Share Detalhada
    st.markdown("### Evolução Temporal RD vs Concorrentes")

    share_trend = processor.get_market_share_trend()

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.6, 0.4],
            subplot_titles=('Vendas: RD vs Concorrentes', 'Market Share (%)'),
            vertical_spacing=0.12,
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
        )

        # Gráfico 1: Vendas absolutas
        fig.add_trace(
            go.Bar(
                x=share_trend['data'],
                y=share_trend['venda_rd'] / 1e6,
                name='Vendas RD',
                marker_color=COLORS['primary'],
                opacity=0.8,
                hovertemplate='%{x|%b/%Y}<br>RD: %{y:.2f}M un<extra></extra>'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=share_trend['data'],
                y=share_trend['venda_concorrente'] / 1e6,
                name='Vendas Concorrentes',
                marker_color=COLORS['accent'],
                opacity=0.8,
                hovertemplate='%{x|%b/%Y}<br>Concorrentes: %{y:.2f}M un<extra></extra>'
            ),
            row=1, col=1
        )

        # Gráfico 2: Market Share %
        fig.add_trace(
            go.Scatter(
                x=share_trend['data'],
                y=share_trend['share'] * 100,
                name='Market Share (%)',
                line=dict(color=COLORS['secondary'], width=4),
                mode='lines+markers',
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor=f'rgba(0, 168, 107, 0.2)',
                hovertemplate='%{x|%b/%Y}<br>Share: %{y:.2f}%<extra></extra>'
            ),
            row=2, col=1
        )

        # Meta no segundo gráfico
        fig.add_hline(
            y=40,
            line_dash="dash",
            line_color=COLORS['danger'],
            line_width=2,
            annotation_text="Meta: 40%",
            annotation_position="right",
            row=2, col=1
        )

        fig.update_xaxes(title_text="Período", row=2, col=1)
        fig.update_yaxes(title_text="Unidades (Milhões)", row=1, col=1)
        fig.update_yaxes(title_text="Market Share (%)", row=2, col=1)

        fig.update_layout(
            height=600,
            hovermode='x unified',
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'},
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Estatísticas de Share")

        # Calcular estatísticas
        share_values = share_trend['share'] * 100
        share_min = share_values.min()
        share_max = share_values.max()
        share_avg = share_values.mean()
        share_current = share_values.iloc[-1]
        share_volatility = share_values.std()

        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 0.8rem; color: #708090; margin-bottom: 0.5rem;">SHARE ATUAL</div>
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['primary']};">{share_current:.2f}%</div>
        </div>

        <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 0.8rem; color: #708090; margin-bottom: 0.5rem;">MÉDIA DO PERÍODO</div>
            <div style="font-size: 1.5rem; font-weight: 600; color: {COLORS['dark']};">{share_avg:.2f}%</div>
        </div>

        <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 0.8rem; color: #708090; margin-bottom: 0.3rem;">AMPLITUDE</div>
            <div style="font-size: 1.2rem; font-weight: 600; color: {COLORS['dark']};">
                <span style="color: {COLORS['danger']};">↓ {share_min:.2f}%</span> /
                <span style="color: {COLORS['secondary']};">↑ {share_max:.2f}%</span>
            </div>
            <div style="font-size: 0.75rem; color: #708090; margin-top: 0.3rem;">Variação: {share_max - share_min:.2f}pp</div>
        </div>

        <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 0.8rem; color: #708090; margin-bottom: 0.3rem;">VOLATILIDADE</div>
            <div style="font-size: 1.2rem; font-weight: 600; color: {COLORS['warning']};">±{share_volatility:.2f}pp</div>
            <div style="font-size: 0.75rem; color: #708090; margin-top: 0.3rem;">Desvio padrão</div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge de atingimento de meta
        meta_achievement = (share_current / 40) * 100
        fig_gauge = create_gauge_chart(
            meta_achievement,
            100,
            "Atingimento da Meta",
            threshold_good=100,
            threshold_warning=85
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Distribuição de Share por Produto
    st.markdown("### Distribuição de Market Share por Produto")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Segmentação de Produtos por Faixa de Share")

        # Calcular distribuição
        df_share = processor.iqvia_data.groupby('cd_produto')['share'].mean().reset_index()

        bins = [0, 0.15, 0.25, 0.35, 0.50, 1.0]
        labels = ['<15%\nCrítico', '15-25%\nBaixo', '25-35%\nMédio', '35-50%\nBom', '>50%\nExcelente']
        df_share['categoria_share'] = pd.cut(df_share['share'], bins=bins, labels=labels)

        dist = df_share['categoria_share'].value_counts().sort_index()

        colors_gradient = [COLORS['danger'], COLORS['warning'], COLORS['neutral'],
                          COLORS['gradient_start'], COLORS['secondary']]

        fig = go.Figure(data=[
            go.Bar(
                x=dist.index,
                y=dist.values,
                marker=dict(
                    color=colors_gradient,
                    line=dict(color=COLORS['dark'], width=2)
                ),
                text=dist.values,
                textposition='outside',
                hovertemplate='%{x}<br>Produtos: %{y:,}<br>% do total: %{customdata:.1f}%<extra></extra>',
                customdata=(dist.values / dist.values.sum() * 100)
            )
        ])

        fig.update_layout(
            height=400,
            xaxis_title="Faixa de Market Share",
            yaxis_title="Número de Produtos",
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'}
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Estatísticas de Distribuição")

        # Estatísticas
        total_products = len(df_share)
        excellent_products = len(df_share[df_share['share'] > 0.50])
        good_products = len(df_share[(df_share['share'] >= 0.35) & (df_share['share'] <= 0.50)])
        critical_products = len(df_share[df_share['share'] < 0.15])

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['secondary']} 0%, {COLORS['gradient_start']} 100%);
                    color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <div style="font-size: 0.9rem; margin-bottom: 0.5rem; opacity: 0.9;">PRODUTOS COM SHARE EXCELENTE (>50%)</div>
            <div style="font-size: 2.5rem; font-weight: 700;">{excellent_products:,}</div>
            <div style="font-size: 0.85rem; margin-top: 0.3rem; opacity: 0.9;">{(excellent_products/total_products*100):.1f}% do portfólio</div>
        </div>

        <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 0.8rem; border-left: 5px solid {COLORS['gradient_start']}; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.8rem; color: #708090;">Share Bom (35-50%)</div>
                    <div style="font-size: 1.5rem; font-weight: 600; color: {COLORS['dark']};">{good_products:,}</div>
                </div>
                <div style="font-size: 0.9rem; color: {COLORS['gradient_start']}; font-weight: 600;">{(good_products/total_products*100):.1f}%</div>
            </div>
        </div>

        <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 0.8rem; border-left: 5px solid {COLORS['warning']}; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.8rem; color: #708090;">Share Médio (25-35%)</div>
                    <div style="font-size: 1.5rem; font-weight: 600; color: {COLORS['dark']};">{len(df_share[(df_share['share'] >= 0.25) & (df_share['share'] < 0.35)]):,}</div>
                </div>
                <div style="font-size: 0.9rem; color: {COLORS['warning']}; font-weight: 600;">{(len(df_share[(df_share['share'] >= 0.25) & (df_share['share'] < 0.35)])/total_products*100):.1f}%</div>
            </div>
        </div>

        <div style="background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); padding: 1rem; border-radius: 10px;
                    border-left: 5px solid {COLORS['danger']}; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.8rem; color: #b71c1c; font-weight: 600;">🔴 CRÍTICO - Share <15%</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: {COLORS['danger']};">{critical_products:,}</div>
                </div>
                <div style="font-size: 1rem; color: {COLORS['danger']}; font-weight: 700;">{(critical_products/total_products*100):.1f}%</div>
            </div>
            <div style="font-size: 0.75rem; color: #b71c1c; margin-top: 0.5rem;">Requer ação imediata</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            create_insight_card(
                "Priorização Estratégica",
                f"Foco nos {critical_products:,} produtos críticos (<15% share) com potencial de rápida melhoria através de ações de disponibilidade e pricing.",
                "action",
                icon="🎯"
            ),
            unsafe_allow_html=True
        )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Top Oportunidades de Vendas Zero
    st.markdown("### Top Oportunidades - Produtos com Venda Zero RD")
    st.markdown("Produtos onde RD tem venda zero mas concorrentes vendem significativamente - maior potencial de ganho rápido")

    zero_sales = processor.get_zero_sales_analysis().head(30)

    if not zero_sales.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            fig = go.Figure()

            # Barras horizontais
            fig.add_trace(
                go.Bar(
                    y=zero_sales['produto'].iloc[::-1],
                    x=zero_sales['venda_concorrente'].iloc[::-1] / 1e3,
                    orientation='h',
                    marker=dict(
                        color=zero_sales['venda_concorrente'].iloc[::-1],
                        colorscale=[
                            [0, COLORS['warning']],
                            [1, COLORS['danger']]
                        ],
                        showscale=True,
                        colorbar=dict(title="Unidades<br>(mil)")
                    ),
                    text=zero_sales['lojas_afetadas'].iloc[::-1],
                    texttemplate='%{text} lojas',
                    textposition='outside',
                    hovertemplate='Produto: %{y}<br>Vendas Concorrentes: %{x:.1f}k un<br>Lojas afetadas: %{text}<extra></extra>'
                )
            )

            fig.update_layout(
                height=700,
                xaxis_title="Vendas dos Concorrentes (mil unidades)",
                yaxis_title="Código do Produto",
                paper_bgcolor='white',
                plot_bgcolor='white',
                font={'family': 'Inter, sans-serif', 'size': 10}
            )

            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
            fig.update_yaxes(showgrid=False)

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Análise de Impacto")

            # Calcular impacto potencial
            top10_potential = zero_sales.head(10)['venda_concorrente'].sum()
            total_potential = zero_sales['venda_concorrente'].sum()
            avg_price = processor.get_revenue_metrics()['avg_price']

            # Assumir captura de 30% das vendas dos concorrentes
            capture_rate = 0.30
            revenue_potential_top10 = top10_potential * capture_rate * avg_price
            revenue_potential_total = total_potential * capture_rate * avg_price

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 1.5rem;
                        border-radius: 10px; margin-bottom: 1rem; border-left: 5px solid {COLORS['primary']};">
                <div style="font-size: 0.85rem; color: #1565c0; font-weight: 600; margin-bottom: 0.5rem;">POTENCIAL TOP 10 PRODUTOS</div>
                <div style="font-size: 2rem; font-weight: 700; color: {COLORS['primary']};">R$ {revenue_potential_top10/1e6:.1f}M</div>
                <div style="font-size: 0.8rem; color: #1976d2; margin-top: 0.3rem;">
                    Assumindo captura de 30% das vendas dos concorrentes
                </div>
            </div>

            <div style="background: white; padding: 1.2rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 0.8rem; color: #708090; margin-bottom: 0.5rem;">POTENCIAL TOTAL (TOP 30)</div>
                <div style="font-size: 1.5rem; font-weight: 600; color: {COLORS['dark']};">R$ {revenue_potential_total/1e6:.1f}M</div>
                <div style="font-size: 0.75rem; color: #708090; margin-top: 0.3rem;">
                    {total_potential/1e6:.1f}M unidades × 30% × R$ {avg_price:.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### Métricas de Oportunidade")

            st.metric(
                "Produtos com Venda Zero",
                f"{len(zero_sales):,}",
                help="Produtos identificados com oportunidade"
            )

            st.metric(
                "Lojas Afetadas (Top 10)",
                f"{zero_sales.head(10)['lojas_afetadas'].sum():,}",
                help="Total de lojas nos top 10 produtos"
            )

            st.metric(
                "Unidades Perdidas (Top 10)",
                f"{top10_potential/1e3:.0f}K",
                help="Vendas dos concorrentes que poderiam ser capturadas"
            )

            st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

            st.markdown(
                create_insight_card(
                    "Ações Prioritárias",
                    "1. Garantir estoque nos top 10 produtos\n2. Revisar distribuição nas lojas afetadas\n3. Treinar equipe comercial\n4. Monitorar fill rate semanalmente",
                    "action",
                    icon="📋"
                ),
                unsafe_allow_html=True
            )

        # Tabela detalhada
        st.markdown("#### Detalhamento dos Top 20 Produtos")

        top20_detail = zero_sales.head(20).copy()
        top20_detail['potencial_receita'] = top20_detail['venda_concorrente'] * 0.30 * avg_price
        top20_detail['ranking'] = range(1, len(top20_detail) + 1)

        display_df = top20_detail[['ranking', 'produto', 'venda_concorrente', 'lojas_afetadas', 'potencial_receita']].copy()
        display_df.columns = ['#', 'Código Produto', 'Vendas Concorrentes', 'Lojas', 'Potencial Receita (30%)']

        st.dataframe(
            display_df.style.format({
                'Vendas Concorrentes': '{:,.0f} un',
                'Lojas': '{:,}',
                'Potencial Receita (30%)': 'R$ {:,.0f}'
            }).background_gradient(subset=['Potencial Receita (30%)'], cmap='Reds'),
            hide_index=True,
            use_container_width=True,
            height=400
        )

# ==================================================
# PÁGINA 3: PERFORMANCE POR CATEGORIA
# ==================================================

with tab3:
    st.markdown('<div class="main-header">Performance por Categoria</div>', unsafe_allow_html=True)
    st.markdown("Análise profunda de neogrupos, produtos e tendências por categoria")

    category_perf = processor.get_category_performance()

    # Seletor de categoria com métricas
    st.markdown("### Selecione a Categoria para Análise Detalhada")

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_category = st.selectbox(
            "Categoria (Neogrupo)",
            category_perf['categoria'].tolist(),
            label_visibility="collapsed"
        )

    with col2:
        comparison_mode = st.toggle("Modo Comparação", value=False, help="Ative para comparar todas as categorias")

    # Dados da categoria selecionada
    cat_data = category_perf[category_perf['categoria'] == selected_category].iloc[0]

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    if not comparison_mode:
        # Modo análise individual da categoria
        st.markdown(f"### Análise Detalhada: {selected_category}")

        # KPIs da categoria
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(
                create_kpi_card(
                    "Receita",
                    cat_data['receita'],
                    format_type="currency",
                    status="excellent"
                ),
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                create_kpi_card(
                    "Part. na Receita",
                    cat_data['pct_receita'],
                    format_type="percentage",
                    status="good"
                ),
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                create_kpi_card(
                    "Unidades",
                    cat_data['unidades'],
                    format_type="number",
                    status="good"
                ),
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                create_kpi_card(
                    "Preço Médio",
                    cat_data['preco_medio'],
                    format_type="currency",
                    status="good"
                ),
                unsafe_allow_html=True
            )

        with col5:
            st.markdown(
                create_kpi_card(
                    "SKUs Ativos",
                    cat_data['produtos'],
                    format_type="number",
                    status="good"
                ),
                unsafe_allow_html=True
            )

        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

        # Análise temporal da categoria
        st.markdown("#### Evolução Temporal Multidimensional")

        cat_temporal = processor.pricing_data[
            processor.pricing_data['neogrupo'] == selected_category
        ].groupby('mes').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean'
        }).reset_index().sort_values('mes')

        # Calcular variações MoM
        cat_temporal['receita_mom'] = cat_temporal['rbv'].pct_change() * 100
        cat_temporal['unidades_mom'] = cat_temporal['qt_unidade_vendida'].pct_change() * 100
        cat_temporal['preco_mom'] = cat_temporal['preco_medio'].pct_change() * 100

        # Gráficos temporais
        col1, col2 = st.columns(2)

        with col1:
            # Receita e Unidades
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            fig.add_trace(
                go.Bar(
                    x=cat_temporal['mes'],
                    y=cat_temporal['rbv'] / 1e6,
                    name='Receita (R$ Mi)',
                    marker_color=COLORS['primary'],
                    opacity=0.7,
                    yaxis='y',
                    hovertemplate='%{x|%b/%Y}<br>Receita: R$ %{y:.2f}M<extra></extra>'
                ),
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(
                    x=cat_temporal['mes'],
                    y=cat_temporal['qt_unidade_vendida'] / 1e3,
                    name='Unidades (mil)',
                    line=dict(color=COLORS['accent'], width=3),
                    mode='lines+markers',
                    marker=dict(size=8),
                    yaxis='y2',
                    hovertemplate='%{x|%b/%Y}<br>Unidades: %{y:.1f}K<extra></extra>'
                ),
                secondary_y=True
            )

            fig.update_xaxes(title_text="Período")
            fig.update_yaxes(title_text="Receita (R$ Milhões)", secondary_y=False)
            fig.update_yaxes(title_text="Unidades Vendidas (mil)", secondary_y=True)

            fig.update_layout(
                title="Receita e Volume de Vendas",
                height=350,
                hovermode='x unified',
                paper_bgcolor='white',
                plot_bgcolor='white',
                font={'family': 'Inter, sans-serif'},
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Preço Médio e Variação
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            fig.add_trace(
                go.Scatter(
                    x=cat_temporal['mes'],
                    y=cat_temporal['preco_medio'],
                    name='Preço Médio',
                    line=dict(color=COLORS['secondary'], width=4),
                    mode='lines+markers',
                    marker=dict(size=10),
                    fill='tozeroy',
                    fillcolor=f'rgba(0, 168, 107, 0.1)',
                    yaxis='y',
                    hovertemplate='%{x|%b/%Y}<br>Preço: R$ %{y:.2f}<extra></extra>'
                ),
                secondary_y=False
            )

            fig.add_trace(
                go.Bar(
                    x=cat_temporal['mes'],
                    y=cat_temporal['preco_mom'],
                    name='Variação MoM (%)',
                    marker=dict(
                        color=cat_temporal['preco_mom'],
                        colorscale=[[0, COLORS['danger']], [0.5, COLORS['neutral']], [1, COLORS['secondary']]],
                        cmid=0
                    ),
                    opacity=0.6,
                    yaxis='y2',
                    hovertemplate='%{x|%b/%Y}<br>Variação: %{y:.2f}%<extra></extra>'
                ),
                secondary_y=True
            )

            fig.update_xaxes(title_text="Período")
            fig.update_yaxes(title_text="Preço Médio (R$)", secondary_y=False)
            fig.update_yaxes(title_text="Variação MoM (%)", secondary_y=True)

            fig.update_layout(
                title="Evolução de Preço e Variação Mensal",
                height=350,
                hovermode='x unified',
                paper_bgcolor='white',
                plot_bgcolor='white',
                font={'family': 'Inter, sans-serif'},
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

            st.plotly_chart(fig, use_container_width=True)

        # Análise de crescimento
        col1, col2, col3 = st.columns(3)

        with col1:
            if len(cat_temporal) >= 2:
                first_month_rev = cat_temporal['rbv'].iloc[0]
                last_month_rev = cat_temporal['rbv'].iloc[-1]
                revenue_growth = ((last_month_rev - first_month_rev) / first_month_rev * 100) if first_month_rev > 0 else 0

                st.metric(
                    "Crescimento de Receita (período)",
                    f"{revenue_growth:+.1f}%",
                    delta=f"R$ {(last_month_rev - first_month_rev)/1e6:+.1f}M",
                    help=f"Primeiro mês: R$ {first_month_rev/1e6:.1f}M | Último mês: R$ {last_month_rev/1e6:.1f}M"
                )

        with col2:
            if len(cat_temporal) >= 2:
                avg_mom_units = cat_temporal['unidades_mom'].mean()
                st.metric(
                    "Variação Média MoM - Unidades",
                    f"{avg_mom_units:+.1f}%",
                    help="Média das variações mensais de volume"
                )

        with col3:
            if len(cat_temporal) >= 2:
                price_volatility = cat_temporal['preco_medio'].std()
                st.metric(
                    "Volatilidade de Preço",
                    f"R$ {price_volatility:.2f}",
                    help="Desvio padrão do preço médio no período"
                )

        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

        # Top produtos da categoria
        st.markdown("#### Top 20 Produtos da Categoria")

        cat_products = processor.pricing_data[
            processor.pricing_data['neogrupo'] == selected_category
        ].groupby('produto').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean'
        }).reset_index().sort_values('rbv', ascending=False).head(20)

        cat_products['pct_receita_cat'] = (cat_products['rbv'] / cat_products['rbv'].sum()) * 100

        # Treemap dos produtos
        col1, col2 = st.columns([2, 1])

        with col1:
            # Preparar dados para treemap
            treemap_data = cat_products.head(15).copy()
            treemap_data['categoria'] = selected_category

            fig = create_treemap(
                treemap_data,
                ['categoria', 'produto'],
                'rbv',
                f"Composição de Receita - Top 15 Produtos em {selected_category}"
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Concentração de Produtos**")

            # Curva de concentração
            top5_pct = cat_products.head(5)['pct_receita_cat'].sum()
            top10_pct = cat_products.head(10)['pct_receita_cat'].sum()
            top20_pct = cat_products['pct_receita_cat'].sum()

            concentration_data = pd.DataFrame({
                'Grupo': ['Top 5', 'Top 10', 'Top 20'],
                'Participação': [top5_pct, top10_pct, top20_pct]
            })

            fig = go.Figure(data=[
                go.Bar(
                    x=concentration_data['Grupo'],
                    y=concentration_data['Participação'],
                    marker=dict(
                        color=concentration_data['Participação'],
                        colorscale=[[0, COLORS['light']], [1, COLORS['primary']]],
                        line=dict(color=COLORS['dark'], width=2)
                    ),
                    text=concentration_data['Participação'].apply(lambda x: f'{x:.1f}%'),
                    textposition='outside',
                    hovertemplate='%{x}<br>Participação: %{y:.1f}%<extra></extra>'
                )
            ])

            fig.update_layout(
                height=300,
                yaxis_title="% da Receita da Categoria",
                yaxis=dict(range=[0, 105]),
                paper_bgcolor='white',
                plot_bgcolor='white',
                font={'family': 'Inter, sans-serif'}
            )

            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                create_insight_card(
                    "Concentração",
                    f"Top 5 produtos representam {top5_pct:.1f}% da receita da categoria - {'alta concentração' if top5_pct > 60 else 'concentração moderada'}.",
                    "info" if top5_pct < 70 else "warning",
                    icon="📊"
                ),
                unsafe_allow_html=True
            )

        # Tabela detalhada de produtos
        st.markdown("**Ranking Completo de Produtos**")

        cat_products['ranking'] = range(1, len(cat_products) + 1)
        display_products = cat_products[['ranking', 'produto', 'rbv', 'qt_unidade_vendida', 'preco_medio', 'pct_receita_cat']].copy()
        display_products.columns = ['#', 'Código', 'Receita', 'Unidades', 'Preço Médio', '% Cat.']

        st.dataframe(
            display_products.style.format({
                'Receita': 'R$ {:.0f}',
                'Unidades': '{:,.0f}',
                'Preço Médio': 'R$ {:.2f}',
                '% Cat.': '{:.2f}%'
            }).background_gradient(subset=['Receita'], cmap='Blues'),
            hide_index=True,
            use_container_width=True,
            height=400
        )

    else:
        # Modo comparação de categorias
        st.markdown("### Comparação entre Categorias")

        # Gráfico de receita por categoria
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Receita por Categoria")

            fig = go.Figure(data=[
                go.Bar(
                    x=category_perf['categoria'],
                    y=category_perf['receita'] / 1e6,
                    marker=dict(
                        color=category_perf['receita'],
                        colorscale=[[0, COLORS['light']], [1, COLORS['primary']]],
                        showscale=True,
                        colorbar=dict(title="Receita<br>(R$ Mi)")
                    ),
                    text=category_perf['pct_receita'].apply(lambda x: f'{x:.1f}%'),
                    textposition='outside',
                    hovertemplate='%{x}<br>Receita: R$ %{y:.1f}M<br>Participação: %{text}<extra></extra>'
                )
            ])

            fig.update_layout(
                height=400,
                xaxis_title="",
                yaxis_title="Receita (R$ Milhões)",
                xaxis_tickangle=-45,
                paper_bgcolor='white',
                plot_bgcolor='white',
                font={'family': 'Inter, sans-serif'}
            )

            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Preço Médio por Categoria")

            fig = go.Figure(data=[
                go.Bar(
                    x=category_perf['categoria'],
                    y=category_perf['preco_medio'],
                    marker=dict(
                        color=category_perf['preco_medio'],
                        colorscale=[[0, COLORS['secondary']], [1, COLORS['accent']]],
                        showscale=True,
                        colorbar=dict(title="Preço<br>Médio (R$)")
                    ),
                    text=category_perf['preco_medio'].apply(lambda x: f'R$ {x:.2f}'),
                    textposition='outside',
                    hovertemplate='%{x}<br>Preço Médio: R$ %{y:.2f}<extra></extra>'
                )
            ])

            fig.update_layout(
                height=400,
                xaxis_title="",
                yaxis_title="Preço Médio (R$)",
                xaxis_tickangle=-45,
                paper_bgcolor='white',
                plot_bgcolor='white',
                font={'family': 'Inter, sans-serif'}
            )

            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

        # Matriz de performance
        st.markdown("#### Matriz de Performance: Volume vs Preço")

        # Scatter plot
        fig = go.Figure()

        # Calcular médias para quadrantes
        avg_price = category_perf['preco_medio'].mean()
        avg_units = category_perf['unidades'].mean()

        # Adicionar scatter
        fig.add_trace(
            go.Scatter(
                x=category_perf['preco_medio'],
                y=category_perf['unidades'] / 1e6,
                mode='markers+text',
                marker=dict(
                    size=category_perf['receita'] / 1e8,  # Tamanho proporcional à receita
                    color=category_perf['pct_receita'],
                    colorscale=[[0, COLORS['light']], [0.5, COLORS['gradient_start']], [1, COLORS['gradient_end']]],
                    showscale=True,
                    colorbar=dict(title="% Receita"),
                    line=dict(color=COLORS['dark'], width=2)
                ),
                text=category_perf['categoria'],
                textposition="top center",
                textfont=dict(size=10),
                hovertemplate='<b>%{text}</b><br>Preço Médio: R$ %{x:.2f}<br>Unidades: %{y:.2f}M<br>Receita: R$ %{customdata:.0f}M<extra></extra>',
                customdata=category_perf['receita'] / 1e6
            )
        )

        # Adicionar linhas de referência
        fig.add_hline(y=avg_units / 1e6, line_dash="dash", line_color=COLORS['neutral'],
                     annotation_text="Média Volume", annotation_position="left")
        fig.add_vline(x=avg_price, line_dash="dash", line_color=COLORS['neutral'],
                     annotation_text="Média Preço", annotation_position="top")

        # Adicionar anotações de quadrantes
        max_price = category_perf['preco_medio'].max()
        max_units = category_perf['unidades'].max() / 1e6

        quadrants = [
            {"x": avg_price * 1.5, "y": avg_units / 1e6 * 1.5, "text": "Premium<br>(Alto Preço, Alto Volume)", "color": COLORS['secondary']},
            {"x": avg_price * 0.5, "y": avg_units / 1e6 * 1.5, "text": "Popular<br>(Baixo Preço, Alto Volume)", "color": COLORS['primary']},
            {"x": avg_price * 1.5, "y": avg_units / 1e6 * 0.5, "text": "Nicho<br>(Alto Preço, Baixo Volume)", "color": COLORS['warning']},
            {"x": avg_price * 0.5, "y": avg_units / 1e6 * 0.5, "text": "Oportunidade<br>(Baixo Preço, Baixo Volume)", "color": COLORS['danger']}
        ]

        for q in quadrants:
            fig.add_annotation(
                x=q["x"], y=q["y"],
                text=q["text"],
                showarrow=False,
                font=dict(size=10, color=q["color"]),
                opacity=0.5
            )

        fig.update_layout(
            title="Posicionamento de Categorias (tamanho = receita)",
            height=500,
            xaxis_title="Preço Médio (R$)",
            yaxis_title="Unidades Vendidas (Milhões)",
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'}
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

        # Tabela comparativa completa
        st.markdown("#### Tabela Comparativa Completa")

        comparison_table = category_perf.copy()
        comparison_table['ranking'] = range(1, len(comparison_table) + 1)
        comparison_table = comparison_table[['ranking', 'categoria', 'receita', 'pct_receita', 'unidades', 'preco_medio', 'produtos']]
        comparison_table.columns = ['#', 'Categoria', 'Receita', '% Total', 'Unidades', 'Preço Médio', 'SKUs']

        st.dataframe(
            comparison_table.style.format({
                'Receita': 'R$ {:.0f}',
                '% Total': '{:.2f}%',
                'Unidades': '{:,.0f}',
                'Preço Médio': 'R$ {:.2f}',
                'SKUs': '{:,}'
            }).background_gradient(subset=['Receita'], cmap='Greens'),
            hide_index=True,
            use_container_width=True,
            height=400
        )

# ==================================================
# PÁGINA 4: ANÁLISE GEOGRÁFICA
# ==================================================

with tab4:
    st.markdown('<div class="main-header">Análise Geográfica</div>', unsafe_allow_html=True)
    st.markdown("Performance por estado, regiões e oportunidades de expansão territorial")

    state_perf = processor.get_state_performance()

    # KPIs Geográficos
    st.markdown("### Visão Geral da Distribuição Geográfica")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            create_kpi_card(
                "Estados Ativos",
                len(state_perf),
                format_type="number",
                status="excellent"
            ),
            unsafe_allow_html=True
        )

    with col2:
        top_state = state_perf.iloc[0]
        st.markdown(
            create_kpi_card(
                "Estado Líder",
                f"{top_state['estado']}: {top_state['pct_receita']:.1f}%",
                format_type="number",
                status="good"
            ),
            unsafe_allow_html=True
        )

    with col3:
        top3_concentration = state_perf.head(3)['pct_receita'].sum()
        concentration_status = "attention" if top3_concentration > 60 else "good"
        st.markdown(
            create_kpi_card(
                "Concentração Top 3",
                top3_concentration,
                format_type="percentage",
                status=concentration_status
            ),
            unsafe_allow_html=True
        )

    with col4:
        avg_revenue_state = state_perf['receita'].mean()
        st.markdown(
            create_kpi_card(
                "Receita Média/Estado",
                avg_revenue_state,
                format_type="currency",
                status="good"
            ),
            unsafe_allow_html=True
        )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Insights Geográficos
    st.markdown("### Insights Estratégicos Regionais")

    col1, col2 = st.columns(2)

    with col1:
        if top3_concentration > 60:
            st.markdown(
                create_insight_card(
                    "Risco de Concentração Geográfica",
                    f"{top3_concentration:.1f}% da receita concentrada em apenas 3 estados: {', '.join(state_perf.head(3)['estado'].tolist())}. Alta exposição a riscos econômicos e regulatórios regionais.",
                    "warning",
                    "Desenvolver plano de expansão focado em estados de médio porte com menor penetração (Nordeste e Centro-Oeste). Meta: reduzir concentração Top 3 para <55% em 12 meses.",
                    icon="⚠"
                ),
                unsafe_allow_html=True
            )

    with col2:
        # Identificar estados com maior potencial (baixa receita mas alta população)
        bottom_10_states = state_perf.tail(10)
        potential_states = bottom_10_states.head(5)['estado'].tolist()

        st.markdown(
            create_insight_card(
                "Oportunidades de Expansão",
                f"Estados sub-explorados identificados: {', '.join(potential_states)}. Representam apenas {bottom_10_states.head(5)['pct_receita'].sum():.2f}% da receita mas têm potencial de crescimento.",
                "action",
                "Priorizar investimento em marketing digital e parcerias locais nesses estados. Potencial estimado de +15-20% em receita com presença fortalecida.",
                icon="🎯"
            ),
            unsafe_allow_html=True
        )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Mapa de Receita por Estado
    st.markdown("### Distribuição Nacional de Receita")

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = go.Figure(data=go.Bar(
            x=state_perf['estado'],
            y=state_perf['receita'] / 1e6,
            marker=dict(
                color=state_perf['receita'],
                colorscale=[
                    [0, COLORS['light']],
                    [0.5, COLORS['gradient_start']],
                    [1, COLORS['gradient_end']]
                ],
                showscale=True,
                colorbar=dict(title="Receita<br>(R$ Mi)", x=1.15)
            ),
            text=state_perf['pct_receita'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Receita: R$ %{y:.1f}M<br>Participação: %{text}<extra></extra>'
        ))

        fig.update_layout(
            height=500,
            xaxis_title="Estado (UF)",
            yaxis_title="Receita (R$ Milhões)",
            xaxis_tickangle=-45,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'}
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Classificação por Performance")

        # Classificar estados em tiers
        state_perf_copy = state_perf.copy()
        state_perf_copy['tier'] = pd.cut(
            state_perf_copy['pct_receita'],
            bins=[0, 1, 5, 15, 100],
            labels=['Emergente', 'Crescimento', 'Consolidado', 'Estratégico']
        )

        tier_counts = state_perf_copy['tier'].value_counts()

        # Gráfico de pizza de tiers
        fig = go.Figure(data=[go.Pie(
            labels=tier_counts.index,
            values=tier_counts.values,
            hole=0.5,
            marker=dict(
                colors=[COLORS['neutral'], COLORS['warning'], COLORS['primary'], COLORS['secondary']],
                line=dict(color='white', width=2)
            ),
            textinfo='label+value',
            hovertemplate='%{label}<br>%{value} estados<br>%{percent}<extra></extra>'
        )])

        fig.update_layout(
            height=300,
            paper_bgcolor='white',
            font={'family': 'Inter, sans-serif'},
            annotations=[dict(text='Estados', x=0.5, y=0.5, font_size=14, showarrow=False)],
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # Métricas de tier
        for tier in ['Estratégico', 'Consolidado', 'Crescimento', 'Emergente']:
            tier_states = state_perf_copy[state_perf_copy['tier'] == tier]
            if not tier_states.empty:
                count = len(tier_states)
                revenue_pct = tier_states['pct_receita'].sum()

                tier_colors = {
                    'Estratégico': COLORS['secondary'],
                    'Consolidado': COLORS['primary'],
                    'Crescimento': COLORS['warning'],
                    'Emergente': COLORS['neutral']
                }

                st.markdown(f"""
                <div style="background: white; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem;
                            border-left: 4px solid {tier_colors[tier]}; box-shadow: 0 2px 4px rgba(0,0,0,0.08);">
                    <div style="font-size: 0.75rem; color: #708090;">{tier}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.3rem;">
                        <span style="font-size: 1.1rem; font-weight: 600; color: {tier_colors[tier]};">{count} UFs</span>
                        <span style="font-size: 0.9rem; color: #495057;">{revenue_pct:.1f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Comparação Top vs Bottom States
    st.markdown("### Análise Comparativa: Melhores vs Piores Desempenhos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏆 Top 10 Estados - Receita")

        top10 = state_perf.head(10)

        fig = go.Figure(data=[
            go.Bar(
                y=top10['estado'],
                x=top10['receita'] / 1e6,
                orientation='h',
                marker=dict(
                    color=COLORS['secondary'],
                    line=dict(color=COLORS['dark'], width=1)
                ),
                text=top10['pct_receita'].apply(lambda x: f'{x:.1f}%'),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Receita: R$ %{x:.1f}M<br>Unidades: %{customdata:,.0f}<extra></extra>',
                customdata=top10['unidades']
            )
        ])

        fig.update_layout(
            height=400,
            xaxis_title="Receita (R$ Milhões)",
            yaxis_title="",
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'}
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Top 10 Estados - Preço Médio")

        top10_price = state_perf.head(10).sort_values('preco_medio', ascending=False).head(10)

        fig = go.Figure(data=[
            go.Bar(
                y=top10_price['estado'],
                x=top10_price['preco_medio'],
                orientation='h',
                marker=dict(
                    color=COLORS['accent'],
                    line=dict(color=COLORS['dark'], width=1)
                ),
                text=top10_price['preco_medio'].apply(lambda x: f'R$ {x:.2f}'),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Preço Médio: R$ %{x:.2f}<extra></extra>'
            )
        ])

        fig.update_layout(
            height=400,
            xaxis_title="Preço Médio (R$)",
            yaxis_title="",
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'}
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Heatmap: Receita por Estado e Mês
    st.markdown("### Análise Temporal por Estado")

    # Preparar dados para heatmap (top 15 estados)
    top15_states = state_perf.head(15)['estado'].tolist()
    state_temporal_data = processor.pricing_data[processor.pricing_data['uf'].isin(top15_states)]

    if not state_temporal_data.empty:
        heatmap_data = state_temporal_data.groupby(['uf', 'mes'])['rbv'].sum().reset_index()
        heatmap_data['rbv_million'] = heatmap_data['rbv'] / 1e6

        fig = create_heatmap(
            heatmap_data,
            'mes',
            'uf',
            'rbv_million',
            'Receita Mensal por Estado (Top 15) - R$ Milhões'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Insights do heatmap
        col1, col2 = st.columns(2)

        with col1:
            # Estado com maior crescimento
            state_growth = {}
            for state in top15_states:
                state_data = heatmap_data[heatmap_data['uf'] == state].sort_values('mes')
                if len(state_data) >= 2:
                    first_month = state_data['rbv_million'].iloc[0]
                    last_month = state_data['rbv_million'].iloc[-1]
                    growth = ((last_month - first_month) / first_month * 100) if first_month > 0 else 0
                    state_growth[state] = growth

            if state_growth:
                best_growth_state = max(state_growth, key=state_growth.get)
                best_growth_value = state_growth[best_growth_state]

                st.markdown(
                    create_insight_card(
                        "Maior Crescimento Relativo",
                        f"{best_growth_state} apresentou crescimento de {best_growth_value:+.1f}% no período analisado - melhor performance de crescimento entre os top estados.",
                        "success",
                        f"Replicar estratégias de sucesso de {best_growth_state} em outros estados com perfil similar.",
                        icon="📈"
                    ),
                    unsafe_allow_html=True
                )

        with col2:
            # Estado com maior volatilidade
            state_volatility = {}
            for state in top15_states:
                state_data = heatmap_data[heatmap_data['uf'] == state]['rbv_million']
                if len(state_data) > 1:
                    volatility = state_data.std()
                    state_volatility[state] = volatility

            if state_volatility:
                most_volatile_state = max(state_volatility, key=state_volatility.get)
                volatility_value = state_volatility[most_volatile_state]

                st.markdown(
                    create_insight_card(
                        "Maior Volatilidade",
                        f"{most_volatile_state} apresenta maior volatilidade mensal (±R$ {volatility_value:.1f}M). Pode indicar sazonalidade forte ou inconsistência operacional.",
                        "warning",
                        f"Investigar causas da volatilidade em {most_volatile_state} e implementar ações para estabilizar operação.",
                        icon="⚠"
                    ),
                    unsafe_allow_html=True
                )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Ranking Completo
    st.markdown("### Ranking Completo de Estados")

    state_display = state_perf.copy()
    state_display['ranking'] = range(1, len(state_display) + 1)
    state_display['receita_per_capita'] = state_display['receita'] / 100000  # Aproximação

    display_cols = ['ranking', 'estado', 'receita', 'pct_receita', 'unidades', 'preco_medio']
    display_names = ['#', 'UF', 'Receita (R$)', '% Total', 'Unidades', 'Preço Médio']

    st.dataframe(
        state_display[display_cols].set_axis(display_names, axis=1).style.format({
            'Receita (R$)': 'R$ {:.0f}',
            '% Total': '{:.2f}%',
            'Unidades': '{:,.0f}',
            'Preço Médio': 'R$ {:.2f}'
        }).background_gradient(subset=['Receita (R$)'], cmap='Greens')
        .background_gradient(subset=['Preço Médio'], cmap='Oranges'),
        hide_index=True,
        use_container_width=True,
        height=500
    )

# ==================================================
# PÁGINA 5: OPORTUNIDADES DE CRESCIMENTO
# ==================================================

with tab5:
    st.markdown('<div class="main-header">Oportunidades de Crescimento</div>', unsafe_allow_html=True)
    st.markdown("Identificação e priorização de oportunidades para acelerar crescimento de receita e market share")

    # Calcular múltiplas oportunidades
    share_metrics = processor.get_market_share_metrics()
    zero_sales = processor.get_zero_sales_analysis()
    revenue_metrics = processor.get_revenue_metrics()

    # KPIs de Oportunidade
    st.markdown("### Panorama de Oportunidades")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_zero_scenarios = len(processor.iqvia_data[processor.iqvia_data['venda_rd'] == 0])
        st.markdown(
            create_kpi_card(
                "Cenários Venda Zero",
                total_zero_scenarios,
                format_type="number",
                status="critical"
            ),
            unsafe_allow_html=True
        )

    with col2:
        zero_rate = share_metrics['zero_sales_rate'] * 100
        st.markdown(
            create_kpi_card(
                "Taxa Venda Zero",
                zero_rate,
                format_type="percentage",
                status="critical"
            ),
            unsafe_allow_html=True
        )

    with col3:
        potential_units = zero_sales['venda_concorrente'].sum()
        st.markdown(
            create_kpi_card(
                "Potencial em Unidades",
                potential_units,
                format_type="number",
                status="attention"
            ),
            unsafe_allow_html=True
        )

    with col4:
        avg_price = revenue_metrics['avg_price']
        potential_revenue = potential_units * avg_price * 0.25  # Assumir captura de 25%
        st.markdown(
            create_kpi_card(
                "Potencial de Receita",
                potential_revenue,
                format_type="currency",
                status="attention"
            ),
            unsafe_allow_html=True
        )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Priorização de Oportunidades
    st.markdown("### Matriz de Priorização de Oportunidades")

    # Calcular scores para cada produto com venda zero
    opportunity_matrix = zero_sales.head(50).copy()
    opportunity_matrix['impacto'] = opportunity_matrix['venda_concorrente'] / opportunity_matrix['venda_concorrente'].max() * 100
    opportunity_matrix['facilidade'] = (1 - (opportunity_matrix['lojas_afetadas'] / opportunity_matrix['lojas_afetadas'].max())) * 100

    col1, col2 = st.columns([2, 1])

    with col1:
        # Scatter plot de priorização
        fig = go.Figure()

        # Definir quadrantes
        avg_impacto = opportunity_matrix['impacto'].mean()
        avg_facilidade = opportunity_matrix['facilidade'].mean()

        # Colorir por quadrante
        colors_priority = []
        priority_labels = []
        for _, row in opportunity_matrix.iterrows():
            if row['impacto'] >= avg_impacto and row['facilidade'] >= avg_facilidade:
                colors_priority.append(COLORS['secondary'])  # Quick Wins
                priority_labels.append('Quick Win')
            elif row['impacto'] >= avg_impacto:
                colors_priority.append(COLORS['primary'])  # Major Projects
                priority_labels.append('Projeto Maior')
            elif row['facilidade'] >= avg_facilidade:
                colors_priority.append(COLORS['warning'])  # Fill-ins
                priority_labels.append('Complementar')
            else:
                colors_priority.append(COLORS['neutral'])  # Thankless Tasks
                priority_labels.append('Baixa Prioridade')

        opportunity_matrix['priority'] = priority_labels

        fig.add_trace(
            go.Scatter(
                x=opportunity_matrix['facilidade'],
                y=opportunity_matrix['impacto'],
                mode='markers',
                marker=dict(
                    size=opportunity_matrix['venda_concorrente'] / 10000,
                    color=colors_priority,
                    line=dict(color=COLORS['dark'], width=1),
                    opacity=0.7
                ),
                text=opportunity_matrix['produto'],
                hovertemplate='<b>%{text}</b><br>Impacto: %{y:.0f}<br>Facilidade: %{x:.0f}<br>Vendas Concorrentes: %{customdata:,.0f}<extra></extra>',
                customdata=opportunity_matrix['venda_concorrente']
            )
        )

        # Linhas de quadrante
        fig.add_hline(y=avg_impacto, line_dash="dash", line_color=COLORS['neutral'], opacity=0.5)
        fig.add_vline(x=avg_facilidade, line_dash="dash", line_color=COLORS['neutral'], opacity=0.5)

        # Anotações de quadrantes
        fig.add_annotation(x=75, y=75, text="<b>Quick Wins</b><br>(Alta prioridade)", showarrow=False,
                          font=dict(size=12, color=COLORS['secondary']), opacity=0.7)
        fig.add_annotation(x=25, y=75, text="<b>Projetos Maiores</b><br>(Alto impacto)", showarrow=False,
                          font=dict(size=12, color=COLORS['primary']), opacity=0.7)
        fig.add_annotation(x=75, y=25, text="<b>Complementares</b><br>(Baixo esforço)", showarrow=False,
                          font=dict(size=12, color=COLORS['warning']), opacity=0.7)
        fig.add_annotation(x=25, y=25, text="<b>Baixa Prioridade</b><br>(Evitar)", showarrow=False,
                          font=dict(size=12, color=COLORS['neutral']), opacity=0.7)

        fig.update_layout(
            title="Matriz Impacto × Facilidade (tamanho = vendas concorrentes)",
            height=500,
            xaxis_title="Facilidade de Implementação →",
            yaxis_title="Impacto Potencial →",
            xaxis=dict(range=[0, 105]),
            yaxis=dict(range=[0, 105]),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'}
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Distribuição por Prioridade")

        priority_counts = opportunity_matrix['priority'].value_counts()

        fig = go.Figure(data=[
            go.Bar(
                x=priority_counts.index,
                y=priority_counts.values,
                marker=dict(
                    color=[COLORS['secondary'], COLORS['primary'], COLORS['warning'], COLORS['neutral']],
                    line=dict(color=COLORS['dark'], width=2)
                ),
                text=priority_counts.values,
                textposition='outside',
                hovertemplate='%{x}<br>%{y} produtos<extra></extra>'
            )
        ])

        fig.update_layout(
            height=300,
            yaxis_title="Número de Produtos",
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'},
            xaxis_tickangle=-30
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

        # Recomendações por prioridade
        quick_wins = opportunity_matrix[opportunity_matrix['priority'] == 'Quick Win']

        st.markdown(
            create_insight_card(
                "Quick Wins Identificados",
                f"{len(quick_wins)} produtos com alto impacto e fácil implementação. Prioridade máxima para ação imediata.",
                "action",
                "Iniciar implementação em até 7 dias com foco total de operações e comercial.",
                icon="🎯"
            ),
            unsafe_allow_html=True
        )

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Top Quick Wins Detalhado
    st.markdown("### 🎯 Top 20 Quick Wins - Ação Imediata Recomendada")

    quick_wins_top = opportunity_matrix[opportunity_matrix['priority'] == 'Quick Win'].head(20)

    if not quick_wins_top.empty:
        # Calcular potencial de receita para cada produto
        quick_wins_top['potencial_receita'] = quick_wins_top['venda_concorrente'] * avg_price * 0.30

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=quick_wins_top['produto'],
                y=quick_wins_top['venda_concorrente'] / 1e3,
                name='Vendas Concorrentes (mil un)',
                marker_color=COLORS['accent'],
                opacity=0.7,
                yaxis='y',
                hovertemplate='%{x}<br>Concorrentes: %{y:.1f}k un<extra></extra>'
            )
        )

        fig.add_trace(
            go.Scatter(
                x=quick_wins_top['produto'],
                y=quick_wins_top['potencial_receita'] / 1e6,
                name='Potencial Receita (R$ Mi)',
                line=dict(color=COLORS['secondary'], width=3),
                mode='lines+markers',
                marker=dict(size=10),
                yaxis='y2',
                hovertemplate='%{x}<br>Potencial: R$ %{y:.2f}M<extra></extra>'
            )
        )

        fig.update_layout(
            title="Vendas dos Concorrentes e Potencial de Receita (captura de 30%)",
            height=450,
            xaxis_title="Código do Produto",
            yaxis=dict(title="Vendas Concorrentes (mil un)", side='left'),
            yaxis2=dict(title="Potencial de Receita (R$ Mi)", side='right', overlaying='y'),
            hovermode='x unified',
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'},
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_tickangle=-45
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

        # Tabela de Quick Wins
        st.markdown("#### Plano de Ação - Quick Wins")

        quick_wins_display = quick_wins_top.copy()
        quick_wins_display['ranking'] = range(1, len(quick_wins_display) + 1)
        quick_wins_display['prazo'] = 'Imediato (7 dias)'
        quick_wins_display['acao'] = 'Garantir estoque + Treinar equipe'

        display_cols = ['ranking', 'produto', 'venda_concorrente', 'lojas_afetadas', 'potencial_receita', 'prazo', 'acao']
        display_names = ['#', 'Produto', 'Vendas Concorrentes', 'Lojas', 'Potencial R$', 'Prazo', 'Ação']

        st.dataframe(
            quick_wins_display[display_cols].set_axis(display_names, axis=1).style.format({
                'Vendas Concorrentes': '{:,.0f} un',
                'Lojas': '{:,}',
                'Potencial R$': 'R$ {:.0f}'
            }).background_gradient(subset=['Potencial R$'], cmap='Greens'),
            hide_index=True,
            use_container_width=True,
            height=400
        )

        # ROI estimado
        total_investment_estimate = len(quick_wins_top) * 5000  # R$ 5k por produto (estoque, treinamento)
        total_potential_revenue = quick_wins_display['potencial_receita'].sum()
        roi = ((total_potential_revenue - total_investment_estimate) / total_investment_estimate * 100) if total_investment_estimate > 0 else 0

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Investimento Estimado", f"R$ {total_investment_estimate/1e3:.0f}K", help="Estoque + treinamento + marketing")

        with col2:
            st.metric("Potencial de Receita", f"R$ {total_potential_revenue/1e6:.1f}M", delta=f"+{roi:.0f}% ROI")

        with col3:
            payback_months = (total_investment_estimate / (total_potential_revenue / 12)) if total_potential_revenue > 0 else 0
            st.metric("Payback Estimado", f"{payback_months:.1f} meses", help="Tempo para retorno do investimento")

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Análise Pareto de Produtos
    st.markdown("### Curva ABC de Produtos - Lei de Pareto")

    product_revenue = processor.pricing_data.groupby('produto')['rbv'].sum().sort_values(ascending=False).reset_index()
    product_revenue['cumsum'] = product_revenue['rbv'].cumsum()
    product_revenue['cumsum_pct'] = (product_revenue['cumsum'] / product_revenue['rbv'].sum()) * 100
    product_revenue['ranking'] = range(1, len(product_revenue) + 1)
    product_revenue['pct_products'] = (product_revenue['ranking'] / len(product_revenue)) * 100

    # Classificação ABC
    product_revenue['classe'] = 'C'
    product_revenue.loc[product_revenue['cumsum_pct'] <= 80, 'classe'] = 'A'
    product_revenue.loc[(product_revenue['cumsum_pct'] > 80) & (product_revenue['cumsum_pct'] <= 95), 'classe'] = 'B'

    class_counts = product_revenue['classe'].value_counts()
    class_revenue = product_revenue.groupby('classe')['rbv'].sum()

    col1, col2 = st.columns([2, 1])

    with col1:
        # Curva de Pareto
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        sample_size = min(100, len(product_revenue))

        fig.add_trace(
            go.Bar(
                x=product_revenue.head(sample_size)['ranking'],
                y=product_revenue.head(sample_size)['rbv'] / 1e6,
                name='Receita Individual',
                marker_color=COLORS['primary'],
                opacity=0.6,
                hovertemplate='Ranking: %{x}<br>Receita: R$ %{y:.2f}M<extra></extra>'
            ),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(
                x=product_revenue.head(sample_size)['ranking'],
                y=product_revenue.head(sample_size)['cumsum_pct'],
                name='% Acumulado',
                line=dict(color=COLORS['accent'], width=4),
                mode='lines',
                hovertemplate='Ranking: %{x}<br>Acumulado: %{y:.1f}%<extra></extra>'
            ),
            secondary_y=True
        )

        # Linhas de referência
        fig.add_hline(y=80, line_dash="dash", line_color=COLORS['secondary'],
                     annotation_text="80% (Classe A)", secondary_y=True, annotation_position="left")
        fig.add_hline(y=95, line_dash="dot", line_color=COLORS['warning'],
                     annotation_text="95% (Classe B)", secondary_y=True, annotation_position="left")

        fig.update_xaxes(title_text="Ranking de Produtos")
        fig.update_yaxes(title_text="Receita Individual (R$ Mi)", secondary_y=False)
        fig.update_yaxes(title_text="% Acumulado da Receita", secondary_y=True, range=[0, 105])

        fig.update_layout(
            title="Curva ABC - Princípio de Pareto 80/20",
            height=450,
            hovermode='x unified',
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'},
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Classificação ABC")

        for classe in ['A', 'B', 'C']:
            count = class_counts.get(classe, 0)
            revenue = class_revenue.get(classe, 0)
            pct_products = (count / len(product_revenue)) * 100
            pct_revenue = (revenue / product_revenue['rbv'].sum()) * 100

            classe_colors = {'A': COLORS['secondary'], 'B': COLORS['warning'], 'C': COLORS['neutral']}
            classe_desc = {
                'A': '80% da receita',
                'B': '80-95% da receita',
                'C': '>95% da receita'
            }

            st.markdown(f"""
            <div style="background: white; padding: 1.2rem; border-radius: 10px; margin-bottom: 1rem;
                        border-left: 5px solid {classe_colors[classe]}; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 1.5rem; font-weight: 700; color: {classe_colors[classe]}; margin-bottom: 0.5rem;">
                    Classe {classe}
                </div>
                <div style="font-size: 0.8rem; color: #708090; margin-bottom: 0.8rem;">
                    {classe_desc[classe]}
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                    <span style="font-size: 0.85rem; color: #495057;">Produtos:</span>
                    <span style="font-size: 0.95rem; font-weight: 600; color: {COLORS['dark']};">{count:,}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                    <span style="font-size: 0.85rem; color: #495057;">% Produtos:</span>
                    <span style="font-size: 0.95rem; font-weight: 600; color: {COLORS['dark']};">{pct_products:.1f}%</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-size: 0.85rem; color: #495057;">% Receita:</span>
                    <span style="font-size: 1.1rem; font-weight: 700; color: {classe_colors[classe]};">{pct_revenue:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            create_insight_card(
                "Estratégia ABC",
                f"**Classe A** ({class_counts.get('A', 0):,} produtos): Gestão intensiva, nunca faltar em estoque.\n\n**Classe B** ({class_counts.get('B', 0):,} produtos): Monitoramento regular, otimizar mix.\n\n**Classe C** ({class_counts.get('C', 0):,} produtos): Avaliar descontinuação dos de baixíssimo giro.",
                "info",
                icon="📚"
            ),
            unsafe_allow_html=True
        )

# ==================================================
# PÁGINA 6: PROJEÇÕES E SIMULAÇÕES
# ==================================================

with tab6:
    st.markdown('<div class="main-header">Projeções e Simulações</div>', unsafe_allow_html=True)
    st.markdown("Predições baseadas em tendências e simulação de cenários de negócio")

    # Projeções de Receita e Market Share
    st.markdown("### Projeções para Próximos Períodos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💰 Projeção de Receita")

        predicted_revenue = processor.predict_next_month_revenue()

        if predicted_revenue:
            current_revenue = processor.get_revenue_metrics()['total_revenue']
            growth_rate = ((predicted_revenue - current_revenue) / current_revenue) * 100 if current_revenue > 0 else 0

            st.markdown(
                create_kpi_card(
                    "Receita Projetada (próximo mês)",
                    predicted_revenue,
                    delta=growth_rate,
                    format_type="currency",
                    status="good" if growth_rate > 0 else "attention"
                ),
                unsafe_allow_html=True
            )

            # Gráfico de tendência com projeção
            revenue_trend = processor.get_revenue_trend()
            last_date = revenue_trend['data'].max()
            next_date = last_date + pd.DateOffset(months=1)

            projection_df = pd.DataFrame({
                'data': [next_date],
                'receita': [predicted_revenue],
                'tipo': ['Projeção']
            })

            revenue_trend['tipo'] = 'Real'
            combined = pd.concat([revenue_trend[['data', 'receita', 'tipo']], projection_df])

            fig = go.Figure()

            # Dados reais
            real_data = combined[combined['tipo'] == 'Real']
            fig.add_trace(
                go.Scatter(
                    x=real_data['data'],
                    y=real_data['receita'] / 1e6,
                    mode='lines+markers',
                    name='Receita Real',
                    line=dict(color=COLORS['primary'], width=3),
                    marker=dict(size=8),
                    hovertemplate='%{x|%b/%Y}<br>Receita: R$ %{y:.1f}M<extra></extra>'
                )
            )

            # Projeção
            proj_data = combined[combined['tipo'] == 'Projeção']
            fig.add_trace(
                go.Scatter(
                    x=proj_data['data'],
                    y=proj_data['receita'] / 1e6,
                    mode='markers',
                    name='Projeção',
                    marker=dict(color=COLORS['accent'], size=20, symbol='star'),
                    hovertemplate='%{x|%b/%Y}<br>Projeção: R$ %{y:.1f}M<extra></extra>'
                )
            )

            # Linha de tendência
            fig.add_trace(
                go.Scatter(
                    x=combined['data'],
                    y=combined['receita'] / 1e6,
                    mode='lines',
                    name='Tendência',
                    line=dict(color=COLORS['secondary'], width=2, dash='dash'),
                    opacity=0.5,
                    hovertemplate='%{x|%b/%Y}<br>Tendência: R$ %{y:.1f}M<extra></extra>'
                )
            )

            fig.update_layout(
                height=400,
                xaxis_title="Período",
                yaxis_title="Receita (R$ Milhões)",
                hovermode='x unified',
                paper_bgcolor='white',
                plot_bgcolor='white',
                font={'family': 'Inter, sans-serif'},
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

            st.plotly_chart(fig, use_container_width=True)

            # Intervalo de confiança (simulado)
            std_dev = revenue_trend['receita'].std()
            lower_bound = predicted_revenue - (std_dev * 0.5)
            upper_bound = predicted_revenue + (std_dev * 0.5)

            st.info(f"**Intervalo de Confiança:** R$ {lower_bound/1e6:.1f}M - R$ {upper_bound/1e6:.1f}M (±{std_dev/1e6:.1f}M)")

    with col2:
        st.markdown("#### 📊 Projeção de Market Share")

        predicted_share = processor.predict_market_share()

        if predicted_share:
            current_share = processor.get_market_share_metrics()['avg_share']
            change = (predicted_share - current_share) * 100

            st.markdown(
                create_kpi_card(
                    "Market Share Projetado",
                    predicted_share * 100,
                    delta=change,
                    delta_text="vs atual (pp)",
                    format_type="percentage",
                    status="excellent" if predicted_share >= 0.40 else "attention"
                ),
                unsafe_allow_html=True
            )

            # Gráfico
            share_trend = processor.get_market_share_trend()
            last_date = share_trend['data'].max()
            next_date = last_date + pd.DateOffset(months=1)

            projection_df = pd.DataFrame({
                'data': [next_date],
                'share': [predicted_share],
                'tipo': ['Projeção']
            })

            share_trend['tipo'] = 'Real'
            combined = pd.concat([share_trend[['data', 'share', 'tipo']], projection_df])

            fig = go.Figure()

            # Dados reais
            real_data = combined[combined['tipo'] == 'Real']
            fig.add_trace(
                go.Scatter(
                    x=real_data['data'],
                    y=real_data['share'] * 100,
                    mode='lines+markers',
                    name='Share Real',
                    line=dict(color=COLORS['secondary'], width=3),
                    marker=dict(size=8),
                    fill='tozeroy',
                    fillcolor=f'rgba(0, 168, 107, 0.1)',
                    hovertemplate='%{x|%b/%Y}<br>Share: %{y:.2f}%<extra></extra>'
                )
            )

            # Projeção
            proj_data = combined[combined['tipo'] == 'Projeção']
            fig.add_trace(
                go.Scatter(
                    x=proj_data['data'],
                    y=proj_data['share'] * 100,
                    mode='markers',
                    name='Projeção',
                    marker=dict(color=COLORS['danger'], size=20, symbol='star'),
                    hovertemplate='%{x|%b/%Y}<br>Projeção: %{y:.2f}%<extra></extra>'
                )
            )

            # Meta
            fig.add_hline(
                y=40,
                line_dash="dash",
                line_color=COLORS['accent'],
                line_width=2,
                annotation_text="Meta: 40%",
                annotation_position="right"
            )

            fig.update_layout(
                height=400,
                xaxis_title="Período",
                yaxis_title="Market Share (%)",
                hovermode='x unified',
                paper_bgcolor='white',
                plot_bgcolor='white',
                font={'family': 'Inter, sans-serif'},
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(range=[0, 50])
            )

            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

            st.plotly_chart(fig, use_container_width=True)

            # Gap para meta
            gap_to_target = 40 - (predicted_share * 100)

            if gap_to_target > 0:
                st.warning(f"**Gap para Meta:** {gap_to_target:.1f}pp - Ações adicionais necessárias para atingir 40%")
            else:
                st.success(f"**Meta Atingida:** Projeção de {predicted_share*100:.1f}% supera a meta de 40%!")

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Simulação de Cenários
    st.markdown("### Simulação de Cenários de Negócio")
    st.markdown("Explore o impacto de diferentes estratégias e iniciativas na receita")

    scenarios = processor.calculate_scenarios()

    # Cards de cenários
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['neutral']} 0%, #95a5a6 100%);
                    color: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <div style="font-size: 0.9rem; margin-bottom: 0.5rem; opacity: 0.9;">CENÁRIO ATUAL</div>
            <div style="font-size: 2rem; font-weight: 700;">R$ {scenarios['current']/1e9:.2f}B</div>
            <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.9;">Baseline</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        impact_1 = ((scenarios['reduce_zero_sales'] - scenarios['current']) / scenarios['current']) * 100
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['secondary']} 0%, #27ae60 100%);
                    color: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <div style="font-size: 0.9rem; margin-bottom: 0.5rem; opacity: 0.9;">REDUZIR VENDA ZERO</div>
            <div style="font-size: 2rem; font-weight: 700;">R$ {scenarios['reduce_zero_sales']/1e9:.2f}B</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem; font-weight: 600;">+{impact_1:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        impact_2 = ((scenarios['increase_share'] - scenarios['current']) / scenarios['current']) * 100
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['primary']} 0%, #2980b9 100%);
                    color: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <div style="font-size: 0.9rem; margin-bottom: 0.5rem; opacity: 0.9;">AUMENTAR SHARE 5pp</div>
            <div style="font-size: 2rem; font-weight: 700;">R$ {scenarios['increase_share']/1e9:.2f}B</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem; font-weight: 600;">+{impact_2:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        impact_3 = ((scenarios['optimize_mix'] - scenarios['current']) / scenarios['current']) * 100
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['gradient_start']} 0%, {COLORS['gradient_end']} 100%);
                    color: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <div style="font-size: 0.9rem; margin-bottom: 0.5rem; opacity: 0.9;">OTIMIZAR MIX</div>
            <div style="font-size: 2rem; font-weight: 700;">R$ {scenarios['optimize_mix']/1e9:.2f}B</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem; font-weight: 600;">+{impact_3:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

    # Gráfico comparativo de cenários
    col1, col2 = st.columns([2, 1])

    with col1:
        scenario_names = ['Atual', 'Reduzir\nVenda Zero\n(-50%)', 'Aumentar\nShare\n(+5pp)', 'Otimizar\nMix\n(Top 20%)']
        scenario_values = [
            scenarios['current'],
            scenarios['reduce_zero_sales'],
            scenarios['increase_share'],
            scenarios['optimize_mix']
        ]
        scenario_colors = [COLORS['neutral'], COLORS['secondary'], COLORS['primary'], COLORS['gradient_start']]

        fig = go.Figure(data=[
            go.Bar(
                x=scenario_names,
                y=[v / 1e9 for v in scenario_values],
                marker=dict(
                    color=scenario_colors,
                    line=dict(color=COLORS['dark'], width=2)
                ),
                text=[f'R$ {v/1e9:.2f}B<br>{((v-scenarios["current"])/scenarios["current"]*100):+.1f}%'
                      if v != scenarios['current'] else f'R$ {v/1e9:.2f}B'
                      for v in scenario_values],
                textposition='outside',
                hovertemplate='%{x}<br>Receita: R$ %{y:.2f}B<extra></extra>'
            )
        ])

        fig.update_layout(
            title="Comparação de Cenários - Receita Potencial",
            height=450,
            yaxis_title="Receita (R$ Bilhões)",
            yaxis=dict(range=[0, max(scenario_values)/1e9 * 1.2]),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter, sans-serif'}
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Detalhamento de Cenários")

        scenarios_detail = [
            {
                'name': 'Reduzir Venda Zero',
                'description': 'Reduzir taxa de venda zero de produtos em 50% através de melhor distribuição',
                'upside': scenarios['reduce_zero_sales'] - scenarios['current'],
                'difficulty': 'Média',
                'timeline': '3-6 meses'
            },
            {
                'name': 'Aumentar Share',
                'description': 'Conquistar 5pp de market share dos concorrentes',
                'upside': scenarios['increase_share'] - scenarios['current'],
                'difficulty': 'Alta',
                'timeline': '6-12 meses'
            },
            {
                'name': 'Otimizar Mix',
                'description': 'Crescer 20% adicional nos top 20% de produtos (Classe A)',
                'upside': scenarios['optimize_mix'] - scenarios['current'],
                'difficulty': 'Baixa',
                'timeline': '1-3 meses'
            }
        ]

        for scenario in scenarios_detail:
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;
                        border-left: 5px solid {COLORS['primary']}; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="font-weight: 600; color: {COLORS['dark']}; margin-bottom: 0.5rem;">{scenario['name']}</div>
                <div style="font-size: 0.85rem; color: #495057; margin-bottom: 0.8rem;">{scenario['description']}</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                    <span style="font-size: 0.8rem; color: #708090;">Upside:</span>
                    <span style="font-size: 0.9rem; font-weight: 600; color: {COLORS['secondary']};">+R$ {scenario['upside']/1e6:.0f}M</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                    <span style="font-size: 0.8rem; color: #708090;">Dificuldade:</span>
                    <span style="font-size: 0.85rem;">{scenario['difficulty']}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-size: 0.8rem; color: #708090;">Timeline:</span>
                    <span style="font-size: 0.85rem;">{scenario['timeline']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Análise de Sensibilidade Interativa
    st.markdown("### Análise de Sensibilidade - Market Share")
    st.markdown("Simule diferentes níveis de aumento de market share e veja o impacto na receita")

    share_increase = st.slider(
        "Aumento de Market Share (pontos percentuais)",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.5,
        help="Ajuste o slider para ver o impacto de diferentes níveis de market share na receita"
    )

    current_metrics = processor.get_revenue_metrics()
    current_share_val = processor.get_market_share_metrics()['avg_share']

    # Calcular impacto
    share_multiplier = (current_share_val + (share_increase / 100)) / current_share_val if current_share_val > 0 else 1
    projected_revenue = current_metrics['total_revenue'] * share_multiplier
    revenue_increase = projected_revenue - current_metrics['total_revenue']

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Market Share Atual",
            f"{current_share_val * 100:.1f}%"
        )

    with col2:
        st.metric(
            "Market Share Projetado",
            f"{(current_share_val + share_increase/100) * 100:.1f}%",
            f"+{share_increase:.1f}pp"
        )

    with col3:
        st.metric(
            "Receita Projetada",
            f"R$ {projected_revenue/1e9:.2f}B",
            f"+{(revenue_increase / current_metrics['total_revenue'] * 100):.1f}%"
        )

    with col4:
        st.metric(
            "Impacto Financeiro",
            f"+R$ {revenue_increase / 1e6:.0f}M",
            "Incremental"
        )

    # Gráfico de sensibilidade
    share_range = np.arange(0, 16, 0.5)
    revenue_range = [
        current_metrics['total_revenue'] * ((current_share_val + (s/100)) / current_share_val)
        for s in share_range
    ]

    fig = go.Figure()

    # Linha de sensibilidade
    fig.add_trace(
        go.Scatter(
            x=share_range,
            y=[r / 1e9 for r in revenue_range],
            mode='lines',
            name='Receita Projetada',
            line=dict(color=COLORS['primary'], width=3),
            fill='tozeroy',
            fillcolor=f'rgba(0, 102, 204, 0.1)',
            hovertemplate='Share +%{x:.1f}pp<br>Receita: R$ %{y:.2f}B<extra></extra>'
        )
    )

    # Marcar ponto selecionado
    fig.add_trace(
        go.Scatter(
            x=[share_increase],
            y=[projected_revenue / 1e9],
            mode='markers',
            name='Cenário Selecionado',
            marker=dict(color=COLORS['accent'], size=20, symbol='star',
                       line=dict(color=COLORS['dark'], width=2)),
            hovertemplate='Share +%{x:.1f}pp<br>Receita: R$ %{y:.2f}B<extra></extra>'
        )
    )

    # Linha de receita atual
    fig.add_hline(
        y=current_metrics['total_revenue'] / 1e9,
        line_dash="dash",
        line_color=COLORS['neutral'],
        annotation_text="Receita Atual",
        annotation_position="left"
    )

    fig.update_layout(
        title="Curva de Sensibilidade: Market Share × Receita",
        height=400,
        xaxis_title="Aumento de Market Share (pontos percentuais)",
        yaxis_title="Receita Projetada (R$ Bilhões)",
        hovermode='x unified',
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'family': 'Inter, sans-serif'},
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

    st.plotly_chart(fig, use_container_width=True)

    # Cálculo de ROI por ponto percentual
    if share_increase > 0:
        revenue_per_point = revenue_increase / share_increase
        st.success(f"**Análise:** Cada ponto percentual de aumento no market share gera aproximadamente R$ {revenue_per_point/1e6:.1f}M em receita adicional")

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Recomendações Finais
    st.markdown("### Recomendações Estratégicas Baseadas nas Simulações")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            create_insight_card(
                "Estratégia de Curto Prazo (1-3 meses)",
                "**Prioridade: Otimizar Mix de Produtos**\n\n"
                f"- Foco nos produtos Classe A (top 20%)\n"
                f"- Potencial de +R$ {(scenarios['optimize_mix']-scenarios['current'])/1e6:.0f}M\n"
                f"- Baixa complexidade de implementação\n"
                f"- ROI rápido e alto",
                "action",
                "Implementar campanha de push para produtos top, garantir disponibilidade 100%, negociar melhores margens com fornecedores.",
                icon="🎯"
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            create_insight_card(
                "Estratégia de Médio Prazo (3-6 meses)",
                "**Prioridade: Reduzir Vendas Zero**\n\n"
                f"- Atacar {share_metrics['zero_sales_rate']*100:.1f}% de cenários com venda zero\n"
                f"- Potencial de +R$ {(scenarios['reduce_zero_sales']-scenarios['current'])/1e6:.0f}M\n"
                f"- Melhorar distribuição e disponibilidade\n"
                f"- Sistema de alerta de ruptura",
                "action",
                "Revisar logística, implementar reposição automática, treinar equipe de vendas nos produtos críticos.",
                icon="📦"
            ),
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            create_insight_card(
                "Estratégia de Longo Prazo (6-12 meses)",
                "**Prioridade: Conquistar Market Share**\n\n"
                f"- Meta de +{share_increase:.1f}pp em market share\n"
                f"- Potencial de +R$ {revenue_increase/1e6:.0f}M\n"
                f"- Campanha competitiva agressiva\n"
                f"- Expansão de cobertura geográfica",
                "info",
                "Desenvolver proposta de valor diferenciada, investir em marketing, melhorar experiência do cliente, parcerias estratégicas.",
                icon="📈"
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            create_insight_card(
                "Estratégia Combinada (Máximo Potencial)",
                "**Abordagem Integrada**\n\n"
                f"Implementando todas as estratégias de forma sequencial:\n\n"
                f"1. Otimizar Mix: +R$ {(scenarios['optimize_mix']-scenarios['current'])/1e6:.0f}M\n"
                f"2. Reduzir Venda Zero: +R$ {(scenarios['reduce_zero_sales']-scenarios['current'])/1e6:.0f}M\n"
                f"3. Ganhar Share: +R$ {revenue_increase/1e6:.0f}M\n\n"
                f"**Total potencial: +R$ {((scenarios['optimize_mix']-scenarios['current']) + (scenarios['reduce_zero_sales']-scenarios['current']) + revenue_increase)/1e6:.0f}M**",
                "success",
                "Roadmap executivo de 12 meses com milestones trimestrais e KPIs de acompanhamento.",
                icon="🏆"
            ),
            unsafe_allow_html=True
        )

# ==================================================
# TAB 7: ANÁLISE COMPETITIVA BH
# ==================================================

with tab7:
    st.markdown('<div class="main-header">🏙️ Análise Competitiva - Belo Horizonte (MG)</div>', unsafe_allow_html=True)
    st.markdown("Análise profunda da competitividade em BH: Market Share, Concorrência e Oportunidades")

    # Filtrar dados de MG
    pricing_mg = processor.get_filtered_pricing_data()
    pricing_mg = pricing_mg[pricing_mg['uf'] == 'MG']

    if len(pricing_mg) == 0:
        st.warning("⚠️ Nenhum dado disponível para Minas Gerais no período selecionado")
    else:
        # KPIs Principais de MG
        st.markdown("### 📊 Performance Geral - Minas Gerais")
        col1, col2, col3, col4 = st.columns(4)

        receita_mg = pricing_mg['rbv'].sum()
        unidades_mg = pricing_mg['qt_unidade_vendida'].sum()
        ticket_mg = receita_mg / unidades_mg if unidades_mg > 0 else 0
        produtos_mg = pricing_mg['produto'].nunique()

        with col1:
            create_kpi_card(
                "Receita Total MG",
                receita_mg,
                format_type="currency",
                tooltip="Soma total de vendas (RBV) em Minas Gerais"
            )

        with col2:
            create_kpi_card(
                "Unidades Vendidas",
                unidades_mg,
                format_type="number",
                tooltip="Total de unidades vendidas em MG"
            )

        with col3:
            create_kpi_card(
                "Ticket Médio MG",
                ticket_mg,
                format_type="currency",
                tooltip="Receita Total / Unidades Vendidas"
            )

        with col4:
            create_kpi_card(
                "SKUs Ativos",
                produtos_mg,
                format_type="number",
                tooltip="Produtos únicos vendidos em MG"
            )

        st.markdown("---")

        # Market Share Intelligence BH
        st.markdown("### 🎯 Market Share & Competitividade")

        # Dados IQVIA para análise competitiva
        iqvia_data = processor.get_filtered_iqvia_data()

        if len(iqvia_data) > 0:
            col1, col2 = st.columns(2)

            with col1:
                # Market Share Evolution
                ms_trend = processor.get_market_share_trend()
                if len(ms_trend) > 0:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=ms_trend['data'],
                        y=ms_trend['share'],
                        mode='lines+markers',
                        name='Market Share RD',
                        line=dict(color=COLORS['primary'], width=3),
                        marker=dict(size=8)
                    ))
                    fig.update_layout(
                        title="Evolução do Market Share - MG",
                        xaxis_title="Período",
                        yaxis_title="Share (%)",
                        yaxis_ticksuffix="%",
                        template="plotly_white",
                        height=350
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Vendas RD vs Concorrente
                ms_data = processor.get_market_share_metrics()
                if ms_data and 'venda_rd' in ms_data and 'venda_concorrente' in ms_data:
                    vendas_rd = ms_data['venda_rd']
                    vendas_conc = ms_data['venda_concorrente']

                    fig = go.Figure(data=[
                        go.Bar(name='Raia Drogasil', x=['Vendas'], y=[vendas_rd], marker_color=COLORS['secondary']),
                        go.Bar(name='Concorrência', x=['Vendas'], y=[vendas_conc], marker_color=COLORS['danger'])
                    ])
                    fig.update_layout(
                        title="RD vs Concorrência - Volume de Vendas",
                        yaxis_title="Unidades",
                        template="plotly_white",
                        barmode='group',
                        height=350
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📊 Dados de competitividade (IQVIA) não disponíveis para o período selecionado")

        st.markdown("---")

        # Análise por Categoria em MG
        st.markdown("### 🏷️ Performance por Categoria - MG")

        cat_performance = pricing_mg.groupby('neogrupo').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'produto': 'nunique'
        }).reset_index()
        cat_performance.columns = ['Categoria', 'Receita', 'Unidades', 'SKUs']
        cat_performance = cat_performance.sort_values('Receita', ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            # Receita por categoria
            fig = px.bar(
                cat_performance.head(10),
                x='Receita',
                y='Categoria',
                orientation='h',
                title="Top 10 Categorias por Receita - MG",
                color='Receita',
                color_continuous_scale='Blues'
            )
            fig.update_layout(template="plotly_white", height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Unidades por categoria
            fig = px.bar(
                cat_performance.head(10),
                x='Unidades',
                y='Categoria',
                orientation='h',
                title="Top 10 Categorias por Volume - MG",
                color='Unidades',
                color_continuous_scale='Greens'
            )
            fig.update_layout(template="plotly_white", height=400)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Evolução Temporal MG
        st.markdown("### 📈 Evolução Temporal - Minas Gerais")

        temporal_mg = pricing_mg.groupby('mes').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum'
        }).reset_index().sort_values('mes')
        temporal_mg['ticket_medio'] = temporal_mg['rbv'] / temporal_mg['qt_unidade_vendida']

        col1, col2 = st.columns(2)

        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=temporal_mg['mes'],
                y=temporal_mg['rbv'],
                mode='lines+markers',
                name='Receita',
                line=dict(color=COLORS['primary'], width=3),
                marker=dict(size=10),
                fill='tozeroy'
            ))
            fig.update_layout(
                title="Evolução da Receita - MG",
                xaxis_title="Mês",
                yaxis_title="Receita (R$)",
                template="plotly_white",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=temporal_mg['mes'],
                y=temporal_mg['ticket_medio'],
                mode='lines+markers',
                name='Ticket Médio',
                line=dict(color=COLORS['secondary'], width=3),
                marker=dict(size=10)
            ))
            fig.update_layout(
                title="Evolução do Ticket Médio - MG",
                xaxis_title="Mês",
                yaxis_title="Ticket Médio (R$)",
                template="plotly_white",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Insights e Recomendações
        st.markdown("### 💡 Insights Estratégicos - BH/MG")

        # Calcular métricas chave
        share_atual = ms_data.get('share', 0) if (ms_data and isinstance(ms_data, dict)) else 0
        crescimento_receita = ((temporal_mg['rbv'].iloc[-1] - temporal_mg['rbv'].iloc[0]) / temporal_mg['rbv'].iloc[0] * 100) if len(temporal_mg) > 1 else 0

        insights_bh = []

        if share_atual > 0 and share_atual < 35:
            insights_bh.append({
                'emoji': '⚠️',
                'title': 'Market Share Abaixo da Média',
                'description': f'Market share de {share_atual:.1f}% está abaixo da meta. Análise de concorrência é crucial.',
                'action': 'Investigar estratégias dos concorrentes e identificar gaps de portfolio'
            })

        if crescimento_receita < 0:
            insights_bh.append({
                'emoji': '📉',
                'title': 'Queda na Receita',
                'description': f'Receita apresentou queda de {abs(crescimento_receita):.1f}% no período.',
                'action': 'Revisar estratégia de precificação e disponibilidade de produtos'
            })
        elif crescimento_receita > 10:
            insights_bh.append({
                'emoji': '📈',
                'title': 'Crescimento Positivo',
                'description': f'Receita cresceu {crescimento_receita:.1f}% no período.',
                'action': 'Manter estratégia atual e expandir para categorias similares'
            })

        # Análise de concentração
        top3_receita = cat_performance.head(3)['Receita'].sum()
        concentracao = (top3_receita / receita_mg * 100) if receita_mg > 0 else 0

        if concentracao > 70:
            insights_bh.append({
                'emoji': '🎯',
                'title': 'Alta Concentração de Receita',
                'description': f'{concentracao:.1f}% da receita vem das top 3 categorias.',
                'action': 'Diversificar portfolio para reduzir dependência de poucas categorias'
            })

        # Exibir insights
        for insight in insights_bh:
            st.markdown(f"""
            <div class="insight-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{insight['emoji']}</div>
                <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: {COLORS['dark']};">
                    {insight['title']}
                </div>
                <div style="font-size: 0.95rem; margin-bottom: 0.75rem; color: {COLORS['neutral']};">
                    {insight['description']}
                </div>
                <div style="font-size: 0.9rem; padding: 0.5rem; background-color: {COLORS['light']}; border-radius: 4px; border-left: 3px solid {COLORS['primary']};">
                    <strong>Ação Recomendada:</strong> {insight['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        if not insights_bh:
            st.success("✅ Performance sólida em MG. Continuar monitorando métricas-chave.")

# ==================================================
# TAB 8: QUALIDADE DOS DADOS
# ==================================================

with tab8:
    st.markdown('<div class="main-header">🔍 Qualidade dos Dados</div>', unsafe_allow_html=True)
    st.markdown("Análise detalhada da qualidade, completude e consistência dos dados carregados")

    # Obter dados
    pricing_data = processor.get_filtered_pricing_data()
    iqvia_data = processor.get_filtered_iqvia_data()

    # Resumo Geral
    st.markdown("### 📊 Resumo dos Dados Carregados")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        create_kpi_card(
            "Registros Pricing",
            len(pricing_data),
            format_type="number",
            tooltip="Total de registros na base de preços"
        )

    with col2:
        create_kpi_card(
            "Registros IQVIA",
            len(iqvia_data),
            format_type="number",
            tooltip="Total de registros na base IQVIA"
        )

    with col3:
        periodo_pricing = f"{pricing_data['mes'].min().strftime('%b/%Y')} - {pricing_data['mes'].max().strftime('%b/%Y')}" if len(pricing_data) > 0 else "N/A"
        st.metric("Período Pricing", periodo_pricing)

    with col4:
        periodo_iqvia = f"{iqvia_data['data'].min().strftime('%b/%Y')} - {iqvia_data['data'].max().strftime('%b/%Y')}" if len(iqvia_data) > 0 else "N/A"
        st.metric("Período IQVIA", periodo_iqvia)

    st.markdown("---")

    # Análise de Completude - Pricing
    st.markdown("### 📋 Completude dos Dados - Pricing")

    col1, col2 = st.columns(2)

    with col1:
        if len(pricing_data) > 0:
            # Calcular missing values
            missing_data = pd.DataFrame({
                'Coluna': pricing_data.columns,
                'Total': len(pricing_data),
                'Missing': pricing_data.isnull().sum(),
                'Missing %': (pricing_data.isnull().sum() / len(pricing_data) * 100).round(2)
            }).sort_values('Missing %', ascending=False)

            fig = px.bar(
                missing_data[missing_data['Missing %'] > 0],
                x='Missing %',
                y='Coluna',
                orientation='h',
                title="Dados Ausentes por Coluna - Pricing",
                color='Missing %',
                color_continuous_scale='Reds'
            )
            fig.update_layout(template="plotly_white", height=300)
            st.plotly_chart(fig, use_container_width=True)

            if missing_data['Missing %'].sum() == 0:
                st.success("✅ Nenhum dado ausente na base Pricing!")

    with col2:
        if len(pricing_data) > 0:
            # Estatísticas descritivas
            st.markdown("**Estatísticas Pricing**")
            stats = pd.DataFrame({
                'Métrica': ['Produtos Únicos', 'UFs', 'Canais', 'Neogrupos', 'Meses'],
                'Valor': [
                    pricing_data['produto'].nunique(),
                    pricing_data['uf'].nunique(),
                    pricing_data['canal'].nunique(),
                    pricing_data['neogrupo'].nunique(),
                    pricing_data['mes'].nunique()
                ]
            })
            st.dataframe(stats, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Análise de Completude - IQVIA
    st.markdown("### 📋 Completude dos Dados - IQVIA")

    col1, col2 = st.columns(2)

    with col1:
        if len(iqvia_data) > 0:
            # Calcular missing values
            missing_iqvia = pd.DataFrame({
                'Coluna': iqvia_data.columns,
                'Total': len(iqvia_data),
                'Missing': iqvia_data.isnull().sum(),
                'Missing %': (iqvia_data.isnull().sum() / len(iqvia_data) * 100).round(2)
            }).sort_values('Missing %', ascending=False)

            fig = px.bar(
                missing_iqvia[missing_iqvia['Missing %'] > 0],
                x='Missing %',
                y='Coluna',
                orientation='h',
                title="Dados Ausentes por Coluna - IQVIA",
                color='Missing %',
                color_continuous_scale='Reds'
            )
            fig.update_layout(template="plotly_white", height=300)
            st.plotly_chart(fig, use_container_width=True)

            if missing_iqvia['Missing %'].sum() == 0:
                st.success("✅ Nenhum dado ausente na base IQVIA!")

    with col2:
        if len(iqvia_data) > 0:
            # Estatísticas descritivas
            st.markdown("**Estatísticas IQVIA**")
            stats_iqvia = pd.DataFrame({
                'Métrica': ['Produtos Únicos', 'Períodos', 'Share Médio (%)', 'Vendas RD Total', 'Vendas Conc. Total'],
                'Valor': [
                    f"{iqvia_data['cd_produto'].nunique():,}",
                    iqvia_data['id_periodo'].nunique(),
                    f"{iqvia_data['share'].mean():.1f}%",
                    f"{iqvia_data['venda_rd'].sum():,.0f}",
                    f"{iqvia_data['venda_concorrente'].sum():,.0f}"
                ]
            })
            st.dataframe(stats_iqvia, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Análise de Consistência
    st.markdown("### ✅ Verificações de Consistência")

    checks = []

    # Check 1: Datas válidas
    if len(pricing_data) > 0:
        datas_validas = pricing_data['mes'].notna().all()
        checks.append({
            'Check': 'Datas válidas (Pricing)',
            'Status': '✅ OK' if datas_validas else '❌ Erro',
            'Descrição': 'Todas as datas são válidas' if datas_validas else 'Existem datas inválidas'
        })

    # Check 2: Valores numéricos positivos
    if len(pricing_data) > 0:
        valores_positivos = (pricing_data['rbv'] >= 0).all() and (pricing_data['qt_unidade_vendida'] >= 0).all()
        checks.append({
            'Check': 'Valores positivos (Pricing)',
            'Status': '✅ OK' if valores_positivos else '⚠️ Aviso',
            'Descrição': 'RBV e quantidades são positivas' if valores_positivos else 'Existem valores negativos'
        })

    # Check 3: Produtos duplicados
    if len(pricing_data) > 0:
        duplicados = pricing_data.duplicated(subset=['mes', 'produto', 'uf', 'canal', 'neogrupo']).sum()
        sem_duplicados = duplicados == 0
        checks.append({
            'Check': 'Registros duplicados (Pricing)',
            'Status': '✅ OK' if sem_duplicados else f'⚠️ {duplicados} duplicados',
            'Descrição': 'Nenhum registro duplicado' if sem_duplicados else f'{duplicados} registros duplicados encontrados'
        })

    # Check 4: Market share válido (0-100%)
    if len(iqvia_data) > 0 and 'share' in iqvia_data.columns:
        share_valido = ((iqvia_data['share'] >= 0) & (iqvia_data['share'] <= 100)).all()
        checks.append({
            'Check': 'Market Share válido (IQVIA)',
            'Status': '✅ OK' if share_valido else '❌ Erro',
            'Descrição': 'Share entre 0-100%' if share_valido else 'Existem valores de share inválidos'
        })

    # Check 5: Consistência temporal
    if len(pricing_data) > 0:
        meses_consecutivos = pricing_data.groupby('mes').size().reset_index().sort_values('mes')
        gaps = (meses_consecutivos['mes'].diff() > pd.Timedelta(days=35)).sum()
        sem_gaps = gaps == 0
        checks.append({
            'Check': 'Continuidade temporal (Pricing)',
            'Status': '✅ OK' if sem_gaps else f'⚠️ {gaps} gaps',
            'Descrição': 'Dados mensais contínuos' if sem_gaps else f'{gaps} gaps temporais encontrados'
        })

    # Exibir checks
    checks_df = pd.DataFrame(checks)
    st.dataframe(checks_df, use_container_width=True, hide_index=True)

    # Resumo de qualidade
    total_checks = len(checks)
    checks_ok = len([c for c in checks if c['Status'].startswith('✅')])
    qualidade_score = (checks_ok / total_checks * 100) if total_checks > 0 else 0

    st.markdown("---")
    st.markdown("### 🎯 Score de Qualidade")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=qualidade_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Qualidade Geral dos Dados"},
            delta={'reference': 90},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': COLORS['primary']},
                'steps': [
                    {'range': [0, 60], 'color': COLORS['light']},
                    {'range': [60, 85], 'color': '#ffd700'},
                    {'range': [85, 100], 'color': COLORS['secondary']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    # Recomendações
    if qualidade_score < 85:
        st.warning(f"⚠️ **Score de qualidade**: {qualidade_score:.0f}% - Revisar dados com problemas identificados")
    elif qualidade_score < 95:
        st.info(f"ℹ️ **Score de qualidade**: {qualidade_score:.0f}% - Boa qualidade, pequenos ajustes recomendados")
    else:
        st.success(f"✅ **Score de qualidade**: {qualidade_score:.0f}% - Excelente qualidade dos dados!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #708090; font-size: 0.85rem; padding: 1rem 0;">
    <strong>Dashboard Executivo Profissional - Raia Drogasil</strong><br>
    Desenvolvido com expertise em análise de dados RD (Resultados Digitais)<br>
    © 2025 | Análise estratégica de performance, vendas e market share
</div>
""", unsafe_allow_html=True)
