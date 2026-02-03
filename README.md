# 🤖 Email Monitor Agent

Agente inteligente de monitoramento de emails usando IA local (Llama 3.2 via Ollama) e Microsoft Graph API.

## 📋 Características

- ✅ Monitoramento automático de emails não lidos
- ✅ Classificação de urgência usando IA (ALTA/MÉDIA/BAIXA)
- ✅ Verificação de eventos do calendário
- ✅ Logging estruturado com rotação de arquivos
- ✅ Cache de token (evita re-autenticação constante)
- ✅ Retry automático em caso de falhas de API
- ✅ Heartbeat para monitoramento de saúde do agente

## 🛠️ Requisitos

### Software
- Python 3.8+
- Ollama instalado e rodando
- Modelo Llama 3.2 3B baixado no Ollama
- Conta Microsoft (Outlook/Office 365)

### Hardware
- CPU: Intel i5 8ª geração ou superior
- RAM: 8GB (mínimo)
- Espaço em disco: ~2GB para o modelo

## 📦 Instalação

### 1. Clone/Copie os arquivos do projeto

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o Ollama

Certifique-se que o Ollama está rodando:

```bash
ollama serve
```

Em outro terminal, verifique se o modelo Llama 3.2 está instalado:

```bash
ollama list
```

Se não estiver, baixe:

```bash
ollama pull llama3.2:3b
```

### 4. Configure o arquivo .env

Copie o template:

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais:

```env
# Microsoft Azure AD Configuration
TENANT_ID=seu-tenant-id-aqui
CLIENT_ID=seu-client-id-aqui

# Email Monitor Settings
CHECK_INTERVAL_SECONDS=30
HEARTBEAT_MINUTES=20
MAX_EMAILS_PER_CHECK=5

# Ollama Configuration
OLLAMA_MODEL=llama3.2:3b
OLLAMA_HOST=http://localhost:11434
OLLAMA_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/email_agent.log
```

## 🚀 Uso

### Executar o agente

```bash
python main.py
```

### Primeira execução

Na primeira execução, você precisará autenticar via Device Flow:

1. O agente mostrará um código e uma URL
2. Acesse a URL no navegador
3. Digite o código
4. Faça login com sua conta Microsoft
5. Autorize as permissões solicitadas

O token ficará em cache, então não precisará autenticar novamente nas próximas execuções (a menos que expire).

### Parar o agente

Pressione `Ctrl+C` para parar o agente gracefully.

## 📁 Estrutura do Projeto

```
email_agent/
├── app/
│   ├── __init__.py
│   ├── agent.py              # Agente principal
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py       # Configurações
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py     # Integração com Ollama
│   │   ├── auth_service.py   # Autenticação Microsoft
│   │   ├── calendar_service.py
│   │   └── email_service.py
│   └── utils/
│       ├── __init__.py
│       ├── heartbeat.py
│       └── logger.py         # Sistema de logging
├── logs/                     # Logs do agente (gerado automaticamente)
├── .env                      # Configurações (NÃO commitar!)
├── .env.example             # Template de configuração
├── .gitignore
├── main.py                  # Entry point
├── requirements.txt
└── README.md
```

## 🔧 Configurações Avançadas

### Ajustar frequência de verificação

No `.env`, modifique:

```env
CHECK_INTERVAL_SECONDS=60  # Verifica a cada 1 minuto
```

### Mudar nível de log

```env
LOG_LEVEL=DEBUG  # Opções: DEBUG, INFO, WARNING, ERROR
```

### Usar modelo diferente

```env
OLLAMA_MODEL=llama3.2:1b  # Modelo menor, mais rápido
```

## 📊 Logs

Os logs são salvos em:
- **Console**: Saída em tempo real
- **Arquivo**: `logs/email_agent.log`

O arquivo de log tem rotação automática:
- Máximo 10MB por arquivo
- Mantém últimos 5 arquivos

## 🐛 Troubleshooting

### "Erro ao conectar no Ollama"

Verifique se o Ollama está rodando:

```bash
ollama serve
```

### "Token expirado"

Delete o cache de token:

```bash
rm .token_cache
```

Execute novamente e autentique.

### "Modelo muito lento"

O modelo Llama 3.2 3B leva ~10s por email. Para acelerar:

1. Use modelo menor: `ollama pull llama3.2:1b`
2. Reduza `MAX_EMAILS_PER_CHECK` no `.env`
3. Aumente `CHECK_INTERVAL_SECONDS`

### Emails não sendo marcados como lidos

Isso será implementado em sprints futuras. Por enquanto, o agente apenas monitora.

## 🗺️ Roadmap

### ✅ Sprint 1 (Atual)
- [x] Logging estruturado
- [x] Configuração com .env
- [x] Integração com Ollama
- [x] Classificação de urgência
- [x] Tratamento de erros

### 🔜 Sprint 2 (Próxima)
- [ ] Análise de sentimento
- [ ] Extração de action items
- [ ] Geração contextualizada de respostas
- [ ] Marcar emails como lidos automaticamente

### 🔮 Sprint 3 (Futuro)
- [ ] Criar tarefas automaticamente
- [ ] Adicionar eventos ao calendário
- [ ] Notificações via Telegram/Slack
- [ ] Dashboard web

### 🚀 Sprint 4 (Produção)
- [ ] Testes unitários
- [ ] Docker
- [ ] CI/CD
- [ ] Documentação completa

## 📝 Licença

Uso interno - Projeto em desenvolvimento

## 👨‍💻 Autor

Desenvolvido para uso pessoal e apresentação empresarial.

---

**Versão**: 1.0.0 (Sprint 1)  
**Última atualização**: Fevereiro 2026
