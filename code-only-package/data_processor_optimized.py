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

    def load_pricing_data_fast(self):
        """Load pricing data - much smaller, loads quickly"""
        pricing_file = self.data_dir / "Preço.csv"
        print("Carregando dados de preços...")
        self.pricing_data = pd.read_csv(pricing_file, encoding='utf-8')
        self.pricing_data['mes'] = pd.to_datetime(self.pricing_data['mes'])
        print(f"✓ Preços carregados: {len(self.pricing_data):,} registros")
        return self.pricing_data

    def load_iqvia_sample(self, sample_months=3):
        """Load only recent months of IQVIA data for faster startup"""
        iqvia_files = sorted(self.data_dir.glob("historico_iqvia_*.parquet"))

        # Load only last N months
        recent_files = iqvia_files[-sample_months:]

        print(f"Carregando IQVIA (últimos {sample_months} meses)...")
        dfs = []
        for file in recent_files:
            print(f"  - {file.name}")
            df = pd.read_parquet(file)
            dfs.append(df)

        self.iqvia_data = pd.concat(dfs, ignore_index=True)
        self.iqvia_data['data'] = pd.to_datetime(
            self.iqvia_data['id_periodo'].astype(str),
            format='%Y%m'
        )

        print(f"✓ IQVIA carregado: {len(self.iqvia_data):,} registros")
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

    def quick_load(self, sample_months=3):
        """Fast loading for dashboard startup"""
        print("\n" + "="*60)
        print("🚀 CARREGAMENTO RÁPIDO INICIADO")
        print("="*60 + "\n")

        # Load pricing (small, fast)
        self.load_pricing_data_fast()

        # Load only recent IQVIA data
        self.load_iqvia_sample(sample_months)

        # Pre-compute aggregations
        self.precompute_aggregations()

        print("\n" + "="*60)
        print("✅ DADOS PRONTOS PARA USO!")
        print("="*60 + "\n")

    def get_revenue_metrics(self):
        """Calculate revenue metrics from pre-aggregated data"""
        if self.pricing_data is None:
            return {}

        total = self.pricing_data['rbv'].sum()
        units = self.pricing_data['qt_unidade_vendida'].sum()

        metrics = {
            'total_revenue': total,
            'total_units': units,
            'avg_price': self.pricing_data['preco_medio'].mean(),
            'unique_products': self.pricing_data['produto'].nunique(),
            'orders_count': len(self.pricing_data)
        }
        return metrics

    def get_market_share_metrics(self):
        """Calculate market share metrics from pre-aggregated data"""
        if self.iqvia_data is None:
            return {}

        metrics = {
            'avg_share': self.iqvia_data['share'].mean(),
            'total_rd_sales': self.iqvia_data['venda_rd'].sum(),
            'total_competitor_sales': self.iqvia_data['venda_concorrente'].sum(),
            'zero_sales_rate': (self.iqvia_data['venda_rd'] == 0).mean(),
            'unique_products': self.iqvia_data['cd_produto'].nunique(),
            'unique_stores': self.iqvia_data['cd_filial'].nunique(),
            'unique_bricks': self.iqvia_data['cd_brick'].nunique()
        }
        return metrics

    def get_revenue_trend(self):
        """Get revenue trend from pre-aggregated data"""
        if self.pricing_aggregated is None:
            return pd.DataFrame()

        df = self.pricing_aggregated['by_month'].copy()
        df.columns = ['data', 'receita', 'unidades', 'preco_medio']
        return df

    def get_market_share_trend(self):
        """Get market share trend from pre-aggregated data"""
        if self.iqvia_aggregated is None:
            return pd.DataFrame()

        df = self.iqvia_aggregated['by_period'].copy()
        df.columns = ['data', 'share', 'venda_rd', 'venda_concorrente', 'produtos']
        return df[['data', 'share', 'venda_rd', 'venda_concorrente']]

    def get_channel_performance(self):
        """Get performance by channel from pre-aggregated data"""
        if self.pricing_aggregated is None:
            return pd.DataFrame()

        df = self.pricing_aggregated['by_channel'].copy()
        df['pct_receita'] = df['rbv'] / df['rbv'].sum() * 100
        return df

    def get_category_performance(self):
        """Get performance by category from pre-aggregated data"""
        if self.pricing_aggregated is None:
            return pd.DataFrame()

        df = self.pricing_aggregated['by_category'].copy()
        df.columns = ['categoria', 'receita', 'unidades', 'preco_medio', 'produtos']
        df['pct_receita'] = df['receita'] / df['receita'].sum() * 100
        df = df.sort_values('receita', ascending=False)
        return df

    def get_state_performance(self):
        """Get performance by state from pre-aggregated data"""
        if self.pricing_aggregated is None:
            return pd.DataFrame()

        df = self.pricing_aggregated['by_state'].copy()
        df.columns = ['estado', 'receita', 'unidades', 'preco_medio']
        df['pct_receita'] = df['receita'] / df['receita'].sum() * 100
        df = df.sort_values('receita', ascending=False)
        return df

    def get_top_products(self, top_n=20, by='revenue'):
        """Get top performing products"""
        if self.pricing_data is None:
            return pd.DataFrame()

        sort_col = 'rbv' if by == 'revenue' else 'qt_unidade_vendida'

        df = self.pricing_data.groupby('produto').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean',
            'neogrupo': 'first'
        }).reset_index()

        df = df.sort_values(sort_col, ascending=False).head(top_n)
        df.columns = ['produto', 'receita', 'unidades', 'preco_medio', 'categoria']
        return df

    def get_zero_sales_analysis(self):
        """Analyze zero sales opportunities from pre-aggregated data"""
        if self.iqvia_aggregated is None or 'zero_sales' not in self.iqvia_aggregated:
            return pd.DataFrame()

        df = self.iqvia_aggregated['zero_sales'].copy()
        df.columns = ['produto', 'venda_concorrente', 'lojas_afetadas']
        df = df.sort_values('venda_concorrente', ascending=False)
        return df

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
        """Calculate different business scenarios"""
        current_metrics = self.get_revenue_metrics()
        current_revenue = current_metrics['total_revenue']

        zero_sales_df = self.get_zero_sales_analysis()
        avg_price = current_metrics['avg_price']
        potential_units = zero_sales_df['venda_concorrente'].sum() * 0.5
        scenario_1_revenue = current_revenue + (potential_units * avg_price)

        current_share = self.get_market_share_metrics()['avg_share']
        share_increase = 0.05
        scenario_2_revenue = current_revenue * (1 + (share_increase / current_share)) if current_share > 0 else current_revenue

        top_products = self.get_top_products(top_n=int(current_metrics['unique_products'] * 0.2))
        top_revenue = top_products['receita'].sum()
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
