# 🚀 Quick Start - Dashboard RD

## Início Rápido em 3 Passos

### 1️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Executar Dashboard
```bash
streamlit run app.py
```

### 3️⃣ Abrir no Navegador
Acesse: **http://localhost:8501**

---

## ⏱️ O Que Esperar

### Primeira Execução
- **Tempo de carregamento**: 10-15 segundos
- **Mensagem**: "🚀 Carregamento rápido... Aguarde 10-15 segundos"
- **O que acontece**:
  - Carrega 4.8M registros de preços (completo)
  - Carrega últimos 3 meses de IQVIA (~166M registros)
  - Pré-computa agregações

### Execuções Seguintes
- **Tempo**: Instantâneo (<1 segundo)
- **Cache**: Streamlit mantém dados na memória
- **Reload automático**: Mudanças no código recarregam app

---

## 📊 Como Usar o Dashboard

### Navegação

#### Barra Lateral (Esquerda)
- **Status**: ✅ Dados carregados + contador de registros
- **Filtros**: Período, Canal, Estado
- **Menu**: Selecione entre 6 dashboards

#### Dashboards Disponíveis

1. **🏠 Dashboard Executivo**
   - KPIs principais
   - Insights automáticos
   - Visão geral de receita e market share

2. **📈 Market Share**
   - Análise competitiva
   - Oportunidades de vendas zero
   - Distribuição de share por produto

3. **🏷️ Performance por Categoria**
   - Análise por Neogrupo
   - Evolução temporal
   - Top 20 produtos

4. **🗺️ Performance Geográfica**
   - Análise por estado
   - Concentração geográfica
   - Ranking de receita

5. **🎯 Análise de Oportunidades**
   - Produtos com venda zero
   - Análise Pareto 80/20
   - Priorização de ações

6. **🔮 Projeções e Cenários**
   - Previsões de receita e share
   - 4 cenários de negócio
   - Análise de sensibilidade

---

## 🎯 Funcionalidades Principais

### Insights Automáticos
O dashboard gera insights automaticamente:
- ✅ Crescimento de receita
- ⚠️ Alertas de performance
- 📊 Análise de market share
- 📱 Performance de canais

### Projeções
- **Receita próximo mês**: Regressão linear
- **Market share projetado**: Tendência calculada
- **Cenários de negócio**: 4 simulações

### Filtros Dinâmicos
- **Período**: Último mês, 3 meses, 6 meses, ano
- **Canal**: Todos, App, Site
- **Estado**: Todos ou UF específica

---

## 💡 Dicas de Uso

### Para Análise Rápida
1. Vá direto ao **Dashboard Executivo**
2. Leia os **insights automáticos**
3. Verifique os **KPIs principais**

### Para Análise Profunda
1. **Market Share**: Identifique produtos com baixo share
2. **Oportunidades**: Veja produtos com venda zero
3. **Cenários**: Simule impacto de ações

### Para Planejamento
1. **Projeções**: Veja tendências futuras
2. **Análise de Sensibilidade**: Teste diferentes cenários
3. **Geografia**: Identifique oportunidades regionais

---

## ⚙️ Configurações Avançadas

### Carregar Mais Histórico

Edite `app.py` linha 75:

```python
# Carregar 6 meses (em vez de 3)
processor.quick_load(sample_months=6)
```

**Trade-off**: Mais lento (~30 segundos), mais histórico

### Ajustar Porta

```bash
streamlit run app.py --server.port 8502
```

### Modo Headless (Servidor)

```bash
streamlit run app.py --server.headless true
```

---

## 🐛 Problemas Comuns

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### "Carregamento muito lento"
- Verifique RAM disponível (precisa ~2GB)
- Reduza `sample_months` para 2 ou 1
- Feche outros aplicativos

### "Porta 8501 já em uso"
```bash
# Matar processo na porta
lsof -ti:8501 | xargs kill -9

# Ou usar outra porta
streamlit run app.py --server.port 8502
```

### "Dados não carregam"
Verifique se os arquivos existem:
```bash
ls -lh *.parquet *.csv
```

---

## 🔄 Atualizar Dados

### Novos Dados IQVIA
1. Coloque novo arquivo `historico_iqvia_YYYYMM.parquet` na pasta
2. Reinicie o app
3. Os 3 meses mais recentes serão carregados automaticamente

### Novos Dados de Preço
1. Substitua `Preço.csv`
2. Reinicie o app ou:
   ```python
   # No Streamlit, pressione 'R' ou 'Rerun'
   ```

### Limpar Cache
```python
# Na sidebar do Streamlit
# Menu > Clear cache
```

Ou progmaticamente:
```python
st.cache_resource.clear()
```

---

## 📱 Atalhos de Teclado

No Streamlit:
- **R**: Rerun app
- **C**: Clear cache
- **Q**: Quit (quando rodando local)
- **?**: Help

---

## 🚀 Performance

### Métricas Esperadas

| Operação | Tempo |
|----------|-------|
| Primeira carga | 10-15s |
| Reload (cache) | <1s |
| Troca de página | Instantâneo |
| Aplicar filtros | <0.5s |
| Gerar gráfico | <0.2s |

### Se estiver mais lento
1. Reduza `sample_months`
2. Feche abas do navegador
3. Verifique uso de memória
4. Considere servidor mais potente

---

## 📞 Suporte

### Logs do Streamlit
```bash
# Ver logs em tempo real
tail -f ~/.streamlit/logs/*.log
```

### Debug Mode
```bash
streamlit run app.py --logger.level=debug
```

### Testar Processador de Dados
```bash
python3 data_processor_optimized.py
```

Deve mostrar:
```
🚀 CARREGAMENTO RÁPIDO INICIADO
Carregando dados de preços...
✓ Preços carregados: 4,762,059 registros
Carregando IQVIA (últimos 3 meses)...
✓ IQVIA carregado: ~166,000,000 registros
Pré-computando agregações...
✓ Agregações pré-computadas
✅ DADOS PRONTOS PARA USO!
```

---

## 🎓 Recursos Adicionais

- **README.md**: Documentação completa
- **PERFORMANCE_OPTIMIZATIONS.md**: Detalhes técnicos de otimização
- **DATA_QUALITY_REPORT.md**: Análise de qualidade dos dados
- **DASHBOARD_BLUEPRINT.md**: Especificações detalhadas

---

**Pronto para começar!** 🚀

Execute `streamlit run app.py` e explore os dashboards!
