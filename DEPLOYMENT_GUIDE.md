# 🚀 Guia de Deploy - Dashboard RD

## Opção Recomendada: Streamlit Cloud (100% GRÁTIS)

### Por que Streamlit Cloud?
- ✅ **Feito especificamente para apps Streamlit**
- ✅ **Totalmente gratuito** (plano Community)
- ✅ **Deploy automático** via GitHub
- ✅ **Suporta arquivos grandes** (até 1GB por repo com Git LFS)
- ✅ **HTTPS automático**
- ✅ **Redeployes automáticos** quando você faz push no GitHub

⚠️ **Netlify NÃO funciona** porque é apenas para sites estáticos (HTML/CSS/JS), não para apps Python que precisam rodar um servidor.

---

## 📋 Pré-requisitos

1. **Conta GitHub** (gratuita): https://github.com
2. **Conta Streamlit Cloud** (gratuita): https://streamlit.io/cloud
3. **Git instalado** no seu computador

---

## 🔧 Passo 1: Preparar o Projeto

### 1.1 Inicializar Git (se ainda não foi feito)

```bash
cd /Users/anon/Documents/RD-new
git init
```

### 1.2 Criar .gitignore

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Streamlit
.streamlit/secrets.toml

# OS
.DS_Store
Thumbs.db

# Dados sensíveis (se houver)
*.env
.env

# Cache
*.cache
EOF
```

### 1.3 Configurar Git LFS para arquivos grandes

⚠️ **IMPORTANTE**: Seus arquivos IQVIA são grandes (~400MB cada). Git LFS é necessário.

```bash
# Instalar Git LFS (se ainda não tiver)
# macOS:
brew install git-lfs

# Inicializar Git LFS
git lfs install

# Rastrear arquivos parquet grandes
git lfs track "*.parquet"
git lfs track "Data/IQVIA/*.parquet"

# Adicionar .gitattributes
git add .gitattributes
```

---

## 📤 Passo 2: Subir para GitHub

### 2.1 Criar repositório no GitHub

1. Acesse https://github.com/new
2. Nome do repositório: `rd-dashboard` (ou outro nome)
3. Visibilidade: **Private** (se dados são confidenciais) ou Public
4. NÃO inicialize com README, .gitignore ou license
5. Clique "Create repository"

### 2.2 Conectar local com GitHub

```bash
# Adicionar todos os arquivos
git add .

# Criar primeiro commit
git commit -m "Initial commit - Dashboard RD com dados completos Jan-Set/2025"

# Conectar com repositório remoto (SUBSTITUA seu-usuario pelo seu username)
git remote add origin https://github.com/seu-usuario/rd-dashboard.git

# Subir código
git branch -M main
git push -u origin main
```

⚠️ **Atenção**: O push pode demorar vários minutos devido aos arquivos grandes (~3GB total).

---

## ☁️ Passo 3: Deploy no Streamlit Cloud

### 3.1 Criar conta no Streamlit Cloud

1. Acesse https://share.streamlit.io/
2. Clique em "Sign up" ou "Continue with GitHub"
3. Autorize Streamlit a acessar seu GitHub

### 3.2 Criar novo app

1. No dashboard do Streamlit Cloud, clique **"New app"**
2. Preencha os campos:
   - **Repository**: `seu-usuario/rd-dashboard`
   - **Branch**: `main`
   - **Main file path**: `app_improved.py`
3. Clique em **"Advanced settings"** (opcional):
   - **Python version**: 3.10 ou 3.11
4. Clique **"Deploy!"**

### 3.3 Aguardar deploy

- ⏱️ Primeira build: 5-10 minutos (instalando dependências)
- 📊 Carregamento de dados: 15-20 segundos (primeira vez)
- ✅ Cache subsequente: Instantâneo

---

## 🔗 Passo 4: Acessar seu Dashboard

Após o deploy, você receberá uma URL do tipo:

```
https://seu-usuario-rd-dashboard-main-app-improved-abc123.streamlit.app
```

🎉 **Pronto!** Seu dashboard está no ar e acessível pela internet.

---

## 🔄 Atualizações Futuras

### Para atualizar o dashboard depois:

```bash
# Fazer alterações nos arquivos
# Commitar alterações
git add .
git commit -m "Descrição da alteração"

# Fazer push
git push

# 🚀 Streamlit Cloud redesploy automático em ~2 minutos!
```

---

## ⚙️ Configurações Avançadas

### Secrets (se precisar de senhas/tokens)

1. No Streamlit Cloud, vá em **"Settings" → "Secrets"**
2. Adicione no formato TOML:

```toml
# .streamlit/secrets.toml (não commite isso!)
[database]
username = "seu_usuario"
password = "sua_senha"
```

3. No código, acesse com:
```python
import streamlit as st
username = st.secrets["database"]["username"]
```

### Recursos do App

- **Memória**: 1GB (plano gratuito)
- **CPU**: Compartilhada
- **Limites**:
  - Repositório: 1GB (com Git LFS)
  - Arquivos individuais: 100MB sem LFS, 2GB com LFS

---

## 🐛 Troubleshooting

### Erro: "File too large"
**Solução**: Certifique-se de que Git LFS está configurado corretamente
```bash
git lfs track "*.parquet"
git add .gitattributes
git add --renormalize .
git commit -m "Fix LFS tracking"
git push --force
```

### Erro: "ModuleNotFoundError"
**Solução**: Verifique se todas as dependências estão em `requirements.txt`

### App fica muito lento
**Solução**:
1. Verifique se `@st.cache_resource` está sendo usado
2. Considere reduzir dados ou usar sampling
3. Upgrade para Streamlit Cloud Team (pago) para mais recursos

### Deploy falha
**Solução**: Verifique os logs no Streamlit Cloud dashboard
- Clique no app → "Manage app" → "Logs"

---

## 💰 Opções Alternativas (se Streamlit Cloud não funcionar)

### 1. Heroku (PAGO - ~$7-25/mês)
- Suporta apps Python
- Mais recursos que Streamlit Cloud
- Setup mais complexo

### 2. Render (FREE tier disponível)
- Similar ao Heroku
- 750h/mês grátis
- Deploy via Docker

### 3. Railway (FREE $5 crédito/mês)
- Deploy automático via GitHub
- Simples como Streamlit Cloud

### 4. Servidor próprio (VPS)
- DigitalOcean, AWS, Google Cloud
- Mais controle, mais trabalho
- $5-50/mês

---

## 📊 Status dos Arquivos

### Arquivo de dados esperados (já existentes):
```
Data/IQVIA/
├── RD_202501.parquet (~400MB)
├── RD_202502.parquet (~400MB)
├── RD_202503.parquet (~400MB)
├── RD_202504.parquet (~400MB)
├── RD_202505.parquet (~400MB)
├── RD_202506.parquet (~400MB)
├── RD_202507.parquet (~400MB)
└── RD_202508.parquet (~400MB)

Data/
└── Preço.csv (~50MB)
```

**Total**: ~3.2GB de dados brutos

---

## ✅ Checklist de Deploy

- [ ] Git instalado e configurado
- [ ] Git LFS instalado e configurado
- [ ] .gitignore criado
- [ ] Repositório GitHub criado
- [ ] Código commitado e pushed
- [ ] Conta Streamlit Cloud criada
- [ ] App deployado no Streamlit Cloud
- [ ] URL do dashboard funcionando
- [ ] Dados carregando corretamente (15-20s primeira vez)
- [ ] Todos os filtros funcionando
- [ ] Todas as 6 abas funcionando

---

## 🎯 Resultado Final

✅ **Dashboard online e acessível 24/7**
✅ **URL compartilhável com equipe**
✅ **Atualizações automáticas via git push**
✅ **100% gratuito com Streamlit Cloud**
✅ **HTTPS seguro automático**

---

**Criado em**: 2025-10-14
**Versão**: 1.0
**Plataforma**: Streamlit Cloud (Recomendado)
