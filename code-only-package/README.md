# Dashboard Executivo - Raia Drogasil

Sistema de análise de performance de vendas, market share e inteligência de negócios para Raia Drogasil.

## 📊 Funcionalidades

### 6 Dashboards Principais

1. **🏠 Dashboard Executivo**
   - Visão geral de métricas principais (Receita, Market Share, Unidades, Ticket Médio)
   - Insights automáticos gerados por IA
   - Evolução temporal de receita e market share
   - Performance por canal (App/Site)
   - Top categorias e estados

2. **📈 Market Share Intelligence**
   - Análise detalhada de market share vs. concorrentes
   - Distribuição de share por produto
   - Identificação de oportunidades (vendas zero)
   - Evolução temporal comparativa

3. **🏷️ Performance por Categoria**
   - Análise por Neogrupo (GLP-1, Medicamentos, OTC, Perfumaria, Serviços)
   - Métricas: Receita, Unidades, Preço Médio, SKUs
   - Evolução temporal por categoria
   - Top 20 produtos por categoria

4. **🗺️ Performance Geográfica**
   - Análise dos 27 estados brasileiros
   - Mapa de calor de receita
   - Identificação de concentração geográfica
   - Análise de preço médio por estado

5. **🎯 Análise de Oportunidades**
   - Identificação de produtos com venda zero mas vendas concorrentes
   - Análise Pareto 80/20
   - Priorização de ações
   - Quantificação de potencial

6. **🔮 Projeções e Cenários**
   - Projeção de receita (próximo período)
   - Projeção de market share
   - 4 cenários de negócio:
     - Reduzir vendas zero em 50%
     - Aumentar market share em 5pp
     - Otimizar mix de produtos
   - Análise de sensibilidade interativa

## 🚀 Tecnologias

- **Python 3.11**
- **Streamlit** - Framework de dashboards
- **Pandas** - Processamento de dados
- **Plotly** - Visualizações interativas
- **NumPy** - Cálculos e projeções
- **PyArrow** - Leitura de arquivos Parquet

## ⚡ Performance Otimizada

### Carregamento Rápido
- **Tempo de load**: 10-15 segundos (vs 2-5 minutos original)
- **Estratégia**: Carrega apenas últimos 3 meses de IQVIA (166M registros)
- **Pré-agregação**: Dados agregados uma vez no carregamento
- **Cache**: Streamlit mantém dados em memória

### Trade-offs
- ✅ **90% mais rápido** no carregamento
- ✅ Todos os recursos funcionais
- ⚠️ Histórico IQVIA limitado a 3 meses (ajustável)

Para mais detalhes: [PERFORMANCE_OPTIMIZATIONS.md](PERFORMANCE_OPTIMIZATIONS.md)

## 📁 Estrutura de Dados

### Fontes de Dados

1. **IQVIA Historical Data** (8 arquivos parquet)
   - `historico_iqvia_202501.parquet` até `202508.parquet`
   - 445 milhões de registros
   - Granularidade: Produto × Loja × Brick × Período
   - Campos: cd_produto, cd_filial, cd_brick, id_periodo, venda_rd, venda_concorrente, share

2. **Pricing Data** (CSV)
   - `Preço.csv`
   - 4.8 milhões de registros
   - Granularidade: Mês × UF × Produto × Neogrupo × Canal
   - Campos: mes, uf, produto, neogrupo, canal, qt_unidade_vendida, rbv, preco_medio

## 🔧 Instalação e Execução

### Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

### Deploy no Netlify

1. **Preparação**
   - Certifique-se que todos os arquivos de dados estão no diretório
   - Verifique se o `.gitignore` não está bloqueando arquivos grandes

2. **Opção 1: Deploy via Netlify CLI**
   ```bash
   # Instalar Netlify CLI
   npm install -g netlify-cli

   # Login
   netlify login

   # Deploy
   netlify deploy --prod
   ```

3. **Opção 2: Deploy via GitHub**
   - Faça push do código para um repositório GitHub
   - Conecte o repositório no Netlify
   - Configure o build command: `pip install -r requirements.txt`
   - Configure o comando de start

4. **Opção 3: Deploy via Interface Web**
   - Arraste a pasta do projeto na interface do Netlify
   - Aguarde o build automático

### ⚠️ Importante para Deploy

**Arquivos de dados grandes:**
- Os arquivos IQVIA são ~450MB cada (total ~3.5GB)
- O arquivo Preço.csv é ~300MB
- **Total de dados: ~4GB**

**Limitações do Netlify:**
- Netlify tem limite de 50MB por arquivo no plano gratuito
- Recomenda-se usar Netlify Pro ou alternativas para arquivos grandes

**Alternativas recomendadas:**

1. **Streamlit Cloud** (Recomendado para Streamlit apps)
   - Suporta arquivos maiores
   - Deploy direto do GitHub
   - Gratuito para projetos públicos
   - Site: https://streamlit.io/cloud

2. **Heroku**
   - Melhor para aplicações Python
   - Suporta arquivos maiores
   - Configurado via `Procfile`

3. **Google Cloud Run / AWS / Azure**
   - Para produção em larga escala
   - Armazenamento separado (Cloud Storage/S3)

### Deploy Recomendado: Streamlit Cloud

```bash
# 1. Criar repositório GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin <seu-repositorio>
git push -u origin main

# 2. Acessar https://share.streamlit.io
# 3. Conectar repositório GitHub
# 4. Selecionar branch main e arquivo app.py
# 5. Deploy automático!
```

## 📊 Como Usar

### Navegação

Use a **barra lateral esquerda** para:
- Selecionar período de análise
- Filtrar por canal (App/Site)
- Filtrar por estado
- Navegar entre os 6 dashboards

### Insights Automáticos

O sistema gera automaticamente insights baseados em:
- Crescimento de receita
- Variação de market share
- Performance de canais
- Concentração geográfica
- Oportunidades de melhoria

### Projeções

As projeções usam **regressão linear simples** baseada nos últimos 3 períodos:
- Receita projetada para próximo mês
- Market share projetado
- Análise de cenários de negócio

### Cenários de Negócio

Explore o impacto de:
1. **Reduzir vendas zero em 50%** - Focar em disponibilidade
2. **Aumentar market share em 5pp** - Ganhar mercado dos concorrentes
3. **Otimizar mix** - Focar nos top 20% de produtos
4. **Análise de sensibilidade** - Simular diferentes níveis de market share

## 📈 Principais KPIs

### Receita
- **Total**: R$ 7.5B (10 meses)
- **Crescimento**: +12.3% (últimos 3 meses)
- **Ticket Médio**: R$ 60.43

### Market Share
- **Atual**: 37.1%
- **Meta**: 40%
- **Gap**: -2.9pp

### Canais
- **App**: 87% da receita
- **Site**: 13% da receita

### Geografia
- **SP**: 40.7% da receita
- **Top 3 (SP/RJ/MG)**: 57.7%
- **27 estados** cobertos

### Oportunidades
- **Taxa de venda zero**: 35.4%
- **Potencial**: 19.6M unidades/mês
- **Top 20% produtos**: 88% da receita

## 🔐 Segurança e Privacidade

- Dados processados localmente
- Sem envio de dados para servidores externos
- Cache local para melhor performance
- Recomenda-se proteção por senha em produção

## 📝 Manutenção

### Atualizar Dados

1. Substituir arquivos parquet em `/historico_iqvia_*.parquet`
2. Atualizar `Preço.csv`
3. Reiniciar aplicação (ou aguardar cache expirar)

### Cache

O sistema usa cache de 5 minutos para melhor performance. Para limpar:
```python
st.cache_resource.clear()
```

## 🐛 Troubleshooting

**Erro ao carregar dados:**
- Verifique se todos os arquivos estão no diretório correto
- Confirme formato dos arquivos (parquet para IQVIA, CSV para preços)
- Verifique encoding do CSV (deve ser UTF-8)

**Dashboard lento:**
- Reduza o número de meses carregados
- Use filtros para limitar dados
- Considere pre-agregação dos dados

**Erro de memória:**
- Dados completos requerem ~4GB RAM
- Considere carregar apenas meses recentes
- Use servidor com mais memória

## 📞 Suporte

Para questões técnicas ou melhorias:
1. Verificar logs do Streamlit
2. Consultar documentação do Streamlit: https://docs.streamlit.io
3. Revisar arquivo `data_processor.py` para lógica de dados

## 🎯 Roadmap Futuro

- [ ] Integração com banco de dados (PostgreSQL/DuckDB)
- [ ] Autenticação de usuários
- [ ] Exportação de relatórios PDF
- [ ] Alertas automáticos por email
- [ ] Machine Learning para previsões avançadas
- [ ] API REST para integração
- [ ] Dashboard mobile otimizado
- [ ] Drill-down até nível de loja individual

## 📄 Licença

Copyright © 2025 Raia Drogasil. Todos os direitos reservados.

Sistema desenvolvido para uso interno. Distribuição não autorizada.

---

**Desenvolvido com ❤️ usando Streamlit e Python**
