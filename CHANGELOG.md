# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

## [1.0.0] - 2026-02-03

### 🎉 Sprint 1 - Fundação Sólida

#### ✨ Adicionado
- Sistema de logging estruturado com rotação de arquivos
- Configuração via arquivo `.env` (sem hardcode de credenciais)
- Integração com Ollama para IA local (Llama 3.2 3B)
- Classificação automática de urgência dos emails (ALTA/MÉDIA/BAIXA)
- Cache de token para evitar re-autenticação constante
- Retry automático com backoff em caso de falhas de API
- Sistema de heartbeat para monitoramento de saúde
- Tratamento robusto de erros em todos os serviços
- Graceful shutdown (Ctrl+C)
- Logs com emojis visuais para melhor UX

#### 🔧 Melhorado
- `AuthService`: Implementado cache de token e silent authentication
- `EmailService`: Adicionado retry automático e tratamento de rate limiting
- `CalendarService`: Busca otimizada de eventos futuros
- `AIService`: Integração real com Ollama (antes era mockado)
- `Agent`: Loop de monitoramento mais resiliente e informativo

#### 📚 Documentação
- README completo com instruções de instalação
- CHANGELOG para tracking de versões
- .env.example como template
- .gitignore configurado
- Comentários em código explicativos

#### 🏗️ Arquitetura
- Separação clara de responsabilidades
- Padrão Singleton no logger
- Configurações centralizadas
- Services desacoplados

### 🐛 Bugs Conhecidos
- Emails não são marcados como lidos automaticamente (feature futura)
- Modelo pode ser lento em hardware limitado (~10s por email)
- Sem persistência de histórico de processamento

### 🔜 Próximos Passos (Sprint 2)
- Análise de sentimento dos emails
- Extração inteligente de action items
- Geração contextualizada de respostas
- Marcar emails processados como lidos
- Cache de análises para evitar reprocessamento

---

## Como Versionar

Este projeto segue [Semantic Versioning](https://semver.org/):

- **MAJOR**: Mudanças incompatíveis de API
- **MINOR**: Novas funcionalidades compatíveis
- **PATCH**: Correções de bugs compatíveis

### Categorias de Mudança

- `✨ Adicionado`: Novas features
- `🔧 Melhorado`: Melhorias em features existentes
- `🐛 Corrigido`: Bug fixes
- `🗑️ Removido`: Features removidas
- `🔒 Segurança`: Correções de vulnerabilidades
- `📚 Documentação`: Mudanças na documentação
- `🏗️ Arquitetura`: Mudanças estruturais
