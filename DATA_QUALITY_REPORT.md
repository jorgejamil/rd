# Data Quality & Management Insights Report
**Raia Drogasil - Analysis Date: October 14, 2025**

---

## Executive Summary

This report analyzes 3 primary datasets containing pharmaceutical sales, market share, and pricing data:
- **IQVIA Historical Data**: 445M records across 8 months (Jan-Aug 2025)
- **Pricing Data**: 4.8M records across 10 months (Jan-Oct 2025)
- **Excel Dashboards**: Daily operational reports with multiple business views

**Overall Data Quality Score: 8.5/10** - High quality with specific optimization opportunities

---

## 1. Data Quality Assessment

### 1.1 IQVIA Historical Market Data

**Dataset Overview:**
- **Volume**: 445,385,005 records (8 parquet files, ~3.5GB total)
- **Granularity**: Product × Store × Geographic Brick × Month
- **Coverage**: January 2025 - August 2025
- **File Structure**: Consistent monthly parquet files (~445MB each)

**Schema:**
```
cd_produto (int64)           - Product code
cd_filial (int64)            - Store/branch code
cd_brick (int64)             - Geographic brick code
id_periodo (int64)           - Period (YYYYMM format)
venda_rd (int64)             - RD sales units
venda_concorrente (int64)    - Competitor sales units
share (float64)              - Market share (0-1)
```

**Data Quality Metrics:**

| Metric | Value | Quality Score |
|--------|-------|---------------|
| Missing Values | 0 (0.00%) | ✅ Excellent |
| Duplicate Records | 0 (0.00%) | ✅ Excellent |
| Invalid Share Values | 0 | ✅ Excellent |
| Unique Products | 33,527 | ✅ Good |
| Unique Stores | 3,741 | ✅ Good |
| Unique Geographic Bricks | 1,331 | ✅ Good |

**Key Findings:**

✅ **Strengths:**
- Zero missing values across all fields
- Perfect data consistency across 8 monthly files
- Valid share calculations (all values between 0-1)
- No duplicate records
- Clean data types and formatting

⚠️ **Issues & Opportunities:**

1. **High Zero-Sales Rate**
   - 35.4% of records (19.6M) have zero RD sales
   - All zero-sales records have competitor sales present
   - **Business Impact**: Indicates significant market presence gaps
   - **Recommendation**: Inventory optimization or product assortment strategy

2. **Market Share Distribution**
   - Average market share: 37.11%
   - 49.8% of products have <25% market share
   - Only 22.8% of products have >50% market share
   - **Opportunity**: Targeted marketing for low-share products

3. **Sales Statistics**
   - Mean RD sales per record: 6.89 units
   - Mean competitor sales: 17.04 units (2.5x higher)
   - **Insight**: Competitors capture majority of market volume

---

### 1.2 Pricing Data

**Dataset Overview:**
- **Volume**: 4,762,059 records (303MB CSV)
- **Granularity**: Month × State × Product × Neogroup × Channel
- **Coverage**: January 2025 - October 2025 (2 months ahead of IQVIA)

**Schema:**
```
mes (object)                 - Month (YYYY-MM-DD format)
uf (object)                  - State code (27 Brazilian states)
produto (int64)              - Product code
neogrupo (object)            - Product category
canal (object)               - Sales channel (App/Site)
qt_unidade_vendida (int64)   - Quantity sold
rbv (float64)                - Revenue (BRL)
preco_medio (float64)        - Average price (BRL)
```

**Data Quality Metrics:**

| Metric | Value | Quality Score |
|--------|-------|---------------|
| Missing Values | 0 (0.00%) | ✅ Excellent |
| Duplicate Records | 0 (0.00%) | ✅ Excellent |
| Negative Values | 0 | ✅ Excellent |
| Price Calculation Accuracy | 100% | ✅ Excellent |
| Zero Values | 0 | ✅ Excellent |
| Geographic Coverage | 27/27 states | ✅ Complete |

**Key Findings:**

✅ **Strengths:**
- Perfect data completeness - no missing values
- Accurate price calculations (preco_medio = rbv/qt_unidade_vendida)
- Complete geographic coverage (all 27 Brazilian states)
- Clean categorical data (7 neogroups, 2 channels)
- Consistent date formatting

**Business Intelligence:**

1. **Product Categories (Neogroups)**

| Category | Avg Price (BRL) | Total Revenue (BRL) | Units Sold | Revenue % |
|----------|----------------|---------------------|------------|-----------|
| GLP-1 MARCA | 912.13 | 1.19B | 970K | 15.9% |
| MEDICAMENTO MARCA | 96.26 | 2.50B | 33.3M | 33.4% |
| MEDICAMENTO GENÉRICO | 36.43 | 806M | 33.5M | 10.8% |
| PERFUMARIA | 48.01 | 1.67B | 41.5M | 22.3% |
| OTC MARCA | 54.19 | 1.14B | 36.4M | 15.2% |
| OTC GENÉRICO | 17.71 | 61M | 5.0M | 0.8% |
| SERVIÇOS | 7.40 | 121M | 15.6M | 1.6% |

**Key Insight**: GLP-1 products have 18x higher unit price but represent significant revenue

2. **Channel Performance**

| Channel | Revenue (BRL) | Units Sold | Avg Price | Revenue Share |
|---------|---------------|------------|-----------|---------------|
| App | 6.51B | 144.6M | 61.01 | 87.0% |
| Site | 970M | 21.6M | 59.20 | 13.0% |

**Critical Finding**: App dominates with 87% of revenue - mobile-first strategy validated

3. **Geographic Performance**
   - Top 3 states: SP (40.7%), RJ (9.8%), MG (7.2%)
   - São Paulo alone represents 40.7% of total revenue
   - Long-tail of 24 states share ~41% of revenue

---

### 1.3 Excel Dashboards

**Files Analyzed:**
1. `One Page de Acompanhamento Diário 210925.xlsx` (114KB)
2. `One Page Omnichannel Diário 210925.xlsx` (164KB)

**Structure:**
- Multiple sheets with different business views (RD, Maduras, GLP-1, Mounjaro)
- Complex formatting with merged cells
- Dashboard-style layout (not normalized data)
- Data as of September 21, 2025

**Data Quality Assessment:**

⚠️ **Limitations:**
- Complex formatting makes programmatic analysis difficult
- Column names unclear ("Unnamed: X" pattern)
- Requires manual interpretation of structure
- Not suitable for direct analytical queries
- Appears to be presentation layer, not source data

✅ **Value:**
- Provides business context and KPI structure
- Shows existing dashboard design patterns
- Indicates key metrics being tracked (EvA, EvM, Ruptura Index, etc.)

**Recommendation**: Use IQVIA and Pricing datasets as primary sources; Excel files for business logic reference only

---

## 2. Cross-Dataset Analysis

### 2.1 Data Integration Opportunities

**Product Code Overlap:**
- IQVIA unique products: 33,527
- Pricing unique products: 24,972
- **Overlap**: 22,711 products (67.7% of IQVIA)
- **IQVIA-only**: 10,816 products (32.3%)
- **Pricing-only**: 2,261 products

**Critical Issue**: 32% of IQVIA products don't appear in pricing data

**Possible Causes:**
1. Discontinued products (appear in market data but no longer sold by RD)
2. Data integration lag
3. Competitors-only products (market data without RD sales)
4. Data quality issue requiring investigation

**Recommendation**: Create product master table to reconcile codes

### 2.2 Time Coverage Gap

- IQVIA: Jan-Aug 2025 (8 months)
- Pricing: Jan-Oct 2025 (10 months)
- **Gap**: 2 months of pricing data without market context

**Opportunity**: Most recent data available for internal analysis; market share projections needed

### 2.3 Dimensional Differences

| Dimension | IQVIA | Pricing | Integration Challenge |
|-----------|-------|---------|----------------------|
| Product | ✅ cd_produto | ✅ produto | 68% overlap - needs mapping |
| Time | ✅ Monthly | ✅ Monthly | Different coverage periods |
| Geography | ✅ Brick (1,331) | ✅ State (27) | Needs brick-to-state mapping |
| Store | ✅ cd_filial (3,741) | ❌ N/A | Cannot link pricing to stores |
| Category | ❌ N/A | ✅ neogrupo (7) | Requires product mapping |
| Channel | ❌ N/A | ✅ canal (2) | IQVIA is market-level |

**Data Model Requirement**: Dimension tables needed for complete integration

---

## 3. Management Insights & Opportunities

### 3.1 Market Position Analysis

**Current State:**
- Average market share: **37.11%** (below 50% threshold)
- Competitor sales 2.5x higher than RD sales on average
- 35% of product-location combinations show zero RD sales despite competitor presence

**Strategic Opportunities:**
1. **Market Share Growth**: Target the 16,694 products with <25% share
2. **Gap Closure**: Address 19.6M zero-sales scenarios
3. **Competitive Intelligence**: Analyze competitor strengths in high-gap products

### 3.2 Product Portfolio Optimization

**Pareto Analysis:**
- Top 20% of products generate **88.36%** of revenue
- 24,972 unique products (likely too broad)
- Average 20,896 products sold per month

**Recommendations:**
1. **Focus Strategy**: Prioritize top revenue generators
2. **Long-tail Optimization**: Review bottom 20% for discontinuation candidates
3. **Category Strategy**: GLP-1 represents high-value opportunity (15.9% revenue, 0.6% units)

### 3.3 Channel Strategy

**Mobile Dominance:**
- App: 87% of revenue, 87% of units
- Site: 13% of revenue, 13% of units
- Similar unit pricing suggests no channel discount strategy

**Opportunities:**
1. Continue app optimization (primary revenue driver)
2. Investigate site underperformance - user experience gap?
3. Monitor for channel preference shifts over time

### 3.4 Geographic Expansion

**Current Concentration:**
- Top 3 states: 57.7% of revenue (SP, RJ, MG)
- São Paulo: 40.7% of revenue (single state)
- High geographic concentration risk

**Strategies:**
1. **Protect Core**: Maintain leadership in SP/RJ/MG
2. **Selective Expansion**: Identify high-potential underperforming states
3. **Risk Diversification**: Reduce dependence on São Paulo

### 3.5 Inventory & Assortment

**Critical Finding:** 35% zero-sales rate indicates:
1. **Overassortment**: Too many products in too many locations
2. **Stock-outs**: Products available to competitors but not RD
3. **Demand Prediction Issues**: Poor forecasting leading to wrong inventory

**Financial Impact:**
- 19.6M missed sales opportunities per month
- Potential revenue at risk: Unknown without pricing merge

**Action Items:**
1. Merge IQVIA + Pricing to quantify revenue at risk
2. Product-location rationalization study
3. Improve demand forecasting models
4. Review distribution strategy

### 3.6 Pricing Strategy

**Category Insights:**
- **High-value**: GLP-1 (R$912 avg), Medicamento Marca (R$96)
- **Volume**: Genéricos (36M units), Perfumaria (42M units)
- **Price Range**: 123x difference between lowest (R$7) and highest (R$912)

**Opportunities:**
1. **Premium Strategy**: GLP-1 shows customers willing to pay premium
2. **Generic Penetration**: Low avg price (R$36) but high volume - margin opportunity
3. **Cross-category**: Bundle high-margin categories with traffic drivers

---

## 4. Dashboard Recommendations

### 4.1 Proposed Dashboard Structure

#### **Executive Dashboard** (Daily/Weekly)
- **Revenue KPIs**: Daily/MTD/YTD revenue vs. target
- **Market Share**: Overall and by key categories
- **Channel Mix**: App vs. Site trends
- **Top 10 Products**: Revenue and units sold
- **Geographic Performance**: State-level heatmap

#### **Category Performance Dashboard**
- **Neogroup Analysis**: Revenue, units, avg price by category
- **Category Trends**: MoM growth rates
- **GLP-1 Deep Dive**: Separate dashboard for high-value category
- **Generic vs. Brand**: Comparative analysis

#### **Market Share Dashboard**
- **Overall Share Trends**: Monthly evolution
- **Product-level Share**: Top/bottom performers
- **Competitive Gap Analysis**: Zero-sales scenarios
- **Share Gain/Loss**: Month-over-month changes

#### **Geographic Dashboard**
- **State Performance**: Revenue, units, market share by UF
- **Brick Analysis**: Detailed geographic performance (IQVIA data)
- **Store Performance**: Store-level sales and efficiency (IQVIA data)
- **Expansion Opportunities**: Identify high-potential areas

#### **Operational Dashboard**
- **Inventory Efficiency**: Zero-sales rate tracking
- **Product Assortment**: Products per location optimization
- **Stockout Analysis**: Competitor-present, RD-absent scenarios
- **Fulfillment Metrics**: Channel-specific performance

### 4.2 Key Metrics (KPIs)

**Financial Metrics:**
- Revenue (RBV): Daily/MTD/QTD/YTD
- Units Sold: Volume trends
- Average Order Value: By channel/category
- Revenue per Store: Efficiency metric

**Market Metrics:**
- Market Share %: Overall and by product
- Share of Voice: vs. top competitors
- Penetration Rate: Products × Locations
- Competitive Gap Index: Zero-sales scenarios / Total opportunities

**Operational Metrics:**
- Active Products: Products sold in period
- Sales per Product: Efficiency ratio
- Zero-Sales Rate: % of product-location combos with no sales
- Stock Coverage: Products available vs. market demand

**Channel Metrics:**
- Channel Mix %: App vs. Site
- Channel Growth Rate: MoM trends
- Channel Conversion: If traffic data available
- Cross-channel Behavior: Customer switching patterns

**Geographic Metrics:**
- Revenue Concentration: Top N states %
- Geographic Penetration: States/Bricks covered
- Regional Growth Rates: State-level YoY/MoM
- Market Share by Region: Performance variations

### 4.3 Technical Requirements

**Data Refresh:**
- IQVIA: Monthly (new file each month)
- Pricing: Daily/Weekly (append to existing)
- Dashboards: Daily refresh at minimum

**Integration Needs:**
1. Product master table (reconcile IQVIA ↔ Pricing codes)
2. Geographic mapping (Brick → State)
3. Store master table (code → name → region)
4. Category hierarchy (Product → Neogroup)
5. Time dimension table (support various aggregations)

**Technology Stack Recommendations:**
- **Storage**: Keep parquet files (efficient columnar storage)
- **ETL**: Python/Pandas for data processing
- **Database**: Consider DuckDB or PostgreSQL for querying
- **Visualization**: Power BI, Tableau, or Looker for dashboards
- **Orchestration**: Airflow or similar for automated pipelines

---

## 5. Data Quality Monitoring

### 5.1 Ongoing Quality Checks

**Daily Checks:**
- [ ] File arrival confirmation (IQVIA/Pricing)
- [ ] Record count validation (vs. historical patterns)
- [ ] Missing value detection
- [ ] Duplicate record identification

**Weekly Checks:**
- [ ] Cross-dataset product overlap % (should be ~68%)
- [ ] Zero-sales rate trends (flag if >40%)
- [ ] Price calculation accuracy audit
- [ ] Channel mix validation (App should be ~85-90%)

**Monthly Checks:**
- [ ] Market share calculation audit
- [ ] Geographic coverage verification
- [ ] Product portfolio changes review
- [ ] Data integration reconciliation

### 5.2 Data Quality Alerts

**Critical Alerts:**
- Missing monthly IQVIA file
- Pricing data >7 days stale
- Product overlap drops below 60%
- Any missing values detected
- Duplicate records found

**Warning Alerts:**
- Zero-sales rate exceeds 40%
- Market share drops >5% MoM
- Revenue concentration in SP exceeds 45%
- Channel mix shifts >10% MoM

---

## 6. Action Plan

### Immediate Actions (Week 1-2)

1. **Create Product Master Table**
   - Reconcile 33,527 IQVIA products with 24,972 pricing products
   - Identify 10,816 IQVIA-only products and classify
   - Map products to neogroups for category analysis

2. **Build Geographic Mapping**
   - Create brick-to-state mapping table
   - Validate coverage across dimensions
   - Enable IQVIA-to-Pricing geographic joins

3. **Set Up Basic Dashboards**
   - Executive dashboard with core KPIs
   - Market share trends dashboard
   - Channel performance dashboard

### Short-term Actions (Month 1)

4. **Zero-Sales Analysis**
   - Merge IQVIA + Pricing to quantify revenue at risk
   - Identify top 100 zero-sales opportunities
   - Present findings to inventory/merchandising teams

5. **Competitive Intelligence**
   - Analyze products with <25% market share
   - Identify competitor strengths by category
   - Recommend targeted marketing campaigns

6. **Data Quality Framework**
   - Implement automated daily checks
   - Set up alerting system
   - Create data quality dashboard

### Medium-term Actions (Quarter 1)

7. **Advanced Analytics**
   - Predictive models for demand forecasting
   - Market share prediction models
   - Price elasticity analysis
   - Product assortment optimization algorithm

8. **Integration Expansion**
   - Integrate additional data sources (if available)
   - Historical trending (expand beyond 8-10 months)
   - Customer-level data integration (if available)

9. **Dashboard Evolution**
   - Add predictive analytics views
   - Implement drill-down capabilities
   - Create mobile-optimized executive views
   - Add automated insights/anomaly detection

---

## 7. Conclusion

### Summary Assessment

**Data Quality: 8.5/10**
- Excellent technical quality (no missing values, duplicates, or errors)
- Strong coverage across products, geographies, and time
- Some integration challenges between datasets
- Opportunity for enhancement through dimension tables

### Key Takeaways

1. **Data is Analysis-Ready**: Both IQVIA and Pricing datasets are clean and reliable
2. **Integration Needed**: 32% product code gap requires investigation and mapping
3. **Significant Opportunity**: 35% zero-sales rate represents major improvement potential
4. **Mobile-First Validated**: 87% app revenue share confirms strategic direction
5. **Portfolio Complexity**: 25K products may be too broad - optimization opportunity

### Recommended Next Steps

1. ✅ Build product master table (Priority 1)
2. ✅ Quantify zero-sales revenue impact (Priority 1)
3. ✅ Launch executive dashboard (Priority 1)
4. ⏸ Set up data quality monitoring (Priority 2)
5. ⏸ Develop predictive models (Priority 2)
6. ⏸ Expand integration to additional sources (Priority 3)

---

**Report Prepared By:** Data Analysis Team
**Date:** October 14, 2025
**Version:** 1.0
