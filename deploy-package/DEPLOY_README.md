# 📦 Dashboard RD - Pacote de Deploy

## ⚠️ Importante sobre Netlify

**Netlify NÃO é recomendado para este dashboard** porque:
- ❌ Arquivos de dados são muito grandes (>50MB limite Netlify)
- ❌ Netlify é otimizado para sites estáticos, não apps Python
- ❌ Streamlit requer servidor Python rodando

## 🚀 Opções de Deploy Recomendadas

### 1. Streamlit Cloud ⭐ MELHOR OPÇÃO

**Por quê?**
- ✅ Feito especificamente para Streamlit
- ✅ Deploy grátis
- ✅ Suporta arquivos grandes com Git LFS
- ✅ SSL automático

**Como fazer:**

1. **Instalar Git LFS** (para arquivos grandes)
```bash
brew install git-lfs  # Mac
sudo apt install git-lfs  # Linux
git lfs install
```

2. **Configurar Git LFS**
```bash
git lfs track "*.parquet"
git lfs track "*.csv"
git add .gitattributes
```

3. **Criar repositório GitHub**
```bash
git init
git add .
git commit -m "Dashboard RD inicial"
git branch -M main
git remote add origin https://github.com/seu-usuario/dashboard-rd.git
git push -u origin main
```

4. **Deploy no Streamlit Cloud**
- Acesse: https://share.streamlit.io
- Login com GitHub
- "New app"
- Selecione seu repositório
- Main file: `app.py`
- Deploy!

**URL final**: `https://dashboard-rd.streamlit.app`

---

### 2. Heroku

**Bom para**: Apps Python com controle

```bash
# Instalar Heroku CLI
brew install heroku/brew/heroku

# Login e criar app
heroku login
heroku create dashboard-rd

# Deploy
git init
git add .
git commit -m "Deploy inicial"
heroku git:remote -a dashboard-rd
git push heroku main
```

**Custo**: ~$7/mês (Hobby Dyno)

---

### 3. VPS (DigitalOcean, AWS, etc)

**Melhor para**: Controle total

```bash
# No servidor
ssh user@seu-servidor

# Instalar Python e dependências
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Rodar dashboard
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

**Configurar como serviço** para rodar sempre:
Ver instruções em `DEPLOYMENT_OPTIONS.md`

---

## 📁 Conteúdo deste Pacote

### Arquivos de Código
- `app.py` - Dashboard principal
- `data_processor_optimized.py` - Processamento de dados otimizado
- `requirements.txt` - Dependências Python
- `runtime.txt` - Versão Python
- `.streamlit/config.toml` - Configurações Streamlit

### Arquivos de Deploy
- `Procfile` - Config Heroku
- `setup.sh` - Script de setup
- `netlify.toml` - Config Netlify (não recomendado)

### Documentação
- `README.md` - Documentação completa
- `QUICK_START.md` - Início rápido
- `DEPLOYMENT_OPTIONS.md` - Todas as opções de deploy
- `PERFORMANCE_OPTIMIZATIONS.md` - Otimizações de performance

### Dados (IMPORTANTE)
⚠️ **Este pacote contém apenas dados de amostra**:
- `historico_iqvia_202508.parquet` (mais recente)
- `Preço.csv` (completo)

**Para dados completos**:
Você precisa copiar todos os 8 arquivos IQVIA parquet da pasta original.

---

## 🎯 Quick Start

### Testar Localmente

```bash
# Instalar dependências
pip3 install -r requirements.txt

# Rodar dashboard
streamlit run app.py
```

Acesse: http://localhost:8501

---

## ⚡ Performance

**Carregamento**: 10-15 segundos
**Memória**: ~1.5GB RAM
**Dados carregados**:
- Últimos 3 meses de IQVIA (ajustável)
- Todos os dados de preços (10 meses)

---

## 🔧 Configurações

### Ajustar meses de dados IQVIA

Edite `app.py` linha 75:
```python
processor.quick_load(sample_months=3)  # Altere para 6 ou 8
```

### Variáveis de Ambiente

Não são necessárias por padrão. Para produção:
- `STREAMLIT_SERVER_PORT` - Porta (default: 8501)
- `STREAMLIT_SERVER_ADDRESS` - IP (default: localhost)

---

## 📞 Suporte

**Problemas comuns**: Ver `QUICK_START.md`
**Opções de deploy**: Ver `DEPLOYMENT_OPTIONS.md`
**Performance**: Ver `PERFORMANCE_OPTIMIZATIONS.md`

---

## 🎯 Recomendação Final

1. **Desenvolvimento/Teste**: Rodar localmente
2. **Deploy público**: Streamlit Cloud
3. **Deploy empresarial**: VPS ou Cloud Run
4. **Deploy interno**: Servidor local

**Não use Netlify** para este projeto.

---

## ✅ Checklist de Deploy

- [ ] Escolher plataforma (Streamlit Cloud recomendado)
- [ ] Instalar Git LFS (se usar Streamlit Cloud)
- [ ] Copiar todos arquivos de dados necessários
- [ ] Criar repositório Git
- [ ] Fazer push para GitHub
- [ ] Deploy na plataforma escolhida
- [ ] Testar dashboard em produção
- [ ] Configurar domínio customizado (opcional)
- [ ] Adicionar autenticação (opcional)

---

**Pronto para deploy!** 🚀

Escolha uma opção acima e siga as instruções.
