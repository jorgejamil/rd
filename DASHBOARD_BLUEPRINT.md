# Dashboard Blueprint & Metrics Framework
**Raia Drogasil - Data-Driven Management Dashboard**

---

## Overview

This document provides a comprehensive blueprint for building management dashboards based on the available data sources:
- IQVIA Historical Data (445M records, Jan-Aug 2025)
- Pricing Data (4.8M records, Jan-Oct 2025)
- Excel Dashboard Templates (current state reference)

---

## Dashboard Architecture

### Tier 1: Executive Dashboard (CEO/C-Suite)
**Purpose**: High-level strategic metrics
**Update Frequency**: Daily
**Users**: Executive leadership

### Tier 2: Operational Dashboards (Directors/Managers)
**Purpose**: Detailed functional area metrics
**Update Frequency**: Daily/Real-time
**Users**: Category managers, regional directors, operations leads

### Tier 3: Analytical Dashboards (Analysts)
**Purpose**: Deep-dive analysis and exploration
**Update Frequency**: As-needed
**Users**: Data analysts, business intelligence team

---

## Dashboard 1: Executive Performance Dashboard

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│                  EXECUTIVE DASHBOARD                         │
│                  Updated: [Timestamp]                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Revenue    │  │ Market Share │  │ Active Orders│      │
│  │  R$ 747M     │  │    37.1%     │  │   166.3M     │      │
│  │  ▲ 12.3%     │  │  ▼ 2.1%      │  │  ▲ 8.7%      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  Revenue Trend (Last 30 Days)                                │
│  ┌────────────────────────────────────────────────────┐     │
│  │                                                      │     │
│  │         [Line Chart: Daily Revenue]                 │     │
│  │                                                      │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌─────────────────────────┐  ┌────────────────────────┐   │
│  │ Channel Performance      │  │ Top 5 Categories       │   │
│  │                          │  │                        │   │
│  │ [Donut Chart]           │  │ [Bar Chart]            │   │
│  │ App:    87.0%           │  │ 1. Med Marca   R$2.5B  │   │
│  │ Site:   13.0%           │  │ 2. Perfumaria  R$1.7B  │   │
│  │                          │  │ 3. GLP-1       R$1.2B  │   │
│  │                          │  │ 4. OTC Marca   R$1.1B  │   │
│  │                          │  │ 5. Med Genérico R$806M │   │
│  └─────────────────────────┘  └────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Geographic Performance (Revenue Heatmap - Brazil)    │   │
│  │                                                        │   │
│  │              [Brazil Map Heatmap]                     │   │
│  │                                                        │   │
│  │  SP: 40.7%  RJ: 9.8%  MG: 7.2%  PR: 5.3%  GO: 4.4%   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics

#### Primary KPIs (Big Numbers)
1. **Total Revenue (MTD/QTD/YTD)**
   - Data Source: `pricing.rbv`
   - Calculation: `SUM(rbv) WHERE mes >= [period_start]`
   - Target Comparison: vs. Budget/Forecast
   - Trend: MoM/YoY % change

2. **Market Share %**
   - Data Source: `iqvia.share`
   - Calculation: `AVG(share) * 100`
   - Target: 40% (aspirational)
   - Trend: MoM change in basis points

3. **Active Orders/Units Sold**
   - Data Source: `pricing.qt_unidade_vendida`
   - Calculation: `SUM(qt_unidade_vendida)`
   - Trend: MoM % change

#### Secondary KPIs

4. **Average Order Value**
   - Calculation: `SUM(rbv) / SUM(qt_unidade_vendida)`
   - Current: R$ 60.43
   - Track by channel/category

5. **Revenue per Product**
   - Calculation: `SUM(rbv) / COUNT(DISTINCT produto)`
   - Efficiency metric for portfolio management

6. **Revenue Concentration**
   - Top 10 products % of total revenue
   - Geographic concentration (Top 3 states %)

### Filters
- Date Range Selector (MTD/QTD/YTD/Custom)
- Channel Filter (All/App/Site)
- Geographic Region (National/State)

### Alerts & Insights
- 🔴 Market share drop >2% MoM
- 🟡 Revenue 5% below target
- 🟢 New category or product breakout performance

---

## Dashboard 2: Market Share Intelligence

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│              MARKET SHARE INTELLIGENCE DASHBOARD             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Overall Market Position                                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Market Share Evolution (Monthly)                  │     │
│  │  [Line Chart: RD vs. Competitor Trend]            │     │
│  │                                                      │     │
│  │  ━━━━ RD (37.1%)    ━ ━ ━ Competitor (62.9%)     │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌──────────────────────────┐  ┌──────────────────────────┐ │
│  │ Share by Category        │  │ Share Distribution       │ │
│  │                          │  │                          │ │
│  │ [Bar Chart: Horizontal] │  │ [Histogram]              │ │
│  │                          │  │                          │ │
│  │ GLP-1 Marca      ████   │  │ <25%: 16,694 products    │ │
│  │ Med Genérico     ████   │  │ 25-50%: 9,185 products   │ │
│  │ Med Marca        ███    │  │ >50%: 7,648 products     │ │
│  │ OTC Genérico     ███    │  │                          │ │
│  │ OTC Marca        ███    │  │ Opportunity: 49.8%       │ │
│  │ Perfumaria       ███    │  │ products <25% share      │ │
│  │ Serviços         ██     │  │                          │ │
│  └──────────────────────────┘  └──────────────────────────┘ │
│                                                               │
│  Product Performance Matrix                                   │
│  ┌────────────────────────────────────────────────────┐     │
│  │                                                      │     │
│  │       [Scatter Plot: Market Share vs Revenue]      │     │
│  │                                                      │     │
│  │   High Share, High Revenue   │  Low Share, High Revenue   │
│  │   (Protect)                   │  (Opportunity)             │
│  │   ─────────────────────────────────────────────────       │
│  │   High Share, Low Revenue    │  Low Share, Low Revenue    │
│  │   (Niche Winners)             │  (Evaluate/Exit)           │
│  │                                                      │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Top 20 Share Gain Opportunities                       │   │
│  │                                                        │   │
│  │ Product      Category       Share   Competitor  Gap   │   │
│  │ ──────────────────────────────────────────────────── │   │
│  │ 753359       Med Marca     15.2%   42.8%      R$12M  │   │
│  │ 81276        GLP-1         8.1%    61.3%      R$8M   │   │
│  │ ...                                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics

1. **Overall Market Share**
   - Current: 37.1%
   - Target: 40%
   - Trend: Last 8 months

2. **Share by Category**
   - Breakdown by 7 neogroups
   - Identify strongest/weakest categories

3. **Share Distribution**
   - Products by share bucket (<25%, 25-50%, >50%)
   - Opportunity sizing

4. **Competitive Gap Index**
   - Products where competitors dominate
   - Merge IQVIA + Pricing to estimate revenue at risk
   - Calculation: `SUM((venda_concorrente - venda_rd) * preco_medio) WHERE venda_rd = 0`

5. **Share Gain/Loss Products**
   - MoM share change by product
   - Top 20 gainers and losers

### Filters
- Date Range
- Category/Neogroup
- Share Bucket (<25%, 25-50%, >50%)
- Geographic Region

### Drill-down Capabilities
- Click product → Product detail view with:
  - Share trend over time
  - Geographic performance
  - Store-level share (IQVIA brick data)
  - Pricing comparison

---

## Dashboard 3: Category Performance

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│              CATEGORY PERFORMANCE DASHBOARD                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Category Selector: [GLP-1 MARCA ▼]                         │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Revenue    │  │  Units Sold  │  │  Avg Price   │      │
│  │  R$ 1.19B    │  │    970K      │  │  R$ 912.13   │      │
│  │  ▲ 15.2%     │  │  ▲ 8.3%      │  │  ▲ 6.4%      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  Revenue & Volume Trend (Last 10 Months)                     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  [Combo Chart: Bar (Revenue) + Line (Units)]      │     │
│  │                                                      │     │
│  │  Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌─────────────────────────┐  ┌────────────────────────┐   │
│  │ Top 10 Products         │  │ Channel Mix            │   │
│  │                          │  │                        │   │
│  │ [Table]                 │  │ [Stacked Bar]          │   │
│  │ Product    Revenue      │  │                        │   │
│  │ ─────────────────────   │  │ App:   R$ 1.04B (87%) │   │
│  │ 753359     R$ 45M       │  │ Site:  R$ 150M  (13%) │   │
│  │ 81276      R$ 38M       │  │                        │   │
│  │ ...                     │  │ [Trend over time]      │   │
│  └─────────────────────────┘  └────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Geographic Performance by State                       │   │
│  │                                                        │   │
│  │ State  Revenue    Units    Avg Price  % of Total     │   │
│  │ ─────────────────────────────────────────────────     │   │
│  │ SP     R$ 485M    395K     R$ 908      40.8%         │   │
│  │ RJ     R$ 117M    98K      R$ 915       9.8%         │   │
│  │ MG     R$ 86M     71K      R$ 911       7.2%         │   │
│  │ ...                                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────┐  ┌────────────────────────┐   │
│  │ Price Trend Analysis    │  │ Market Share           │   │
│  │                          │  │                        │   │
│  │ [Line Chart]            │  │ [Gauge Chart]          │   │
│  │                          │  │                        │   │
│  │ Avg: R$ 912.13          │  │ Current: 42.3%         │   │
│  │ Min: R$ 850             │  │ Target:  50.0%         │   │
│  │ Max: R$ 985             │  │                        │   │
│  │                          │  │ vs Comp: Losing       │   │
│  └─────────────────────────┘  └────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Categories to Track
1. GLP-1 MARCA (High-value)
2. MEDICAMENTO MARCA (Largest revenue)
3. MEDICAMENTO GENÉRICO (Volume play)
4. PERFUMARIA (Traffic driver)
5. OTC MARCA (Margin opportunity)
6. OTC GENÉRICO (Low penetration)
7. SERVIÇOS (Emerging)

### Key Metrics per Category

1. **Revenue & Growth**
   - Total revenue
   - MoM/YoY growth %
   - % of total company revenue

2. **Volume & Units**
   - Total units sold
   - Units per transaction
   - Volume growth rate

3. **Pricing Metrics**
   - Average price
   - Price trend (up/down)
   - Price elasticity (if A/B test data available)

4. **Market Share**
   - Category-specific market share from IQVIA
   - Share trend
   - Competitive position

5. **Channel Performance**
   - Revenue by channel (App/Site)
   - Channel preference shifts

6. **Geographic Distribution**
   - Revenue by state
   - High/low performing regions
   - Penetration rate

### Filters
- Category/Neogroup selector
- Date range
- Channel
- State/Region

---

## Dashboard 4: Geographic Performance

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│              GEOGRAPHIC PERFORMANCE DASHBOARD                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Brazil Overview                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │                                                      │     │
│  │         [Interactive Brazil Map - Choropleth]      │     │
│  │                                                      │     │
│  │  Colored by Revenue Intensity                       │     │
│  │  Click state for detail view                        │     │
│  │                                                      │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  State Performance Ranking                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Rank State  Revenue    Share  Units    Avg Price     │   │
│  │ ──────────────────────────────────────────────────── │   │
│  │  1   SP     R$ 3.04B  40.7%  50.2M    R$ 60.58      │   │
│  │  2   RJ     R$ 733M    9.8%  12.4M    R$ 59.11      │   │
│  │  3   MG     R$ 542M    7.2%   9.1M    R$ 59.56      │   │
│  │  4   PR     R$ 398M    5.3%   6.7M    R$ 59.40      │   │
│  │  5   GO     R$ 332M    4.4%   5.6M    R$ 59.29      │   │
│  │  ... (27 states total)                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────┐  ┌────────────────────────┐   │
│  │ State Concentration     │  │ Growth Rate by State   │   │
│  │                          │  │                        │   │
│  │ [Treemap]               │  │ [Bar Chart]            │   │
│  │                          │  │                        │   │
│  │ SP (40.7%) dominates    │  │ Top Growers:           │   │
│  │ Top 3: 57.7% of revenue │  │ 1. RR  +45.2%          │   │
│  │ Long tail: 24 states    │  │ 2. AC  +32.1%          │   │
│  │                          │  │ 3. AP  +28.7%          │   │
│  └─────────────────────────┘  └────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### State Detail View (Drill-down)

When user clicks a state (e.g., SP):

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back to Brazil Overview        STATE: SÃO PAULO (SP)     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Revenue    │  │ Market Share │  │    Units     │      │
│  │  R$ 3.04B    │  │    38.2%     │  │    50.2M     │      │
│  │  40.7% total │  │  ▼ 1.5%      │  │  ▲ 9.1%      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌─────────────────────────┐  ┌────────────────────────┐   │
│  │ Top Categories in SP    │  │ Brick Performance      │   │
│  │                          │  │                        │   │
│  │ [Pie Chart]             │  │ [Table: Top 20 Bricks] │   │
│  │                          │  │                        │   │
│  │ Med Marca:     35%      │  │ Brick  Revenue  Share  │   │
│  │ Perfumaria:    23%      │  │ ───────────────────── │   │
│  │ GLP-1:         18%      │  │ 245    R$ 85M   45.2%  │   │
│  │ OTC Marca:     12%      │  │ 1764   R$ 78M   32.1%  │   │
│  │ Med Genérico:  10%      │  │ ...                   │   │
│  │ Other:          2%      │  │                        │   │
│  └─────────────────────────┘  └────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Store Performance in SP (IQVIA Data)                 │   │
│  │                                                        │   │
│  │ Store ID  Revenue  Market Share  Zero-Sales Rate     │   │
│  │ ──────────────────────────────────────────────────── │   │
│  │ 3396      R$ 12.5M    42.1%         28.3%            │   │
│  │ 2503      R$ 11.8M    38.7%         31.2%            │   │
│  │ 3954      R$ 10.2M    35.4%         35.8%            │   │
│  │ ...       (stores in SP)                             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics

1. **Revenue by State**
   - Total and % of company revenue
   - Ranking (1-27)
   - Trend (MoM/YoY growth)

2. **Market Share by State**
   - From IQVIA brick data rolled up to state
   - vs. National average
   - Competitive position

3. **Revenue Concentration**
   - Herfindahl index or similar
   - % from top N states
   - Risk assessment

4. **Growth Opportunities**
   - Underperforming states with high potential
   - Population vs. revenue correlation
   - Competitive intensity analysis

5. **Brick-Level Analysis (IQVIA)**
   - 1,331 geographic bricks
   - Revenue and share by brick
   - Identify micro-market opportunities

### Filters
- State selector
- Category filter
- Date range
- Channel

---

## Dashboard 5: Operational Efficiency

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│            OPERATIONAL EFFICIENCY DASHBOARD                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Inventory & Assortment Metrics                              │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Zero-Sales    │  │Active Products│ │ Sales/Product│      │
│  │   Rate       │  │              │  │              │      │
│  │   35.4%      │  │   20,896     │  │   R$ 35.8K   │      │
│  │   🔴 High    │  │   ▼ 2.1%     │  │   ▲ 14.2%    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  Zero-Sales Analysis                                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │                                                      │     │
│  │  [Waterfall Chart: Impact Quantification]          │     │
│  │                                                      │     │
│  │  Total Opportunities:    19.6M scenarios           │     │
│  │  Competitor present:      19.6M                     │     │
│  │  Est. Revenue at Risk:    R$ 1.2B/month           │     │
│  │                                                      │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌─────────────────────────┐  ┌────────────────────────┐   │
│  │ Top 50 Zero-Sales Opps  │  │ Zero-Sales by Category │   │
│  │                          │  │                        │   │
│  │ [Table: Sortable]       │  │ [Bar Chart]            │   │
│  │                          │  │                        │   │
│  │ Product  Category  Est  │  │ Med Marca:     42%     │   │
│  │          Revenue        │  │ Perfumaria:    28%     │   │
│  │ ──────────────────────  │  │ GLP-1:         18%     │   │
│  │ 753359   Med Marca R$8M │  │ OTC Marca:     8%      │   │
│  │ 81276    GLP-1    R$6M  │  │ Med Genérico:  3%      │   │
│  │ ...                     │  │ Other:         1%      │   │
│  │                          │  │                        │   │
│  └─────────────────────────┘  └────────────────────────┘   │
│                                                               │
│  Product Portfolio Health                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                                                        │   │
│  │  [Scatter: Revenue vs Units Sold]                    │   │
│  │                                                        │   │
│  │  High Rev, High Units  │  High Rev, Low Units        │   │
│  │  (Superstars)          │  (Premium/GLP-1)            │   │
│  │  ────────────────────────────────────────────        │   │
│  │  Low Rev, High Units   │  Low Rev, Low Units         │   │
│  │  (Evaluate pricing)    │  (Consider discontinue)     │   │
│  │                                                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Store Efficiency Metrics (IQVIA Data)                │   │
│  │                                                        │   │
│  │ Store    Revenue  Products  Sales/Product Zero-Rate  │   │
│  │ ──────────────────────────────────────────────────── │   │
│  │ 3396     R$ 12.5M   1,245      R$ 10.0K     28.3%    │   │
│  │ 2503     R$ 11.8M   1,189      R$ 9.9K      31.2%    │   │
│  │ ...      (3,741 stores)                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics

1. **Zero-Sales Rate**
   - % of product-location combos with no sales
   - Current: 35.4%
   - Target: <20%
   - Trend over time

2. **Zero-Sales Revenue Impact**
   - Merge IQVIA (zero sales scenarios) + Pricing (avg price)
   - Calculation: `SUM(venda_concorrente * preco_medio) WHERE venda_rd = 0`
   - Estimated monthly revenue at risk

3. **Product Assortment Efficiency**
   - Total products available
   - Active products (sold in period)
   - Sales per product
   - Revenue per product

4. **Store Performance**
   - Revenue per store
   - Products per store
   - Zero-sales rate by store
   - Market share by store

5. **Portfolio Rationalization Candidates**
   - Low revenue, low volume products
   - Products with <X sales in 90 days
   - Long-tail analysis

### Filters
- Date range
- Category
- Store/Region
- Zero-sales threshold

### Recommended Actions Section
- Top 20 products to add to specific stores
- Products to discontinue (low performers)
- Store assortment optimization suggestions

---

## Dashboard 6: Pricing Analytics

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│                PRICING ANALYTICS DASHBOARD                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Overall Pricing Metrics                                      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Avg Order    │  │ Price Range  │  │ Price Changes│      │
│  │   Value      │  │              │  │  (30 days)   │      │
│  │  R$ 60.43    │  │ R$7 - R$912  │  │     847      │      │
│  │  ▲ 3.2%      │  │  123x range  │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  Price Distribution by Category                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │                                                      │     │
│  │  [Box Plot: Price Distribution by Neogroup]        │     │
│  │                                                      │     │
│  │  GLP-1 Marca       ─────────────────■──────────    │     │
│  │  Med Marca         ────────■────────────            │     │
│  │  Perfumaria        ──────■──────                    │     │
│  │  OTC Marca         ─────■──────                     │     │
│  │  Med Genérico      ────■────                        │     │
│  │  OTC Genérico      ──■───                           │     │
│  │  Serviços          ■──                              │     │
│  │                                                      │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌─────────────────────────┐  ┌────────────────────────┐   │
│  │ Price Changes (30 days) │  │ Price Elasticity       │   │
│  │                          │  │                        │   │
│  │ [Table: Sortable]       │  │ [Scatter Plot]         │   │
│  │                          │  │                        │   │
│  │ Product  Old    New  Δ% │  │ Price Change vs        │   │
│  │ ───────────────────────  │  │ Volume Change          │   │
│  │ 753359   R$95  R$105 +11│  │                        │   │
│  │ 81276    R$905 R$890 -2 │  │ Identify elastic vs    │   │
│  │ ...                     │  │ inelastic products     │   │
│  └─────────────────────────┘  └────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Price Comparison: Channel Analysis                    │   │
│  │                                                        │   │
│  │ Category         App Avg    Site Avg    Difference   │   │
│  │ ──────────────────────────────────────────────────── │   │
│  │ GLP-1 Marca      R$ 913     R$ 908      +0.6%        │   │
│  │ Med Marca        R$ 96.45   R$ 95.21    +1.3%        │   │
│  │ Perfumaria       R$ 48.12   R$ 47.45    +1.4%        │   │
│  │ ...                                                   │   │
│  │                                                        │   │
│  │ Insight: Minimal channel pricing differences         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Geographic Pricing Variation                          │   │
│  │                                                        │   │
│  │ [Heatmap: Product × State showing price variance]    │   │
│  │                                                        │   │
│  │ Identify opportunities for regional pricing          │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics

1. **Average Order Value**
   - Overall: R$ 60.43
   - By channel, category, state
   - Trend analysis

2. **Price Distribution**
   - Min, max, median, quartiles
   - By category
   - Outlier identification

3. **Price Changes**
   - Products with recent price changes
   - Magnitude and frequency
   - Impact on volume (elasticity)

4. **Price Elasticity**
   - Calculate: % change in quantity / % change in price
   - Identify elastic vs. inelastic products
   - Optimize pricing strategy

5. **Channel Price Comparison**
   - App vs. Site pricing
   - Current: ~1% difference (minimal)
   - Opportunity for channel-specific pricing?

6. **Geographic Price Variation**
   - Price differences across states
   - Cost of living adjustment opportunities
   - Competitive pricing by region

### Filters
- Category
- Product
- State
- Channel
- Date range

---

## Data Integration Requirements

### Required Dimension Tables

#### 1. Product Master Table
```sql
CREATE TABLE dim_product (
    produto_id INT PRIMARY KEY,
    cd_produto INT,  -- IQVIA code
    produto_nome VARCHAR(255),
    neogrupo VARCHAR(50),
    categoria VARCHAR(50),
    subcategoria VARCHAR(50),
    ativo BOOLEAN,
    data_cadastro DATE
);
```

#### 2. Geographic Mapping
```sql
CREATE TABLE dim_geography (
    brick_id INT PRIMARY KEY,
    cd_brick INT,  -- IQVIA brick code
    brick_nome VARCHAR(255),
    uf CHAR(2),
    municipio VARCHAR(100),
    regiao VARCHAR(50)
);
```

#### 3. Store Master
```sql
CREATE TABLE dim_store (
    filial_id INT PRIMARY KEY,
    cd_filial INT,  -- IQVIA store code
    filial_nome VARCHAR(255),
    uf CHAR(2),
    municipio VARCHAR(100),
    tipo_loja VARCHAR(50),  -- Mature, New, etc.
    data_abertura DATE
);
```

#### 4. Time Dimension
```sql
CREATE TABLE dim_time (
    date_id INT PRIMARY KEY,
    data DATE,
    ano INT,
    mes INT,
    dia INT,
    trimestre INT,
    semana INT,
    dia_semana VARCHAR(20),
    mes_ano VARCHAR(7),  -- YYYY-MM
    id_periodo INT  -- YYYYMM for IQVIA
);
```

### Fact Tables

#### 1. IQVIA Sales Fact
```sql
CREATE TABLE fact_iqvia_sales (
    id BIGINT PRIMARY KEY,
    produto_id INT,
    filial_id INT,
    brick_id INT,
    date_id INT,
    venda_rd INT,
    venda_concorrente INT,
    share DECIMAL(10,6),
    FOREIGN KEY (produto_id) REFERENCES dim_product,
    FOREIGN KEY (filial_id) REFERENCES dim_store,
    FOREIGN KEY (brick_id) REFERENCES dim_geography,
    FOREIGN KEY (date_id) REFERENCES dim_time
);
```

#### 2. Pricing/Sales Fact
```sql
CREATE TABLE fact_pricing_sales (
    id BIGINT PRIMARY KEY,
    date_id INT,
    produto_id INT,
    uf CHAR(2),
    neogrupo VARCHAR(50),
    canal VARCHAR(10),
    qt_unidade_vendida INT,
    rbv DECIMAL(15,2),
    preco_medio DECIMAL(10,2),
    FOREIGN KEY (produto_id) REFERENCES dim_product,
    FOREIGN KEY (date_id) REFERENCES dim_time
);
```

---

## Technical Implementation

### ETL Pipeline

```python
# Pseudocode for daily ETL process

def daily_etl_pipeline():
    # 1. Extract
    iqvia_files = check_new_iqvia_files()  # Monthly
    pricing_data = load_pricing_incremental()  # Daily/Weekly

    # 2. Transform
    iqvia_clean = clean_iqvia_data(iqvia_files)
    pricing_clean = clean_pricing_data(pricing_data)

    # 3. Enrich
    products = enrich_product_dimensions(iqvia_clean, pricing_clean)
    geography = map_brick_to_state(iqvia_clean)

    # 4. Load
    load_to_fact_table(iqvia_clean, 'fact_iqvia_sales')
    load_to_fact_table(pricing_clean, 'fact_pricing_sales')

    # 5. Aggregate
    build_aggregates()  # Pre-calculate common queries

    # 6. Quality Checks
    run_data_quality_checks()
    send_alerts_if_issues()

    # 7. Refresh Dashboards
    refresh_all_dashboards()
```

### Performance Optimization

1. **Pre-aggregated Tables**
   - Daily/monthly aggregates by category
   - State-level rollups
   - Product performance summaries

2. **Indexing Strategy**
   - Index on frequently filtered columns (date, product, state)
   - Composite indexes for common join patterns

3. **Partitioning**
   - Partition fact tables by month
   - Improve query performance for recent data

4. **Caching**
   - Cache dashboard queries for 15 minutes
   - Invalidate on new data arrival

### Technology Stack

**Recommended:**
- **Storage**: Parquet files (current) + PostgreSQL/DuckDB for analytics
- **ETL**: Python (Pandas, Polars) + Airflow for orchestration
- **Visualization**:
  - Power BI (Microsoft ecosystem integration)
  - Tableau (advanced visualizations)
  - Looker (embedded analytics)
  - Streamlit (quick prototyping)
- **Infrastructure**: Cloud-based (AWS/Azure/GCP) for scalability

---

## KPI Definitions & Calculations

### Revenue Metrics

**1. Total Revenue (RBV)**
```sql
SELECT SUM(rbv) as total_revenue
FROM fact_pricing_sales
WHERE date_id BETWEEN start_date AND end_date;
```

**2. Revenue Growth Rate**
```sql
SELECT
    ((current_period.revenue - prior_period.revenue) / prior_period.revenue) * 100 as growth_rate
FROM
    (SELECT SUM(rbv) as revenue FROM fact_pricing_sales WHERE mes = current_month) current_period,
    (SELECT SUM(rbv) as revenue FROM fact_pricing_sales WHERE mes = prior_month) prior_period;
```

### Market Share Metrics

**3. Overall Market Share**
```sql
SELECT AVG(share) * 100 as market_share_pct
FROM fact_iqvia_sales
WHERE date_id BETWEEN start_date AND end_date;
```

**4. Market Share by Category**
```sql
SELECT
    p.neogrupo,
    AVG(i.share) * 100 as market_share_pct
FROM fact_iqvia_sales i
JOIN dim_product p ON i.produto_id = p.produto_id
WHERE i.date_id BETWEEN start_date AND end_date
GROUP BY p.neogrupo;
```

### Efficiency Metrics

**5. Zero-Sales Rate**
```sql
SELECT
    (COUNT(*) FILTER (WHERE venda_rd = 0)::FLOAT / COUNT(*)) * 100 as zero_sales_rate
FROM fact_iqvia_sales
WHERE date_id = current_period;
```

**6. Revenue at Risk (Zero-Sales Impact)**
```sql
SELECT SUM(i.venda_concorrente * p.preco_medio) as revenue_at_risk
FROM fact_iqvia_sales i
JOIN fact_pricing_sales p
    ON i.produto_id = p.produto_id
    AND i.date_id = p.date_id
WHERE i.venda_rd = 0
    AND i.venda_concorrente > 0;
```

**7. Sales per Product**
```sql
SELECT
    SUM(rbv) / COUNT(DISTINCT produto_id) as revenue_per_product
FROM fact_pricing_sales
WHERE date_id BETWEEN start_date AND end_date;
```

### Channel Metrics

**8. Channel Mix**
```sql
SELECT
    canal,
    SUM(rbv) as channel_revenue,
    (SUM(rbv)::FLOAT / (SELECT SUM(rbv) FROM fact_pricing_sales WHERE date_id = current_period)) * 100 as pct_total
FROM fact_pricing_sales
WHERE date_id = current_period
GROUP BY canal;
```

### Geographic Metrics

**9. Revenue by State**
```sql
SELECT
    uf,
    SUM(rbv) as state_revenue,
    (SUM(rbv)::FLOAT / (SELECT SUM(rbv) FROM fact_pricing_sales WHERE date_id = current_period)) * 100 as pct_total
FROM fact_pricing_sales
WHERE date_id = current_period
GROUP BY uf
ORDER BY state_revenue DESC;
```

**10. Revenue Concentration (Herfindahl Index)**
```sql
SELECT
    SUM(POWER(state_pct, 2)) as herfindahl_index
FROM (
    SELECT
        (SUM(rbv)::FLOAT / (SELECT SUM(rbv) FROM fact_pricing_sales)) as state_pct
    FROM fact_pricing_sales
    GROUP BY uf
) subquery;
-- Index closer to 1 = high concentration, closer to 0 = distributed
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- ✅ Set up data infrastructure (database, ETL pipeline)
- ✅ Create dimension tables (product, geography, time, store)
- ✅ Load historical data from IQVIA and Pricing sources
- ✅ Build data quality monitoring framework
- ✅ Implement basic ETL automation

### Phase 2: Core Dashboards (Weeks 3-4)
- ✅ Executive Dashboard (Priority 1)
- ✅ Market Share Intelligence Dashboard (Priority 1)
- ✅ Category Performance Dashboard (Priority 2)
- ⏸ Set up automated daily refreshes

### Phase 3: Advanced Analytics (Weeks 5-6)
- ⏸ Geographic Performance Dashboard
- ⏸ Operational Efficiency Dashboard
- ⏸ Pricing Analytics Dashboard
- ⏸ Implement drill-down and cross-filtering

### Phase 4: Optimization (Weeks 7-8)
- ⏸ Performance tuning (queries, aggregates, caching)
- ⏸ User training and documentation
- ⏸ Feedback collection and iteration
- ⏸ Advanced features (alerts, mobile views, API access)

### Phase 5: Advanced Features (Ongoing)
- ⏸ Predictive analytics (demand forecasting, share prediction)
- ⏸ Automated insights and anomaly detection
- ⏸ What-if scenario modeling
- ⏸ Integration with additional data sources

---

## Success Metrics

**Adoption Metrics:**
- Daily active users
- Dashboard views per user
- Time spent in dashboards

**Business Impact:**
- Decisions made using dashboard insights
- Zero-sales rate reduction
- Market share improvement
- Revenue growth attributed to insights

**Technical Performance:**
- Dashboard load time <3 seconds
- Data freshness <24 hours
- 99.9% uptime
- Query performance <5 seconds

---

**Document Version:** 1.0
**Last Updated:** October 14, 2025
**Owner:** Data & Analytics Team
