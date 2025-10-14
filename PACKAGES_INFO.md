# 📦 Pacotes de Deploy - Dashboard RD

## Pacotes Criados

### 1. dashboard-rd-code-only.zip (28KB) ⭐ RECOMENDADO

**Conteúdo**:
- ✅ Código completo da aplicação
- ✅ Arquivos de configuração
- ✅ Documentação completa
- ❌ SEM arquivos de dados

**Use quando**:
- Deploy com Git/GitHub
- Deploy com dados em cloud storage
- Transferência rápida de código
- Controle de versão

**Tamanho**: 28KB (muito leve!)

---

### 2. dashboard-rd-deploy.zip (503MB)

**Conteúdo**:
- ✅ Código completo da aplicação
- ✅ Arquivos de configuração
- ✅ Documentação completa
- ✅ 1 mês de dados IQVIA (Aug 2025)
- ✅ Dados completos de preços (10 meses)

**Use quando**:
- Deploy rápido e auto-contido
- Servidor com espaço disponível
- Teste inicial

**Tamanho**: 503MB

---

## 📊 Comparação

| Aspecto | Code-Only | Deploy Completo |
|---------|-----------|-----------------|
| Tamanho | 28KB | 503MB |
| Dados incluídos | Nenhum | 1 mês IQVIA + Preços |
| Upload rápido | ✅ Sim | ❌ Lento |
| Git-friendly | ✅ Sim | ⚠️ Precisa Git LFS |
| Pronto para rodar | ❌ Precisa dados | ✅ Sim |
| Recomendado para | Git/GitHub | Teste rápido |

---

## 🚀 Como Usar Cada Pacote

### Usando dashboard-rd-code-only.zip

1. **Extrair**:
```bash
unzip dashboard-rd-code-only.zip
cd code-only-package
```

2. **Adicionar dados** (ver `DATA_INSTRUCTIONS.md`):
```bash
# Copiar da pasta original:
cp ../historico_iqvia_202508.parquet .
cp ../Preço.csv .
```

3. **Instalar e rodar**:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

### Usando dashboard-rd-deploy.zip

1. **Extrair**:
```bash
unzip dashboard-rd-deploy.zip
cd deploy-package
```

2. **Instalar e rodar** (dados já incluídos):
```bash
pip install -r requirements.txt
streamlit run app.py
```

**Nota**: Inclui apenas 1 mês de IQVIA. Para mais histórico, copie outros arquivos parquet.

---

## 🎯 Escolhendo o Pacote Certo

### Use Code-Only quando:
- ✅ Vai fazer deploy via Git/GitHub
- ✅ Quer usar Streamlit Cloud
- ✅ Vai usar cloud storage (S3, GCS)
- ✅ Precisa controlar versão do código
- ✅ Quer upload rápido

### Use Deploy Completo quando:
- ✅ Quer testar rapidamente
- ✅ Deploy em servidor local
- ✅ Não precisa de controle de versão
- ✅ Tem conexão rápida

---

## 📁 Conteúdo Detalhado

### Arquivos de Código (em ambos)
```
├── app.py                              # Dashboard principal
├── data_processor_optimized.py         # Processador de dados
├── requirements.txt                    # Dependências
├── runtime.txt                         # Python 3.11
├── .streamlit/config.toml             # Config Streamlit
├── Procfile                            # Config Heroku
├── setup.sh                            # Setup script
├── netlify.toml                        # Config Netlify
└── .gitignore                          # Git ignore
```

### Documentação (em ambos)
```
├── README.md                           # Documentação completa
├── QUICK_START.md                      # Guia rápido
├── DEPLOYMENT_OPTIONS.md               # Opções de deploy
├── PERFORMANCE_OPTIMIZATIONS.md        # Otimizações
└── DEPLOY_README.md (deploy) ou
    DATA_INSTRUCTIONS.md (code-only)    # Instruções específicas
```

### Dados (apenas em deploy completo)
```
├── historico_iqvia_202508.parquet     # IQVIA Aug 2025 (~430MB)
└── Preço.csv                           # Preços completos (~300MB)
```

---

## 🌐 Deploy para Diferentes Plataformas

### Streamlit Cloud (RECOMENDADO)

**Use**: `dashboard-rd-code-only.zip`

```bash
# 1. Extrair código
unzip dashboard-rd-code-only.zip

# 2. Adicionar TODOS os dados desejados
cp ../historico_iqvia_*.parquet code-only-package/
cp ../Preço.csv code-only-package/

# 3. Git + Git LFS
cd code-only-package
git init
git lfs install
git lfs track "*.parquet"
git lfs track "*.csv"
git add .
git commit -m "Initial commit"
git push

# 4. Deploy no Streamlit Cloud
# https://share.streamlit.io
```

---

### Heroku

**Use**: `dashboard-rd-deploy.zip` (teste) ou code-only (produção)

```bash
unzip dashboard-rd-deploy.zip
cd deploy-package
git init
git add .
git commit -m "Deploy"
heroku create dashboard-rd
git push heroku main
```

---

### VPS/Servidor

**Use**: `dashboard-rd-deploy.zip`

```bash
# Upload via SCP
scp dashboard-rd-deploy.zip user@servidor:/opt/

# No servidor
ssh user@servidor
cd /opt
unzip dashboard-rd-deploy.zip
cd deploy-package
pip3 install -r requirements.txt
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

### Docker

**Use**: `dashboard-rd-code-only.zip`

```bash
unzip dashboard-rd-code-only.zip
cd code-only-package

# Criar Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
EOF

# Build e run
docker build -t dashboard-rd .
docker run -p 8501:8501 dashboard-rd
```

---

## ⚠️ Importante sobre Netlify

**NÃO USE NETLIFY** para este dashboard!

Por quê?
- ❌ Arquivos >50MB (Netlify não suporta)
- ❌ Netlify é para sites estáticos, não Python apps
- ❌ Streamlit precisa de servidor rodando

**Alternativa**: Use Streamlit Cloud (grátis e feito para isso)

---

## 💾 Adicionar Mais Dados

Ambos os pacotes podem receber mais arquivos de dados:

```bash
# Adicionar mais meses de IQVIA
cp historico_iqvia_202501.parquet seu-pacote/
cp historico_iqvia_202502.parquet seu-pacote/
# ... (até 202508)

# O dashboard carregará automaticamente
# os últimos N meses disponíveis
```

Ajuste quantos meses carregar em `app.py`:
```python
processor.quick_load(sample_months=3)  # Altere aqui
```

---

## 📊 Requisitos do Sistema

### Mínimo
- Python 3.11+
- 2GB RAM
- 1GB disco livre

### Recomendado
- Python 3.11+
- 4GB RAM
- 5GB disco livre (para todos os dados)
- CPU: 2+ cores

---

## 🔐 Segurança

### Dados Sensíveis
Se seus dados são sensíveis:
1. **Não** faça upload para repositórios públicos
2. Use repositório privado no GitHub
3. Ou use servidor próprio/VPS
4. Configure autenticação no Streamlit

### Adicionar Autenticação
Ver: https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso

---

## 📞 Suporte

**Problemas com pacotes?**
- Verifique integridade do ZIP
- Re-extraia em pasta limpa
- Verifique permissões de arquivo

**Problemas com deploy?**
- Consulte `DEPLOYMENT_OPTIONS.md`
- Logs do Streamlit: `~/.streamlit/logs/`
- GitHub Issues do projeto

---

## ✅ Checklist de Deploy

- [ ] Escolher pacote (code-only recomendado)
- [ ] Extrair pacote
- [ ] Adicionar dados (se code-only)
- [ ] Testar localmente: `streamlit run app.py`
- [ ] Escolher plataforma (Streamlit Cloud recomendado)
- [ ] Seguir guia de deploy da plataforma
- [ ] Verificar dashboard em produção
- [ ] Configurar domínio customizado (opcional)
- [ ] Adicionar autenticação (se necessário)

---

## 📈 Próximos Passos

1. **Escolha seu pacote**:
   - Code-only: Para Git/GitHub/Cloud
   - Deploy completo: Para teste rápido

2. **Leia a documentação**:
   - `QUICK_START.md` - Começar rapidamente
   - `DEPLOYMENT_OPTIONS.md` - Escolher plataforma
   - `README.md` - Documentação completa

3. **Faça deploy**:
   - Streamlit Cloud (recomendado)
   - Heroku, VPS, ou Docker

4. **Configure produção**:
   - Domínio customizado
   - Autenticação
   - Monitoramento

---

**Arquivos prontos para deploy!** 🚀

Escolha um pacote e siga as instruções acima.
