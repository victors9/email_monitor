# 🔧 Guia de Setup Completo

Este guia vai te ajudar a configurar o Email Monitor Agent do zero.

## 📋 Pré-requisitos

### 1. WSL2 (Windows Subsystem for Linux)

Se você ainda não tem o WSL2 configurado:

```bash
# No PowerShell como Admin
wsl --install -d Ubuntu
```

### 2. Python 3.8+

Verifique a versão:

```bash
python3 --version
```

Se não tiver, instale:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 3. Ollama

#### Instalação no WSL

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Iniciar o Ollama

```bash
ollama serve
```

Deixe rodando em um terminal separado.

#### Baixar o modelo Llama 3.2 3B

Em outro terminal:

```bash
ollama pull llama3.2:3b
```

Isso vai baixar ~2GB. Aguarde a conclusão.

#### Verificar instalação

```bash
ollama list
```

Deve mostrar:

```
NAME              ID              SIZE      MODIFIED
llama3.2:3b       abc123...       2.0 GB    X minutes ago
```

#### Testar o modelo

```bash
ollama run llama3.2:3b "Oi, me explique em uma frase o que você faz"
```

Se responder, está funcionando!

---

## 🔐 Configurar Azure AD (Microsoft Graph)

Para o agente acessar seus emails, você precisa registrar um app no Azure.

### Opção 1: Usar App Registration Existente

Se você já tem `TENANT_ID` e `CLIENT_ID`, pule para "Instalar o Projeto".

### Opção 2: Criar Novo App Registration

1. **Acesse o Azure Portal**
   - https://portal.azure.com
   - Login com sua conta Microsoft

2. **Registre o App**
   - Busque "Azure Active Directory"
   - Vá em "App registrations" > "New registration"
   - Nome: `EmailMonitorAgent`
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI: Deixe em branco
   - Clique "Register"

3. **Anote as Credenciais**
   - Na página do app, copie:
     - `Application (client) ID` → seu CLIENT_ID
     - `Directory (tenant) ID` → seu TENANT_ID

4. **Configure Permissões**
   - Vá em "API permissions"
   - Clique "Add a permission"
   - Selecione "Microsoft Graph" > "Delegated permissions"
   - Adicione:
     - `Mail.Read`
     - `Mail.ReadWrite`
     - `Calendars.Read`
   - Clique "Add permissions"
   - Clique "Grant admin consent" (se tiver permissão)

5. **Configure Autenticação**
   - Vá em "Authentication"
   - Em "Advanced settings" > "Allow public client flows"
   - Marque "Yes"
   - Clique "Save"

---

## 📦 Instalar o Projeto

### 1. Navegue até a pasta do projeto

```bash
cd /caminho/para/email_agent_refactor
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o .env

Copie o template:

```bash
cp .env.example .env
```

Edite com suas credenciais:

```bash
nano .env
```

Substitua:

```env
TENANT_ID=cole-seu-tenant-id-aqui
CLIENT_ID=cole-seu-client-id-aqui
```

Salve (Ctrl+O) e saia (Ctrl+X).

### 5. Crie a pasta de logs

```bash
mkdir -p logs
```

---

## 🚀 Primeira Execução

### 1. Certifique-se que Ollama está rodando

Em um terminal:

```bash
ollama serve
```

### 2. Execute o agente

Em outro terminal:

```bash
cd /caminho/para/email_agent_refactor
source venv/bin/activate  # Se estiver usando venv
python main.py
```

### 3. Autentique

Na primeira execução, você verá algo assim:

```
To sign in, use a web browser to open the page https://microsoft.com/devicelogin 
and enter the code ABC12DEF to authenticate.
```

1. Abra o navegador
2. Acesse https://microsoft.com/devicelogin
3. Digite o código mostrado
4. Faça login com sua conta Microsoft
5. Autorize as permissões

### 4. Aguarde o agente iniciar

Você verá logs como:

```
2026-02-03 10:30:00 | INFO     | EmailMonitorAgent | 🚀 Agente iniciado e monitorando...
2026-02-03 10:30:00 | INFO     | EmailMonitorAgent | ⏱️  Verificando a cada 30 segundos
```

Pronto! O agente está rodando.

---

## ✅ Verificar se Está Funcionando

### Teste 1: Envie um email para você mesmo

1. Envie um email de teste para sua conta
2. Aguarde até 30 segundos
3. Verifique os logs do agente

Você deve ver:

```
📧 NOVO EMAIL
De: seu-email@exemplo.com
Assunto: Teste
Urgência: 🟡 MÉDIA
```

### Teste 2: Verifique o arquivo de log

```bash
tail -f logs/email_agent.log
```

Você deve ver todas as operações sendo logadas.

---

## 🛑 Parar o Agente

Pressione `Ctrl+C` no terminal onde o agente está rodando.

Você verá:

```
⚠️  Interrupção detectada. Finalizando agente...
🛑 Agente finalizado
```

---

## 🔄 Executar Novamente

Nas próximas execuções, o token estará em cache:

```bash
cd /caminho/para/email_agent_refactor
source venv/bin/activate
python main.py
```

Não precisará autenticar novamente (a menos que o token expire).

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'ollama'"

```bash
pip install ollama
```

### Erro: "Connection refused" ao chamar Ollama

Certifique-se que o Ollama está rodando:

```bash
ollama serve
```

### Erro: "Token inválido"

Delete o cache:

```bash
rm .token_cache
```

Execute novamente e autentique.

### Modelo muito lento

Use um modelo menor:

```bash
ollama pull llama3.2:1b
```

No `.env`:

```env
OLLAMA_MODEL=llama3.2:1b
```

### Sem emails sendo detectados

Verifique:

1. Você tem emails não lidos?
2. As permissões do Azure estão corretas?
3. Você autenticou com a conta certa?

---

## 🎯 Próximos Passos

Agora que está funcionando:

1. **Teste com emails reais** - Monitore sua caixa de entrada
2. **Ajuste as configurações** - Mude intervalo, heartbeat, etc
3. **Monitore os logs** - Veja como a IA classifica seus emails
4. **Reporte bugs** - Anote comportamentos inesperados

Pronto para a **Sprint 2**? Fale com o dev!

---

**Algum problema?** Verifique os logs em `logs/email_agent.log` para detalhes.
