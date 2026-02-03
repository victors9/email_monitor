# 🚀 Guia Rápido - Menu Interativo

## Instalação em 3 Passos

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar credenciais
cp .env.example .env
nano .env  # Cole TENANT_ID e CLIENT_ID

# 3. Executar
python main.py
```

---

## 📖 Como Usar Cada Opção

### Opção 1: Resumo de Emails de Hoje

**Quando usar:**
- Início do dia para ver o que chegou
- Antes de sair do trabalho
- Quando precisa ver apenas emails de hoje

**O que mostra:**
- Total de emails recebidos hoje
- Quantos têm anexos (📎)
- Lista com remetente, assunto e hora

**Exemplo de output:**
```
📊 RESUMO DE EMAILS RECEBIDOS HOJE
═══════════════════════════════════════
📬 Total de emails: 8
📎 Com anexos: 2
📄 Sem anexos: 6
```

---

### Opção 2: Emails Sem Resposta

**Quando usar:**
- Fim do dia para ver o que ficou pendente
- Início da semana
- Quando quer garantir que não esqueceu ninguém

**O que mostra:**
- Emails dos últimos 7 dias que você NÃO respondeu
- Urgência visual por cor:
  - 🔴 3+ dias sem resposta (URGENTE!)
  - 🟡 1-2 dias sem resposta (Atenção)
  - 🟢 Hoje (Tranquilo)

**NOTA:** Só detecta emails que você recebeu. Se você enviou o primeiro email, não aparece aqui.

---

### Opção 3: Status de Usuários

**Quando usar:**
- Precisa falar com alguém e quer saber se está disponível
- Ver quem está online
- Verificar quem está em reunião

**O que mostra:**
- Lista de todos os usuários da empresa (até 50)
- Status de cada um:
  - 🟢 Disponível
  - 🔴 Ocupado
  - 📅 Em Reunião
  - 📞 Em Chamada
  - ⚫ Offline
  - E mais...

**NOTA:** Pode demorar alguns segundos (faz 1 request por usuário).

---

### Opção 4: Monitoramento Contínuo

**Quando usar:**
- Quer deixar rodando durante o dia
- Precisa ser alertado de emails urgentes

**O que faz:**
- Entra no modo loop (igual v1.0)
- Verifica emails a cada 30s
- Classifica urgência com IA
- Imprime no terminal em tempo real

**Como parar:**
- Pressione `Ctrl+C`
- Volta automaticamente ao menu

---

## 🎮 Navegação

### Menu Principal
```
Digite o número da opção → Enter
```

### Sair de qualquer tela
```
Pressione Enter quando pedir
```

### Sair do programa
```
Digite 0 → Enter
```

### Interromper monitoramento
```
Ctrl+C → Volta ao menu
```

---

## ⚡ Atalhos

### Ver tudo de uma vez

```bash
# Opção 1 + 2 em sequência
python main.py
> Digite: 1
[vê resumo do dia]
> Enter
> Digite: 2
[vê emails sem resposta]
> Enter
> Digite: 0
[sai]
```

---

## 🐛 Problemas Comuns

### "TENANT_ID not found"
```bash
cp .env.example .env
nano .env  # Preencha as credenciais
```

### "Erro ao buscar usuários"
Falta permissão no Azure. Adicione:
- `User.Read.All`
- `Presence.Read.All`

### "Nenhum email sem resposta"
Parabéns! Você respondeu todos os emails 🎉

### Menu não limpa tela
Normal em alguns terminais. Funciona no WSL/Linux.

---

## 💡 Dicas Pro

### Dica 1: Rotina Diária
```
Manhã:
1. Opção 1 → Ver emails de hoje
2. Opção 2 → Ver pendências

Fim do dia:
1. Opção 2 → Garantir que não esqueceu ninguém
```

### Dica 2: Antes de Reunião
```
Opção 3 → Ver quem está disponível
```

### Dica 3: Monitoramento
```
Opção 4 → Deixa rodando durante o dia
```

---

## 🔄 Workflow Sugerido

```
┌─────────────────────┐
│ Iniciar o dia       │
│ Opção 1             │ ← Ver o que chegou
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ Verificar pendências│
│ Opção 2             │ ← Emails sem resposta
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ Durante o dia       │
│ Opção 4             │ ← Monitoramento contínuo
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ Antes de sair       │
│ Opção 2 novamente   │ ← Final check
└─────────────────────┘
```

---

## ❓ FAQ

**P: Posso rodar as 3 opções ao mesmo tempo?**
R: Não. Escolha uma por vez. Mas você pode rodar rapidamente uma após a outra.

**P: Os relatórios salvam em arquivo?**
R: Não nesta versão. Mas você pode copiar do terminal ou fazer screenshot.

**P: Posso mudar o período de "emails sem resposta"?**
R: Sim! Edite `app/menu.py` linha onde tem `days=7` e mude para `days=14`.

**P: Quantos usuários ele busca?**
R: 50 por padrão. Pode mudar para `max_users=100` no código.

**P: Funciona offline?**
R: Não. Precisa de internet para acessar Microsoft Graph API.

---

## 🎯 Próximo Passo

Agora que sabe usar o menu, explore cada opção e veja qual mais te ajuda no dia-a-dia!

**Sugestão:** Teste opção 2 (emails sem resposta) agora. Pode ter surpresas! 😄
