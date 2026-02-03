# 🎓 Explicação Técnica - Menu Interativo

## Para Desenvolvedores Júnior

Este documento explica **como funciona o sistema de menu** e **o que cada novo componente faz**.

---

## 🏗️ Arquitetura do Sistema

### Visão Geral

```
┌──────────────┐
│   main.py    │  ← Entry point
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Autenticação │  ← AuthService
└──────┬───────┘
       │
       ▼
┌──────────────────────────────┐
│ Inicializa Serviços:         │
│ - EmailService               │
│ - UserService         (NOVO) │
│ - ReportService       (NOVO) │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────┐
│  MenuSystem  │  (NOVO) ← Loop interativo
└──────┬───────┘
       │
       ├─ Opção 1 → ReportService.get_today_summary()
       ├─ Opção 2 → ReportService.get_unanswered_emails()
       ├─ Opção 3 → UserService.get_all_users_with_presence()
       └─ Opção 4 → EmailMonitorAgent.run()
```

---

## 📦 Novos Componentes

### 1. UserService (`app/services/user_service.py`)

**Responsabilidade:** Gerenciar usuários e status de presença.

**Métodos principais:**

```python
def get_all_users(self) -> list:
    """
    Busca TODOS os usuários da organização.
    
    API usada:
    GET https://graph.microsoft.com/v1.0/users
    
    Retorna:
    [
        {
            'id': 'abc123...',
            'displayName': 'João Silva',
            'mail': 'joao@empresa.com'
        },
        ...
    ]
    """
```

```python
def get_user_presence(self, user_id: str) -> dict:
    """
    Busca STATUS de presença de um usuário.
    
    API usada:
    GET https://graph.microsoft.com/v1.0/users/{id}/presence
    
    Retorna:
    {
        'availability': 'Available',  # ou 'Busy', 'Away', etc
        'activity': 'Available'
    }
    """
```

**Como funciona a presença:**

```python
# Microsoft Graph retorna algo assim:
{
    "availability": "Busy",
    "activity": "InAMeeting"
}

# Mapeamos para algo amigável:
PRESENCE_MAP = {
    'Busy': {'emoji': '🔴', 'description': 'Ocupado'},
    'InAMeeting': {'emoji': '📅', 'description': 'Em Reunião'}
}

# Resultado final mostrado pro usuário:
🔴 Ocupado
ou
📅 Em Reunião
```

**Por que é lento?**

Para cada usuário, fazemos 1 request de presença:

```python
users = get_all_users()  # 1 request → retorna 50 usuários
for user in users:
    presence = get_user_presence(user['id'])  # 50 requests!
```

Total: **51 requests** = ~5-10 segundos

**Como otimizar no futuro:**
- Usar batch request (1 request pra vários usuários)
- Cache de presença (válido por 5 min)
- Processar em paralelo (threads)

---

### 2. ReportService (`app/services/report_service.py`)

**Responsabilidade:** Gerar relatórios e análises de emails.

#### Método: `get_today_summary()`

```python
def get_today_summary(self) -> Dict:
    """Gera resumo de emails de HOJE."""
    
    # 1. Calcula data de hoje às 00:00
    today_start = datetime.now().replace(hour=0, minute=0, second=0)
    today_start_iso = today_start.isoformat() + 'Z'
    
    # 2. Monta query OData
    url = (
        f"/me/messages"
        f"?$filter=receivedDateTime ge {today_start_iso}"  # Recebidos DEPOIS de hoje 00:00
        f"&$select=id,subject,from,hasAttachments"         # Só campos necessários
        f"&$top=100"                                        # Max 100 emails
    )
    
    # 3. Faz request
    result = self.email_service._make_request(url)
    emails = result.get('value', [])
    
    # 4. Separa por anexo
    with_attachments = [e for e in emails if e.get('hasAttachments')]
    without_attachments = [e for e in emails if not e.get('hasAttachments')]
    
    # 5. Retorna estatísticas
    return {
        'total': len(emails),
        'with_attachments': len(with_attachments),
        'without_attachments': len(without_attachments),
        'emails': emails
    }
```

**Explicação do filtro OData:**

```
$filter=receivedDateTime ge {today_start_iso}

ge = Greater or Equal (>=)
receivedDateTime >= 2026-02-03T00:00:00Z

Tradução: "Recebidos hoje ou depois"
```

---

#### Método: `get_unanswered_emails()`

**Lógica complexa!** Vou explicar passo a passo:

```python
def get_unanswered_emails(self, days: int = 7) -> List[Dict]:
    """Busca emails SEM resposta dos últimos X dias."""
    
    # PASSO 1: Buscar emails recebidos nos últimos 7 dias
    start_date = datetime.now() - timedelta(days=7)
    emails = buscar_emails_desde(start_date)
    
    # PASSO 2: Para CADA email, verificar se EU respondi
    unanswered = []
    
    for email in emails:
        conversation_id = email['conversationId']  # ID da thread
        
        # PASSO 3: Buscar TODOS os emails dessa conversa
        thread_emails = buscar_emails_da_conversa(conversation_id)
        
        # PASSO 4: Verificar se algum é MEU (eu que enviei)
        my_replies = [e for e in thread_emails 
                      if e['from']['address'] == MEU_EMAIL]
        
        # PASSO 5: Se não tem nenhum meu = NÃO RESPONDI
        if len(my_replies) == 0:
            unanswered.append(email)
    
    return unanswered
```

**Exemplo visual:**

```
Email 1: "Orçamento urgente" (de cliente@exemplo.com)
  └─ conversationId: "abc123"
  
Busco TODOS emails com conversationId = "abc123":
  1. "Orçamento urgente" (de: cliente@exemplo.com) ← Email original
  2. "Re: Orçamento urgente" (de: eu@empresa.com)  ← MINHA resposta!
  
Conclusão: TEM resposta minha → NÃO adiciona na lista
```

```
Email 2: "Dúvida sobre projeto" (de: parceiro@exemplo.com)
  └─ conversationId: "xyz789"
  
Busco emails com conversationId = "xyz789":
  1. "Dúvida sobre projeto" (de: parceiro@exemplo.com) ← Só esse

Conclusão: NÃO TEM resposta minha → ADICIONA na lista de sem resposta
```

**Por que usa conversationId?**

Emails fazem parte de threads (conversas). O Microsoft Graph agrupa emails da mesma conversa com o mesmo `conversationId`.

---

### 3. MenuSystem (`app/menu.py`)

**Responsabilidade:** Interface de menu no terminal.

**Estrutura:**

```python
class MenuSystem:
    def __init__(self, email_service, user_service, report_service):
        # Guarda referência dos serviços
        self.email_service = email_service
        self.user_service = user_service
        self.report_service = report_service
    
    def run(self):
        """Loop principal do menu."""
        while True:
            self.print_header()
            self.print_menu()
            
            choice = input("Digite sua opção: ")
            
            if choice == '1':
                self.option_1_today_summary()
            elif choice == '2':
                self.option_2_unanswered_emails()
            # ...
```

**Como funciona o loop infinito:**

```python
while True:  # Loop infinito
    # Mostra menu
    print("1. Opção A")
    print("2. Opção B")
    
    # Lê escolha
    choice = input("Digite: ")
    
    # Executa ação
    if choice == '1':
        fazer_opcao_a()
    
    # Volta pro início do loop (mostra menu de novo)
```

**Como sai do loop:**

```python
if choice == '0':
    sys.exit(0)  # Termina o programa
```

ou

```python
except KeyboardInterrupt:  # Ctrl+C
    sys.exit(0)
```

---

## 🔄 Fluxo Completo - Opção 1

Vamos ver o que acontece quando usuário escolhe "Opção 1":

```python
# 1. Usuário digita "1"
choice = input("Digite sua opção: ")  # → "1"

# 2. Menu chama método
if choice == '1':
    self.option_1_today_summary()

# 3. Método executa
def option_1_today_summary(self):
    print("🔄 Buscando emails...")
    
    # 4. Chama ReportService
    summary = self.report_service.get_today_summary()
    
    # 5. ReportService chama EmailService
    # (dentro de get_today_summary)
    result = self.email_service._make_request(url)
    
    # 6. EmailService faz request HTTP
    response = requests.get(url, headers=self.headers)
    
    # 7. Microsoft Graph retorna JSON
    {
        "value": [
            {"subject": "Email 1", "hasAttachments": true},
            {"subject": "Email 2", "hasAttachments": false}
        ]
    }
    
    # 8. ReportService processa
    summary = {
        'total': 2,
        'with_attachments': 1,
        'without_attachments': 1,
        'emails': [...]
    }
    
    # 9. Menu formata e imprime
    formatted = self.report_service.format_today_summary(summary)
    print(formatted)
    
    # 10. Pausa
    input("Pressione ENTER...")
    
    # 11. Volta ao início do loop (mostra menu de novo)
```

---

## 🎨 Formatação de Tabelas

Você viu tabelas ASCII no output. Como funcionam?

```python
def format_users_table(self, users: list) -> str:
    lines = []
    
    # Header
    lines.append("=" * 80)  # 80 caracteres de "="
    lines.append(f"{'Status':<10} {'Nome':<30} {'Email':<40}")
    #                    ↑ Alinha à esquerda em 10 chars
    
    # Body
    for user in users:
        status = f"{user['emoji']} {user['status']}"
        name = user['name'][:28]  # Trunca em 28 chars
        email = user['email'][:38]
        
        lines.append(f"{status:<10} {name:<30} {email:<40}")
    
    return "\n".join(lines)
```

**Exemplo de formatação:**

```python
# Sem formatação:
print(emoji, status, name, email)
# Output: 🟢 Disponível João Silva joao@empresa.com (tudo junto, feio)

# Com formatação:
print(f"{status:<10} {name:<30} {email:<40}")
# Output:
# 🟢 Disponível   João Silva                 joao@empresa.com
```

**Código de formatação:**
- `<10` = Alinha à esquerda, ocupa 10 caracteres
- Se texto é menor, preenche com espaços
- Se texto é maior, trunca

---

## 🧪 Como Testar Localmente

### Testar UserService

```python
from app.services.user_service import UserService

token = "seu_token_aqui"
user_service = UserService(token)

# Testar busca de usuários
users = user_service.get_all_users()
print(f"Total: {len(users)}")

# Testar presença
if users:
    presence = user_service.get_user_presence(users[0]['id'])
    print(presence)
```

### Testar ReportService

```python
from app.services.report_service import ReportService
from app.services.email_service import EmailService

token = "seu_token_aqui"
email_service = EmailService(token)
report_service = ReportService(email_service)

# Testar resumo
summary = report_service.get_today_summary()
print(summary)

# Testar emails sem resposta
unanswered = report_service.get_unanswered_emails(days=7)
print(f"Sem resposta: {len(unanswered)}")
```

---

## 🐛 Debugging

### Problema: "Nenhum usuário encontrado"

**Causa:** Falta permissão `User.Read.All`

**Debug:**
```python
try:
    users = user_service.get_all_users()
except Exception as e:
    print(f"Erro: {e}")
    # Vai mostrar: "403 Forbidden" ou similar
```

### Problema: "Emails sem resposta sempre vazio"

**Causa:** Lógica está verificando se VOCÊ enviou algo na thread.

**Debug:**
```python
# Adicione prints temporários
for email in emails:
    print(f"Verificando: {email['subject']}")
    thread_emails = buscar_thread(email['conversationId'])
    print(f"  Emails na thread: {len(thread_emails)}")
    
    my_replies = [e for e in thread_emails if ...]
    print(f"  Minhas respostas: {len(my_replies)}")
```

---

## 💡 Melhorias Futuras

### Otimização de Performance

1. **Cache de usuários**
```python
# Em vez de buscar sempre
users = user_service.get_all_users()

# Cache por 1 hora
@lru_cache(maxsize=1)
def get_cached_users():
    return user_service.get_all_users()
```

2. **Requisições paralelas**
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as executor:
    presences = executor.map(get_user_presence, user_ids)
```

### Novas Features

1. **Filtros no menu**
```
1. Resumo de hoje
   └─ a) Todos
   └─ b) Apenas com anexo
   └─ c) Apenas urgentes
```

2. **Exportar relatórios**
```python
def export_to_csv(summary):
    import csv
    with open('relatorio.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Remetente', 'Assunto', 'Anexo'])
        for email in summary['emails']:
            writer.writerow([...])
```

---

## 🎯 Resumo

**O que você aprendeu:**

1. **UserService** busca usuários e presença via Microsoft Graph
2. **ReportService** gera relatórios de emails (hoje, sem resposta)
3. **MenuSystem** implementa interface interativa em loop
4. **Formatação** de tabelas ASCII com f-strings
5. **Lógica de threads** pra detectar emails sem resposta
6. **Filtros OData** para buscar emails específicos

**Próximo passo:** Rode o código, teste cada opção e experimente modificar!
