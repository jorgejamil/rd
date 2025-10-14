"""
Optimized Data Processing Pipeline for Raia Drogasil Dashboard
Fast loading with lazy evaluation and pre-aggregation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class OptimizedDataProcessor:
    """Optimized data processing class with lazy loading"""

    def __init__(self, data_dir="."):
        self.data_dir = Path(data_dir)
        self.iqvia_data = None
        self.pricing_data = None
        self.iqvia_aggregated = None
        self.pricing_aggregated = None
        self.date_filter_start = None
        self.date_filter_end = None

    def load_pricing_data_fast(self, load_all=True):
        """Load pricing data - much smaller, loads quickly"""
        pricing_file = self.data_dir / "Preço.csv"
        print("Carregando dados de preços...")

        # Ler apenas colunas necessárias para acelerar
        required_cols = ['mes', 'rbv', 'qt_unidade_vendida', 'preco_medio',
                        'produto', 'canal', 'neogrupo', 'uf']
        self.pricing_data = pd.read_csv(pricing_file, encoding='utf-8', usecols=required_cols)
        self.pricing_data['mes'] = pd.to_datetime(self.pricing_data['mes'])

        # Filtrar de janeiro/2025 até 30/09/2025
        start_date = pd.Timestamp('2025-01-01')
        cutoff_date = pd.Timestamp('2025-09-30')
        self.pricing_data = self.pricing_data[
            (self.pricing_data['mes'] >= start_date) &
            (self.pricing_data['mes'] <= cutoff_date)
        ]

        print(f"✓ Preços carregados: {len(self.pricing_data):,} registros (Jan-Set/2025)")
        return self.pricing_data

    def load_iqvia_all(self):
        """Load ALL IQVIA data from Jan-Aug 2025 with memory-efficient aggregation"""
        iqvia_files = sorted(self.data_dir.glob("historico_iqvia_*.parquet"))

        print(f"Carregando IQVIA (TODOS os meses de 2025 disponíveis com agregação)...")

        # Ler apenas colunas necessárias
        required_cols = ['id_periodo', 'cd_produto', 'cd_filial', 'cd_brick',
                        'share', 'venda_rd', 'venda_concorrente']

        # ESTRATÉGIA: Agregar cada arquivo antes de concatenar (economiza memória)
        aggregated_dfs = []

        # Filtrar apenas arquivos de 2025
        for file in iqvia_files:
            # Extrair ano/mês do nome do arquivo
            filename = file.stem
            period_str = filename.split('_')[-1]

            if len(period_str) == 6:  # YYYYMM format
                year = int(period_str[:4])
                month = int(period_str[4:])

                # Carregar todos os meses de 2025 até setembro
                if year == 2025 and 1 <= month <= 9:
                    print(f"  - Processando {file.name}...")
                    df = pd.read_parquet(file, columns=required_cols)

                    # Agregar imediatamente para reduzir memória
                    # Manter apenas agregações por período, produto, filial
                    df_agg = df.groupby(['id_periodo', 'cd_produto']).agg({
                        'share': 'mean',
                        'venda_rd': 'sum',
                        'venda_concorrente': 'sum',
                        'cd_filial': 'nunique',
                        'cd_brick': 'nunique'
                    }).reset_index()

                    aggregated_dfs.append(df_agg)
                    del df  # Liberar memória imediatamente

        if not aggregated_dfs:
            print("⚠️  Nenhum arquivo IQVIA encontrado!")
            return pd.DataFrame()

        # Concatenar agregações (muito menor que dados originais)
        self.iqvia_data = pd.concat(aggregated_dfs, ignore_index=True)
        del aggregated_dfs  # Liberar memória

        self.iqvia_data['data'] = pd.to_datetime(
            self.iqvia_data['id_periodo'].astype(str),
            format='%Y%m'
        )

        # Filtrar dados de janeiro até 30/09/2025
        start_date = pd.Timestamp('2025-01-01')
        cutoff_date = pd.Timestamp('2025-09-30')
        self.iqvia_data = self.iqvia_data[
            (self.iqvia_data['data'] >= start_date) &
            (self.iqvia_data['data'] <= cutoff_date)
        ]

        # Identificar período real de dados
        min_month = self.iqvia_data['data'].min().strftime('%b')
        max_month = self.iqvia_data['data'].max().strftime('%b')
        print(f"✓ IQVIA carregado e agregado: {len(self.iqvia_data):,} registros ({min_month}-{max_month}/2025)")
        print(f"  Produtos únicos: {self.iqvia_data['cd_produto'].nunique():,}")
        return self.iqvia_data

    def precompute_aggregations(self):
        """Pre-compute common aggregations for faster queries"""
        print("Pré-computando agregações...")

        # IQVIA aggregations
        if self.iqvia_data is not None:
            self.iqvia_aggregated = {
                'by_period': self.iqvia_data.groupby('data').agg({
                    'share': 'mean',
                    'venda_rd': 'sum',
                    'venda_concorrente': 'sum',
                    'cd_produto': 'nunique'
                }).reset_index(),

                'by_product': self.iqvia_data.groupby('cd_produto').agg({
                    'share': 'mean',
                    'venda_rd': 'sum',
                    'venda_concorrente': 'sum'
                }).reset_index(),

                'zero_sales': self.iqvia_data[self.iqvia_data['venda_rd'] == 0].groupby('cd_produto').agg({
                    'venda_concorrente': 'sum',
                    'cd_filial': 'nunique'
                }).reset_index()
            }

        # Pricing aggregations
        if self.pricing_data is not None:
            self.pricing_aggregated = {
                'by_month': self.pricing_data.groupby('mes').agg({
                    'rbv': 'sum',
                    'qt_unidade_vendida': 'sum',
                    'preco_medio': 'mean'
                }).reset_index(),

                'by_channel': self.pricing_data.groupby('canal').agg({
                    'rbv': 'sum',
                    'qt_unidade_vendida': 'sum',
                    'preco_medio': 'mean'
                }).reset_index(),

                'by_category': self.pricing_data.groupby('neogrupo').agg({
                    'rbv': 'sum',
                    'qt_unidade_vendida': 'sum',
                    'preco_medio': 'mean',
                    'produto': 'nunique'
                }).reset_index(),

                'by_state': self.pricing_data.groupby('uf').agg({
                    'rbv': 'sum',
                    'qt_unidade_vendida': 'sum',
                    'preco_medio': 'mean'
                }).reset_index()
            }

        print("✓ Agregações pré-computadas")

    def quick_load(self):
        """Load ALL available data from 2025"""
        print("\n" + "="*60)
        print("🚀 CARREGAMENTO COMPLETO (Janeiro - Setembro 2025)")
        print("="*60 + "\n")

        # Load pricing - todos os meses de 2025 até setembro
        self.load_pricing_data_fast()

        # Load all IQVIA data available from 2025
        self.load_iqvia_all()

        # Pre-compute aggregations
        self.precompute_aggregations()

        # Mostrar resumo dos dados carregados
        if self.pricing_data is not None:
            pricing_months = self.pricing_data['mes'].nunique()
        else:
            pricing_months = 0

        if self.iqvia_data is not None:
            iqvia_months = self.iqvia_data['data'].nunique()
        else:
            iqvia_months = 0

        print("\n" + "="*60)
        print(f"✅ DADOS PRONTOS PARA USO!")
        print(f"   Pricing: {pricing_months} meses | IQVIA: {iqvia_months} meses")
        print("="*60 + "\n")

    def get_revenue_metrics(self):
        """Calculate revenue metrics from pre-aggregated data (com filtro de data)"""
        df = self.get_filtered_pricing_data()
        if df.empty:
            return {}

        total = df['rbv'].sum()
        units = df['qt_unidade_vendida'].sum()

        metrics = {
            'total_revenue': total,
            'total_units': units,
            'avg_price': df['preco_medio'].mean(),
            'unique_products': df['produto'].nunique(),
            'orders_count': len(df)
        }
        return metrics

    def get_market_share_metrics(self):
        """Calculate market share metrics from pre-aggregated data (com filtro de data)"""
        df = self.get_filtered_iqvia_data()
        if df.empty:
            return {}

        # Como dados já estão agregados por produto, ajustar cálculos
        metrics = {
            'avg_share': df['share'].mean(),
            'total_rd_sales': df['venda_rd'].sum(),
            'total_competitor_sales': df['venda_concorrente'].sum(),
            'zero_sales_rate': (df['venda_rd'] == 0).mean(),
            'unique_products': df['cd_produto'].nunique(),
            'unique_stores': df['cd_filial'].sum() if 'cd_filial' in df.columns else 0,  # Já é count agregado
            'unique_bricks': df['cd_brick'].sum() if 'cd_brick' in df.columns else 0  # Já é count agregado
        }
        return metrics

    def get_revenue_trend(self):
        """Get revenue trend from pre-aggregated data (com filtro de data)"""
        df = self.get_filtered_pricing_data()
        if df.empty:
            return pd.DataFrame()

        result = df.groupby('mes').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean'
        }).reset_index()
        result.columns = ['data', 'receita', 'unidades', 'preco_medio']
        return result

    def get_market_share_trend(self):
        """Get market share trend from pre-aggregated data (com filtro de data)"""
        df = self.get_filtered_iqvia_data()
        if df.empty:
            return pd.DataFrame()

        result = df.groupby('data').agg({
            'share': 'mean',
            'venda_rd': 'sum',
            'venda_concorrente': 'sum'
        }).reset_index()
        return result

    def get_channel_performance(self):
        """Get performance by channel from pre-aggregated data (com filtro de data)"""
        df = self.get_filtered_pricing_data()
        if df.empty:
            return pd.DataFrame()

        result = df.groupby('canal').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean'
        }).reset_index()
        result['pct_receita'] = result['rbv'] / result['rbv'].sum() * 100
        return result

    def get_category_performance(self):
        """Get performance by category from pre-aggregated data (com filtro de data)"""
        df = self.get_filtered_pricing_data()
        if df.empty:
            return pd.DataFrame()

        result = df.groupby('neogrupo').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean',
            'produto': 'nunique'
        }).reset_index()
        result.columns = ['categoria', 'receita', 'unidades', 'preco_medio', 'produtos']
        result['pct_receita'] = result['receita'] / result['receita'].sum() * 100
        result = result.sort_values('receita', ascending=False)
        return result

    def get_state_performance(self):
        """Get performance by state from pre-aggregated data (com filtro de data)"""
        df = self.get_filtered_pricing_data()
        if df.empty:
            return pd.DataFrame()

        result = df.groupby('uf').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean'
        }).reset_index()
        result.columns = ['estado', 'receita', 'unidades', 'preco_medio']
        result['pct_receita'] = result['receita'] / result['receita'].sum() * 100
        result = result.sort_values('receita', ascending=False)
        return result

    def get_top_products(self, top_n=20, by='revenue'):
        """Get top performing products (com filtro de data)"""
        df = self.get_filtered_pricing_data()
        if df.empty:
            return pd.DataFrame()

        sort_col = 'rbv' if by == 'revenue' else 'qt_unidade_vendida'

        result = df.groupby('produto').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean',
            'neogrupo': 'first'
        }).reset_index()

        result = result.sort_values(sort_col, ascending=False).head(top_n)
        result.columns = ['produto', 'receita', 'unidades', 'preco_medio', 'categoria']
        return result

    def get_zero_sales_analysis(self):
        """Analyze zero sales opportunities from pre-aggregated data (com filtro de data)"""
        df = self.get_filtered_iqvia_data()
        if df.empty:
            return pd.DataFrame()

        # Como dados já estão agregados por produto, filtrar zeros
        zero_sales_df = df[df['venda_rd'] == 0].copy()

        # Agregar por produto
        result = zero_sales_df.groupby('cd_produto').agg({
            'venda_concorrente': 'sum',
            'cd_filial': 'sum'  # Já é count agregado
        }).reset_index()
        result.columns = ['produto', 'venda_concorrente', 'lojas_afetadas']
        result = result.sort_values('venda_concorrente', ascending=False)
        return result

    def get_growth_rates(self, periods=3):
        """Calculate growth rates"""
        revenue_trend = self.get_revenue_trend()

        if len(revenue_trend) < periods + 1:
            return {'revenue_growth': 0, 'share_growth': 0}

        revenue_trend = revenue_trend.sort_values('data')
        current = revenue_trend['receita'].iloc[-1]
        previous = revenue_trend['receita'].iloc[-(periods + 1)]
        revenue_growth = ((current - previous) / previous) * 100 if previous > 0 else 0

        share_trend = self.get_market_share_trend()

        if len(share_trend) < periods + 1:
            return {'revenue_growth': revenue_growth, 'share_growth': 0}

        share_trend = share_trend.sort_values('data')
        current_share = share_trend['share'].iloc[-1]
        previous_share = share_trend['share'].iloc[-(periods + 1)]
        share_growth = ((current_share - previous_share) / previous_share) * 100 if previous_share > 0 else 0

        return {
            'revenue_growth': revenue_growth,
            'share_growth': share_growth
        }

    def predict_next_month_revenue(self, periods=3):
        """Simple linear regression prediction"""
        trend = self.get_revenue_trend()

        if len(trend) < 2:
            return None

        trend = trend.sort_values('data').tail(periods)
        x = np.arange(len(trend))
        y = trend['receita'].values

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        next_value = p(len(trend))

        return max(0, next_value)

    def predict_market_share(self, periods=3):
        """Predict market share trend"""
        trend = self.get_market_share_trend()

        if len(trend) < 2:
            return None

        trend = trend.sort_values('data').tail(periods)
        x = np.arange(len(trend))
        y = trend['share'].values

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        next_value = p(len(trend))

        return max(0, min(1, next_value))

    def calculate_scenarios(self):
        """Calculate different business scenarios (com filtro de data)"""
        current_metrics = self.get_revenue_metrics()
        current_revenue = current_metrics.get('total_revenue', 0)

        zero_sales_df = self.get_zero_sales_analysis()
        avg_price = current_metrics.get('avg_price', 0)
        potential_units = zero_sales_df['venda_concorrente'].sum() * 0.5 if not zero_sales_df.empty else 0
        scenario_1_revenue = current_revenue + (potential_units * avg_price)

        current_share = self.get_market_share_metrics().get('avg_share', 0)
        share_increase = 0.05
        scenario_2_revenue = current_revenue * (1 + (share_increase / current_share)) if current_share > 0 else current_revenue

        unique_products = current_metrics.get('unique_products', 0)
        top_n = max(1, int(unique_products * 0.2)) if unique_products > 0 else 20
        top_products = self.get_top_products(top_n=top_n)
        top_revenue = top_products['receita'].sum() if not top_products.empty else 0
        scenario_3_revenue = current_revenue + (top_revenue * 0.2)

        scenarios = {
            'current': current_revenue,
            'reduce_zero_sales': scenario_1_revenue,
            'increase_share': scenario_2_revenue,
            'optimize_mix': scenario_3_revenue
        }

        return scenarios

    def generate_insights(self):
        """Generate automated insights"""
        insights = []

        revenue_metrics = self.get_revenue_metrics()
        growth = self.get_growth_rates()

        if growth['revenue_growth'] > 10:
            insights.append({
                'type': 'positive',
                'category': 'Receita',
                'message': f'Crescimento forte de {growth["revenue_growth"]:.1f}% na receita nos últimos meses'
            })
        elif growth['revenue_growth'] < -5:
            insights.append({
                'type': 'negative',
                'category': 'Receita',
                'message': f'Queda de {abs(growth["revenue_growth"]):.1f}% na receita - requer atenção'
            })

        share_metrics = self.get_market_share_metrics()

        if share_metrics.get('zero_sales_rate', 0) > 0.30:
            insights.append({
                'type': 'warning',
                'category': 'Market Share',
                'message': f'{share_metrics["zero_sales_rate"]*100:.1f}% das oportunidades têm venda zero - grande potencial de melhoria'
            })

        if share_metrics.get('avg_share', 0) < 0.40:
            insights.append({
                'type': 'warning',
                'category': 'Market Share',
                'message': f'Market share de {share_metrics["avg_share"]*100:.1f}% abaixo da meta de 40%'
            })

        channel_perf = self.get_channel_performance()
        if not channel_perf.empty:
            app_data = channel_perf[channel_perf['canal'] == 'App']
            if not app_data.empty:
                app_pct = app_data['pct_receita'].values[0]
                if app_pct > 85:
                    insights.append({
                        'type': 'positive',
                        'category': 'Canal',
                        'message': f'App dominando com {app_pct:.1f}% da receita - estratégia mobile validada'
                    })

        category_perf = self.get_category_performance()
        if not category_perf.empty:
            top_category = category_perf.iloc[0]
            insights.append({
                'type': 'info',
                'category': 'Categoria',
                'message': f'{top_category["categoria"]} lidera com {top_category["pct_receita"]:.1f}% da receita'
            })

        state_perf = self.get_state_performance()
        if not state_perf.empty:
            sp_data = state_perf[state_perf['estado'] == 'SP']
            if not sp_data.empty:
                sp_pct = sp_data['pct_receita'].values[0]
                if sp_pct > 35:
                    insights.append({
                        'type': 'warning',
                        'category': 'Geografia',
                        'message': f'São Paulo concentra {sp_pct:.1f}% da receita - risco de concentração'
                    })

        return insights

    def set_date_filter(self, start_date, end_date):
        """Define filtro de datas para análises"""
        self.date_filter_start = pd.Timestamp(start_date)
        self.date_filter_end = pd.Timestamp(end_date)

    def _apply_date_filter_pricing(self, df):
        """Aplica filtro de data no dataframe de preços"""
        if self.date_filter_start is None or self.date_filter_end is None:
            return df
        return df[(df['mes'] >= self.date_filter_start) & (df['mes'] <= self.date_filter_end)]

    def _apply_date_filter_iqvia(self, df):
        """Aplica filtro de data no dataframe IQVIA"""
        if self.date_filter_start is None or self.date_filter_end is None:
            return df
        return df[(df['data'] >= self.date_filter_start) & (df['data'] <= self.date_filter_end)]

    def get_filtered_pricing_data(self):
        """Retorna dados de preços filtrados por data"""
        if self.pricing_data is None:
            return pd.DataFrame()
        return self._apply_date_filter_pricing(self.pricing_data)

    def get_filtered_iqvia_data(self):
        """Retorna dados IQVIA filtrados por data"""
        if self.iqvia_data is None:
            return pd.DataFrame()
        return self._apply_date_filter_iqvia(self.iqvia_data)


if __name__ == "__main__":
    # Test optimized processor
    processor = OptimizedDataProcessor()
    processor.quick_load(sample_months=3)

    print("\n=== Revenue Metrics ===")
    print(processor.get_revenue_metrics())

    print("\n=== Market Share Metrics ===")
    print(processor.get_market_share_metrics())

    print("\n=== Insights ===")
    for insight in processor.generate_insights():
        print(f"[{insight['type']}] {insight['category']}: {insight['message']}")
