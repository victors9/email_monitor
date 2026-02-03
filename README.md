# 🤖 Email Monitor Agent v2.1 - Menu Interativo + Chat IA

Agente inteligente de monitoramento de emails com **sistema de menu interativo**, **relatórios avançados** e **chat com IA**.

## 🆕 Novidades da Versão 2.1

### ✨ Chat Interativo com IA (NOVO!)

**💬 Converse com o agente sobre seus emails!**

```
👤 Você: Quantos emails não lidos eu tenho?

🤖 Agente: Você tem 5 emails não lidos. 3 são de hoje e 2 de ontem.
           Quer que eu te diga quais são os mais importantes?

👤 Você: Sim, quais são?

🤖 Agente: Os mais importantes são:
           - "Reunião urgente" de joao@empresa.com
           - "Proposta - prazo hoje" de cliente@exemplo.com
```

**Features do Chat:**
- 🧠 IA com contexto dos últimos 3 dias de emails
- 💭 Memória de conversa (últimas 5 mensagens)
- ⚡ Comandos especiais (`/help`, `/resumo`, `/sugestões`)
- 🎯 Respostas personalizadas baseadas na sua caixa

### ✨ Funcionalidades Novas

1. **📊 Resumo Diário de Emails**
   - Visualiza todos os emails recebidos hoje
   - Indica quais têm anexos (📎)
   - Estatísticas organizadas

2. **⚠️ Emails Sem Resposta**
   - Lista emails dos últimos 7 dias que você ainda não respondeu
   - Indica urgência por tempo (🔴 3+ dias, 🟡 1+ dia, 🟢 recente)
   - Ajuda a não esquecer de responder ninguém

3. **👥 Status de Usuários**
   - Mostra presença de todos os usuários da organização
   - Status: Online, Offline, Em reunião, Ocupado, etc.
   - Útil para saber quem está disponível

4. **🎮 Menu Interativo**
   - Interface amigável em terminal
   - Navegação simples por números
   - Pode voltar ao menu a qualquer momento

5. **🔄 Modo Monitoramento Contínuo**
   - Opção para rodar o agente em loop (como antes)
   - Pode ser iniciado pelo menu
   - Ctrl+C volta ao menu

---

## 📦 Instalação

### 1. Pré-requisitos

- Python 3.8+
- Ollama rodando (`ollama serve`)
- Modelo Llama 3.2 (`ollama pull llama3.2:3b`)
- Conta Microsoft configurada

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar .env

```bash
cp .env.example .env
nano .env  # Cole suas credenciais
```

---

## 🚀 Uso

### Iniciar o Menu

```bash
python main.py
```

### Menu Principal

```
🤖 EMAIL MONITOR AGENT - MENU PRINCIPAL
================================================================================

ESCOLHA UMA OPÇÃO:

1️⃣  Resumo de Emails Recebidos Hoje
    └─ Visualiza emails do dia com informação de anexos

2️⃣  Emails Sem Resposta (Últimos 7 dias)
    └─ Lista emails que você ainda não respondeu

3️⃣  Status de Usuários da Organização
    └─ Mostra presença (online/offline/reunião) de todos

4️⃣  Iniciar Monitoramento Automático
    └─ Inicia o agente em modo contínuo (loop)

5️⃣  Chat com o Agente (IA)
    └─ Converse com a IA sobre seus emails

0️⃣  Sair

--------------------------------------------------------------------------------
Digite sua opção:
```

---

## 📋 Exemplos de Uso

### Opção 1: Resumo do Dia

```
================================================================================
📊 RESUMO DE EMAILS RECEBIDOS HOJE
================================================================================

📬 Total de emails: 12
📎 Com anexos: 3
📄 Sem anexos: 9

--------------------------------------------------------------------------------
DETALHES DOS EMAILS:
--------------------------------------------------------------------------------

1. 📎 [2026-02-03 09:15] Relatório Q4 - Análise Financeira
   De: joao@empresa.com

2.    [2026-02-03 10:30] RE: Reunião de Alinhamento
   De: maria@empresa.com

3. 📎 [2026-02-03 11:45] Proposta Comercial - Cliente XYZ
   De: vendas@empresa.com
```

### Opção 2: Emails Sem Resposta

```
================================================================================
⚠️  EMAILS SEM RESPOSTA (Últimos 7 dias)
================================================================================

📭 Total: 5 emails aguardando resposta

--------------------------------------------------------------------------------

1. 🔴 Solicitação de Orçamento - Urgente
   De: cliente@exemplo.com
   Recebido: 2026-01-31 (3 dia(s) atrás)

2. 🟡 Dúvida sobre projeto
   De: parceiro@empresa.com
   Recebido: 2026-02-02 (1 dia(s) atrás)

3. 🟢 Convite para evento
   De: eventos@comunidade.com
   Recebido: 2026-02-03 (0 dia(s) atrás)
```

### Opção 3: Status de Usuários

```
================================================================================
👥 STATUS DE USUÁRIOS DA ORGANIZAÇÃO
================================================================================

📊 Total de usuários: 15

Resumo por status:
  🟢 Disponível: 8 usuário(s)
  🔴 Ocupado: 3 usuário(s)
  📅 Em Reunião: 2 usuário(s)
  ⚫ Offline: 2 usuário(s)

--------------------------------------------------------------------------------
DETALHES:
--------------------------------------------------------------------------------
Status     Nome                           Email
--------------------------------------------------------------------------------
🟢 Disponível  João Silva                     joao.silva@empresa.com
🔴 Ocupado     Maria Santos                   maria.santos@empresa.com
📅 Em Reunião  Pedro Costa                    pedro.costa@empresa.com
⚫ Offline     Ana Lima                       ana.lima@empresa.com
```

---

## ⚙️ Configurações

### Ajustar Limite de Usuários

No código (`app/menu.py`):

```python
users = self.user_service.get_all_users_with_presence(max_users=100)  # Padrão: 50
```

### Alterar Período de Emails Sem Resposta

```python
unanswered = self.report_service.get_unanswered_emails(days=14)  # Padrão: 7
```

---

## 🏗️ Arquitetura

### Novos Componentes

```
app/
├── menu.py                  # Sistema de menu interativo
├── services/
│   ├── user_service.py      # Gerenciamento de usuários e presença
│   └── report_service.py    # Geração de relatórios
```

### Fluxo do Menu

```
main.py
  ↓
Autenticação
  ↓
Inicializa Serviços
  ↓
MenuSystem.run()
  ↓
┌─────────────────────────┐
│ Loop do Menu            │
│  1. Mostra opções       │
│  2. Lê escolha          │
│  3. Executa ação        │
│  4. Volta ao menu       │
└─────────────────────────┘
```

---

## 🔧 Troubleshooting

### "Erro ao buscar presença de usuários"

Pode ser falta de permissão. Certifique-se que seu app tem:
- `Presence.Read.All` (Application permission)

Para adicionar no Azure Portal:
1. Vá em "API permissions"
2. Adicione "Presence.Read.All"
3. Clique "Grant admin consent"

### "Emails sem resposta está vazio mas sei que tem"

A detecção verifica threads de conversa. Se o email foi respondido em outra plataforma (mobile, webmail), pode não aparecer.

### Menu não limpa a tela

Depende do sistema operacional. No WSL deve funcionar normalmente.

---

## 📚 Comparação v1.0 vs v2.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Monitoramento contínuo | ✅ | ✅ |
| Classificação IA | ✅ | ✅ |
| Menu interativo | ❌ | ✅ |
| Resumo diário | ❌ | ✅ |
| Emails sem resposta | ❌ | ✅ |
| Status de usuários | ❌ | ✅ |
| Relatórios formatados | ❌ | ✅ |

---

## 🎯 Próximos Passos

**Sprint 3** (sugestões):
- [ ] Exportar relatórios em PDF
- [ ] Enviar resumo diário por email automaticamente
- [ ] Dashboard web (Streamlit)
- [ ] Integração com Telegram
- [ ] Análise de sentimento nos emails
- [ ] Detecção de phishing

---

## 📝 Changelog

### v2.1 (03/02/2026)
- ✨ **NOVO**: Chat interativo com IA
- ✨ Converse naturalmente sobre seus emails
- ✨ Comandos especiais (/help, /resumo, /sugestões)
- ✨ IA com memória de conversa
- 🔧 Contexto automático dos últimos 3 dias
- 📚 Guia completo de uso do chat

### v2.0 (02/02/2026)
- ✨ Adicionado sistema de menu interativo
- ✨ Relatório de emails recebidos hoje com info de anexos
- ✨ Detecção de emails sem resposta (7 dias)
- ✨ Visualização de status/presença de usuários
- 🔧 UserService para gerenciar usuários
- 🔧 ReportService para gerar relatórios

### v1.0 (03/02/2026)
- 🎉 Versão inicial com monitoramento contínuo
- ✅ Integração com Ollama (Llama 3.2)
- ✅ Logging estruturado
- ✅ Cache de token

---

## 👨‍💻 Autor

Desenvolvido como projeto de aprendizado e uso corporativo.

**Versão**: 2.0  
**Data**: Fevereiro 2026  
**Licença**: Uso interno
