# 📁 Instruções para Adicionar Dados

Este pacote contém **apenas o código** do dashboard.

## ⚠️ Dados Necessários

Para rodar o dashboard, você precisa dos seguintes arquivos de dados:

### 1. Arquivos IQVIA (Obrigatório)
Pelo menos **1 arquivo** (recomendado: últimos 3 meses)

```
historico_iqvia_202506.parquet
historico_iqvia_202507.parquet
historico_iqvia_202508.parquet
```

**Onde obter**: Pasta original do projeto
**Tamanho**: ~430MB cada
**Local**: Copiar para mesma pasta que `app.py`

### 2. Arquivo de Preços (Obrigatório)
```
Preço.csv
```

**Onde obter**: Pasta original do projeto
**Tamanho**: ~300MB
**Local**: Copiar para mesma pasta que `app.py`

---

## 📦 Como Adicionar os Dados

### Opção 1: Copiar Manualmente

```bash
# Da pasta original, copie os arquivos:
cp historico_iqvia_202506.parquet code-only-package/
cp historico_iqvia_202507.parquet code-only-package/
cp historico_iqvia_202508.parquet code-only-package/
cp Preço.csv code-only-package/
```

### Opção 2: Usar Cloud Storage

Em vez de incluir dados no pacote, você pode:

1. **Upload para S3/Google Cloud Storage**
2. **Modificar `data_processor_optimized.py`** para baixar de lá
3. **Vantagem**: Deploy leve, dados atualizados centralmente

Ver: `DEPLOYMENT_OPTIONS.md` seção "Cloud Storage"

---

## ✅ Estrutura Final Esperada

```
code-only-package/
├── app.py
├── data_processor_optimized.py
├── requirements.txt
├── historico_iqvia_202506.parquet  ← ADICIONE
├── historico_iqvia_202507.parquet  ← ADICIONE
├── historico_iqvia_202508.parquet  ← ADICIONE
├── Preço.csv                        ← ADICIONE
├── .streamlit/
│   └── config.toml
└── ... (outros arquivos)
```

---

## 🚀 Depois de Adicionar os Dados

1. **Testar localmente**:
```bash
pip install -r requirements.txt
streamlit run app.py
```

2. **Fazer deploy**:
Ver instruções em `DEPLOYMENT_OPTIONS.md`

---

## 💡 Dica: Quantos Meses Carregar?

O dashboard carrega **últimos 3 meses** por padrão.

**Recomendações**:
- **Teste rápido**: 1 mês (~430MB)
- **Uso normal**: 3 meses (~1.3GB)
- **Análise completa**: 8 meses (~3.5GB)

Ajustar em `app.py` linha 75:
```python
processor.quick_load(sample_months=3)
```

---

## ❓ Problemas?

**"Erro ao carregar dados"**
- Verifique se os arquivos estão na mesma pasta que `app.py`
- Verifique nomes dos arquivos (case-sensitive)
- Verifique se arquivos não estão corrompidos

**"Dashboard muito lento"**
- Use menos meses de dados
- Verifique RAM disponível (~2GB recomendado)

---

**Adicione os dados e você estará pronto para rodar!** 🚀
