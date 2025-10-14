# Opções de Deploy - Dashboard RD

## ⚠️ Importante: Tamanho dos Dados

**Total de dados**: ~4GB
- IQVIA: 8 arquivos × ~430MB = ~3.5GB
- Preço.csv: ~300MB
- Excel: ~300KB

**Problema**: Netlify tem limite de 50MB por arquivo no plano gratuito.

---

## 🚀 Opções de Deploy Recomendadas

### Opção 1: Streamlit Cloud ⭐ RECOMENDADO

**Melhor para**: Dashboards Streamlit com dados grandes

#### Vantagens
✅ Gratuito para projetos públicos
✅ Suporta arquivos grandes via Git LFS
✅ Deploy automático do GitHub
✅ Otimizado para Streamlit
✅ SSL grátis

#### Como Fazer

1. **Instalar Git LFS** (para arquivos grandes)
```bash
# Mac
brew install git-lfs

# Linux
sudo apt-get install git-lfs

# Windows
# Download de git-lfs.github.com

# Inicializar
git lfs install
```

2. **Configurar Git LFS para arquivos grandes**
```bash
git lfs track "*.parquet"
git lfs track "*.csv"
git add .gitattributes
```

3. **Criar repositório e fazer push**
```bash
git init
git add .
git commit -m "Dashboard RD - Deploy inicial"
git remote add origin https://github.com/seu-usuario/dashboard-rd.git
git push -u origin main
```

4. **Deploy no Streamlit Cloud**
   - Acesse: https://share.streamlit.io
   - Login com GitHub
   - New app → Selecione seu repositório
   - Main file: `app.py`
   - Deploy!

**URL final**: `https://seu-usuario-dashboard-rd.streamlit.app`

---

### Opção 2: Heroku

**Melhor para**: Aplicações Python com controle total

#### Vantagens
✅ Suporta arquivos grandes (slug até 500MB comprimido)
✅ Python nativo
✅ Fácil escalar

#### Limitações
⚠️ Dados podem exceder limite de slug
⚠️ Requer plano pago para produção

#### Como Fazer

1. **Instalar Heroku CLI**
```bash
# Mac
brew tap heroku/brew && brew install heroku

# Ou download de heroku.com/downloads
```

2. **Login e criar app**
```bash
heroku login
heroku create dashboard-rd
```

3. **Deploy**
```bash
git push heroku main
```

**Solução para dados grandes**: Usar Amazon S3 ou Google Cloud Storage

---

### Opção 3: Servidor Próprio (VPS)

**Melhor para**: Controle total, dados sensíveis

#### Opções de Servidor
- **DigitalOcean**: $6/mês (1GB RAM)
- **AWS Lightsail**: $5/mês
- **Google Cloud Compute**: $10/mês
- **Azure VM**: $13/mês

#### Setup Básico

```bash
# SSH no servidor
ssh user@seu-servidor.com

# Instalar dependências
sudo apt update
sudo apt install python3-pip nginx

# Clonar código
git clone <seu-repo>
cd dashboard-rd

# Instalar dependências
pip3 install -r requirements.txt

# Rodar com Supervisor/systemd
streamlit run app.py --server.port 8501
```

**Configurar Nginx** como reverse proxy para HTTPS

---

### Opção 4: Docker + Cloud Storage

**Melhor para**: Produção empresarial

#### Arquitetura
```
┌─────────────────────────────────────┐
│  Docker Container                   │
│  - Streamlit App                    │
│  - Código Python                    │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Cloud Storage                      │
│  - Amazon S3 / Google Cloud Storage │
│  - Dados Parquet/CSV                │
└─────────────────────────────────────┘
```

#### Criar Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Deploy em:
- **Google Cloud Run** (serverless, auto-escala)
- **AWS ECS** (container service)
- **Azure Container Instances**

---

## 📦 Opção 5: Deploy Local/Interno

**Melhor para**: Dashboard interno da empresa

### Setup Rápido

```bash
# No servidor interno
cd /path/to/dashboard
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

**Acessível na rede interna**: `http://ip-servidor:8501`

### Rodar como Serviço (Linux)

Criar `/etc/systemd/system/dashboard-rd.service`:

```ini
[Unit]
Description=Dashboard RD Streamlit
After=network.target

[Service]
Type=simple
User=dashboarduser
WorkingDirectory=/opt/dashboard-rd
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativar:
```bash
sudo systemctl enable dashboard-rd
sudo systemctl start dashboard-rd
```

---

## 🎯 Comparação de Opções

| Opção | Custo | Facilidade | Dados Grandes | Produção | Recomendação |
|-------|-------|------------|---------------|----------|--------------|
| Streamlit Cloud | Grátis | ⭐⭐⭐⭐⭐ | ✅ (Git LFS) | ⭐⭐⭐ | **Melhor para começar** |
| Heroku | $7-25/mês | ⭐⭐⭐⭐ | ⚠️ Limitado | ⭐⭐⭐⭐ | Bom para produção |
| VPS | $5-20/mês | ⭐⭐⭐ | ✅ Sem limites | ⭐⭐⭐⭐⭐ | Controle total |
| Docker + Cloud | $10-50/mês | ⭐⭐ | ✅ Storage separado | ⭐⭐⭐⭐⭐ | Escala empresarial |
| Servidor Interno | Grátis | ⭐⭐⭐⭐ | ✅ Sem limites | ⭐⭐⭐ | Dashboard interno |

---

## 💡 Solução Híbrida: Cloud Storage

Para qualquer opção, você pode separar código e dados:

### 1. Hospedar Dados em Cloud Storage

**Amazon S3**:
```python
import boto3
s3 = boto3.client('s3')
s3.download_file('meu-bucket', 'historico_iqvia_202508.parquet', 'local.parquet')
```

**Google Cloud Storage**:
```python
from google.cloud import storage
client = storage.Client()
bucket = client.bucket('dashboard-rd-data')
blob = bucket.blob('historico_iqvia_202508.parquet')
blob.download_to_filename('local.parquet')
```

### 2. Modificar data_processor_optimized.py

```python
def load_from_cloud(self, cloud_provider='s3'):
    if cloud_provider == 's3':
        # Download de S3
        import boto3
        s3 = boto3.client('s3')
        # ...
    elif cloud_provider == 'gcs':
        # Download de Google Cloud Storage
        from google.cloud import storage
        # ...
```

### Vantagens
✅ Código leve (~1MB)
✅ Deploy rápido
✅ Dados atualizados centralmente
✅ Custo baixo (S3: ~$0.02/GB/mês)

---

## 📝 Netlify NÃO É RECOMENDADO

**Por quê?**
- ❌ Limite de 50MB por arquivo
- ❌ Não suporta Streamlit nativamente
- ❌ Otimizado para sites estáticos (React, Vue)
- ❌ Não roda Python server-side

**Alternativa**: Use Netlify para frontend + API backend separada

---

## 🎯 Recomendação Final

### Para começar AGORA:
**Streamlit Cloud** + Git LFS

### Para produção empresarial:
**VPS/Cloud Run** + Cloud Storage (S3/GCS)

### Para uso interno:
**Servidor interno** com systemd service

---

## 📞 Próximos Passos

1. Escolher opção de deploy
2. Seguir guia específico acima
3. Testar dashboard em produção
4. Configurar atualizações automáticas de dados
5. Adicionar autenticação se necessário

---

**Precisa de ajuda?** Consulte os guias específicos de cada plataforma.
