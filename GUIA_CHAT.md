# 💬 Guia do Chat Interativo com IA

## O que é?

O **Chat com o Agente** é uma conversa em tempo real com uma IA que conhece seus emails. Você pode fazer perguntas naturais e receber respostas contextualizadas sobre sua caixa de entrada.

---

## 🚀 Como Usar

### 1. Iniciar o Chat

No menu principal, escolha:

```
5️⃣  Chat com o Agente (IA)
```

Você verá:

```
================================================================================
💬 CHAT COM O AGENTE
================================================================================

🤖 Olá! Sou seu assistente inteligente.
📧 Posso responder perguntas sobre seus emails.

💡 Dica: Digite /help para ver comandos especiais
💡 Digite /sugestões para ver perguntas exemplo
💡 Digite /sair para voltar ao menu

--------------------------------------------------------------------------------

👤 Você: _
```

### 2. Fazer Perguntas

Digite sua pergunta e pressione Enter:

```
👤 Você: Quantos emails não lidos eu tenho?

🤖 Agente: ⏳ Pensando...
🤖 Agente: Você tem 5 emails não lidos nos últimos 3 dias. 
           3 deles são de hoje. Quer que eu te diga quais são os mais importantes?
```

### 3. Continuar a Conversa

A IA lembra do contexto da conversa:

```
👤 Você: Sim, quais são os importantes?

🤖 Agente: Os emails mais importantes são:
           1. "Reunião urgente amanhã" de joao@empresa.com
           2. "Proposta comercial - prazo hoje" de cliente@exemplo.com
           Recomendo responder esses primeiro!
```

### 4. Sair do Chat

Digite `/sair` ou `sair`:

```
👤 Você: /sair

👋 Voltando ao menu principal...
```

---

## 💡 Perguntas Exemplo

### Sobre Quantidade

```
- Quantos emails não lidos eu tenho?
- Quantos emails recebi hoje?
- Há muitos emails com anexos?
```

### Sobre Remetentes

```
- Quem mais me enviou emails esta semana?
- Recebi algo do João?
- Quem me mandou email hoje?
```

### Sobre Urgência

```
- Tenho algum email importante?
- Há emails urgentes para responder?
- O que preciso fazer primeiro?
```

### Sobre Conteúdo

```
- Me fale sobre os emails de hoje
- Resuma minha caixa de entrada
- Qual foi o último email que recebi?
- Há alguma reunião mencionada nos emails?
```

### Sobre Ações

```
- Preciso responder algum email?
- O que devo priorizar agora?
- Há algo que não posso esquecer?
```

---

## 🤖 Comandos Especiais

Digite comandos que começam com `/`:

### `/help`
Mostra lista de comandos disponíveis

```
👤 Você: /help

🤖 Agente: 
🤖 COMANDOS DISPONÍVEIS

/resumo - Resumo rápido de hoje
/limpar - Limpa histórico de chat
/sugestões - Mostra perguntas sugeridas
/sair - Volta ao menu

Ou faça perguntas normalmente!
```

### `/sugestões`
Mostra perguntas de exemplo

```
👤 Você: /sugestões

🤖 Agente:
💡 PERGUNTAS SUGERIDAS:

1. Quantos emails não lidos eu tenho?
2. Quem mais me enviou emails esta semana?
3. Tenho algum email importante ou urgente?
4. Me fale sobre os emails de hoje
5. Há emails com anexos?
6. Preciso responder algum email?
7. Qual foi o último email que recebi?
8. Resuma minha caixa de entrada
```

### `/resumo`
Resumo rápido de hoje (sem usar IA)

```
👤 Você: /resumo

🤖 Agente:
📊 RESUMO RÁPIDO

Total hoje: 8
Com anexos: 2
Sem anexos: 6
```

### `/limpar`
Limpa o histórico da conversa (a IA "esquece" o que foi dito)

```
👤 Você: /limpar

🤖 Agente: ✅ Histórico de conversa limpo!
```

### `/sair`
Volta ao menu principal

---

## 🧠 Como a IA Funciona

### O que a IA Sabe

A IA tem acesso a:
- ✅ Emails dos últimos 3 dias (até 50)
- ✅ Status de leitura (lido/não lido)
- ✅ Remetentes
- ✅ Assuntos
- ✅ Anexos
- ✅ Importância marcada
- ✅ Histórico da conversa atual

### O que a IA NÃO Sabe

- ❌ Conteúdo completo dos emails (só assunto e preview)
- ❌ Emails de mais de 3 dias atrás
- ❌ Calendário
- ❌ Informações fora do email

### Memória da Conversa

A IA lembra das últimas **5 mensagens** da conversa:

```
Você: Tenho emails importantes?
IA: Sim, 2 emails importantes.

Você: Quais são?
IA: [lembra da pergunta anterior e lista os emails]

Você: Devo responder agora?
IA: [ainda lembra do contexto]
```

Após 5 mensagens, ela "esquece" as anteriores. Use `/limpar` para resetar.

---

## 🎯 Casos de Uso

### Caso 1: Início do Dia

```
👤 Você: Bom dia! O que chegou hoje?

🤖 Agente: Bom dia! Hoje você recebeu 8 emails. 
           3 são não lidos. Os principais são:
           - Relatório Q4 (com anexo)
           - Reunião cancelada
           - Proposta comercial
           Quer detalhes de algum?
```

### Caso 2: Antes de Reunião

```
👤 Você: Recebi algum email sobre a reunião das 14h?

🤖 Agente: Sim! João enviou "Pauta reunião 14h" há 2 horas.
           Ele está marcado como importante.
```

### Caso 3: Verificação Rápida

```
👤 Você: Preciso urgente de algo?

🤖 Agente: Sim, você tem 1 email urgente:
           "Sistema fora do ar" de TI, recebido há 15 minutos.
           Recomendo verificar imediatamente.
```

### Caso 4: Pesquisa Específica

```
👤 Você: O cliente XYZ me enviou algo?

🤖 Agente: Não encontrei emails de cliente XYZ nos últimos 3 dias.
           O último email foi provavelmente há mais tempo.
```

---

## 💡 Dicas Pro

### Dica 1: Seja Específico

❌ Ruim: "Emails"
✅ Bom: "Quantos emails não lidos tenho hoje?"

### Dica 2: Use Contexto

Após uma pergunta, faça follow-ups:

```
1. Tenho emails importantes?
2. Quais são? [usa contexto da 1]
3. Devo responder agora? [usa contexto da 2]
```

### Dica 3: Use Comandos para Rapidez

Se quer só um resumo rápido, use `/resumo` em vez de perguntar.

### Dica 4: Limpe Quando Mudar de Assunto

```
[Falando sobre emails de trabalho]
👤 Você: /limpar
👤 Você: Agora me fale sobre emails pessoais
```

### Dica 5: Combine com Outras Opções

```
1. Use opção 5 (Chat) para perguntas gerais
2. Use opção 1 (Resumo) para ver lista completa
3. Use opção 2 (Sem resposta) para ação
```

---

## 🐛 Resolução de Problemas

### "A IA demorou muito"

- Normal! Llama 3.2 leva ~10-15s para responder
- Se demorar mais de 30s, pode ser problema com Ollama
- Verifique: `ollama list` no terminal

### "A IA deu resposta genérica"

- Ela não tem acesso ao conteúdo completo dos emails
- Só vê assunto e preview
- Para detalhes, use as outras opções do menu

### "A IA disse que não sabe"

- Pode ser que a informação não esteja nos últimos 3 dias
- Ou o email é muito antigo
- Ou a pergunta foi ambígua

### "A IA não lembra do que falamos"

- Após 5 mensagens ela esquece as antigas
- Use `/limpar` e comece de novo
- Seja mais específico na próxima vez

### "Erro ao processar mensagem"

- Verifique se Ollama está rodando: `ollama serve`
- Verifique logs: `logs/email_agent.log`
- Tente `/limpar` e pergunte de novo

---

## 🎓 Exemplos Avançados

### Análise Comparativa

```
👤 Você: Quem me enviou mais emails: João ou Maria?

🤖 Agente: Nos últimos 3 dias:
           - João: 5 emails
           - Maria: 2 emails
           João enviou mais!
```

### Priorização

```
👤 Você: Do que tenho que não li, o que é mais urgente?

🤖 Agente: Dos 5 não lidos, o mais urgente é:
           "Sistema crítico parado" de TI (há 1 hora)
           Recomendo ler este primeiro.
```

### Busca Temporal

```
👤 Você: Recebi algo importante ontem?

🤖 Agente: Sim, ontem você recebeu 2 emails importantes:
           - "Proposta aprovada" de diretor
           - "Novo cliente" de vendas
```

---

## 🔮 Limitações Atuais

**O chat NÃO pode:**
- ❌ Enviar emails
- ❌ Marcar como lido/não lido
- ❌ Mover emails para pastas
- ❌ Criar tarefas
- ❌ Acessar anexos
- ❌ Ler corpo completo do email

**O chat PODE:**
- ✅ Responder perguntas sobre emails
- ✅ Sugerir prioridades
- ✅ Resumir informações
- ✅ Identificar padrões
- ✅ Dar contexto

---

## 🚀 Próximas Features (Futuro)

Ideias para melhorar o chat:

1. **Ações diretas**: "Marque este email como lido"
2. **Busca avançada**: "Mostre emails sobre projeto X"
3. **Análise de sentimento**: "Há emails negativos?"
4. **Sugestões proativas**: IA avisa de emails urgentes
5. **Integração com calendário**: "Tenho reunião hoje?"

---

## 📝 Resumo

**Para usar bem o chat:**

1. ✅ Faça perguntas claras e específicas
2. ✅ Use o contexto da conversa (follow-ups)
3. ✅ Experimente os comandos especiais (`/help`)
4. ✅ Seja paciente (~10s por resposta)
5. ✅ Limpe o histórico quando mudar de assunto

**O chat é melhor para:**
- Perguntas rápidas
- Visão geral da caixa
- Priorização
- Busca contextual

**Use outras opções do menu para:**
- Listas detalhadas (Opção 1, 2, 3)
- Monitoramento contínuo (Opção 4)

---

Agora é só testar! Digite `5` no menu e comece a conversar! 💬🤖
