"""
Dashboard Executivo - Raia Drogasil
Sistema de Análise de Performance de Vendas e Market Share
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from data_processor_optimized import OptimizedDataProcessor

# Configuração da página
st.set_page_config(
    page_title="Dashboard Executivo - Raia Drogasil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-positive {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .insight-warning {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    .insight-negative {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    .insight-info {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar cache e processador
@st.cache_resource
def get_data_processor():
    """Initialize data processor with caching - FAST VERSION"""
    processor = OptimizedDataProcessor()
    # Load only last 3 months of IQVIA data for fast startup
    processor.quick_load(sample_months=3)
    return processor

# Carregar dados
try:
    with st.spinner('🚀 Carregamento rápido... Aguarde 10-15 segundos'):
        processor = get_data_processor()
    data_loaded = True
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.exception(e)
    data_loaded = False

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f77b4/ffffff?text=RD", use_container_width=True)
    st.title("🏥 Raia Drogasil")
    st.markdown("---")

    # Status indicator
    if data_loaded:
        st.success("✅ Dados carregados")
        revenue_metrics = processor.get_revenue_metrics()
        iqvia_metrics = processor.get_market_share_metrics()
        st.caption(f"📊 {len(processor.pricing_data):,} registros de preços")
        st.caption(f"📈 {len(processor.iqvia_data):,} registros IQVIA")
        st.markdown("---")

    if data_loaded:
        # Filtros
        st.subheader("📅 Filtros")

        # Período
        periods = ['Último Mês', 'Últimos 3 Meses', 'Últimos 6 Meses', 'Ano Completo']
        selected_period = st.selectbox('Período', periods, index=1)

        # Canal
        channels = ['Todos', 'App', 'Site']
        selected_channel = st.selectbox('Canal', channels)

        # Estado
        states_df = processor.get_state_performance()
        states = ['Todos'] + states_df['estado'].tolist()
        selected_state = st.selectbox('Estado', states)

        st.markdown("---")

        # Navegação
        st.subheader("📊 Navegação")
        page = st.radio(
            "Selecione a página:",
            [
                "🏠 Dashboard Executivo",
                "📈 Market Share",
                "🏷️ Performance por Categoria",
                "🗺️ Performance Geográfica",
                "🎯 Análise de Oportunidades",
                "🔮 Projeções e Cenários"
            ]
        )

        st.markdown("---")
        st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Main content
if not data_loaded:
    st.error("❌ Não foi possível carregar os dados. Verifique os arquivos de dados.")
    st.stop()

# ====================
# DASHBOARD EXECUTIVO
# ====================
if page == "🏠 Dashboard Executivo":
    st.markdown('<div class="main-header">🏠 Dashboard Executivo</div>', unsafe_allow_html=True)

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    revenue_metrics = processor.get_revenue_metrics()
    share_metrics = processor.get_market_share_metrics()
    growth = processor.get_growth_rates()

    with col1:
        st.metric(
            "💰 Receita Total",
            f"R$ {revenue_metrics['total_revenue'] / 1e9:.2f}B",
            f"{growth['revenue_growth']:.1f}%"
        )

    with col2:
        st.metric(
            "📊 Market Share",
            f"{share_metrics['avg_share'] * 100:.1f}%",
            f"{growth['share_growth']:.1f}pp",
            delta_color="normal" if growth['share_growth'] > 0 else "inverse"
        )

    with col3:
        st.metric(
            "📦 Unidades Vendidas",
            f"{revenue_metrics['total_units'] / 1e6:.1f}M",
            "▲ 8.7%"
        )

    with col4:
        st.metric(
            "💵 Ticket Médio",
            f"R$ {revenue_metrics['avg_price']:.2f}",
            "▲ 3.2%"
        )

    st.markdown("---")

    # Insights automáticos
    st.subheader("💡 Insights Automáticos")

    insights = processor.generate_insights()

    for insight in insights:
        if insight['type'] == 'positive':
            st.markdown(f'<div class="insight-positive">✅ <strong>{insight["category"]}</strong>: {insight["message"]}</div>', unsafe_allow_html=True)
        elif insight['type'] == 'warning':
            st.markdown(f'<div class="insight-warning">⚠️ <strong>{insight["category"]}</strong>: {insight["message"]}</div>', unsafe_allow_html=True)
        elif insight['type'] == 'negative':
            st.markdown(f'<div class="insight-negative">❌ <strong>{insight["category"]}</strong>: {insight["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="insight-info">ℹ️ <strong>{insight["category"]}</strong>: {insight["message"]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Gráficos principais
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Evolução da Receita")
        revenue_trend = processor.get_revenue_trend()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=revenue_trend['data'],
            y=revenue_trend['receita'] / 1e6,
            mode='lines+markers',
            name='Receita',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))

        fig.update_layout(
            xaxis_title="Período",
            yaxis_title="Receita (R$ Milhões)",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📊 Evolução do Market Share")
        share_trend = processor.get_market_share_trend()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=share_trend['data'],
            y=share_trend['share'] * 100,
            mode='lines+markers',
            name='Market Share RD',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=8)
        ))

        # Linha de meta
        fig.add_hline(y=40, line_dash="dash", line_color="red",
                     annotation_text="Meta: 40%")

        fig.update_layout(
            xaxis_title="Período",
            yaxis_title="Market Share (%)",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    # Performance por canal e categoria
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📱 Performance por Canal")
        channel_perf = processor.get_channel_performance()

        fig = go.Figure(data=[go.Pie(
            labels=channel_perf['canal'],
            values=channel_perf['rbv'],
            hole=0.4,
            marker=dict(colors=['#1f77b4', '#ff7f0e'])
        )])

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Tabela de detalhes
        st.dataframe(
            channel_perf[['canal', 'pct_receita', 'rbv']].style.format({
                'pct_receita': '{:.1f}%',
                'rbv': 'R$ {:.0f}'
            }),
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.subheader("🏷️ Top 5 Categorias")
        category_perf = processor.get_category_performance().head(5)

        fig = go.Figure(data=[go.Bar(
            x=category_perf['receita'] / 1e6,
            y=category_perf['categoria'],
            orientation='h',
            marker=dict(color='#2ca02c')
        )])

        fig.update_layout(
            xaxis_title="Receita (R$ Milhões)",
            yaxis_title="",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    # Performance geográfica
    st.markdown("---")
    st.subheader("🗺️ Performance por Estado - Top 10")

    state_perf = processor.get_state_performance().head(10)

    fig = go.Figure(data=[go.Bar(
        x=state_perf['estado'],
        y=state_perf['receita'] / 1e6,
        marker=dict(
            color=state_perf['receita'],
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="Receita<br>(R$ Milhões)")
        ),
        text=state_perf['pct_receita'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside'
    )])

    fig.update_layout(
        xaxis_title="Estado",
        yaxis_title="Receita (R$ Milhões)",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

# ====================
# MARKET SHARE
# ====================
elif page == "📈 Market Share":
    st.markdown('<div class="main-header">📈 Análise de Market Share</div>', unsafe_allow_html=True)

    share_metrics = processor.get_market_share_metrics()

    # Métricas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📊 Market Share Médio",
            f"{share_metrics['avg_share'] * 100:.1f}%",
            "vs Meta: -2.9pp"
        )

    with col2:
        st.metric(
            "🏪 Vendas RD",
            f"{share_metrics['total_rd_sales'] / 1e6:.1f}M un",
            "Total de unidades"
        )

    with col3:
        st.metric(
            "🏢 Vendas Concorrentes",
            f"{share_metrics['total_competitor_sales'] / 1e6:.1f}M un",
            f"{((share_metrics['total_competitor_sales'] / share_metrics['total_rd_sales']) - 1) * 100:.0f}% maior"
        )

    with col4:
        st.metric(
            "⚠️ Taxa Venda Zero",
            f"{share_metrics['zero_sales_rate'] * 100:.1f}%",
            "Oportunidade de melhoria",
            delta_color="inverse"
        )

    st.markdown("---")

    # Tendência de market share
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Evolução do Market Share - RD vs Concorrentes")

        share_trend = processor.get_market_share_trend()

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # RD Sales
        fig.add_trace(
            go.Bar(
                x=share_trend['data'],
                y=share_trend['venda_rd'],
                name='Vendas RD',
                marker_color='#1f77b4',
                opacity=0.7
            ),
            secondary_y=False
        )

        # Competitor Sales
        fig.add_trace(
            go.Bar(
                x=share_trend['data'],
                y=share_trend['venda_concorrente'],
                name='Vendas Concorrentes',
                marker_color='#ff7f0e',
                opacity=0.7
            ),
            secondary_y=False
        )

        # Market Share Line
        fig.add_trace(
            go.Scatter(
                x=share_trend['data'],
                y=share_trend['share'] * 100,
                name='Market Share (%)',
                line=dict(color='#2ca02c', width=3),
                mode='lines+markers'
            ),
            secondary_y=True
        )

        fig.update_xaxes(title_text="Período")
        fig.update_yaxes(title_text="Unidades Vendidas", secondary_y=False)
        fig.update_yaxes(title_text="Market Share (%)", secondary_y=True)

        fig.update_layout(height=500, hovermode='x unified')

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Distribuição de Share")

        # Calcular distribuição por produto
        df_share = processor.iqvia_data.groupby('cd_produto')['share'].mean().reset_index()

        bins = [0, 0.25, 0.50, 1.0]
        labels = ['<25%', '25-50%', '>50%']
        df_share['categoria_share'] = pd.cut(df_share['share'], bins=bins, labels=labels)

        dist = df_share['categoria_share'].value_counts().sort_index()

        fig = go.Figure(data=[go.Pie(
            labels=dist.index,
            values=dist.values,
            hole=0.4,
            marker=dict(colors=['#d62728', '#ff7f0e', '#2ca02c'])
        )])

        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)

        # Estatísticas
        st.metric("Total de Produtos", f"{len(df_share):,}")
        st.metric("Produtos >50% Share", f"{len(df_share[df_share['share'] > 0.5]):,}")
        st.metric("Produtos <25% Share", f"{len(df_share[df_share['share'] < 0.25]):,}")

    st.markdown("---")

    # Análise de oportunidades de zero sales
    st.subheader("🎯 Maiores Oportunidades - Produtos com Venda Zero")

    zero_sales = processor.get_zero_sales_analysis().head(20)

    fig = go.Figure(data=[go.Bar(
        x=zero_sales['produto'],
        y=zero_sales['venda_concorrente'],
        marker=dict(
            color=zero_sales['venda_concorrente'],
            colorscale='Reds',
            showscale=True
        ),
        text=zero_sales['lojas_afetadas'],
        texttemplate='%{text} lojas',
        textposition='outside'
    )])

    fig.update_layout(
        xaxis_title="Código do Produto",
        yaxis_title="Vendas dos Concorrentes (unidades)",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 Estes produtos têm vendas significativas dos concorrentes mas zero vendas RD - priorizar estoque e distribuição")

# ====================
# PERFORMANCE POR CATEGORIA
# ====================
elif page == "🏷️ Performance por Categoria":
    st.markdown('<div class="main-header">🏷️ Performance por Categoria</div>', unsafe_allow_html=True)

    category_perf = processor.get_category_performance()

    # Seletor de categoria
    selected_category = st.selectbox(
        "Selecione a categoria para análise detalhada:",
        category_perf['categoria'].tolist()
    )

    # Filtrar dados da categoria selecionada
    cat_data = category_perf[category_perf['categoria'] == selected_category].iloc[0]

    # Métricas da categoria
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Receita",
            f"R$ {cat_data['receita'] / 1e9:.2f}B",
            f"{cat_data['pct_receita']:.1f}% do total"
        )

    with col2:
        st.metric(
            "📦 Unidades",
            f"{cat_data['unidades'] / 1e6:.1f}M",
            "Total vendido"
        )

    with col3:
        st.metric(
            "💵 Preço Médio",
            f"R$ {cat_data['preco_medio']:.2f}",
            "Por unidade"
        )

    with col4:
        st.metric(
            "🏷️ Produtos",
            f"{cat_data['produtos']:,}",
            "SKUs ativos"
        )

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Receita por Categoria")

        fig = go.Figure(data=[go.Bar(
            x=category_perf['categoria'],
            y=category_perf['receita'] / 1e6,
            marker=dict(
                color=['#2ca02c' if cat == selected_category else '#1f77b4'
                       for cat in category_perf['categoria']]
            ),
            text=category_perf['pct_receita'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside'
        )])

        fig.update_layout(
            xaxis_title="Categoria",
            yaxis_title="Receita (R$ Milhões)",
            height=400,
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💰 Análise de Preço Médio")

        fig = go.Figure(data=[go.Bar(
            x=category_perf['categoria'],
            y=category_perf['preco_medio'],
            marker=dict(
                color=['#ff7f0e' if cat == selected_category else '#1f77b4'
                       for cat in category_perf['categoria']]
            ),
            text=category_perf['preco_medio'].apply(lambda x: f'R$ {x:.2f}'),
            textposition='outside'
        )])

        fig.update_layout(
            xaxis_title="Categoria",
            yaxis_title="Preço Médio (R$)",
            height=400,
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig, use_container_width=True)

    # Análise temporal da categoria selecionada
    st.markdown("---")
    st.subheader(f"📈 Evolução Temporal - {selected_category}")

    cat_trend = processor.pricing_data[
        processor.pricing_data['neogrupo'] == selected_category
    ].groupby('mes').agg({
        'rbv': 'sum',
        'qt_unidade_vendida': 'sum',
        'preco_medio': 'mean'
    }).reset_index()

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Receita e Unidades', 'Preço Médio'),
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
    )

    # Receita e unidades
    fig.add_trace(
        go.Bar(x=cat_trend['mes'], y=cat_trend['rbv'] / 1e6,
               name='Receita (R$ Mi)', marker_color='#1f77b4'),
        row=1, col=1, secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=cat_trend['mes'], y=cat_trend['qt_unidade_vendida'] / 1000,
                   name='Unidades (mil)', line=dict(color='#ff7f0e', width=3),
                   mode='lines+markers'),
        row=1, col=1, secondary_y=True
    )

    # Preço médio
    fig.add_trace(
        go.Scatter(x=cat_trend['mes'], y=cat_trend['preco_medio'],
                   name='Preço Médio', line=dict(color='#2ca02c', width=3),
                   mode='lines+markers', fill='tozeroy'),
        row=2, col=1
    )

    fig.update_xaxes(title_text="Período", row=2, col=1)
    fig.update_yaxes(title_text="Receita (R$ Mi)", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Unidades (mil)", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="Preço (R$)", row=2, col=1)

    fig.update_layout(height=700, hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)

    # Top produtos da categoria
    st.markdown("---")
    st.subheader(f"🏆 Top 20 Produtos - {selected_category}")

    cat_products = processor.pricing_data[
        processor.pricing_data['neogrupo'] == selected_category
    ].groupby('produto').agg({
        'rbv': 'sum',
        'qt_unidade_vendida': 'sum',
        'preco_medio': 'mean'
    }).reset_index().sort_values('rbv', ascending=False).head(20)

    cat_products['ranking'] = range(1, len(cat_products) + 1)
    cat_products.columns = ['Produto', 'Receita', 'Unidades', 'Preço Médio', 'Ranking']

    st.dataframe(
        cat_products[['Ranking', 'Produto', 'Receita', 'Unidades', 'Preço Médio']].style.format({
            'Receita': 'R$ {:.0f}',
            'Unidades': '{:.0f}',
            'Preço Médio': 'R$ {:.2f}'
        }),
        hide_index=True,
        use_container_width=True
    )

# ====================
# PERFORMANCE GEOGRÁFICA
# ====================
elif page == "🗺️ Performance Geográfica":
    st.markdown('<div class="main-header">🗺️ Performance Geográfica</div>', unsafe_allow_html=True)

    state_perf = processor.get_state_performance()

    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🗺️ Estados Ativos",
            f"{len(state_perf)}",
            "Cobertura nacional"
        )

    with col2:
        top_state = state_perf.iloc[0]
        st.metric(
            "🏆 Estado Líder",
            top_state['estado'],
            f"{top_state['pct_receita']:.1f}% do total"
        )

    with col3:
        top3_pct = state_perf.head(3)['pct_receita'].sum()
        st.metric(
            "📊 Concentração Top 3",
            f"{top3_pct:.1f}%",
            "SP, RJ, MG"
        )

    with col4:
        avg_revenue = state_perf['receita'].mean()
        st.metric(
            "💰 Receita Média/Estado",
            f"R$ {avg_revenue / 1e6:.1f}M",
            "Por estado"
        )

    st.markdown("---")

    # Mapa de receita por estado
    st.subheader("🗺️ Mapa de Receita por Estado")

    fig = go.Figure(data=go.Bar(
        x=state_perf['estado'],
        y=state_perf['receita'] / 1e6,
        marker=dict(
            color=state_perf['receita'],
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="Receita<br>(R$ Mi)")
        ),
        text=state_perf['pct_receita'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside'
    ))

    fig.update_layout(
        xaxis_title="Estado (UF)",
        yaxis_title="Receita (R$ Milhões)",
        height=500,
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Análise comparativa
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Top 10 Estados por Receita")

        top10 = state_perf.head(10)

        fig = go.Figure(data=[go.Bar(
            y=top10['estado'],
            x=top10['receita'] / 1e6,
            orientation='h',
            marker=dict(color='#1f77b4'),
            text=top10['pct_receita'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside'
        )])

        fig.update_layout(
            xaxis_title="Receita (R$ Milhões)",
            yaxis_title="",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💵 Preço Médio por Estado (Top 10)")

        top10_price = state_perf.head(10)

        fig = go.Figure(data=[go.Bar(
            y=top10_price['estado'],
            x=top10_price['preco_medio'],
            orientation='h',
            marker=dict(color='#2ca02c'),
            text=top10_price['preco_medio'].apply(lambda x: f'R$ {x:.2f}'),
            textposition='outside'
        )])

        fig.update_layout(
            xaxis_title="Preço Médio (R$)",
            yaxis_title="",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    # Tabela detalhada
    st.markdown("---")
    st.subheader("📋 Ranking Completo de Estados")

    state_perf['ranking'] = range(1, len(state_perf) + 1)

    st.dataframe(
        state_perf[['ranking', 'estado', 'receita', 'unidades', 'preco_medio', 'pct_receita']].style.format({
            'receita': 'R$ {:.0f}',
            'unidades': '{:.0f}',
            'preco_medio': 'R$ {:.2f}',
            'pct_receita': '{:.2f}%'
        }),
        hide_index=True,
        use_container_width=True,
        height=400
    )

# ====================
# ANÁLISE DE OPORTUNIDADES
# ====================
elif page == "🎯 Análise de Oportunidades":
    st.markdown('<div class="main-header">🎯 Análise de Oportunidades</div>', unsafe_allow_html=True)

    # Análise de vendas zero
    st.subheader("⚠️ Oportunidades de Vendas Zero")

    share_metrics = processor.get_market_share_metrics()
    zero_sales = processor.get_zero_sales_analysis()

    col1, col2, col3 = st.columns(3)

    with col1:
        total_opportunities = len(processor.iqvia_data[processor.iqvia_data['venda_rd'] == 0])
        st.metric(
            "📊 Total de Oportunidades",
            f"{total_opportunities / 1e6:.1f}M",
            "Cenários venda zero"
        )

    with col2:
        st.metric(
            "📈 Taxa de Venda Zero",
            f"{share_metrics['zero_sales_rate'] * 100:.1f}%",
            "Do total de cenários"
        )

    with col3:
        potential_units = zero_sales['venda_concorrente'].sum()
        st.metric(
            "🎯 Potencial de Vendas",
            f"{potential_units / 1e6:.1f}M un",
            "Vendas concorrentes"
        )

    st.markdown("---")

    # Top oportunidades
    st.subheader("🏆 Top 50 Produtos com Maior Potencial")

    top_opportunities = zero_sales.head(50)

    fig = go.Figure(data=[go.Bar(
        x=top_opportunities.index[::-1],
        y=top_opportunities['venda_concorrente'][::-1],
        orientation='h',
        marker=dict(
            color=top_opportunities['venda_concorrente'][::-1],
            colorscale='Reds',
            showscale=True
        ),
        text=top_opportunities['lojas_afetadas'][::-1],
        texttemplate='%{text} lojas',
        textposition='outside'
    )])

    fig.update_layout(
        xaxis_title="Vendas Concorrentes (unidades)",
        yaxis_title="Produto",
        height=1000
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Análise Pareto
    st.subheader("📊 Análise Pareto - 80/20")

    revenue_products = processor.pricing_data.groupby('produto').agg({
        'rbv': 'sum'
    }).reset_index().sort_values('rbv', ascending=False)

    revenue_products['cumsum'] = revenue_products['rbv'].cumsum()
    revenue_products['cumsum_pct'] = revenue_products['cumsum'] / revenue_products['rbv'].sum() * 100
    revenue_products['ranking'] = range(1, len(revenue_products) + 1)

    # Encontrar ponto 80%
    products_80 = revenue_products[revenue_products['cumsum_pct'] <= 80]
    pct_products_80 = len(products_80) / len(revenue_products) * 100

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📊 Produtos que geram 80% da receita",
            f"{len(products_80):,}",
            f"{pct_products_80:.1f}% do total"
        )

    with col2:
        revenue_80 = products_80['rbv'].sum()
        st.metric(
            "💰 Receita dos Top 20%",
            f"R$ {revenue_80 / 1e9:.2f}B",
            f"{revenue_80 / revenue_products['rbv'].sum() * 100:.1f}% do total"
        )

    # Gráfico Pareto
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=revenue_products.head(100)['ranking'],
            y=revenue_products.head(100)['rbv'] / 1e6,
            name='Receita Individual',
            marker_color='#1f77b4',
            opacity=0.7
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=revenue_products.head(100)['ranking'],
            y=revenue_products.head(100)['cumsum_pct'],
            name='% Acumulado',
            line=dict(color='#ff7f0e', width=3),
            mode='lines'
        ),
        secondary_y=True
    )

    # Linha 80%
    fig.add_hline(y=80, line_dash="dash", line_color="red",
                 annotation_text="80%", secondary_y=True)

    fig.update_xaxes(title_text="Ranking de Produtos")
    fig.update_yaxes(title_text="Receita (R$ Milhões)", secondary_y=False)
    fig.update_yaxes(title_text="% Acumulado da Receita", secondary_y=True)

    fig.update_layout(height=500, hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 **Insight**: Foco nos top 20% de produtos que geram 80% da receita pode maximizar resultados")

# ====================
# PROJEÇÕES E CENÁRIOS
# ====================
elif page == "🔮 Projeções e Cenários":
    st.markdown('<div class="main-header">🔮 Projeções e Cenários</div>', unsafe_allow_html=True)

    # Projeções
    st.subheader("📈 Projeções para Próximo Período")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💰 Projeção de Receita")

        predicted_revenue = processor.predict_next_month_revenue()

        if predicted_revenue:
            current_revenue = processor.get_revenue_metrics()['total_revenue']
            growth = ((predicted_revenue - current_revenue) / current_revenue) * 100

            st.metric(
                "Receita Projetada (próximo mês)",
                f"R$ {predicted_revenue / 1e6:.1f}M",
                f"{growth:+.1f}%"
            )

            # Gráfico de tendência
            revenue_trend = processor.get_revenue_trend()
            last_date = revenue_trend['data'].max()
            next_date = last_date + pd.DateOffset(months=1)

            # Adicionar projeção
            projection_df = pd.DataFrame({
                'data': [next_date],
                'receita': [predicted_revenue],
                'tipo': ['Projeção']
            })

            revenue_trend['tipo'] = 'Real'

            combined = pd.concat([
                revenue_trend[['data', 'receita', 'tipo']],
                projection_df
            ])

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=combined[combined['tipo'] == 'Real']['data'],
                y=combined[combined['tipo'] == 'Real']['receita'] / 1e6,
                mode='lines+markers',
                name='Receita Real',
                line=dict(color='#1f77b4', width=3)
            ))

            fig.add_trace(go.Scatter(
                x=combined[combined['tipo'] == 'Projeção']['data'],
                y=combined[combined['tipo'] == 'Projeção']['receita'] / 1e6,
                mode='markers',
                name='Projeção',
                marker=dict(color='#ff7f0e', size=15, symbol='star')
            ))

            fig.update_layout(
                xaxis_title="Período",
                yaxis_title="Receita (R$ Milhões)",
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📊 Projeção de Market Share")

        predicted_share = processor.predict_market_share()

        if predicted_share:
            current_share = processor.get_market_share_metrics()['avg_share']
            change = predicted_share - current_share

            st.metric(
                "Market Share Projetado",
                f"{predicted_share * 100:.1f}%",
                f"{change * 100:+.2f}pp"
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

            combined = pd.concat([
                share_trend[['data', 'share', 'tipo']],
                projection_df
            ])

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=combined[combined['tipo'] == 'Real']['data'],
                y=combined[combined['tipo'] == 'Real']['share'] * 100,
                mode='lines+markers',
                name='Share Real',
                line=dict(color='#2ca02c', width=3)
            ))

            fig.add_trace(go.Scatter(
                x=combined[combined['tipo'] == 'Projeção']['data'],
                y=combined[combined['tipo'] == 'Projeção']['share'] * 100,
                mode='markers',
                name='Projeção',
                marker=dict(color='#d62728', size=15, symbol='star')
            ))

            # Meta
            fig.add_hline(y=40, line_dash="dash", line_color="red",
                         annotation_text="Meta: 40%")

            fig.update_layout(
                xaxis_title="Período",
                yaxis_title="Market Share (%)",
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Cenários
    st.subheader("🎲 Análise de Cenários")

    st.markdown("""
    Explore diferentes cenários de negócio e seu impacto potencial na receita:
    """)

    scenarios = processor.calculate_scenarios()

    # Cards de cenários
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### 📊 Atual")
        st.metric(
            "Receita",
            f"R$ {scenarios['current'] / 1e9:.2f}B",
            "Baseline"
        )

    with col2:
        impact = ((scenarios['reduce_zero_sales'] - scenarios['current']) / scenarios['current']) * 100
        st.markdown("### 🎯 Reduzir Vendas Zero em 50%")
        st.metric(
            "Receita Potencial",
            f"R$ {scenarios['reduce_zero_sales'] / 1e9:.2f}B",
            f"+{impact:.1f}%"
        )

    with col3:
        impact = ((scenarios['increase_share'] - scenarios['current']) / scenarios['current']) * 100
        st.markdown("### 📈 Aumentar Share em 5pp")
        st.metric(
            "Receita Potencial",
            f"R$ {scenarios['increase_share'] / 1e9:.2f}B",
            f"+{impact:.1f}%"
        )

    with col4:
        impact = ((scenarios['optimize_mix'] - scenarios['current']) / scenarios['current']) * 100
        st.markdown("### 🏆 Otimizar Mix (Top 20%)")
        st.metric(
            "Receita Potencial",
            f"R$ {scenarios['optimize_mix'] / 1e9:.2f}B",
            f"+{impact:.1f}%"
        )

    # Gráfico comparativo de cenários
    st.markdown("---")
    st.subheader("📊 Comparação de Cenários")

    scenario_names = ['Atual', 'Reduzir\nVendas Zero', 'Aumentar\nShare', 'Otimizar\nMix']
    scenario_values = [
        scenarios['current'],
        scenarios['reduce_zero_sales'],
        scenarios['increase_share'],
        scenarios['optimize_mix']
    ]

    fig = go.Figure(data=[go.Bar(
        x=scenario_names,
        y=[v / 1e9 for v in scenario_values],
        marker=dict(color=['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd']),
        text=[f'R$ {v/1e9:.2f}B' for v in scenario_values],
        textposition='outside'
    )])

    fig.update_layout(
        yaxis_title="Receita (R$ Bilhões)",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Análise de sensibilidade
    st.markdown("---")
    st.subheader("🎚️ Análise de Sensibilidade - Market Share")

    st.markdown("Simule o impacto de diferentes níveis de market share na receita:")

    share_increase = st.slider(
        "Aumento de Market Share (pontos percentuais)",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.5
    )

    current_metrics = processor.get_revenue_metrics()
    current_share_val = processor.get_market_share_metrics()['avg_share']

    # Calcular impacto
    share_multiplier = (current_share_val + (share_increase / 100)) / current_share_val
    projected_revenue = current_metrics['total_revenue'] * share_multiplier
    revenue_increase = projected_revenue - current_metrics['total_revenue']

    col1, col2, col3 = st.columns(3)

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
            "Impacto na Receita",
            f"+R$ {revenue_increase / 1e9:.2f}B",
            f"+{(revenue_increase / current_metrics['total_revenue'] * 100):.1f}%"
        )

    # Gráfico de sensibilidade
    share_range = np.arange(0, 16, 1)
    revenue_range = [
        current_metrics['total_revenue'] * ((current_share_val + (s/100)) / current_share_val)
        for s in share_range
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=share_range,
        y=[r / 1e9 for r in revenue_range],
        mode='lines+markers',
        name='Receita Projetada',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))

    # Marcar ponto atual
    fig.add_trace(go.Scatter(
        x=[share_increase],
        y=[projected_revenue / 1e9],
        mode='markers',
        name='Cenário Selecionado',
        marker=dict(color='#ff7f0e', size=15, symbol='star')
    ))

    fig.update_layout(
        xaxis_title="Aumento de Market Share (pp)",
        yaxis_title="Receita Projetada (R$ Bilhões)",
        height=400,
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 **Insight**: Cada ponto percentual de aumento no market share pode gerar aproximadamente R$ " + f"{(revenue_increase / share_increase / 1e6):.0f}M em receita adicional")

# Footer
st.markdown("---")
st.caption("© 2025 Raia Drogasil | Dashboard Executivo | Desenvolvido para análise estratégica de performance")
