"""
Data Processing Pipeline for Raia Drogasil Dashboard
Handles data loading, transformation, and aggregation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class DataProcessor:
    """Main data processing class for dashboard"""

    def __init__(self, data_dir="."):
        self.data_dir = Path(data_dir)
        self.iqvia_data = None
        self.pricing_data = None
        self.merged_data = None

    def load_all_data(self):
        """Load all data sources"""
        print("Carregando dados IQVIA...")
        self.load_iqvia_data()
        print("Carregando dados de preços...")
        self.load_pricing_data()
        print("Dados carregados com sucesso!")

    def load_iqvia_data(self, months=None):
        """Load IQVIA parquet files"""
        iqvia_files = sorted(self.data_dir.glob("historico_iqvia_*.parquet"))

        if months:
            iqvia_files = iqvia_files[:months]

        dfs = []
        for file in iqvia_files:
            df = pd.read_parquet(file)
            dfs.append(df)

        self.iqvia_data = pd.concat(dfs, ignore_index=True)

        # Add date column
        self.iqvia_data['data'] = pd.to_datetime(
            self.iqvia_data['id_periodo'].astype(str),
            format='%Y%m'
        )

        return self.iqvia_data

    def load_pricing_data(self):
        """Load pricing CSV file"""
        pricing_file = self.data_dir / "Preço.csv"
        self.pricing_data = pd.read_csv(pricing_file, encoding='utf-8')
        self.pricing_data['mes'] = pd.to_datetime(self.pricing_data['mes'])
        return self.pricing_data

    def get_revenue_metrics(self, start_date=None, end_date=None):
        """Calculate revenue metrics"""
        df = self.pricing_data.copy()

        if start_date:
            df = df[df['mes'] >= start_date]
        if end_date:
            df = df[df['mes'] <= end_date]

        metrics = {
            'total_revenue': df['rbv'].sum(),
            'total_units': df['qt_unidade_vendida'].sum(),
            'avg_price': df['preco_medio'].mean(),
            'unique_products': df['produto'].nunique(),
            'orders_count': len(df)
        }

        return metrics

    def get_market_share_metrics(self, start_date=None, end_date=None):
        """Calculate market share metrics"""
        df = self.iqvia_data.copy()

        if start_date:
            df = df[df['data'] >= start_date]
        if end_date:
            df = df[df['data'] <= end_date]

        metrics = {
            'avg_share': df['share'].mean(),
            'total_rd_sales': df['venda_rd'].sum(),
            'total_competitor_sales': df['venda_concorrente'].sum(),
            'zero_sales_rate': (df['venda_rd'] == 0).mean(),
            'unique_products': df['cd_produto'].nunique(),
            'unique_stores': df['cd_filial'].nunique(),
            'unique_bricks': df['cd_brick'].nunique()
        }

        return metrics

    def get_revenue_trend(self, period='D'):
        """Get revenue trend over time"""
        df = self.pricing_data.groupby('mes').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean'
        }).reset_index()

        df.columns = ['data', 'receita', 'unidades', 'preco_medio']
        return df

    def get_market_share_trend(self):
        """Get market share trend over time"""
        df = self.iqvia_data.groupby('data').agg({
            'share': 'mean',
            'venda_rd': 'sum',
            'venda_concorrente': 'sum'
        }).reset_index()

        df.columns = ['data', 'share', 'venda_rd', 'venda_concorrente']
        return df

    def get_channel_performance(self):
        """Get performance by channel"""
        df = self.pricing_data.groupby('canal').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean'
        }).reset_index()

        df['pct_receita'] = df['rbv'] / df['rbv'].sum() * 100
        return df

    def get_category_performance(self):
        """Get performance by category"""
        df = self.pricing_data.groupby('neogrupo').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean',
            'produto': 'nunique'
        }).reset_index()

        df.columns = ['categoria', 'receita', 'unidades', 'preco_medio', 'produtos']
        df['pct_receita'] = df['receita'] / df['receita'].sum() * 100
        df = df.sort_values('receita', ascending=False)

        return df

    def get_state_performance(self):
        """Get performance by state"""
        df = self.pricing_data.groupby('uf').agg({
            'rbv': 'sum',
            'qt_unidade_vendida': 'sum',
            'preco_medio': 'mean'
        }).reset_index()

        df.columns = ['estado', 'receita', 'unidades', 'preco_medio']
        df['pct_receita'] = df['receita'] / df['receita'].sum() * 100
        df = df.sort_values('receita', ascending=False)

        return df

    def get_top_products(self, top_n=20, by='revenue'):
        """Get top performing products"""
        if by == 'revenue':
            sort_col = 'rbv'
        else:
            sort_col = 'qt_unidade_vendida'

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
        """Analyze zero sales opportunities"""
        df = self.iqvia_data[self.iqvia_data['venda_rd'] == 0].copy()

        # Group by product
        zero_sales = df.groupby('cd_produto').agg({
            'venda_concorrente': 'sum',
            'cd_filial': 'nunique'
        }).reset_index()

        zero_sales.columns = ['produto', 'venda_concorrente', 'lojas_afetadas']
        zero_sales = zero_sales.sort_values('venda_concorrente', ascending=False)

        return zero_sales

    def calculate_pareto(self, df, value_col, id_col='produto'):
        """Calculate Pareto 80/20 analysis"""
        df_sorted = df.sort_values(value_col, ascending=False).copy()
        df_sorted['cumsum'] = df_sorted[value_col].cumsum()
        df_sorted['cumsum_pct'] = df_sorted['cumsum'] / df_sorted[value_col].sum() * 100

        return df_sorted

    def get_growth_rates(self, periods=3):
        """Calculate growth rates for recent periods"""
        # Revenue growth
        revenue_trend = self.get_revenue_trend()
        revenue_trend = revenue_trend.sort_values('data')

        if len(revenue_trend) >= periods + 1:
            current = revenue_trend['receita'].iloc[-1]
            previous = revenue_trend['receita'].iloc[-(periods + 1)]
            revenue_growth = ((current - previous) / previous) * 100
        else:
            revenue_growth = 0

        # Market share growth
        share_trend = self.get_market_share_trend()
        share_trend = share_trend.sort_values('data')

        if len(share_trend) >= periods + 1:
            current_share = share_trend['share'].iloc[-1]
            previous_share = share_trend['share'].iloc[-(periods + 1)]
            share_growth = ((current_share - previous_share) / previous_share) * 100
        else:
            share_growth = 0

        return {
            'revenue_growth': revenue_growth,
            'share_growth': share_growth
        }

    def predict_next_month_revenue(self, periods=3):
        """Simple linear regression prediction for next month revenue"""
        trend = self.get_revenue_trend()
        trend = trend.sort_values('data').tail(periods)

        if len(trend) < 2:
            return None

        # Simple linear regression
        x = np.arange(len(trend))
        y = trend['receita'].values

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)

        # Predict next period
        next_value = p(len(trend))

        return max(0, next_value)

    def predict_market_share(self, periods=3):
        """Predict market share trend"""
        trend = self.get_market_share_trend()
        trend = trend.sort_values('data').tail(periods)

        if len(trend) < 2:
            return None

        # Simple linear regression
        x = np.arange(len(trend))
        y = trend['share'].values

        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)

        # Predict next period
        next_value = p(len(trend))

        return max(0, min(1, next_value))

    def calculate_scenarios(self):
        """Calculate different business scenarios"""
        current_metrics = self.get_revenue_metrics()
        current_revenue = current_metrics['total_revenue']

        # Scenario 1: Reduce zero sales by 50%
        zero_sales_df = self.get_zero_sales_analysis()

        # Try to estimate revenue impact (simplified)
        avg_price = current_metrics['avg_price']
        potential_units = zero_sales_df['venda_concorrente'].sum() * 0.5
        scenario_1_revenue = current_revenue + (potential_units * avg_price)

        # Scenario 2: Increase market share by 5pp
        current_share = self.get_market_share_metrics()['avg_share']
        share_increase = 0.05
        scenario_2_revenue = current_revenue * (1 + (share_increase / current_share))

        # Scenario 3: Optimize product mix (focus on top 20%)
        top_products = self.get_top_products(top_n=int(current_metrics['unique_products'] * 0.2))
        top_revenue = top_products['receita'].sum()
        # Assume 20% increase in top products
        scenario_3_revenue = current_revenue + (top_revenue * 0.2)

        scenarios = {
            'current': current_revenue,
            'reduce_zero_sales': scenario_1_revenue,
            'increase_share': scenario_2_revenue,
            'optimize_mix': scenario_3_revenue
        }

        return scenarios

    def generate_insights(self):
        """Generate automated insights from data"""
        insights = []

        # Revenue insights
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

        # Market share insights
        share_metrics = self.get_market_share_metrics()

        if share_metrics['zero_sales_rate'] > 0.30:
            insights.append({
                'type': 'warning',
                'category': 'Market Share',
                'message': f'{share_metrics["zero_sales_rate"]*100:.1f}% das oportunidades têm venda zero - grande potencial de melhoria'
            })

        if share_metrics['avg_share'] < 0.40:
            insights.append({
                'type': 'warning',
                'category': 'Market Share',
                'message': f'Market share de {share_metrics["avg_share"]*100:.1f}% abaixo da meta de 40%'
            })

        # Channel insights
        channel_perf = self.get_channel_performance()
        app_pct = channel_perf[channel_perf['canal'] == 'App']['pct_receita'].values

        if len(app_pct) > 0 and app_pct[0] > 85:
            insights.append({
                'type': 'positive',
                'category': 'Canal',
                'message': f'App dominando com {app_pct[0]:.1f}% da receita - estratégia mobile validada'
            })

        # Category insights
        category_perf = self.get_category_performance()
        top_category = category_perf.iloc[0]

        insights.append({
            'type': 'info',
            'category': 'Categoria',
            'message': f'{top_category["categoria"]} lidera com {top_category["pct_receita"]:.1f}% da receita'
        })

        # Geographic insights
        state_perf = self.get_state_performance()
        sp_pct = state_perf[state_perf['estado'] == 'SP']['pct_receita'].values

        if len(sp_pct) > 0 and sp_pct[0] > 35:
            insights.append({
                'type': 'warning',
                'category': 'Geografia',
                'message': f'São Paulo concentra {sp_pct[0]:.1f}% da receita - risco de concentração'
            })

        return insights


class CacheManager:
    """Simple cache manager to improve dashboard performance"""

    def __init__(self):
        self.cache = {}
        self.cache_time = {}
        self.ttl = 300  # 5 minutes

    def get(self, key):
        """Get cached value if still valid"""
        if key in self.cache:
            if (datetime.now() - self.cache_time[key]).seconds < self.ttl:
                return self.cache[key]
        return None

    def set(self, key, value):
        """Set cache value"""
        self.cache[key] = value
        self.cache_time[key] = datetime.now()

    def clear(self):
        """Clear all cache"""
        self.cache = {}
        self.cache_time = {}


if __name__ == "__main__":
    # Test data processor
    processor = DataProcessor()
    processor.load_all_data()

    print("\n=== Revenue Metrics ===")
    print(processor.get_revenue_metrics())

    print("\n=== Market Share Metrics ===")
    print(processor.get_market_share_metrics())

    print("\n=== Channel Performance ===")
    print(processor.get_channel_performance())

    print("\n=== Category Performance ===")
    print(processor.get_category_performance())

    print("\n=== Insights ===")
    for insight in processor.generate_insights():
        print(f"[{insight['type']}] {insight['category']}: {insight['message']}")
